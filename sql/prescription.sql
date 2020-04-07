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
CREATE DATABASE IF NOT EXISTS `prescription` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `prescription`;

-- --------------------------------------------------------

--
-- Table structure for table `prescription`
--
DROP TABLE IF EXISTS `prescription`;
CREATE TABLE IF NOT EXISTS `prescription` (
  `itemID` int(64) NOT NULL, 
  `patientID` int(64) NOT NULL,
  `bookingID` int(64) NOT NULL,
  `medicineID` int(64) NOT NULL,
  `medicine_quantity` int(64) NOT NULL,
  PRIMARY KEY (`itemID`)
--  KEY `FK_medicineID` (`medicineID`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;

-- Add in `prescription` values
-- INSERT INTO `prescription` (`itemID`, `patientID`, `bookingID`, `medicineID`, `medicine_quantity`) VALUES
-- (5, 1, 1, 1, 4),
-- (6, 2, 2, 2, 2),
-- (7, 3, 3, 3, 3),
-- (8, 4, 4, 2, 1),
-- (9, 5, 5, 3, 3);
-- COMMIT;