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
CREATE DATABASE IF NOT EXISTS `diagnosis` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `diagnosis`;

-- --------------------------------------------------------

--
-- Table structure for table `diagnosis`
--
DROP TABLE IF EXISTS `diagnosis`;
CREATE TABLE IF NOT EXISTS `diagnosis` (
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `diagnosis` varchar(100),
  PRIMARY KEY (`bookingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add in `diagnosis` values
INSERT INTO `diagnosis` (`patientID`, `bookingID`, `diagnosis`) VALUES
(1, 1, "Common Cold"),
(2, 2, "Possibility of COVID-19"),
(3, 3, "Food poisoning"),
(4, 4, "Eczema"),
(5, 5, "Stomach Flu");
COMMIT;