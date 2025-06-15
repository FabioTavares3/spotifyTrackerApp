CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_played` 
AS select `f`.`SQ_PK_SONGS` AS `SQ_PK_SONGS`,`f`.`song_name` AS `song_name`,`f`.`SONG_ID` AS `SONG_ID`,`f`.`USER_ID` AS `USER_ID`,
`f`.`timestamp` AS `timestamp`,`f`.`DURATION` AS `DURATION`,`f`.`dt_listened` AS `dt_listened`,`j`.`artist_id` AS `artist_id`
 from (`f_played` `f` join `d_songs_artists` `j`) where (`j`.`song_id` = `f`.`SONG_ID`);
 
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
 
CREATE TABLE `d_songs_artists` (
   `song_id` varchar(80) NOT NULL,
   `artist_id` varchar(80) NOT NULL,
   PRIMARY KEY (`song_id`,`artist_id`),
   KEY `artist_id` (`artist_id`),
   CONSTRAINT `d_songs_artists_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `d_songs` (`song_id`),
   CONSTRAINT `d_songs_artists_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `d_artists` (`artist_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

CREATE TABLE `f_played` (
   `SQ_PK_SONGS` int NOT NULL AUTO_INCREMENT,
   `song_name` char(100) DEFAULT NULL,
   `SONG_ID` varchar(45) NOT NULL,
   `USER_ID` varchar(45) NOT NULL,
   `timestamp` timestamp NULL DEFAULT NULL,
   `DURATION` int NOT NULL,
   `dt_listened` date DEFAULT NULL,
   PRIMARY KEY (`SQ_PK_SONGS`),
   UNIQUE KEY `UQ_f_played` (`timestamp`,`SONG_ID`,`USER_ID`),
   KEY `USER_ID_FK_idx` (`USER_ID`),
   KEY `SONG_ID_FK_idx` (`SONG_ID`),
   KEY `DT_LISTENED_idx` (`dt_listened`),
   CONSTRAINT `SONG_ID_FK` FOREIGN KEY (`SONG_ID`) REFERENCES `d_songs` (`song_id`),
   CONSTRAINT `USER_ID_FK` FOREIGN KEY (`USER_ID`) REFERENCES `d_user` (`user_id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci