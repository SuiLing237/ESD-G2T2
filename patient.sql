-- I HAVE ERROR, NOT FIXED YET

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
CREATE DATABASE IF NOT EXISTS 'patient' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE 'patient';

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS 'patient' (
  `patientID` int(64) NOT NULL,
  `patient_name` varchar(64) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` int(8) NOT NULL,
  PRIMARY KEY ('patientID')
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Dumping data for table `patient`
--

INSERT INTO 'patient' ('patientID', 'patient_name', 'address', 'phone', 'prescription') VALUES
('1', 'Jane', 'harbourfront', 12348888, 'metformin');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
