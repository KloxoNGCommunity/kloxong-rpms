CREATE DATABASE spamdyke;
USE spamdyke;
CREATE TABLE `spamdyke_log_table` (
	`id` bigint(7) NOT NULL auto_increment,
	`time` timestamp NOT NULL default CURRENT_TIMESTAMP,
	`reason` varchar(20) character set utf8 NOT NULL,
	`from` varchar(50) character set utf8 NOT NULL,
	`to` varchar(50) character set utf8 NOT NULL,
	`ip` varchar(15) character set utf8 NOT NULL,
	`rdns` varchar(50) character set utf8 NOT NULL,
	`auth` varchar(25) character set utf8 NOT NULL,
	PRIMARY KEY  (`id`),
	KEY `time` (`time`),
	KEY `reason` (`reason`,`from`,`to`,`ip`,`rdns`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
GRANT ALL ON spamdyke.* TO 'spamdyke'@'localhost' IDENTIFIED BY 'spamdyke';
