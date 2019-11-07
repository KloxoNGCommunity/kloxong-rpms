-- phpMyAdmin SQL Dump
-- version 4.3.12
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 27, 2015 at 01:29 AM
-- Server version: 10.0.17-MariaDB
-- PHP Version: 5.4.39

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

-- Database: `afterlogic`

CREATE DATABASE IF NOT EXISTS afterlogic;

USE afterlogic;

-- --------------------------------------------------------

--
-- Table structure for table `acal_appointments`
--

CREATE TABLE IF NOT EXISTS `acal_appointments` (
  `id_appointment` int(11) NOT NULL,
  `id_event` int(11) NOT NULL DEFAULT '0',
  `id_user` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) DEFAULT NULL,
  `access_type` tinyint(4) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `hash` varchar(32) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_awm_fnbl_runs`
--

CREATE TABLE IF NOT EXISTS `acal_awm_fnbl_runs` (
  `id_run` int(11) NOT NULL,
  `run_date` datetime DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_calendars`
--

CREATE TABLE IF NOT EXISTS `acal_calendars` (
  `calendar_id` int(11) NOT NULL,
  `calendar_str_id` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `calendar_name` varchar(100) NOT NULL DEFAULT '',
  `calendar_description` text,
  `calendar_color` int(11) NOT NULL DEFAULT '0',
  `calendar_active` tinyint(1) NOT NULL DEFAULT '1'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_cron_runs`
--

CREATE TABLE IF NOT EXISTS `acal_cron_runs` (
  `id_run` bigint(20) NOT NULL,
  `run_date` datetime DEFAULT NULL,
  `latest_date` datetime DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_eventrepeats`
--

CREATE TABLE IF NOT EXISTS `acal_eventrepeats` (
  `id_repeat` int(11) NOT NULL,
  `id_event` int(11) DEFAULT NULL,
  `repeat_period` tinyint(1) NOT NULL DEFAULT '0',
  `repeat_order` tinyint(1) NOT NULL DEFAULT '1',
  `repeat_num` int(11) NOT NULL DEFAULT '0',
  `repeat_until` datetime DEFAULT NULL,
  `sun` tinyint(1) NOT NULL DEFAULT '0',
  `mon` tinyint(1) NOT NULL DEFAULT '0',
  `tue` tinyint(1) NOT NULL DEFAULT '0',
  `wed` tinyint(1) NOT NULL DEFAULT '0',
  `thu` tinyint(1) NOT NULL DEFAULT '0',
  `fri` tinyint(1) NOT NULL DEFAULT '0',
  `sat` tinyint(1) NOT NULL DEFAULT '0',
  `week_number` tinyint(1) DEFAULT NULL,
  `repeat_end` tinyint(1) NOT NULL DEFAULT '0',
  `excluded` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_events`
--

CREATE TABLE IF NOT EXISTS `acal_events` (
  `event_id` int(11) NOT NULL,
  `event_str_id` varchar(255) DEFAULT NULL,
  `calendar_id` int(11) DEFAULT NULL,
  `event_timefrom` datetime DEFAULT NULL,
  `event_timetill` datetime DEFAULT NULL,
  `event_allday` tinyint(1) NOT NULL DEFAULT '0',
  `event_name` varchar(100) NOT NULL DEFAULT '',
  `event_text` text,
  `event_priority` tinyint(4) DEFAULT NULL,
  `event_repeats` tinyint(1) NOT NULL DEFAULT '0',
  `event_last_modified` datetime DEFAULT NULL,
  `event_owner_email` varchar(255) NOT NULL DEFAULT '',
  `event_appointment_access` tinyint(4) NOT NULL DEFAULT '0',
  `event_deleted` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_exclusions`
--

CREATE TABLE IF NOT EXISTS `acal_exclusions` (
  `id_exclusion` int(11) NOT NULL,
  `id_event` int(11) DEFAULT NULL,
  `id_calendar` int(11) DEFAULT NULL,
  `id_repeat` int(11) DEFAULT NULL,
  `id_recurrence_date` datetime DEFAULT NULL,
  `event_timefrom` datetime DEFAULT NULL,
  `event_timetill` datetime DEFAULT NULL,
  `event_name` varchar(100) DEFAULT NULL,
  `event_text` text,
  `event_allday` tinyint(1) NOT NULL DEFAULT '0',
  `event_last_modified` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_publications`
--

CREATE TABLE IF NOT EXISTS `acal_publications` (
  `id_publication` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_calendar` int(11) DEFAULT NULL,
  `str_md5` varchar(32) DEFAULT NULL,
  `int_access_level` tinyint(4) NOT NULL DEFAULT '1',
  `access_type` tinyint(4) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_reminders`
--

CREATE TABLE IF NOT EXISTS `acal_reminders` (
  `id_reminder` int(11) NOT NULL,
  `id_event` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  `notice_type` tinyint(4) NOT NULL DEFAULT '0',
  `remind_offset` int(11) NOT NULL DEFAULT '0',
  `sent` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_sharing`
--

CREATE TABLE IF NOT EXISTS `acal_sharing` (
  `id_share` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id_calendar` int(11) DEFAULT NULL,
  `id_to_user` int(11) DEFAULT NULL,
  `str_to_email` varchar(255) NOT NULL DEFAULT '',
  `int_access_level` tinyint(4) NOT NULL DEFAULT '2',
  `calendar_active` tinyint(1) NOT NULL DEFAULT '1'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `acal_users_data`
--

CREATE TABLE IF NOT EXISTS `acal_users_data` (
  `settings_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL DEFAULT '0',
  `showweekends` tinyint(1) NOT NULL DEFAULT '0',
  `workdaystarts` tinyint(4) NOT NULL DEFAULT '9',
  `workdayends` tinyint(4) NOT NULL DEFAULT '17',
  `showworkday` tinyint(1) NOT NULL DEFAULT '0',
  `weekstartson` tinyint(4) NOT NULL DEFAULT '0',
  `defaulttab` tinyint(4) NOT NULL DEFAULT '2'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_addressbooks`
--

CREATE TABLE IF NOT EXISTS `adav_addressbooks` (
  `id` int(11) unsigned NOT NULL,
  `principaluri` varchar(255) DEFAULT NULL,
  `displayname` varchar(255) DEFAULT NULL,
  `uri` varchar(200) DEFAULT NULL,
  `description` text,
  `ctag` int(11) unsigned NOT NULL DEFAULT '1'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_cache`
--

CREATE TABLE IF NOT EXISTS `adav_cache` (
  `id` int(11) NOT NULL,
  `user` varchar(255) DEFAULT NULL,
  `calendaruri` varchar(255) DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `starttime` int(11) DEFAULT NULL,
  `eventid` varchar(45) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_calendarobjects`
--

CREATE TABLE IF NOT EXISTS `adav_calendarobjects` (
  `id` int(11) unsigned NOT NULL,
  `calendardata` mediumtext,
  `uri` varchar(255) DEFAULT NULL,
  `calendarid` int(11) unsigned NOT NULL,
  `lastmodified` int(11) DEFAULT NULL,
  `etag` varchar(32) NOT NULL DEFAULT '',
  `size` int(11) unsigned NOT NULL DEFAULT '0',
  `componenttype` varchar(8) NOT NULL DEFAULT '',
  `firstoccurence` int(11) unsigned DEFAULT NULL,
  `lastoccurence` int(11) unsigned DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_calendars`
--

CREATE TABLE IF NOT EXISTS `adav_calendars` (
  `id` int(11) unsigned NOT NULL,
  `principaluri` varchar(100) DEFAULT NULL,
  `displayname` varchar(100) DEFAULT NULL,
  `uri` varchar(255) DEFAULT NULL,
  `ctag` int(11) unsigned NOT NULL DEFAULT '0',
  `description` text,
  `calendarorder` int(11) unsigned NOT NULL DEFAULT '0',
  `calendarcolor` varchar(10) DEFAULT NULL,
  `timezone` text,
  `components` varchar(20) DEFAULT NULL,
  `transparent` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_calendarshares`
--

CREATE TABLE IF NOT EXISTS `adav_calendarshares` (
  `id` int(11) unsigned NOT NULL,
  `calendarid` int(11) unsigned DEFAULT NULL,
  `member` int(11) unsigned DEFAULT NULL,
  `status` tinyint(2) DEFAULT NULL,
  `readonly` tinyint(1) NOT NULL DEFAULT '0',
  `summary` varchar(150) DEFAULT NULL,
  `displayname` varchar(100) DEFAULT NULL,
  `color` varchar(10) DEFAULT NULL,
  `principaluri` varchar(255) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_cards`
--

CREATE TABLE IF NOT EXISTS `adav_cards` (
  `id` int(11) unsigned NOT NULL,
  `addressbookid` int(11) unsigned NOT NULL,
  `carddata` mediumtext,
  `uri` varchar(255) DEFAULT NULL,
  `lastmodified` int(11) unsigned DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_groupmembers`
--

CREATE TABLE IF NOT EXISTS `adav_groupmembers` (
  `id` int(11) unsigned NOT NULL,
  `principal_id` int(11) unsigned NOT NULL,
  `member_id` int(11) unsigned NOT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_locks`
--

CREATE TABLE IF NOT EXISTS `adav_locks` (
  `id` int(11) unsigned NOT NULL,
  `owner` varchar(100) DEFAULT NULL,
  `timeout` int(11) unsigned DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `token` varchar(100) DEFAULT NULL,
  `scope` tinyint(4) DEFAULT NULL,
  `depth` tinyint(4) DEFAULT NULL,
  `uri` text
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_principals`
--

CREATE TABLE IF NOT EXISTS `adav_principals` (
  `id` int(11) unsigned NOT NULL,
  `uri` varchar(255) NOT NULL,
  `email` varchar(80) DEFAULT NULL,
  `vcardurl` varchar(80) DEFAULT NULL,
  `displayname` varchar(80) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `adav_reminders`
--

CREATE TABLE IF NOT EXISTS `adav_reminders` (
  `id` int(11) unsigned NOT NULL,
  `user` varchar(100) NOT NULL,
  `calendaruri` varchar(255) DEFAULT NULL,
  `eventid` varchar(255) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `starttime` int(11) DEFAULT NULL,
  `allday` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_attachments`
--

CREATE TABLE IF NOT EXISTS `ahd_attachments` (
  `id_helpdesk_attachment` int(11) unsigned NOT NULL,
  `id_helpdesk_post` int(11) DEFAULT NULL,
  `id_helpdesk_thread` int(11) DEFAULT NULL,
  `id_tenant` int(11) DEFAULT NULL,
  `id_owner` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `size_in_bytes` int(11) unsigned DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `hash` text
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_fetcher`
--

CREATE TABLE IF NOT EXISTS `ahd_fetcher` (
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL DEFAULT '',
  `last_uid` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_online`
--

CREATE TABLE IF NOT EXISTS `ahd_online` (
  `id_helpdesk_thread` int(11) NOT NULL DEFAULT '0',
  `id_helpdesk_user` int(11) NOT NULL DEFAULT '0',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `ping_time` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_posts`
--

CREATE TABLE IF NOT EXISTS `ahd_posts` (
  `id_helpdesk_post` int(11) unsigned NOT NULL,
  `id_helpdesk_thread` int(11) DEFAULT NULL,
  `id_tenant` int(11) DEFAULT NULL,
  `id_owner` int(11) DEFAULT NULL,
  `type` smallint(6) NOT NULL DEFAULT '0',
  `system_type` smallint(6) NOT NULL DEFAULT '0',
  `text` text,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created` datetime DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_reads`
--

CREATE TABLE IF NOT EXISTS `ahd_reads` (
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `id_owner` int(11) DEFAULT NULL,
  `id_helpdesk_thread` int(11) DEFAULT NULL,
  `last_post_id` int(11) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_threads`
--

CREATE TABLE IF NOT EXISTS `ahd_threads` (
  `id_helpdesk_thread` int(11) unsigned NOT NULL,
  `str_helpdesk_hash` varchar(50) NOT NULL DEFAULT '',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `id_owner` int(11) NOT NULL DEFAULT '0',
  `post_count` int(11) NOT NULL DEFAULT '0',
  `last_post_id` int(11) NOT NULL DEFAULT '0',
  `last_post_owner_id` int(11) NOT NULL DEFAULT '0',
  `type` smallint(6) NOT NULL DEFAULT '0',
  `has_attachments` tinyint(1) NOT NULL DEFAULT '0',
  `archived` tinyint(1) NOT NULL DEFAULT '0',
  `notificated` tinyint(1) NOT NULL DEFAULT '0',
  `subject` varchar(255) NOT NULL DEFAULT '',
  `created` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ahd_users`
--

CREATE TABLE IF NOT EXISTS `ahd_users` (
  `id_helpdesk_user` int(11) unsigned NOT NULL,
  `id_system_user` int(11) NOT NULL DEFAULT '0',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `is_agent` tinyint(1) NOT NULL DEFAULT '0',
  `activated` tinyint(1) NOT NULL DEFAULT '0',
  `activate_hash` varchar(255) NOT NULL DEFAULT '',
  `blocked` tinyint(1) NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL DEFAULT '',
  `notification_email` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(255) NOT NULL DEFAULT '',
  `social_id` varchar(255) NOT NULL DEFAULT '',
  `social_type` varchar(255) NOT NULL DEFAULT '',
  `language` varchar(100) NOT NULL DEFAULT 'English',
  `date_format` varchar(50) NOT NULL DEFAULT '',
  `time_format` smallint(6) NOT NULL DEFAULT '0',
  `password_hash` varchar(255) NOT NULL DEFAULT '',
  `password_salt` varchar(255) NOT NULL DEFAULT '',
  `mail_notifications` tinyint(1) NOT NULL DEFAULT '0',
  `created` datetime DEFAULT NULL,
  `signature` varchar(255) NOT NULL DEFAULT '',
  `signature_enable` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_accounts`
--

CREATE TABLE IF NOT EXISTS `awm_accounts` (
  `id_acct` int(11) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `id_domain` int(11) NOT NULL DEFAULT '0',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `def_acct` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `quota` int(11) unsigned NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL DEFAULT '',
  `friendly_nm` varchar(255) DEFAULT NULL,
  `mail_protocol` tinyint(4) NOT NULL DEFAULT '1',
  `mail_inc_host` varchar(255) DEFAULT NULL,
  `mail_inc_port` int(11) NOT NULL DEFAULT '143',
  `mail_inc_login` varchar(255) DEFAULT NULL,
  `mail_inc_pass` varchar(255) DEFAULT NULL,
  `mail_inc_ssl` tinyint(1) NOT NULL DEFAULT '0',
  `mail_out_host` varchar(255) DEFAULT NULL,
  `mail_out_port` int(11) NOT NULL DEFAULT '25',
  `mail_out_login` varchar(255) DEFAULT NULL,
  `mail_out_pass` varchar(255) DEFAULT NULL,
  `mail_out_auth` tinyint(4) NOT NULL DEFAULT '0',
  `mail_out_ssl` tinyint(1) NOT NULL DEFAULT '0',
  `signature` text,
  `signature_type` tinyint(4) NOT NULL DEFAULT '1',
  `signature_opt` tinyint(4) NOT NULL DEFAULT '0',
  `mailbox_size` bigint(20) NOT NULL DEFAULT '0',
  `mailing_list` tinyint(1) NOT NULL DEFAULT '0',
  `hide_in_gab` tinyint(1) NOT NULL DEFAULT '0',
  `custom_fields` text,
  `is_password_specified` tinyint(1) NOT NULL DEFAULT '1',
  `allow_mail` tinyint(1) NOT NULL DEFAULT '1'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_account_quotas`
--

CREATE TABLE IF NOT EXISTS `awm_account_quotas` (
  `name` varchar(100) NOT NULL DEFAULT '',
  `quota_usage_messages` bigint(20) unsigned NOT NULL DEFAULT '0',
  `quota_usage_bytes` bigint(20) unsigned NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_addr_book`
--

CREATE TABLE IF NOT EXISTS `awm_addr_book` (
  `id_addr` bigint(20) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `id_domain` int(11) NOT NULL DEFAULT '0',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `str_id` varchar(255) DEFAULT NULL,
  `type` tinyint(4) NOT NULL DEFAULT '0',
  `type_id` varchar(100) NOT NULL DEFAULT '',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `view_email` varchar(255) NOT NULL DEFAULT '',
  `use_friendly_nm` tinyint(1) NOT NULL DEFAULT '1',
  `firstname` varchar(100) NOT NULL DEFAULT '',
  `surname` varchar(100) NOT NULL DEFAULT '',
  `nickname` varchar(100) NOT NULL DEFAULT '',
  `skype` varchar(100) NOT NULL DEFAULT '',
  `facebook` varchar(255) NOT NULL DEFAULT '',
  `h_email` varchar(255) DEFAULT NULL,
  `h_street` varchar(255) DEFAULT NULL,
  `h_city` varchar(200) DEFAULT NULL,
  `h_state` varchar(200) DEFAULT NULL,
  `h_zip` varchar(10) DEFAULT NULL,
  `h_country` varchar(200) DEFAULT NULL,
  `h_phone` varchar(50) DEFAULT NULL,
  `h_fax` varchar(50) DEFAULT NULL,
  `h_mobile` varchar(50) DEFAULT NULL,
  `h_web` varchar(255) DEFAULT NULL,
  `b_email` varchar(255) DEFAULT NULL,
  `b_company` varchar(200) DEFAULT NULL,
  `b_street` varchar(255) DEFAULT NULL,
  `b_city` varchar(200) DEFAULT NULL,
  `b_state` varchar(200) DEFAULT NULL,
  `b_zip` varchar(10) DEFAULT NULL,
  `b_country` varchar(200) DEFAULT NULL,
  `b_job_title` varchar(100) DEFAULT NULL,
  `b_department` varchar(200) DEFAULT NULL,
  `b_office` varchar(200) DEFAULT NULL,
  `b_phone` varchar(50) DEFAULT NULL,
  `b_fax` varchar(50) DEFAULT NULL,
  `b_web` varchar(255) DEFAULT NULL,
  `other_email` varchar(255) DEFAULT NULL,
  `primary_email` tinyint(4) DEFAULT NULL,
  `birthday_day` tinyint(4) NOT NULL DEFAULT '0',
  `birthday_month` tinyint(4) NOT NULL DEFAULT '0',
  `birthday_year` smallint(6) NOT NULL DEFAULT '0',
  `id_addr_prev` bigint(20) DEFAULT NULL,
  `tmp` tinyint(1) NOT NULL DEFAULT '0',
  `use_frequency` int(11) NOT NULL DEFAULT '11',
  `auto_create` tinyint(1) NOT NULL DEFAULT '0',
  `notes` varchar(255) DEFAULT NULL,
  `etag` varchar(100) NOT NULL DEFAULT '',
  `shared_to_all` tinyint(1) NOT NULL DEFAULT '0',
  `hide_in_gab` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_addr_groups`
--

CREATE TABLE IF NOT EXISTS `awm_addr_groups` (
  `id_group` int(11) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `group_nm` varchar(255) DEFAULT NULL,
  `group_str_id` varchar(100) DEFAULT NULL,
  `use_frequency` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) DEFAULT NULL,
  `company` varchar(200) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `state` varchar(200) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `country` varchar(200) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `fax` varchar(50) DEFAULT NULL,
  `web` varchar(255) DEFAULT NULL,
  `organization` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_addr_groups_contacts`
--

CREATE TABLE IF NOT EXISTS `awm_addr_groups_contacts` (
  `id_addr` bigint(20) NOT NULL DEFAULT '0',
  `id_group` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_addr_groups_events`
--

CREATE TABLE IF NOT EXISTS `awm_addr_groups_events` (
  `id` bigint(20) NOT NULL DEFAULT '0',
  `id_group` int(11) NOT NULL DEFAULT '0',
  `id_calendar` varchar(250) DEFAULT NULL,
  `id_event` varchar(250) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_channels`
--

CREATE TABLE IF NOT EXISTS `awm_channels` (
  `id_channel` int(11) NOT NULL,
  `login` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_columns`
--

CREATE TABLE IF NOT EXISTS `awm_columns` (
  `id` int(11) NOT NULL,
  `id_column` int(11) NOT NULL DEFAULT '0',
  `id_user` int(11) NOT NULL DEFAULT '0',
  `column_value` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_domains`
--

CREATE TABLE IF NOT EXISTS `awm_domains` (
  `id_domain` int(11) NOT NULL,
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `user_quota` int(11) NOT NULL DEFAULT '0',
  `override_settings` tinyint(1) NOT NULL DEFAULT '0',
  `mail_protocol` tinyint(4) NOT NULL DEFAULT '1',
  `mail_inc_host` varchar(255) DEFAULT NULL,
  `mail_inc_port` int(11) NOT NULL DEFAULT '143',
  `mail_inc_ssl` tinyint(1) NOT NULL DEFAULT '0',
  `mail_out_host` varchar(255) DEFAULT NULL,
  `mail_out_port` int(11) NOT NULL DEFAULT '25',
  `mail_out_auth` tinyint(4) NOT NULL DEFAULT '1',
  `mail_out_login` varchar(255) DEFAULT NULL,
  `mail_out_pass` varchar(255) DEFAULT NULL,
  `mail_out_ssl` tinyint(1) NOT NULL DEFAULT '0',
  `mail_out_method` tinyint(4) NOT NULL DEFAULT '1',
  `quota_mbytes_limit` int(11) unsigned NOT NULL DEFAULT '0',
  `quota_usage_bytes` bigint(20) unsigned NOT NULL DEFAULT '0',
  `quota_usage_messages` bigint(20) unsigned NOT NULL DEFAULT '0',
  `allow_webmail` tinyint(1) NOT NULL DEFAULT '1',
  `site_name` varchar(255) DEFAULT NULL,
  `allow_change_interface_settings` tinyint(1) NOT NULL DEFAULT '0',
  `allow_users_add_acounts` tinyint(1) NOT NULL DEFAULT '0',
  `allow_change_account_settings` tinyint(1) NOT NULL DEFAULT '0',
  `allow_new_users_register` tinyint(1) NOT NULL DEFAULT '1',
  `allow_open_pgp` tinyint(1) NOT NULL DEFAULT '0',
  `def_user_timezone` int(11) NOT NULL DEFAULT '0',
  `def_user_timeformat` tinyint(4) NOT NULL DEFAULT '0',
  `def_user_dateformat` varchar(100) NOT NULL DEFAULT 'MM/DD/YYYY',
  `msgs_per_page` smallint(6) NOT NULL DEFAULT '20',
  `skin` varchar(255) DEFAULT NULL,
  `lang` varchar(255) DEFAULT NULL,
  `ext_imap_host` varchar(255) NOT NULL DEFAULT '',
  `ext_smtp_host` varchar(255) NOT NULL DEFAULT '',
  `ext_dav_host` varchar(255) NOT NULL DEFAULT '',
  `allow_contacts` tinyint(1) NOT NULL DEFAULT '1',
  `contacts_per_page` smallint(6) NOT NULL DEFAULT '20',
  `allow_calendar` tinyint(1) NOT NULL DEFAULT '1',
  `cal_week_starts_on` tinyint(4) NOT NULL DEFAULT '0',
  `cal_show_weekends` tinyint(1) NOT NULL DEFAULT '0',
  `cal_workday_starts` tinyint(4) NOT NULL DEFAULT '9',
  `cal_workday_ends` tinyint(4) NOT NULL DEFAULT '18',
  `cal_show_workday` tinyint(1) NOT NULL DEFAULT '0',
  `cal_default_tab` tinyint(4) NOT NULL DEFAULT '2',
  `layout` tinyint(4) NOT NULL DEFAULT '0',
  `xlist` tinyint(1) NOT NULL DEFAULT '1',
  `global_addr_book` tinyint(4) NOT NULL DEFAULT '0',
  `check_interval` int(11) NOT NULL DEFAULT '0',
  `allow_registration` tinyint(1) NOT NULL DEFAULT '0',
  `allow_pass_reset` tinyint(1) NOT NULL DEFAULT '0',
  `allow_files` tinyint(1) NOT NULL DEFAULT '1',
  `allow_helpdesk` tinyint(1) NOT NULL DEFAULT '1',
  `use_threads` tinyint(1) NOT NULL DEFAULT '1',
  `is_internal` tinyint(1) NOT NULL DEFAULT '0',
  `disabled` tinyint(1) NOT NULL DEFAULT '0',
  `default_tab` varchar(255) NOT NULL DEFAULT 'mailbox',
  `is_default_for_tenant` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_domain_quotas`
--

CREATE TABLE IF NOT EXISTS `awm_domain_quotas` (
  `name` varchar(100) NOT NULL DEFAULT '',
  `quota_usage_messages` bigint(20) unsigned NOT NULL DEFAULT '0',
  `quota_usage_bytes` bigint(20) unsigned NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_fetchers`
--

CREATE TABLE IF NOT EXISTS `awm_fetchers` (
  `id_fetcher` int(11) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `id_user` int(11) NOT NULL DEFAULT '0',
  `id_domain` int(11) NOT NULL DEFAULT '0',
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `locked` tinyint(1) NOT NULL DEFAULT '0',
  `mail_check_interval` int(11) NOT NULL DEFAULT '0',
  `mail_check_lasttime` int(11) NOT NULL DEFAULT '0',
  `leave_messages` tinyint(1) NOT NULL DEFAULT '1',
  `frienly_name` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `signature` text,
  `signature_opt` tinyint(4) NOT NULL DEFAULT '0',
  `inc_host` varchar(255) NOT NULL DEFAULT '',
  `inc_port` int(11) NOT NULL DEFAULT '110',
  `inc_login` varchar(255) NOT NULL DEFAULT '',
  `inc_password` varchar(255) NOT NULL DEFAULT '',
  `inc_security` tinyint(4) NOT NULL DEFAULT '0',
  `out_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `out_host` varchar(255) NOT NULL DEFAULT '',
  `out_port` int(11) NOT NULL DEFAULT '110',
  `out_auth` tinyint(1) NOT NULL DEFAULT '1',
  `out_security` tinyint(4) NOT NULL DEFAULT '0',
  `dest_folder` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_filters`
--

CREATE TABLE IF NOT EXISTS `awm_filters` (
  `id_filter` int(11) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `field` tinyint(4) NOT NULL DEFAULT '0',
  `condition` tinyint(4) NOT NULL DEFAULT '0',
  `filter` varchar(255) DEFAULT NULL,
  `action` tinyint(4) NOT NULL DEFAULT '0',
  `id_folder` bigint(20) NOT NULL DEFAULT '0',
  `applied` tinyint(1) NOT NULL DEFAULT '1'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_folders`
--

CREATE TABLE IF NOT EXISTS `awm_folders` (
  `id_folder` bigint(20) NOT NULL,
  `id_parent` bigint(20) NOT NULL DEFAULT '0',
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `type` smallint(6) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `full_path` varchar(255) DEFAULT NULL,
  `sync_type` tinyint(4) NOT NULL DEFAULT '0',
  `hide` tinyint(1) NOT NULL DEFAULT '0',
  `fld_order` smallint(6) NOT NULL DEFAULT '1',
  `flags` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_folders_order`
--

CREATE TABLE IF NOT EXISTS `awm_folders_order` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `folders_order` text
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_folders_order_names`
--

CREATE TABLE IF NOT EXISTS `awm_folders_order_names` (
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `real_name` varchar(255) NOT NULL DEFAULT '',
  `order_name` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_folders_tree`
--

CREATE TABLE IF NOT EXISTS `awm_folders_tree` (
  `id` int(11) NOT NULL,
  `id_folder` bigint(20) NOT NULL DEFAULT '0',
  `id_parent` bigint(20) NOT NULL DEFAULT '0',
  `folder_level` tinyint(4) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_identities`
--

CREATE TABLE IF NOT EXISTS `awm_identities` (
  `id_identity` int(11) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `email` varchar(255) NOT NULL DEFAULT '',
  `friendly_nm` varchar(255) NOT NULL DEFAULT '',
  `signature` text,
  `signature_type` tinyint(4) NOT NULL DEFAULT '1',
  `use_signature` tinyint(1) NOT NULL DEFAULT '0',
  `def_identity` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_mailaliases`
--

CREATE TABLE IF NOT EXISTS `awm_mailaliases` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) DEFAULT NULL,
  `alias_name` varchar(255) NOT NULL DEFAULT '',
  `alias_domain` varchar(255) NOT NULL DEFAULT '',
  `alias_to` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_mailforwards`
--

CREATE TABLE IF NOT EXISTS `awm_mailforwards` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) DEFAULT NULL,
  `forward_name` varchar(255) NOT NULL DEFAULT '',
  `forward_domain` varchar(255) NOT NULL DEFAULT '',
  `forward_to` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_mailinglists`
--

CREATE TABLE IF NOT EXISTS `awm_mailinglists` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) DEFAULT NULL,
  `list_name` varchar(255) NOT NULL DEFAULT '',
  `list_to` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_messages`
--

CREATE TABLE IF NOT EXISTS `awm_messages` (
  `id` bigint(20) NOT NULL,
  `id_msg` bigint(20) NOT NULL DEFAULT '0',
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `id_folder_srv` bigint(20) NOT NULL DEFAULT '0',
  `id_folder_db` bigint(20) NOT NULL DEFAULT '0',
  `str_uid` varchar(255) DEFAULT NULL,
  `int_uid` bigint(20) NOT NULL DEFAULT '0',
  `from_msg` varchar(255) DEFAULT NULL,
  `to_msg` varchar(255) DEFAULT NULL,
  `cc_msg` varchar(255) DEFAULT NULL,
  `bcc_msg` varchar(255) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `msg_date` datetime DEFAULT NULL,
  `attachments` tinyint(1) NOT NULL DEFAULT '0',
  `size` bigint(20) NOT NULL DEFAULT '0',
  `seen` tinyint(1) NOT NULL DEFAULT '0',
  `flagged` tinyint(1) NOT NULL DEFAULT '0',
  `priority` tinyint(4) NOT NULL DEFAULT '0',
  `downloaded` tinyint(1) NOT NULL DEFAULT '0',
  `x_spam` tinyint(1) NOT NULL DEFAULT '0',
  `rtl` tinyint(1) NOT NULL DEFAULT '0',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  `is_full` tinyint(1) NOT NULL DEFAULT '1',
  `replied` tinyint(1) DEFAULT NULL,
  `forwarded` tinyint(1) DEFAULT NULL,
  `flags` int(11) DEFAULT NULL,
  `body_text` longtext,
  `grayed` tinyint(1) NOT NULL DEFAULT '0',
  `charset` int(11) NOT NULL DEFAULT '-1',
  `sensitivity` tinyint(4) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_messages_body`
--

CREATE TABLE IF NOT EXISTS `awm_messages_body` (
  `id` bigint(20) NOT NULL,
  `id_msg` bigint(20) NOT NULL DEFAULT '0',
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `msg` longblob
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_min`
--

CREATE TABLE IF NOT EXISTS `awm_min` (
  `hash_id` varchar(32) NOT NULL DEFAULT '',
  `hash` varchar(20) NOT NULL DEFAULT '',
  `data` text
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_reads`
--

CREATE TABLE IF NOT EXISTS `awm_reads` (
  `id_read` bigint(20) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `str_uid` varchar(255) DEFAULT NULL,
  `tmp` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_senders`
--

CREATE TABLE IF NOT EXISTS `awm_senders` (
  `id` int(11) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) DEFAULT NULL,
  `safety` tinyint(4) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_settings`
--

CREATE TABLE IF NOT EXISTS `awm_settings` (
  `id_setting` int(11) NOT NULL,
  `id_user` int(11) NOT NULL DEFAULT '0',
  `id_subscription` int(11) NOT NULL DEFAULT '0',
  `id_helpdesk_user` int(11) NOT NULL DEFAULT '0',
  `msgs_per_page` smallint(6) NOT NULL DEFAULT '20',
  `contacts_per_page` smallint(6) NOT NULL DEFAULT '20',
  `created_time` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `last_login_now` datetime DEFAULT NULL,
  `logins_count` int(11) NOT NULL DEFAULT '0',
  `auto_checkmail_interval` int(11) NOT NULL DEFAULT '0',
  `def_skin` varchar(255) NOT NULL DEFAULT 'Default',
  `def_editor` tinyint(1) NOT NULL DEFAULT '1',
  `layout` tinyint(4) NOT NULL DEFAULT '0',
  `save_mail` tinyint(4) NOT NULL DEFAULT '0',
  `def_timezone` smallint(6) NOT NULL DEFAULT '0',
  `def_time_fmt` varchar(255) DEFAULT NULL,
  `def_lang` varchar(255) DEFAULT NULL,
  `def_date_fmt` varchar(100) NOT NULL DEFAULT 'MM/DD/YYYY',
  `mailbox_limit` bigint(20) NOT NULL DEFAULT '0',
  `incoming_charset` varchar(30) NOT NULL DEFAULT 'iso-8859-1',
  `question_1` varchar(255) DEFAULT NULL,
  `answer_1` varchar(255) DEFAULT NULL,
  `question_2` varchar(255) DEFAULT NULL,
  `answer_2` varchar(255) DEFAULT NULL,
  `sip_enable` tinyint(1) NOT NULL DEFAULT '1',
  `sip_impi` varchar(255) NOT NULL DEFAULT '',
  `sip_password` varchar(255) NOT NULL DEFAULT '',
  `twilio_number` varchar(255) NOT NULL DEFAULT '',
  `twilio_enable` tinyint(1) NOT NULL DEFAULT '1',
  `twilio_default_number` tinyint(1) NOT NULL DEFAULT '0',
  `files_enable` tinyint(1) NOT NULL DEFAULT '1',
  `use_threads` tinyint(1) NOT NULL DEFAULT '1',
  `save_replied_messages_to_current_folder` tinyint(1) NOT NULL DEFAULT '0',
  `desktop_notifications` tinyint(1) NOT NULL DEFAULT '0',
  `allow_change_input_direction` tinyint(1) NOT NULL DEFAULT '0',
  `allow_helpdesk_notifications` tinyint(1) NOT NULL DEFAULT '0',
  `enable_open_pgp` tinyint(1) NOT NULL DEFAULT '0',
  `allow_autosave_in_drafts` tinyint(1) NOT NULL DEFAULT '1',
  `autosign_outgoing_emails` tinyint(1) NOT NULL DEFAULT '0',
  `capa` varchar(255) DEFAULT NULL,
  `client_timezone` varchar(100) NOT NULL DEFAULT '',
  `custom_fields` text,
  `helpdesk_signature` varchar(255) NOT NULL DEFAULT '',
  `helpdesk_signature_enable` tinyint(1) NOT NULL DEFAULT '0',
  `email_notification` varchar(255) NOT NULL DEFAULT '',
  `password_reset_hash` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_social`
--

CREATE TABLE IF NOT EXISTS `awm_social` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `id_social` varchar(255) DEFAULT NULL,
  `type` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) DEFAULT NULL,
  `access_token` text,
  `refresh_token` varchar(255) DEFAULT NULL,
  `type_str` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `scopes` varchar(255) DEFAULT NULL,
  `disabled` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_subscriptions`
--

CREATE TABLE IF NOT EXISTS `awm_subscriptions` (
  `id_subscription` int(11) NOT NULL,
  `id_tenant` int(11) NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL DEFAULT '',
  `description` varchar(255) NOT NULL DEFAULT '',
  `capa` varchar(255) NOT NULL DEFAULT '',
  `limit` int(11) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_system_folders`
--

CREATE TABLE IF NOT EXISTS `awm_system_folders` (
  `id` int(11) NOT NULL,
  `id_acct` int(11) NOT NULL DEFAULT '0',
  `id_user` int(11) NOT NULL DEFAULT '0',
  `folder_full_name` varchar(255) DEFAULT NULL,
  `system_type` tinyint(4) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_tenants`
--

CREATE TABLE IF NOT EXISTS `awm_tenants` (
  `id_tenant` int(11) NOT NULL,
  `id_channel` int(11) NOT NULL DEFAULT '0',
  `disabled` tinyint(1) NOT NULL DEFAULT '0',
  `login_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `login` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `quota` int(11) NOT NULL DEFAULT '0',
  `files_usage_bytes` bigint(20) unsigned NOT NULL DEFAULT '0',
  `user_count_limit` int(11) NOT NULL DEFAULT '0',
  `domain_count_limit` int(11) NOT NULL DEFAULT '0',
  `capa` varchar(255) NOT NULL DEFAULT '',
  `allow_change_email` tinyint(1) NOT NULL DEFAULT '1',
  `allow_change_password` tinyint(1) NOT NULL DEFAULT '1',
  `expared_timestamp` int(11) unsigned NOT NULL DEFAULT '0',
  `pay_url` varchar(255) NOT NULL DEFAULT '',
  `is_trial` tinyint(1) NOT NULL DEFAULT '0',
  `hd_admin_email_account` varchar(255) NOT NULL DEFAULT '',
  `hd_client_iframe_url` varchar(255) NOT NULL DEFAULT '',
  `hd_agent_iframe_url` varchar(255) NOT NULL DEFAULT '',
  `hd_site_name` varchar(255) NOT NULL DEFAULT '',
  `hd_style_allow` tinyint(1) NOT NULL DEFAULT '0',
  `hd_style_image` varchar(255) NOT NULL DEFAULT '',
  `hd_style_text` text,
  `login_style_image` varchar(255) NOT NULL DEFAULT '',
  `app_style_image` varchar(255) NOT NULL DEFAULT '',
  `hd_facebook_allow` tinyint(1) NOT NULL DEFAULT '0',
  `hd_facebook_id` varchar(255) NOT NULL DEFAULT '',
  `hd_facebook_secret` varchar(255) NOT NULL DEFAULT '',
  `hd_google_allow` tinyint(1) NOT NULL DEFAULT '0',
  `hd_google_id` varchar(255) NOT NULL DEFAULT '',
  `hd_google_secret` varchar(255) NOT NULL DEFAULT '',
  `hd_twitter_allow` tinyint(1) NOT NULL DEFAULT '0',
  `hd_twitter_id` varchar(255) NOT NULL DEFAULT '',
  `hd_twitter_secret` varchar(255) NOT NULL DEFAULT '',
  `hd_allow_fetcher` tinyint(1) NOT NULL DEFAULT '0',
  `hd_fetcher_type` int(11) NOT NULL DEFAULT '0',
  `hd_fetcher_timer` int(11) NOT NULL DEFAULT '0',
  `social_facebook_allow` tinyint(1) NOT NULL DEFAULT '0',
  `social_facebook_id` varchar(255) NOT NULL DEFAULT '',
  `social_facebook_secret` varchar(255) NOT NULL DEFAULT '',
  `social_google_allow` tinyint(1) NOT NULL DEFAULT '0',
  `social_google_id` varchar(255) NOT NULL DEFAULT '',
  `social_google_secret` varchar(255) NOT NULL DEFAULT '',
  `social_google_api_key` varchar(255) NOT NULL DEFAULT '',
  `social_twitter_allow` tinyint(1) NOT NULL DEFAULT '0',
  `social_twitter_id` varchar(255) NOT NULL DEFAULT '',
  `social_twitter_secret` varchar(255) NOT NULL DEFAULT '',
  `social_dropbox_allow` tinyint(1) NOT NULL DEFAULT '0',
  `social_dropbox_secret` varchar(255) NOT NULL DEFAULT '',
  `social_dropbox_key` varchar(255) NOT NULL DEFAULT '',
  `sip_allow` tinyint(1) NOT NULL DEFAULT '0',
  `sip_allow_configuration` tinyint(1) NOT NULL DEFAULT '0',
  `sip_realm` varchar(255) NOT NULL DEFAULT '',
  `sip_websocket_proxy_url` varchar(255) NOT NULL DEFAULT '',
  `sip_outbound_proxy_url` varchar(255) NOT NULL DEFAULT '',
  `sip_caller_id` varchar(255) NOT NULL DEFAULT '',
  `twilio_allow` tinyint(1) NOT NULL DEFAULT '0',
  `twilio_allow_configuration` tinyint(1) NOT NULL DEFAULT '0',
  `twilio_phone_number` varchar(255) NOT NULL DEFAULT '',
  `twilio_account_sid` varchar(255) NOT NULL DEFAULT '',
  `twilio_auth_token` varchar(255) NOT NULL DEFAULT '',
  `twilio_app_sid` varchar(255) NOT NULL DEFAULT '',
  `calendar_notification_email_account` varchar(255) NOT NULL DEFAULT '',
  `invite_notification_email_account` varchar(255) NOT NULL DEFAULT ''
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_tenant_quotas`
--

CREATE TABLE IF NOT EXISTS `awm_tenant_quotas` (
  `name` varchar(100) NOT NULL DEFAULT '',
  `quota_usage_messages` bigint(20) unsigned NOT NULL DEFAULT '0',
  `quota_usage_bytes` bigint(20) unsigned NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `awm_tenant_socials`
--

CREATE TABLE IF NOT EXISTS `awm_tenant_socials` (
  `id` int(11) NOT NULL,
  `id_tenant` int(11) DEFAULT NULL,
  `social_allow` tinyint(1) NOT NULL DEFAULT '0',
  `social_name` varchar(255) DEFAULT NULL,
  `social_id` varchar(255) DEFAULT NULL,
  `social_secret` varchar(255) DEFAULT NULL,
  `social_api_key` varchar(255) DEFAULT NULL,
  `social_scopes` varchar(255) DEFAULT NULL
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `a_users`
--

CREATE TABLE IF NOT EXISTS `a_users` (
  `id_user` int(11) NOT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0'
) DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `twofa_accounts`
--

CREATE TABLE IF NOT EXISTS `twofa_accounts` (
  `id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `auth_type` varchar(255) NOT NULL DEFAULT 'authy',
  `data_type` int(11) NOT NULL DEFAULT '1',
  `data_value` varchar(255) DEFAULT NULL
) DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acal_appointments`
--
ALTER TABLE `acal_appointments`
  ADD PRIMARY KEY (`id_appointment`);

--
-- Indexes for table `acal_awm_fnbl_runs`
--
ALTER TABLE `acal_awm_fnbl_runs`
  ADD PRIMARY KEY (`id_run`);

--
-- Indexes for table `acal_calendars`
--
ALTER TABLE `acal_calendars`
  ADD PRIMARY KEY (`calendar_id`);

--
-- Indexes for table `acal_cron_runs`
--
ALTER TABLE `acal_cron_runs`
  ADD PRIMARY KEY (`id_run`);

--
-- Indexes for table `acal_eventrepeats`
--
ALTER TABLE `acal_eventrepeats`
  ADD PRIMARY KEY (`id_repeat`);

--
-- Indexes for table `acal_events`
--
ALTER TABLE `acal_events`
  ADD PRIMARY KEY (`event_id`);

--
-- Indexes for table `acal_exclusions`
--
ALTER TABLE `acal_exclusions`
  ADD PRIMARY KEY (`id_exclusion`);

--
-- Indexes for table `acal_publications`
--
ALTER TABLE `acal_publications`
  ADD PRIMARY KEY (`id_publication`);

--
-- Indexes for table `acal_reminders`
--
ALTER TABLE `acal_reminders`
  ADD PRIMARY KEY (`id_reminder`);

--
-- Indexes for table `acal_sharing`
--
ALTER TABLE `acal_sharing`
  ADD PRIMARY KEY (`id_share`);

--
-- Indexes for table `acal_users_data`
--
ALTER TABLE `acal_users_data`
  ADD PRIMARY KEY (`settings_id`),
  ADD KEY `ACAL_USERS_DATA_USER_ID_INDEX` (`user_id`);

--
-- Indexes for table `adav_addressbooks`
--
ALTER TABLE `adav_addressbooks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_cache`
--
ALTER TABLE `adav_cache`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_calendarobjects`
--
ALTER TABLE `adav_calendarobjects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_calendars`
--
ALTER TABLE `adav_calendars`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_calendarshares`
--
ALTER TABLE `adav_calendarshares`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_cards`
--
ALTER TABLE `adav_cards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ADAV_CARDS_ADDRESSBOOKID_INDEX` (`addressbookid`);

--
-- Indexes for table `adav_groupmembers`
--
ALTER TABLE `adav_groupmembers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ADAV_GROUPMEMBERS_MEMBER_ID_PRINCIPAL_ID_INDEX` (`principal_id`,`member_id`);

--
-- Indexes for table `adav_locks`
--
ALTER TABLE `adav_locks`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `adav_principals`
--
ALTER TABLE `adav_principals`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ADAV_PRINCIPALS_URI_INDEX` (`uri`);

--
-- Indexes for table `adav_reminders`
--
ALTER TABLE `adav_reminders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ahd_attachments`
--
ALTER TABLE `ahd_attachments`
  ADD PRIMARY KEY (`id_helpdesk_attachment`);

--
-- Indexes for table `ahd_posts`
--
ALTER TABLE `ahd_posts`
  ADD PRIMARY KEY (`id_helpdesk_post`);

--
-- Indexes for table `ahd_threads`
--
ALTER TABLE `ahd_threads`
  ADD PRIMARY KEY (`id_helpdesk_thread`);

--
-- Indexes for table `ahd_users`
--
ALTER TABLE `ahd_users`
  ADD PRIMARY KEY (`id_helpdesk_user`);

--
-- Indexes for table `awm_accounts`
--
ALTER TABLE `awm_accounts`
  ADD PRIMARY KEY (`id_acct`),
  ADD KEY `AWM_ACCOUNTS_ID_USER_INDEX` (`id_user`),
  ADD KEY `AWM_ACCOUNTS_ID_ACCT_ID_USER_INDEX` (`id_acct`,`id_user`),
  ADD KEY `AWM_ACCOUNTS_MAIL_INC_LOGIN_INDEX` (`mail_inc_login`),
  ADD KEY `AWM_ACCOUNTS_EMAIL_INDEX` (`email`);

--
-- Indexes for table `awm_account_quotas`
--
ALTER TABLE `awm_account_quotas`
  ADD KEY `AWM_ACCOUNT_QUOTAS_NAME_INDEX` (`name`);

--
-- Indexes for table `awm_addr_book`
--
ALTER TABLE `awm_addr_book`
  ADD PRIMARY KEY (`id_addr`),
  ADD KEY `AWM_ADDR_BOOK_ID_USER_INDEX` (`id_user`),
  ADD KEY `AWM_ADDR_BOOK_DELETED_ID_USER_INDEX` (`id_user`,`deleted`),
  ADD KEY `AWM_ADDR_BOOK_USE_FREQUENCY_INDEX` (`use_frequency`),
  ADD KEY `AWM_ADDR_BOOK_VIEW_EMAIL_INDEX` (`view_email`);

--
-- Indexes for table `awm_addr_groups`
--
ALTER TABLE `awm_addr_groups`
  ADD PRIMARY KEY (`id_group`),
  ADD KEY `AWM_ADDR_GROUPS_ID_USER_INDEX` (`id_user`),
  ADD KEY `AWM_ADDR_GROUPS_USE_FREQUENCY_INDEX` (`use_frequency`);

--
-- Indexes for table `awm_channels`
--
ALTER TABLE `awm_channels`
  ADD PRIMARY KEY (`id_channel`);

--
-- Indexes for table `awm_columns`
--
ALTER TABLE `awm_columns`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_COLUMNS_ID_USER_INDEX` (`id_user`);

--
-- Indexes for table `awm_domains`
--
ALTER TABLE `awm_domains`
  ADD PRIMARY KEY (`id_domain`);

--
-- Indexes for table `awm_domain_quotas`
--
ALTER TABLE `awm_domain_quotas`
  ADD KEY `AWM_DOMAIN_QUOTAS_NAME_INDEX` (`name`);

--
-- Indexes for table `awm_fetchers`
--
ALTER TABLE `awm_fetchers`
  ADD PRIMARY KEY (`id_fetcher`);

--
-- Indexes for table `awm_filters`
--
ALTER TABLE `awm_filters`
  ADD PRIMARY KEY (`id_filter`),
  ADD KEY `AWM_FILTERS_ID_ACCT_ID_FOLDER_INDEX` (`id_acct`,`id_folder`);

--
-- Indexes for table `awm_folders`
--
ALTER TABLE `awm_folders`
  ADD PRIMARY KEY (`id_folder`),
  ADD KEY `AWM_FOLDERS_ID_ACCT_ID_FOLDER_INDEX` (`id_acct`,`id_folder`),
  ADD KEY `AWM_FOLDERS_ID_ACCT_ID_PARENT_INDEX` (`id_acct`,`id_parent`);

--
-- Indexes for table `awm_folders_order`
--
ALTER TABLE `awm_folders_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_FOLDERS_ORDER_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_folders_order_names`
--
ALTER TABLE `awm_folders_order_names`
  ADD KEY `AWM_FOLDERS_ORDER_NAMES_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_folders_tree`
--
ALTER TABLE `awm_folders_tree`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_FOLDERS_TREE_ID_FOLDER_INDEX` (`id_folder`),
  ADD KEY `AWM_FOLDERS_TREE_ID_FOLDER_ID_PARENT_INDEX` (`id_folder`,`id_parent`);

--
-- Indexes for table `awm_identities`
--
ALTER TABLE `awm_identities`
  ADD PRIMARY KEY (`id_identity`);

--
-- Indexes for table `awm_mailaliases`
--
ALTER TABLE `awm_mailaliases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_MAILALIASES_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_mailforwards`
--
ALTER TABLE `awm_mailforwards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_MAILFORWARDS_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_mailinglists`
--
ALTER TABLE `awm_mailinglists`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_MAILINGLISTS_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_messages`
--
ALTER TABLE `awm_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_MESSAGES_ID_ACCT_ID_FOLDER_DB_INDEX` (`id_acct`,`id_folder_db`),
  ADD KEY `AWM_MESSAGES_ID_ACCT_ID_FOLDER_DB_SEEN_INDEX` (`id_acct`,`id_folder_db`,`seen`);

--
-- Indexes for table `awm_messages_body`
--
ALTER TABLE `awm_messages_body`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `AWM_MESSAGES_BODY_ID_ACCT_ID_MSG_INDEX` (`id_acct`,`id_msg`);

--
-- Indexes for table `awm_min`
--
ALTER TABLE `awm_min`
  ADD KEY `AWM_MIN_HASH_INDEX` (`hash`);

--
-- Indexes for table `awm_reads`
--
ALTER TABLE `awm_reads`
  ADD PRIMARY KEY (`id_read`),
  ADD KEY `AWM_READS_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_senders`
--
ALTER TABLE `awm_senders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_SENDERS_ID_USER_INDEX` (`id_user`);

--
-- Indexes for table `awm_settings`
--
ALTER TABLE `awm_settings`
  ADD PRIMARY KEY (`id_setting`),
  ADD UNIQUE KEY `AWM_SETTINGS_ID_USER_INDEX` (`id_user`);

--
-- Indexes for table `awm_social`
--
ALTER TABLE `awm_social`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_SOCIAL_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_subscriptions`
--
ALTER TABLE `awm_subscriptions`
  ADD PRIMARY KEY (`id_subscription`);

--
-- Indexes for table `awm_system_folders`
--
ALTER TABLE `awm_system_folders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `AWM_SYSTEM_FOLDERS_ID_ACCT_INDEX` (`id_acct`);

--
-- Indexes for table `awm_tenants`
--
ALTER TABLE `awm_tenants`
  ADD PRIMARY KEY (`id_tenant`);

--
-- Indexes for table `awm_tenant_quotas`
--
ALTER TABLE `awm_tenant_quotas`
  ADD KEY `AWM_TENANT_QUOTAS_NAME_INDEX` (`name`);

--
-- Indexes for table `awm_tenant_socials`
--
ALTER TABLE `awm_tenant_socials`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `a_users`
--
ALTER TABLE `a_users`
  ADD PRIMARY KEY (`id_user`);

--
-- Indexes for table `twofa_accounts`
--
ALTER TABLE `twofa_accounts`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `acal_appointments`
--
ALTER TABLE `acal_appointments`
  MODIFY `id_appointment` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_awm_fnbl_runs`
--
ALTER TABLE `acal_awm_fnbl_runs`
  MODIFY `id_run` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_calendars`
--
ALTER TABLE `acal_calendars`
  MODIFY `calendar_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_cron_runs`
--
ALTER TABLE `acal_cron_runs`
  MODIFY `id_run` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_eventrepeats`
--
ALTER TABLE `acal_eventrepeats`
  MODIFY `id_repeat` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_events`
--
ALTER TABLE `acal_events`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_exclusions`
--
ALTER TABLE `acal_exclusions`
  MODIFY `id_exclusion` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_publications`
--
ALTER TABLE `acal_publications`
  MODIFY `id_publication` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_reminders`
--
ALTER TABLE `acal_reminders`
  MODIFY `id_reminder` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_sharing`
--
ALTER TABLE `acal_sharing`
  MODIFY `id_share` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `acal_users_data`
--
ALTER TABLE `acal_users_data`
  MODIFY `settings_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_addressbooks`
--
ALTER TABLE `adav_addressbooks`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_cache`
--
ALTER TABLE `adav_cache`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_calendarobjects`
--
ALTER TABLE `adav_calendarobjects`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_calendars`
--
ALTER TABLE `adav_calendars`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_calendarshares`
--
ALTER TABLE `adav_calendarshares`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_cards`
--
ALTER TABLE `adav_cards`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_groupmembers`
--
ALTER TABLE `adav_groupmembers`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_locks`
--
ALTER TABLE `adav_locks`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_principals`
--
ALTER TABLE `adav_principals`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `adav_reminders`
--
ALTER TABLE `adav_reminders`
  MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ahd_attachments`
--
ALTER TABLE `ahd_attachments`
  MODIFY `id_helpdesk_attachment` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ahd_posts`
--
ALTER TABLE `ahd_posts`
  MODIFY `id_helpdesk_post` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ahd_threads`
--
ALTER TABLE `ahd_threads`
  MODIFY `id_helpdesk_thread` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ahd_users`
--
ALTER TABLE `ahd_users`
  MODIFY `id_helpdesk_user` int(11) unsigned NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_accounts`
--
ALTER TABLE `awm_accounts`
  MODIFY `id_acct` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_addr_book`
--
ALTER TABLE `awm_addr_book`
  MODIFY `id_addr` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_addr_groups`
--
ALTER TABLE `awm_addr_groups`
  MODIFY `id_group` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_channels`
--
ALTER TABLE `awm_channels`
  MODIFY `id_channel` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_columns`
--
ALTER TABLE `awm_columns`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_domains`
--
ALTER TABLE `awm_domains`
  MODIFY `id_domain` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_fetchers`
--
ALTER TABLE `awm_fetchers`
  MODIFY `id_fetcher` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_filters`
--
ALTER TABLE `awm_filters`
  MODIFY `id_filter` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_folders`
--
ALTER TABLE `awm_folders`
  MODIFY `id_folder` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_folders_order`
--
ALTER TABLE `awm_folders_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_folders_tree`
--
ALTER TABLE `awm_folders_tree`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_identities`
--
ALTER TABLE `awm_identities`
  MODIFY `id_identity` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_mailaliases`
--
ALTER TABLE `awm_mailaliases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_mailforwards`
--
ALTER TABLE `awm_mailforwards`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_mailinglists`
--
ALTER TABLE `awm_mailinglists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_messages`
--
ALTER TABLE `awm_messages`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_messages_body`
--
ALTER TABLE `awm_messages_body`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_reads`
--
ALTER TABLE `awm_reads`
  MODIFY `id_read` bigint(20) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_senders`
--
ALTER TABLE `awm_senders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_settings`
--
ALTER TABLE `awm_settings`
  MODIFY `id_setting` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_social`
--
ALTER TABLE `awm_social`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_subscriptions`
--
ALTER TABLE `awm_subscriptions`
  MODIFY `id_subscription` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_system_folders`
--
ALTER TABLE `awm_system_folders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_tenants`
--
ALTER TABLE `awm_tenants`
  MODIFY `id_tenant` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `awm_tenant_socials`
--
ALTER TABLE `awm_tenant_socials`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `a_users`
--
ALTER TABLE `a_users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `twofa_accounts`
--
ALTER TABLE `twofa_accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
