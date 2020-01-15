<?php

/**
 * Local config overrides.
 *
 * You can override the config.php settings here.
 * Don't do it unless you know what you're doing.
 * Use standard PHP syntax, see config.php for examples.
 *
 * @copyright &copy; 2002-2006 The SquirrelMail Project Team
 * @license http://opensource.org/licenses/gpl-license.php GNU Public License
 * @version $Id: config_local.php,v 1.2 2006/07/11 03:33:47 wtogami Exp $
 * @package squirrelmail
 * @subpackage config
 */

$default_folder_prefix		= '';

// Courier-imapd settings for Kloxo Next Generation

$sendmail_path = '/var/qmail/bin/sendmail';
$useSendmail = true;

$imap_type = 'courier';

if ($imap_type === 'dovecot') {
	$imap_server_type = 'dovecot';
	$default_folder_prefix = '';
	$trash_folder = 'Trash';
	$sent_folder = 'Sent';
	$draft_folder = 'Drafts';
	$show_prefix_option = false;
	$default_sub_of_inbox = false;
	$show_contain_subfolders_option = false;
	$optional_delimiter = 'detect';
	$delete_folder = false;
	$force_username_lowercase = true;
} elseif ($imap_type === 'courier') {
	$imap_server_type = 'courier';
	$default_folder_prefix = 'INBOX.';
	$trash_folder = 'Trash';
	$sent_folder = 'Sent';
	$draft_folder = 'Drafts';
	$show_prefix_option = false;
	$default_sub_of_inbox = false;
	$show_contain_subfolders_option = false;
	$optional_delimiter = '.';
	$delete_folder = true;
	$force_username_lowercase = false;
}

?>
