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
(1, "18-02-2020", "3PM to 4PM", "Yes"),
(2, "22-02-2020", "11AM to 12PM","No"),
(3, "22-02-2020", "1.30PM to 2.30PM", "No"),
(4, "24-02-2020", "3PM to 4PM","Yes"),
(5, "27-02-2020", "4.30PM to 5.30PM", "Yes");
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
