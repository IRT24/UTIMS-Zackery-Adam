from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib import messages
import re

def admin_required(view_func):
    """
    Decorator for views that checks if the user is an admin,
    redirecting to the home page if not.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("You don't have permission to access this page.")
    return _wrapped_view 

def validate_input(fields=None, patterns=None):
    """
    Decorator to validate input fields against SQL injection and XSS attack patterns.
    
    Args:
        fields: List of request parameters to validate (None = all)
        patterns: Dictionary of custom regex patterns to check against
    """
    if patterns is None:
        patterns = {
            'sql_injection': r'(\b(select|insert|update|delete|drop|alter|exec|union|create|where)\b)|(\b(from|into|table|database)\b.*\b(select|insert|update|delete)\b)|(-{2,})|(/\*.*\*/)',
            'xss': r'(<script.*?>)|(javascript:)|(data:text/html)|(vbscript:)|(onclick)|(onmouseover)|(onload)|(onerror)|(onunload)|(onsubmit)|(onblur)|(onfocus)|(onreset)|(onchange)|(onmove)|(onabort)|(ondblclick)|(document\.cookie)|(document\.write)|(document\.location)|(window\.location)|(eval\()|(setTimeout\()|(setInterval\()|(new\s+Function\()|(alert\()|(prompt\()|(confirm\()|(String\.fromCharCode)|(&#x[0-9a-f]+;)|(&#\d+;)|(<iframe)|(</iframe>)|(style=[\'\"].*?expression\()',
            'path_traversal': r'(\.\./)|(\.\.\%2F)|(\.\.\%5C)'
        }
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Skip validation for trusted users to prevent false positives
            if hasattr(request, 'user') and request.user.is_authenticated and request.user.role == 'admin':
                return view_func(request, *args, **kwargs)
                
            # Determine which parameters to validate
            data_sources = []
            
            # Add GET parameters if they exist
            if hasattr(request, 'GET') and request.GET:
                data_sources.append(('GET', request.GET))
                
            # Add POST parameters if they exist
            if hasattr(request, 'POST') and request.method == 'POST' and request.POST:
                data_sources.append(('POST', request.POST))
            
            # Validate each parameter
            for source_name, source in data_sources:
                for param, value in source.items():
                    # Skip CSRF token and other internal fields
                    if param in ('csrfmiddlewaretoken', '_method'):
                        continue
                        
                    # Skip fields not in the specified list if a list is provided
                    if fields is not None and param not in fields:
                        continue
                        
                    # Check each pattern
                    for pattern_name, pattern in patterns.items():
                        if re.search(pattern, value, re.IGNORECASE):
                            # Potential attack detected - log and block
                            if hasattr(request, 'user') and request.user.is_authenticated:
                                user_id = request.user.id
                            else:
                                user_id = 'Anonymous'
                                
                            # Log the attempt
                            print(f"Security warning: Potential {pattern_name} detected from user {user_id}")
                            print(f"Request: {source_name} parameter '{param}' with value '{value}'")
                            
                            # Show message to user
                            if hasattr(request, 'user'):
                                messages.error(
                                    request, 
                                    "Invalid input detected. Please avoid special characters."
                                )
                            
                            # Return HTTP 400 Bad Request
                            return HttpResponseBadRequest(
                                "Invalid input detected. Please avoid special characters and try again."
                            )
            
            # All inputs are safe, proceed with the view
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator 