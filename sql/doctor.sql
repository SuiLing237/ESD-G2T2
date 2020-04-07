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
-- Table structure for table `doctor_info`
--
DROP TABLE IF EXISTS `doctor_info`;
CREATE TABLE IF NOT EXISTS `doctor_info` (
  `doctorID` int(64),
  `doctor_name` varchar(64) NOT NULL,
  `doctor_email` varchar(64) NOT NULL,
  `doctor_password` varchar(64) NOT NULL,
  PRIMARY KEY (`doctorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor_info`
--
INSERT INTO `doctor_info` (`doctorID`, `doctor_name`, `doctor_email`, `doctor_password`) VALUES
(1, "Jackson Tan", "jacksontan@hotmail.com", "jackson123");
COMMIT;

--
-- Table structure for table `doctor`
--
DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `bookingID` int(64),
  `patientID` int(64),
  `date` varchar(64) NOT NULL,
  `timeslot` varchar(64) NOT NULL,
  `availability` varchar(64) NOT NULL,
  PRIMARY KEY (`bookingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--
INSERT INTO `doctor` (`bookingID`, `patientID`, `date`, `timeslot`, `availability`) VALUES
(1, 1, "13-04-2020", "0800", "NO"),
(2, 2, "13-04-2020", "0830","NO"),
(3, 3, "13-04-2020", "0900", "NO"),
(4, 4, "13-04-2020", "0930","NO"),
(5, 5, "13-04-2020", "1000", "NO"),
(6, null, "13-04-2020", "1030", "YES"),
(7, null, "13-04-2020", "1100", "YES"),
(8, null, "13-04-2020", "1130", "YES"),
(9, null, "13-04-2020", "1200", "YES"),
(10, null, "13-04-2020", "1230", "YES"),
(11, null, "13-04-2020", "1300", "YES"),
(12, null, "13-04-2020", "1330", "YES"),
(13, null, "13-04-2020", "1400", "YES"),
(14, null, "13-04-2020", "1430", "YES"),
(15, null, "13-04-2020", "1500", "YES"),
(16, null, "13-04-2020", "1530", "YES"),
(17, null, "13-04-2020", "1600", "YES"),
(18, null, "13-04-2020", "1630", "YES"),
(19, null, "13-04-2020", "1700", "YES"),
(20, null, "14-04-2020", "0800", "YES"),
(21, null, "14-04-2020", "0830", "YES"),
(22, null, "14-04-2020", "0900", "YES"),
(23, null, "14-04-2020", "0930", "YES"),
(24, null, "14-04-2020", "1000", "YES"),
(25, null, "14-04-2020", "1030", "YES"),
(26, null, "14-04-2020", "1100", "YES"),
(27, null, "14-04-2020", "1130", "YES"),
(28, null, "14-04-2020", "1200", "YES"),
(29, null, "14-04-2020", "1230", "YES"),
(30, null, "14-04-2020", "1300", "YES"),
(31, null, "14-04-2020", "1330", "YES"),
(32, null, "14-04-2020", "1400", "YES"),
(33, null, "14-04-2020", "1430", "YES"),
(34, null, "14-04-2020", "1500", "YES"),
(35, null, "14-04-2020", "1530", "YES"),
(36, null, "14-04-2020", "1600", "YES"),
(37, null, "14-04-2020", "1630", "YES"),
(38, null, "14-04-2020", "1700", "YES"),
(39, null, "15-04-2020", "0800", "YES"),
(40, null, "15-04-2020", "0830", "YES"),
(41, null, "15-04-2020", "0900", "YES"),
(42, null, "15-04-2020", "0930", "YES"),
(43, null, "15-04-2020", "1000", "YES"),
(44, null, "15-04-2020", "1030", "YES"),
(45, null, "15-04-2020", "1100", "YES"),
(46, null, "15-04-2020", "1130", "YES"),
(47, null, "15-04-2020", "1200", "YES"),
(48, null, "15-04-2020", "1230", "YES"),
(49, null, "15-04-2020", "1300", "YES"),
(50, null, "15-04-2020", "1330", "YES"),
(51, null, "15-04-2020", "1400", "YES"),
(52, null, "15-04-2020", "1430", "YES"),
(53, null, "15-04-2020", "1500", "YES"),
(54, null, "15-04-2020", "1530", "YES"),
(55, null, "15-04-2020", "1600", "YES"),
(56, null, "15-04-2020", "1630", "YES"),
(57, null, "15-04-2020", "1700", "YES"),
(58, null, "16-04-2020", "0800", "YES"),
(59, null, "16-04-2020", "0830", "YES"),
(60, null, "16-04-2020", "0900", "YES"),
(61, null, "16-04-2020", "0930", "YES"),
(62, null, "16-04-2020", "1000", "YES"),
(63, null, "16-04-2020", "1030", "YES"),
(64, null, "16-04-2020", "1100", "YES"),
(65, null, "16-04-2020", "1130", "YES"),
(66, null, "16-04-2020", "1200", "YES"),
(67, null, "16-04-2020", "1230", "YES"),
(68, null, "16-04-2020", "1300", "YES"),
(69, null, "16-04-2020", "1330", "YES"),
(70, null, "16-04-2020", "1400", "YES"),
(71, null, "16-04-2020", "1430", "YES"),
(72, null, "16-04-2020", "1500", "YES"),
(73, null, "16-04-2020", "1530", "YES"),
(74, null, "16-04-2020", "1600", "YES"),
(75, null, "16-04-2020", "1630", "YES"),
(76, null, "16-04-2020", "1700", "YES"),
(77, null, "17-04-2020", "0800", "YES"),
(78, null, "17-04-2020", "0830", "YES"),
(79, null, "17-04-2020", "0900", "YES"),
(80, null, "17-04-2020", "0930", "YES"),
(81, null, "17-04-2020", "1000", "YES"),
(82, null, "17-04-2020", "1030", "YES"),
(83, null, "17-04-2020", "1100", "YES"),
(84, null, "17-04-2020", "1130", "YES"),
(85, null, "17-04-2020", "1200", "YES"),
(86, null, "17-04-2020", "1230", "YES"),
(87, null, "17-04-2020", "1300", "YES"),
(88, null, "17-04-2020", "1330", "YES"),
(89, null, "17-04-2020", "1400", "YES"),
(90, null, "17-04-2020", "1430", "YES"),
(91, null, "17-04-2020", "1500", "YES"),
(92, null, "17-04-2020", "1530", "YES"),
(93, null, "17-04-2020", "1600", "YES"),
(94, null, "17-04-2020", "1630", "YES"),
(95, null, "17-04-2020", "1700", "YES");
COMMIT;