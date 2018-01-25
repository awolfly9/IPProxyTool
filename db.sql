-- MySQL dump 10.13  Distrib 5.5.58, for Linux (x86_64)
--
-- Host: localhost    Database: ipproxy
-- ------------------------------------------------------
-- Server version	5.5.58

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `free_ipproxy`
--

DROP TABLE IF EXISTS `free_ipproxy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `free_ipproxy` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `ip` char(25) NOT NULL,
  `port` int(4) NOT NULL,
  `country` text,
  `anonymity` int(2) DEFAULT NULL,
  `https` char(4) DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `source` char(20) DEFAULT NULL,
  `save_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vali_count` int(5) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `proxy_field` (`ip`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `free_ipproxy`
--

LOCK TABLES `free_ipproxy` WRITE;
/*!40000 ALTER TABLE `free_ipproxy` DISABLE KEYS */;
/*!40000 ALTER TABLE `free_ipproxy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `httpbin`
--

DROP TABLE IF EXISTS `httpbin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `httpbin` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `ip` char(25) NOT NULL,
  `port` int(4) NOT NULL,
  `country` text,
  `anonymity` int(2) DEFAULT NULL,
  `https` char(4) DEFAULT NULL,
  `speed` float DEFAULT NULL,
  `source` char(20) DEFAULT NULL,
  `save_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vali_count` int(5) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `proxy_field` (`ip`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `httpbin`
--

LOCK TABLES `httpbin` WRITE;
/*!40000 ALTER TABLE `httpbin` DISABLE KEYS */;
/*!40000 ALTER TABLE `httpbin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-24 13:38:56
