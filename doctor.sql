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
-- Database: 'doctor'
--
CREATE DATABASE IF NOT EXISTS `doctor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `doctor`;

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `bookingID` int(64),
  `date` varchar(64) NOT NULL,
  `timeslot` varchar(64) NOT NULL,
  `availability` varchar(64) NOT NULL,
  PRIMARY KEY (`bookingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--
INSERT INTO `doctor` (`bookingID`, `date`, `timeslot`, `availability`) VALUES
(1, "17-02-2020", "0800", "YES"),
(2, "17-02-2020", "0830","YES"),
(3, "17-02-2020", "0900", "YES"),
(4, "17-02-2020", "0930","YES"),
(5, "17-02-2020", "1000", "YES"),
(6, "17-02-2020", "1030", "YES"),
(7, "17-02-2020", "1100", "YES"),
(8, "17-02-2020", "1130", "YES"),
(9, "17-02-2020", "1200", "YES"),
(10, "17-02-2020", "1230", "YES"),
(11, "17-02-2020", "1300", "YES"),
(12, "17-02-2020", "1330", "YES"),
(13, "17-02-2020", "1400", "YES"),
(14, "17-02-2020", "1430", "YES"),
(15, "17-02-2020", "1500", "YES"),
(16, "17-02-2020", "1530", "YES"),
(17, "17-02-2020", "1600", "YES"),
(18, "17-02-2020", "1630", "YES"),
(19, "17-02-2020", "1700", "YES"),
(20, "18-02-2020", "0800", "YES"),
(21, "18-02-2020", "0830","YES"),
(22, "18-02-2020", "0900", "YES"),
(23, "18-02-2020", "0930","YES"),
(24, "18-02-2020", "1000", "YES"),
(25, "18-02-2020", "1030", "YES"),
(26, "18-02-2020", "1100", "YES"),
(27, "18-02-2020", "1130", "YES"),
(28, "18-02-2020", "1200", "YES"),
(29, "18-02-2020", "1230", "YES"),
(30, "18-02-2020", "1300", "YES"),
(31, "18-02-2020", "1330", "YES"),
(32, "18-02-2020", "1400", "YES"),
(33, "18-02-2020", "1430", "YES"),
(34, "18-02-2020", "1500", "YES"),
(35, "18-02-2020", "1530", "YES"),
(36, "18-02-2020", "1600", "YES"),
(37, "18-02-2020", "1630", "YES"),
(38, "18-02-2020", "1700", "YES");
COMMIT;