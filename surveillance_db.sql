-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 29, 2015 at 02:08 AM
-- Server version: 5.5.46-0ubuntu0.14.04.2
-- PHP Version: 5.5.30-1+deb.sury.org~trusty+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `surveillance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `access_entries`
--

CREATE TABLE IF NOT EXISTS `access_entries` (
  `access_id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `access_time` text NOT NULL,
  `confidence` double NOT NULL,
  `origin_x` int(11) NOT NULL,
  `origin_y` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  PRIMARY KEY (`access_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `access_entries`
--

INSERT INTO `access_entries` (`access_id`, `subject_id`, `access_time`, `confidence`, `origin_x`, `origin_y`, `height`, `width`) VALUES
(1, 3, 'Sunday 29 November 2015 01-01-37AM', 66.1728843408, 14, 14, 186, 186),
(2, 3, 'Sunday 29 November 2015 01-01-41AM', 74.0709625602, 19, 17, 176, 176),
(3, 3, 'Sunday 29 November 2015 01-01-45AM', 74.4543692117, 25, 20, 172, 172),
(4, 1, 'Sunday 29 November 2015 01-01-49AM', 69.619361111, 15, 14, 179, 179),
(5, 1, 'Sunday 29 November 2015 01-28-00AM', 85.8113494137, 11, 11, 152, 152),
(6, 1, 'Sunday 29 November 2015 01-28-04AM', 87.0801421979, 10, 10, 151, 151),
(7, 3, 'Sunday 29 November 2015 02-04-46AM', 68.5952725937, 12, 8, 191, 191);

-- --------------------------------------------------------

--
-- Table structure for table `motion_entries`
--

CREATE TABLE IF NOT EXISTS `motion_entries` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `occupied_time` text NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=40 ;

--
-- Dumping data for table `motion_entries`
--

INSERT INTO `motion_entries` (`event_id`, `room_id`, `occupied_time`) VALUES
(1, 1, 'Sunday 29 November 2015 01-35-23AM'),
(2, 1, 'Sunday 29 November 2015 01-35-23AM'),
(3, 1, 'Sunday 29 November 2015 01-35-24AM'),
(4, 1, 'Sunday 29 November 2015 01-35-24AM'),
(5, 1, 'Sunday 29 November 2015 01-35-24AM'),
(6, 1, 'Sunday 29 November 2015 01-35-24AM'),
(7, 1, 'Sunday 29 November 2015 01-35-24AM'),
(8, 1, 'Sunday 29 November 2015 01-35-25AM'),
(9, 1, 'Sunday 29 November 2015 01-35-25AM'),
(10, 1, 'Sunday 29 November 2015 01-35-27AM'),
(11, 1, 'Sunday 29 November 2015 01-35-30AM'),
(12, 1, 'Sunday 29 November 2015 01-35-30AM'),
(13, 1, 'Sunday 29 November 2015 01-35-30AM'),
(14, 1, 'Sunday 29 November 2015 01-35-31AM'),
(15, 1, 'Sunday 29 November 2015 01-35-31AM'),
(16, 1, 'Sunday 29 November 2015 01-35-31AM'),
(17, 1, 'Sunday 29 November 2015 01-35-31AM'),
(18, 1, 'Sunday 29 November 2015 01-35-34AM'),
(19, 1, 'Sunday 29 November 2015 01-35-34AM'),
(20, 1, 'Sunday 29 November 2015 01-37-36AM'),
(21, 1, 'Sunday 29 November 2015 01-37-36AM'),
(22, 1, 'Sunday 29 November 2015 01-37-36AM'),
(23, 1, 'Sunday 29 November 2015 01-37-37AM'),
(24, 1, 'Sunday 29 November 2015 01-37-37AM'),
(25, 1, 'Sunday 29 November 2015 02-04-23AM'),
(26, 1, 'Sunday 29 November 2015 02-04-24AM'),
(27, 1, 'Sunday 29 November 2015 02-04-24AM'),
(28, 1, 'Sunday 29 November 2015 02-04-24AM'),
(29, 1, 'Sunday 29 November 2015 02-04-24AM'),
(30, 1, 'Sunday 29 November 2015 02-04-25AM'),
(31, 1, 'Sunday 29 November 2015 02-04-25AM'),
(32, 1, 'Sunday 29 November 2015 02-04-25AM'),
(33, 1, 'Sunday 29 November 2015 02-04-25AM'),
(34, 1, 'Sunday 29 November 2015 02-04-26AM'),
(35, 1, 'Sunday 29 November 2015 02-04-26AM'),
(36, 1, 'Sunday 29 November 2015 02-04-27AM'),
(37, 1, 'Sunday 29 November 2015 02-04-27AM'),
(38, 1, 'Sunday 29 November 2015 02-04-27AM'),
(39, 1, 'Sunday 29 November 2015 02-04-27AM');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE IF NOT EXISTS `subjects` (
  `subject_id` int(11) NOT NULL,
  `subject_name` text NOT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`subject_id`, `subject_name`) VALUES
(1, 'Saleh'),
(2, 'Tawhid');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
