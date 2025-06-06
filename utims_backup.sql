-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: utims_db
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add category',7,'add_category'),(26,'Can change category',7,'change_category'),(27,'Can delete category',7,'delete_category'),(28,'Can view category',7,'view_category'),(29,'Can add inventory item',8,'add_inventoryitem'),(30,'Can change inventory item',8,'change_inventoryitem'),(31,'Can delete inventory item',8,'delete_inventoryitem'),(32,'Can view inventory item',8,'view_inventoryitem'),(33,'Can add inventory log',9,'add_inventorylog'),(34,'Can change inventory log',9,'change_inventorylog'),(35,'Can delete inventory log',9,'delete_inventorylog'),(36,'Can view inventory log',9,'view_inventorylog'),(37,'Can add task',10,'add_task'),(38,'Can change task',10,'change_task'),(39,'Can delete task',10,'delete_task'),(40,'Can view task',10,'view_task'),(41,'Can add expense',11,'add_expense'),(42,'Can change expense',11,'change_expense'),(43,'Can delete expense',11,'delete_expense'),(44,'Can view expense',11,'view_expense');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$FWptvWhzlGsxFBIh64tk6z$jjpbi42oA8aD7mQmra7kc/8F/v5fuiAyw5VG9vhgHiM=','2025-02-25 08:16:10.045396',1,'superuser','','','superuser@superuser.com',1,1,'2025-02-23 10:38:26.916011'),(2,'pbkdf2_sha256$870000$I9W71UH6xpmCNhaSA7Qedn$ef48enkHAvaL3rRuo7oKE7Vu8DwEuvQFBS/RvBU1ZSM=','2025-02-25 08:17:33.384700',1,'superuser2','','','superuser2@superuser2.com',1,1,'2025-02-25 08:17:14.885821');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-02-23 10:49:33.831436','1','Vegetables',1,'[{\"added\": {}}]',7,1),(2,'2025-02-23 10:49:43.721556','1','Fruits - 200 units',1,'[{\"added\": {}}]',8,1),(3,'2025-02-23 13:07:45.675837','5','Example',3,'',7,1),(4,'2025-02-23 13:28:41.103983','1','Fruits - 200 units',2,'[{\"changed\": {\"fields\": [\"Category\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(11,'expenses','expense'),(7,'inventory','category'),(8,'inventory','inventoryitem'),(9,'inventory','inventorylog'),(6,'sessions','session'),(10,'tasks','task');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-02-23 08:03:02.407997'),(2,'auth','0001_initial','2025-02-23 08:03:02.810567'),(3,'admin','0001_initial','2025-02-23 08:03:02.911569'),(4,'admin','0002_logentry_remove_auto_add','2025-02-23 08:03:02.916805'),(5,'admin','0003_logentry_add_action_flag_choices','2025-02-23 08:03:02.922137'),(6,'contenttypes','0002_remove_content_type_name','2025-02-23 08:03:02.999870'),(7,'auth','0002_alter_permission_name_max_length','2025-02-23 08:03:03.043480'),(8,'auth','0003_alter_user_email_max_length','2025-02-23 08:03:03.060579'),(9,'auth','0004_alter_user_username_opts','2025-02-23 08:03:03.065559'),(10,'auth','0005_alter_user_last_login_null','2025-02-23 08:03:03.106587'),(11,'auth','0006_require_contenttypes_0002','2025-02-23 08:03:03.108557'),(12,'auth','0007_alter_validators_add_error_messages','2025-02-23 08:03:03.113576'),(13,'auth','0008_alter_user_username_max_length','2025-02-23 08:03:03.159850'),(14,'auth','0009_alter_user_last_name_max_length','2025-02-23 08:03:03.204887'),(15,'auth','0010_alter_group_name_max_length','2025-02-23 08:03:03.235242'),(16,'auth','0011_update_proxy_permissions','2025-02-23 08:03:03.241578'),(17,'auth','0012_alter_user_first_name_max_length','2025-02-23 08:03:03.292775'),(18,'sessions','0001_initial','2025-02-23 08:03:03.319950'),(19,'inventory','0001_initial','2025-02-23 08:56:22.708187'),(20,'tasks','0001_initial','2025-02-23 13:39:15.531137'),(21,'expenses','0001_initial','2025-02-25 07:51:51.186662'),(22,'expenses','0002_alter_expense_category','2025-02-25 09:03:38.127749'),(23,'tasks','0002_remove_task_assigned_to_remove_task_status_and_more','2025-02-26 13:16:47.698677'),(24,'tasks','0003_alter_task_options_task_due_date_task_priority_and_more','2025-03-02 08:55:19.764700');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('8krvw7eerd98t5vfffe422kfs44xlg88','.eJxVjMsOgjAQRf-la9MMbQdbl-75hmYeRVADCYWV8d-VhIVu7znnvkymbR3yVsuSRzUX48zpd2OSR5l2oHeabrOVeVqXke2u2INW281antfD_TsYqA7fGmJKZ_GYYlBuo_RCPYcAAZRRhbkoAKBDQPENhpadS7Et0buGPJN5fwDfejeR:1tmq8D:D_MyyNLqOxjol3A1JzKvP-G0WcfMFCjMG0wtAdk-q80','2025-03-11 08:17:33.387932');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses_expense`
--

DROP TABLE IF EXISTS `expenses_expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses_expense` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `category` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `description` longtext,
  `receipt` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses_expense`
--

LOCK TABLES `expenses_expense` WRITE;
/*!40000 ALTER TABLE `expenses_expense` DISABLE KEYS */;
INSERT INTO `expenses_expense` VALUES (2,'Dinner Ingredients',60.75,'UTILITIES','2025-02-25','',''),(3,'Dinner Ingredients 2',71.75,'FOOD','2025-02-25','',''),(4,'Barang KEWJIBAN',2000.25,'GROCERIES','2025-03-08','1. Susu Segar 5L\r\n2. Tepung Gandum 1KG X 20','');
/*!40000 ALTER TABLE `expenses_expense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_category`
--

DROP TABLE IF EXISTS `inventory_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_category`
--

LOCK TABLES `inventory_category` WRITE;
/*!40000 ALTER TABLE `inventory_category` DISABLE KEYS */;
INSERT INTO `inventory_category` VALUES (3,'Dry Items'),(4,'Fruits'),(1,'Vegetables'),(2,'Wet Items');
/*!40000 ALTER TABLE `inventory_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventoryitem`
--

DROP TABLE IF EXISTS `inventory_inventoryitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventoryitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `price_per_unit` decimal(10,2) NOT NULL,
  `low_stock_threshold` int unsigned NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `inventory_inventoryi_category_id_06acb4f3_fk_inventory` (`category_id`),
  CONSTRAINT `inventory_inventoryi_category_id_06acb4f3_fk_inventory` FOREIGN KEY (`category_id`) REFERENCES `inventory_category` (`id`),
  CONSTRAINT `inventory_inventoryitem_chk_1` CHECK ((`quantity` >= 0)),
  CONSTRAINT `inventory_inventoryitem_chk_2` CHECK ((`low_stock_threshold` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventoryitem`
--

LOCK TABLES `inventory_inventoryitem` WRITE;
/*!40000 ALTER TABLE `inventory_inventoryitem` DISABLE KEYS */;
INSERT INTO `inventory_inventoryitem` VALUES (1,'Fruits',51,20.00,50,'2025-03-30 00:27:40.222358',4),(2,'Chicken',2000,10.00,5,'2025-03-30 00:26:03.465846',2),(3,'Sugar',200,2.50,20,'2025-03-30 00:25:52.323110',3),(4,'Apple',29,1.50,30,'2025-03-30 00:28:07.389615',4),(6,'Cinnamon Rolls',90,1.00,30,'2025-03-30 00:27:51.788319',3);
/*!40000 ALTER TABLE `inventory_inventoryitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventorylog`
--

DROP TABLE IF EXISTS `inventory_inventorylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventorylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(10) NOT NULL,
  `quantity_changed` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `remarks` longtext,
  `item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_inventoryl_item_id_542bde0d_fk_inventory` (`item_id`),
  CONSTRAINT `inventory_inventoryl_item_id_542bde0d_fk_inventory` FOREIGN KEY (`item_id`) REFERENCES `inventory_inventoryitem` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventorylog`
--

LOCK TABLES `inventory_inventorylog` WRITE;
/*!40000 ALTER TABLE `inventory_inventorylog` DISABLE KEYS */;
INSERT INTO `inventory_inventorylog` VALUES (1,'ADD',200,'2025-03-29 23:09:45.644557','Initial stock created: 200 units',6),(2,'REMOVE',28,'2025-03-29 23:09:59.382474','Updated quantity from 30 to 2',2),(3,'REMOVE',152,'2025-03-29 23:10:41.180606','Updated quantity from 200 to 48',1),(4,'REMOVE',277,'2025-03-30 00:18:02.457890','Updated quantity from 300 to 23',3),(5,'REMOVE',11,'2025-03-30 00:18:08.479900','Updated quantity from 23 to 12',3),(6,'REMOVE',188,'2025-03-30 00:18:37.455339','Updated quantity from 200 to 12',6),(7,'REMOVE',17,'2025-03-30 00:25:32.467832','Updated quantity from 20 to 3',4),(8,'ADD',188,'2025-03-30 00:25:52.327515','Updated quantity from 12 to 200',3),(9,'ADD',1998,'2025-03-30 00:26:03.468065','Updated quantity from 2 to 2000',2),(10,'ADD',147,'2025-03-30 00:26:08.668976','Updated quantity from 3 to 150',4),(11,'ADD',3,'2025-03-30 00:27:40.224328','Updated quantity from 48 to 51',1),(12,'ADD',78,'2025-03-30 00:27:51.795371','Updated quantity from 12 to 90',6),(13,'REMOVE',121,'2025-03-30 00:28:07.395224','Updated quantity from 150 to 29',4);
/*!40000 ALTER TABLE `inventory_inventorylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks_task`
--

DROP TABLE IF EXISTS `tasks_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `due_date` date DEFAULT NULL,
  `priority` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks_task`
--

LOCK TABLES `tasks_task` WRITE;
/*!40000 ALTER TABLE `tasks_task` DISABLE KEYS */;
INSERT INTO `tasks_task` VALUES (1,'Kitchen Cleaning','Wash the floors!','2025-02-23 13:56:40.479257',NULL,'medium','in_progress','2025-03-03 10:31:31.682898'),(2,'Dining Area Cleaning','Clean the Dining Tables, and Prepare Cutleries','2025-03-02 09:04:41.358362','2025-10-14','high','pending','2025-03-02 17:49:14.809311'),(3,'eXAMPLE','PLEASEDO THIS','2025-03-03 10:30:54.944810','2025-10-19','high','completed','2025-03-03 10:30:54.944828'),(4,'EXAMPLE2','ok DONE!','2025-03-03 10:31:20.195066','2025-11-17','low','in_progress','2025-03-03 10:31:20.195082');
/*!40000 ALTER TABLE `tasks_task` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-30 16:10:01
