-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: 'patient'
--
CREATE DATABASE IF NOT EXISTS `patient` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `patient`;

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--
DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS `patient` (
  `patientID` int(64) NOT NULL,
  `patient_name` varchar(64) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` int(8) NOT NULL,
--   `prescription` varchar(100),
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `patient`
--
-- INSERT INTO `patient` (`patientID`, `patient_name`, `address`, `phone`, `prescription`) VALUES
-- (1, "Anne", "Harbourfront", 12348888, "paracetamol"),
-- (2, "Ben", "Telok Blangah", 43211234, "metformin"),
-- (3, "Cathy", "Tampines", 56789999, "pamabrom"),
-- (4, "Dan", "Yio Chu Kang", 11107778, "anatacid"),
-- (5, "Edward", "Bencoolen", 96719999, "dextromethorphan");
-- COMMIT;

-- Without Prescription
INSERT INTO `patient` (`patientID`, `patient_name`, `phone`) VALUES
(1, "Anne", 12348888),
(2, "Ben", 43211234),
(3, "Cathy", 56789999),
(4, "Dan", 11107778),
(5, "Edward", 96719999);
COMMIT;


-- Table structure for table patient prescription
DROP TABLE IF EXISTS `prescription`;
CREATE TABLE IF NOT EXISTS `prescription` (
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `medicineID` int(64) NOT NULL,
  `medicineQuantity` int(64) NOT NULL,
  PRIMARY KEY (`patientID`),
  KEY `FK_medicineID` (`medicineID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `prescription` (`patientID`, `bookingID`, `medicineID`, `medicineQuantity`) VALUES
(1, 1, 1, 4),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 2, 1),
(5, 5, 3, 3);