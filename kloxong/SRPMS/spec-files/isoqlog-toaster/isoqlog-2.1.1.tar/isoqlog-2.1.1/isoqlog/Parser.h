#ifndef PARSER_H
#define PARSER_H

#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <errno.h>

typedef struct hist_stat {
	unsigned inode;
        int saved_pos;
} hist_stat;

void lowercase(char *);


/* Parser  routines for Qmail */
void readQmailLogFile(char *);
void parseQmailFromBytesLine(char *);
void parseQmailToRemoteLine(char *);
void parseQmailToLocalLine(char *);


/* Parser  routines for Sendmail  and Postfix*/
void readSendmailLogFile(char *);
void parseSendmailFromBytesLine(char *);
void parseSendmailToLine(char *);
int check_syslog_date(char *);

/* Parser  routines for Exim */
void readEximLogFile(char *);
void parseEximFromBytesLine(char *);
void parseEximToLine(char *);

#endif
