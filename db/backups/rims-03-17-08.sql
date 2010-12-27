-- phpMyAdmin SQL Dump
-- version 2.11.2.1
-- http://www.phpmyadmin.net
--
-- Host: db.freebiketools.org
-- Generation Time: Mar 17, 2008 at 01:13 PM
-- Server version: 4.1.16
-- PHP Version: 4.4.7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `wb_prod`
--

-- --------------------------------------------------------

--
-- Table structure for table `rims`
--

DROP TABLE IF EXISTS `rims`;
CREATE TABLE IF NOT EXISTS `rims` (
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(255) NOT NULL default '',
  `erd` float NOT NULL default '0',
  `osb` float NOT NULL default '0',
  `size` int(11) NOT NULL default '0',
  `created_on` datetime default NULL,
  `updated_on` datetime default NULL,
  `comment` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  KEY `index_rims_on_size` (`size`),
  FULLTEXT KEY `index_rims_on_description` (`description`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=21 ;

--
-- Dumping data for table `rims`
--

INSERT INTO `rims` (`id`, `description`, `erd`, `osb`, `size`, `created_on`, `updated_on`, `comment`) VALUES
(1, 'Velocity Deep V', 582, 0, 622, '2007-11-29 01:27:51', '2007-11-29 01:27:51', NULL),
(2, 'Velocity Deep V', 531, 0, 571, '2007-11-29 01:40:01', '2007-11-29 01:40:01', NULL),
(3, 'Velocity Fusion', 591, 0, 622, '2007-12-14 13:02:29', '2007-12-14 13:02:29', NULL),
(4, 'Velocity Fusion', 541, 0, 571, '2007-12-14 13:02:58', '2007-12-14 13:02:58', NULL),
(5, 'Velocity Aerohead', 602, 0, 622, '2007-12-14 13:04:00', '2007-12-14 13:04:00', NULL),
(6, 'Velocity Aerohead', 554, 0, 571, '2007-12-14 13:04:24', '2007-12-14 13:04:24', NULL),
(7, 'Velocity Aeroheat', 536, 0, 559, '2007-12-14 13:08:03', '2007-12-14 13:08:03', NULL),
(8, 'Velocity Aerohead OC', 598, 4, 622, '2007-12-14 14:09:18', '2007-12-14 14:09:18', NULL),
(9, 'Alex Adventurer', 608, 0, 622, '2007-12-14 15:01:15', '2007-12-14 15:01:15', ''),
(10, 'Salsa Delgado 29er Disc Rim (29mm width)', 605, 0, 622, '2007-12-14 15:34:01', '2007-12-14 15:34:01', ''),
(11, 'DT Swiss RR 1.1', 599, 0, 622, '2007-12-14 17:32:01', '2007-12-14 17:32:01', 'Single and double'),
(12, 'Velocity Dyad', 596, 0, 622, '2007-12-17 15:37:24', '2007-12-17 15:37:24', ''),
(13, 'Mavic Open Pro', 602, 0, 622, '2007-12-17 17:25:29', '2007-12-17 17:25:29', ''),
(14, 'Mavic Open Sport', 606, 0, 622, '2007-12-17 17:31:19', '2007-12-17 17:31:19', ''),
(15, 'Velocity Razor', 607, 0, 622, '2008-03-15 18:57:55', '2008-03-15 18:57:55', ''),
(16, 'Surly Large Marge XC', 536, 0, 559, '2008-03-17 12:48:13', '2008-03-17 12:48:13', 'requires 16mm nipples'),
(17, 'Surly Large Marge DH', 489, 0, 507, '2008-03-17 12:50:22', '2008-03-17 12:50:22', 'requires 16mm nipples'),
(18, 'Surly Large Marge DH', 536, 0, 559, '2008-03-17 12:52:20', '2008-03-17 12:52:20', 'requires 16mm nipples'),
(19, 'Surly Large Marge OC DH', 535, 6, 559, '2008-03-17 12:53:35', '2008-03-17 12:53:35', 'requires 12mm nipples'),
(20, 'Surly Large Marge OC XC', 535, 6, 559, '2008-03-17 12:54:27', '2008-03-17 12:54:27', 'requires 12mm nipples');
