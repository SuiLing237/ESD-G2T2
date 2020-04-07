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
-- Database: 'payment'
--
CREATE DATABASE IF NOT EXISTS `payment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `payment`;

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--
DROP TABLE IF EXISTS `payment`;
CREATE TABLE IF NOT EXISTS `payment` (
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `total_price` double(64,2) NOT NULL,
  PRIMARY KEY (`bookingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Add in `payment` values
INSERT INTO `payment` (`patientID`, `bookingID`, `total_price`) VALUES
(1, 1, 90.00);
COMMIT;