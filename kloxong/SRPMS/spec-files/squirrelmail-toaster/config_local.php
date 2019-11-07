<?php
####################
# Local configuration for Qmail Toaster
# configure to suit your requirements
$hide_sm_attributions = true;
$useSendmail = false;
$imap_server_type = 'courier';
$optional_delimiter = '.';
$default_folder_prefix = 'INBOX.';
$show_prefix_option = false;
$show_contain_subfolders_option = false;
$delete_folder = true;
$plugins[] = 'calendar';
$plugins[] = 'notes';
$plugins[] = 'filters';
$plugins[] = 'quota_usage';
$plugins[] = 'unsafe_image_rules';
$plugins[] = 'qmailadmin_login';
?>
