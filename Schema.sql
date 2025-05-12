CREATE DATABASE  IF NOT EXISTS `spotify_tracker_schema` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `spotify_tracker_schema`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: spotify_tracker_schema
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `d_artists`
--

DROP TABLE IF EXISTS `d_artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_artists` (
  `artist_id` varchar(50) NOT NULL,
  `artist_name` varchar(60) NOT NULL,
  `artist_url` char(80) NOT NULL,
  `artist_uri` char(80) NOT NULL,
  `artist_image` blob,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `artist_id_UNIQUE` (`artist_id`),
  UNIQUE KEY `artist_url` (`artist_url`),
  UNIQUE KEY `artist_uri` (`artist_uri`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `d_artists`
--

LOCK TABLES `d_artists` WRITE;
/*!40000 ALTER TABLE `d_artists` DISABLE KEYS */;
/*!40000 ALTER TABLE `d_artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `d_songs`
--

DROP TABLE IF EXISTS `d_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_songs` (
  `song_id` varchar(80) NOT NULL,
  `song_name` char(100) DEFAULT NULL,
  `duration` int NOT NULL,
  `album_name` char(100) DEFAULT NULL,
  `song_image` blob,
  `song_url` char(80) NOT NULL,
  `song_uri` char(80) NOT NULL,
  `album_url` char(70) NOT NULL,
  `album_id` char(80) NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `idd_songs_UNIQUE` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `d_songs`
--

LOCK TABLES `d_songs` WRITE;
/*!40000 ALTER TABLE `d_songs` DISABLE KEYS */;
/*!40000 ALTER TABLE `d_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `d_songs_artists`
--

DROP TABLE IF EXISTS `d_songs_artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_songs_artists` (
  `song_id` char(80) NOT NULL,
  `artist_id` char(80) NOT NULL,
  PRIMARY KEY (`song_id`,`artist_id`),
  KEY `artist_id` (`artist_id`),
  CONSTRAINT `d_songs_artists_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `d_songs` (`song_id`),
  CONSTRAINT `d_songs_artists_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `d_artists` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `d_songs_artists`
--

LOCK TABLES `d_songs_artists` WRITE;
/*!40000 ALTER TABLE `d_songs_artists` DISABLE KEYS */;
/*!40000 ALTER TABLE `d_songs_artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `d_user`
--

DROP TABLE IF EXISTS `d_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_user` (
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `email` char(50) NOT NULL,
  `country` char(20) NOT NULL,
  `membership` char(30) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `d_user`
--

LOCK TABLES `d_user` WRITE;
/*!40000 ALTER TABLE `d_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `d_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `f_played`
--

DROP TABLE IF EXISTS `f_played`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `f_played` (
  `SQ_PK_SONGS` int NOT NULL AUTO_INCREMENT,
  `song_name` char(100) DEFAULT NULL,
  `SONG_ID` varchar(45) NOT NULL,
  `USER_ID` varchar(45) NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `DURATION` int NOT NULL,
  `dt_listened` date DEFAULT NULL,
  PRIMARY KEY (`SQ_PK_SONGS`),
  UNIQUE KEY `timestamp` (`timestamp`),
  UNIQUE KEY `UQ_f_played` (`timestamp`,`SONG_ID`,`USER_ID`),
  KEY `USER_ID_FK_idx` (`USER_ID`),
  KEY `SONG_ID_FK_idx` (`SONG_ID`),
  KEY `TIMESTAMP_idx` (`timestamp`),
  CONSTRAINT `SONG_ID_FK` FOREIGN KEY (`SONG_ID`) REFERENCES `d_songs` (`song_id`),
  CONSTRAINT `USER_ID_FK` FOREIGN KEY (`USER_ID`) REFERENCES `d_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `f_played`
--

LOCK TABLES `f_played` WRITE;
/*!40000 ALTER TABLE `f_played` DISABLE KEYS */;
/*!40000 ALTER TABLE `f_played` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-11 22:13:42
