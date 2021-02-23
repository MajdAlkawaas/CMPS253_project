-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2021 at 05:58 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `queueMakerDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `AdminID` int(11) NOT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `Permission` enum('SuperAdmin','SubAdmin','Admin') DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `CategoryID` int(11) NOT NULL,
  `Name` varchar(150) DEFAULT NULL,
  `QueueID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CustomerID` int(11) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `ContactFirstName` varchar(45) DEFAULT NULL,
  `ContactLastName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `PhoneNumber` varchar(45) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `director`
--

CREATE TABLE `director` (
  `DirectorID` int(11) NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `guest`
--

CREATE TABLE `guest` (
  `GuestID` int(11) NOT NULL,
  `PhoneNumber` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `QueueID` int(11) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL,
  `QueueoperatorID` int(11) DEFAULT NULL,
  `DirectorID` int(11) DEFAULT NULL,
  `WalkedAway` bit(1) DEFAULT NULL,
  `Kickedout` bit(1) DEFAULT NULL,
  `Served` bit(1) DEFAULT NULL,
  `GuestNumber` int(11) DEFAULT NULL,
  `beginOfServiceTime` datetime DEFAULT NULL,
  `endOfServiceTime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `queue`
--

CREATE TABLE `queue` (
  `QueueID` int(11) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `DirectorID` int(11) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `Active` bit(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `queueoperator`
--

CREATE TABLE `queueoperator` (
  `QueueoperatorID` int(11) NOT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `CreatedAt` datetime DEFAULT NULL,
  `DirectorID` int(11) DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `QueueID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`AdminID`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`CategoryID`),
  ADD KEY `QueueID_idx` (`QueueID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CustomerID`);

--
-- Indexes for table `director`
--
ALTER TABLE `director`
  ADD PRIMARY KEY (`DirectorID`),
  ADD KEY `Customer_ID_idx` (`CustomerID`);

--
-- Indexes for table `guest`
--
ALTER TABLE `guest`
  ADD PRIMARY KEY (`GuestID`),
  ADD KEY `CustomerID_idx` (`CustomerID`),
  ADD KEY `Queue_ID_idx` (`QueueID`),
  ADD KEY `Category_ID_idx` (`CategoryID`),
  ADD KEY `Director_ID_idx` (`DirectorID`),
  ADD KEY `Queueoperator_ID_idx` (`QueueoperatorID`);

--
-- Indexes for table `queue`
--
ALTER TABLE `queue`
  ADD PRIMARY KEY (`QueueID`),
  ADD KEY `Director_ID_idx` (`DirectorID`);

--
-- Indexes for table `queueoperator`
--
ALTER TABLE `queueoperator`
  ADD PRIMARY KEY (`QueueoperatorID`),
  ADD KEY `FK_queueoperator_director` (`DirectorID`),
  ADD KEY `FK_queueoperator_customer` (`CustomerID`),
  ADD KEY `FK_queueoperator_queue` (`QueueID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `category`
--
ALTER TABLE `category`
  ADD CONSTRAINT `FK_category_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`);

--
-- Constraints for table `director`
--
ALTER TABLE `director`
  ADD CONSTRAINT `FK_director_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`);

--
-- Constraints for table `guest`
--
ALTER TABLE `guest`
  ADD CONSTRAINT `FK_guest_category` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`),
  ADD CONSTRAINT `FK_guest_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `FK_guest_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`),
  ADD CONSTRAINT `FK_guest_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`),
  ADD CONSTRAINT `FK_guest_queueoperator` FOREIGN KEY (`QueueoperatorID`) REFERENCES `queueoperator` (`QueueoperatorID`);

--
-- Constraints for table `queue`
--
ALTER TABLE `queue`
  ADD CONSTRAINT `FK_queue_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`);

--
-- Constraints for table `queueoperator`
--
ALTER TABLE `queueoperator`
  ADD CONSTRAINT `FK_queueoperator_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`),
  ADD CONSTRAINT `FK_queueoperator_director` FOREIGN KEY (`DirectorID`) REFERENCES `director` (`DirectorID`),
  ADD CONSTRAINT `FK_queueoperator_queue` FOREIGN KEY (`QueueID`) REFERENCES `queue` (`QueueID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
