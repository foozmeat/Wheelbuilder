# CocoaMySQL dump
# Version 0.7b5
# http://cocoamysql.sourceforge.net
#
# Host: localhost (MySQL 5.0.51-log)
# Database: wb_dev
# Generation Time: 2008-03-19 16:57:55 -0700
# ************************************************************

# Dump of table hubs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `hubs`;

CREATE TABLE `hubs` (
  `id` int(11) NOT NULL auto_increment,
  `description` varchar(255) NOT NULL default '',
  `s` float NOT NULL default '2.5',
  `dl` float NOT NULL default '0',
  `dr` float NOT NULL default '0',
  `wl` float NOT NULL default '0',
  `wr` float NOT NULL default '0',
  `old` float NOT NULL default '0',
  `forr` varchar(255) NOT NULL default 'f',
  `created_on` datetime default NULL,
  `updated_on` datetime default NULL,
  `comment` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  KEY `index_hubs_on_forr` (`forr`),
  KEY `index_hubs_on_description` (`description`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('1','Shimano XT M756 Disc','2.6','61','61','21.1','31.7','100','F','2007-12-14 16:36:25','2007-12-14 16:36:25','');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('2','Shimano XT M756 Disc','2.6','61','61','32.2','18.5','135','R','2007-12-14 16:43:30','2007-12-14 16:43:30','');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('3','Formula high-flange track','2.5','62','62','34.5','34.5','100','F','2007-12-27 12:25:10','2007-12-29 09:53:31','Same as IRO');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('4','Formula high-flange track','2.5','62','62','31','31','120','R','2007-12-28 08:42:38','2007-12-29 09:54:19','Same as IRO');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('6','Shimano Ultrgra 9-speed fh-6500','2.5','44.5','44.5','35','18','130','R','2008-03-15 12:47:19','2008-03-15 19:03:46','');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('7','Surly 1x1 (old)','2.4','43','43','33','33','100','F','2008-03-17 12:15:18','2008-03-17 12:15:18','These say 1x1 on the hub body');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('8','Surly 1x1 (old)','2.4','43','43','39','39','135','R','2008-03-17 12:16:18','2008-03-17 12:16:18','These say 1x1 on the hub body');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('9','Surly 1x1 (New)','2.4','54','54','32.2','32.2','100','F','2008-03-17 12:18:23','2008-03-17 12:18:23','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('10','Surly 1x1 (New) - Disc','2.4','58','58','22.5','32','100','F','2008-03-17 12:19:10','2008-03-17 12:19:10','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('11','Surly 1x1 (New) - Fixed/Fixed - Track','2.4','54','54','30','30','120','R','2008-03-17 12:20:15','2008-03-17 12:20:15','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('12','Surly 1x1 (New) - Fixed/Free - Track','2.4','54','54','31','30','120','R','2008-03-17 12:23:01','2008-03-17 12:23:01','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('13','Surly 1x1 - Fixed/Free - Road','2.4','54','54','33','31.5','130','R','2008-03-17 12:24:20','2008-03-17 12:24:20','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('14','Surly 1x1 - Free/Free - Mountain','2.4','54','54','38.5','38.5','135','R','2008-03-17 12:24:58','2008-03-17 12:24:58','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('15','Surly 1x1 - Fixed/Free - Mountain','2.4','54','54','37.5','38.5','135','R','2008-03-17 12:26:16','2008-03-17 12:26:16','These say Surly on the hub');
INSERT INTO `hubs` (`id`,`description`,`s`,`dl`,`dr`,`wl`,`wr`,`old`,`forr`,`created_on`,`updated_on`,`comment`) VALUES ('16','Surly 1x1 - Disc - Mountain','2.4','58','58','34','38.5','135','R','2008-03-17 12:28:58','2008-03-17 12:28:58','These say Surly on the hub');


