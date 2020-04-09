-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 20, 2020 at 10:01 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `price`
--
CREATE DATABASE IF NOT EXISTS `medicine` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `medicine`;

-- --------------------------------------------------------

--
-- Table structure for table `medicine`
--

DROP TABLE IF EXISTS `medicine`;
CREATE TABLE IF NOT EXISTS `medicine` (
  `medicineID` int(64) NOT NULL,
  `medicine_name` varchar(64) NOT NULL,
  `medicine_price` double(64,2) NOT NULL,
  PRIMARY KEY (`medicineID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `price`
--

INSERT INTO `medicine` (`medicineID`, `medicine_name`, `medicine_price`) VALUES
(1, 'Vicodin', 10.00),
(2, 'Simvastatin', 11.00),
(3, 'Lisinopril', 12.00),
(4, 'Levothyroxine', 13.00),
(5, 'Azithromycin', 14.00),
(6, 'Metformin', 15.00),
(7, 'Liptor', 16.00),
(8, 'Amlodipine', 17.00),
(9, 'Amoxicillin', 18.00),
(10, 'Hydrochlorothiazide', 19.00);
COMMIT;