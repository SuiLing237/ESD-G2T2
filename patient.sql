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
  `phone` int(8) NOT NULL,
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add in `patient` values
INSERT INTO `patient` (`patientID`, `patient_name`, `phone`) VALUES
(1, "Anne", 12348888),
(2, "Ben", 43211234),
(3, "Cathy", 56789999),
(4, "Dan", 11107778),
(5, "Edward", 96719999);
COMMIT;

--
-- Table structure for table `diagnosis`
--
DROP TABLE IF EXISTS `diagnosis`;
CREATE TABLE IF NOT EXISTS `diagnosis` (
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `diagnosis` varchar(100),
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add in `diagnosis` values
INSERT INTO `diagnosis` (`patientID`, `bookingID`, `diagnosis`) VALUES
(1, 1, "Common Cold"),
(2, 2, "Possibility of COVID-19"),
(3, 3, "Food poisoning"),
(4, 4, "Eczema"),
(5, 5, "Stomach Flu");
COMMIT;

--
-- Table structure for table `prescription`
--
DROP TABLE IF EXISTS `prescription`;
CREATE TABLE IF NOT EXISTS `prescription` (
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `medicineID` int(64) NOT NULL,
  `medicine_quantity` int(64) NOT NULL,
  PRIMARY KEY (`patientID`),
  KEY `FK_medicineID` (`medicineID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add in `prescription` values
INSERT INTO `prescription` (`patientID`, `bookingID`, `medicineID`, `medicine_quantity`) VALUES
(1, 1, 1, 4),
(2, 2, 2, 2),
(3, 3, 3, 3),
(4, 4, 2, 1),
(5, 5, 3, 3);
COMMIT;