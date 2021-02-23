
DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `AdminID` int NOT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `Permission` enum('SuperAdmin','SubAdmin','Admin') DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`AdminID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;



DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `ContactFirstName` varchar(45) DEFAULT NULL,
  `ContactLastName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(45) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;


DROP TABLE IF EXISTS `director`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `director` (
  `DirectorID` int NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `password` varchar(45),
  `CustomerID` int DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`DirectorID`),
  KEY `Customer_ID_idx` (`CustomerID`),  -- TODO: What is this??
  CONSTRAINT `FK_director_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `queue` (
  `QueueID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `DirectorID` int DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `Active` bit(1) DEFAULT NULL,
  PRIMARY KEY (`QueueID`),
  KEY `Director_ID_idx` (`DirectorID`),
  CONSTRAINT `FK_queue_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `queueoperator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `queueoperator` (
  `QueueoperatorID` int NOT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `DirectorID` int DEFAULT NULL,
  `CustomerID` int DEFAULT NULL,
  `QueueID` int DEFAULT NULL,
  PRIMARY KEY (`QueueoperatorID`),

  -- KEY `CustomerID_idx` (`CustomerID`),
  -- KEY `Queue_ID_idx` (`QueueID`),
  -- KEY `Director_ID_idx` (`DirectorID`),
  
  CONSTRAINT `FK_queueoperator_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`),
  CONSTRAINT `FK_queueoperator_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  CONSTRAINT `FK_queueoperator_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`)
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CategoryID` int NOT NULL,
  `Name` varchar(150) DEFAULT NULL,
  `QueueID` int DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`CategoryID`),
  KEY `QueueID_idx` (`QueueID`),
  CONSTRAINT `FK_category_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;



DROP TABLE IF EXISTS `guest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guest` (
  `GuestID` int NOT NULL,
  `PhoneNumber` int DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `CustomerID` int DEFAULT NULL,
  `QueueID` int DEFAULT NULL,
  `CategoryID` int DEFAULT NULL,
  `QueueoperatorID` int DEFAULT NULL,
  `DirectorID` int DEFAULT NULL,
  `WalkedAway` bit(1) DEFAULT NULL,
  `Kickedout` bit(1) DEFAULT NULL,
  `Served` bit(1) DEFAULT NULL,
  `GuestNumber` int DEFAULT NULL,
  `beginOfServiceTime` datetime DEFAULT NULL,
  `endOfServiceTime` datetime DEFAULT NULL,
  PRIMARY KEY (`GuestID`),
  KEY `CustomerID_idx` (`CustomerID`),
  KEY `Queue_ID_idx` (`QueueID`),
  KEY `Category_ID_idx` (`CategoryID`),
  KEY `Director_ID_idx` (`DirectorID`),
  KEY `Queueoperator_ID_idx` (`QueueoperatorID`),
  CONSTRAINT `FK_guest_queueoperator` FOREIGN KEY (`QueueoperatorID`) REFERENCES `queueoperator` (`QueueoperatorID`),
  CONSTRAINT `FK_guest_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`),
  CONSTRAINT `FK_guest_category` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`),
  CONSTRAINT `FK_guest_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  CONSTRAINT `FK_guest_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;


