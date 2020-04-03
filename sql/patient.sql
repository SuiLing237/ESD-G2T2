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
  `patient_phone` int(8) NOT NULL,
  `patient_email` varchar(128) NOT NULL,
  `patient_password` varchar(128) NOT NULL,
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;

-- Add in `patient` values
INSERT INTO `patient` (`patientID`, `patient_name`, `patient_phone`,`patient_email`,`patient_password`) VALUES
(1, "Anne", 12348888, "Anne@hotmail.com", "anne123"),
(2, "Ben", 43211234, "Ben@hotmail.com", "ben123"),
(3, "Cathy", 56789999, "Cathy@hotmail.com", "cathy123"),
(4, "Dan", 11107778, "Dan@hotmail.com", "dan123"),
(5, "Edward", 96719999, "Edward@hotmail.com", "edward123"),
(6, "Mushi", 12345678, "mushi.lee.2018@sis.smu.edu.sg", "MushiMart"),
(7, "Sui Ling", 88888888, "slchua.2018@sis.smu.edu.sg", "SuiLing");
COMMIT;