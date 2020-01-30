#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <errno.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "Data.h"
#include "loadconfig.h"
#include "Parser.h"

extern char hostname[VALSIZE];
extern char outputdir[VALSIZE];
extern int cur_year, cur_month, cur_day;
char *months[12] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};


void lowercase(char *s)
{
	        while (*s) {
			*s = tolower(*s);
			s++;
		}
}


/* These three functions read the logfile and fill the data structure	*/
void readQmailLogFile(char *fn) 
{	

	FILE *fp;
	char buf[1024];

	if ((fp = fopen(fn, "r")) == NULL) {
		fprintf(stderr, "fopen: %s: %s\n", fn, strerror(errno));
		exit(-1);
	}

	while ((fgets(buf, 1024, fp)) != NULL) {
		if ((strstr(buf, " from ")) != NULL)  /* if this is from line */
			parseQmailFromBytesLine(buf);
		else if ((strstr(buf, " to remote ")) != NULL) {
			parseQmailToRemoteLine(buf);
			}
		else if ((strstr(buf, " to local ")) != NULL) {
			parseQmailToLocalLine(buf);
		}
	}
	fclose(fp);
}	

void readSendmailLogFile(char *fn) 
{	
	FILE *fp;
	char buf[1024];

	if ((fp = fopen(fn, "r")) == NULL) {
		fprintf(stderr, "fopen: %s: %s\n", fn, strerror(errno));
		exit(-1);
	}
	 /* Get the historical values of last read log file's inode number
	    If both inode numbers are the same, we assume that log file 
	    has not been changed (i.e rotated, removed), so we can 
	    go past offset bytes and continue to read new logs */

	while ((fgets(buf, 1024, fp)) != NULL) {
		if ((check_syslog_date(buf)) > 0) {
			if ((strstr(buf, " from=")) != NULL)  /* if this is from line */
				parseSendmailFromBytesLine(buf);
			else if ((strstr(buf, " to=")) != NULL)
				parseSendmailToLine(buf);
		}
	}

	/* close */
	fclose(fp);
}

int check_syslog_date(char *buf)
{
	unsigned char m[3]= {0};
	int day = 0, i = 0, j;

		 for (i = 0; buf[i] != ' ' && buf[i] != '\n' && buf[i] != EOF; i++)
			 m[i] = buf[i];
		 	 m[3] = '\0';
		while(buf[i] ==' ')
			i++;
		 for (j = i++; buf[j] != ' ' && buf[j] != '\n' && buf[j] != EOF; j++)
			 day =  10 * day + (buf[j] - '0');
		 if ((strcmp(months[cur_month -1], m) == 0) && (day == cur_day ))  
		 	return 1;
		 return -1;
}
/* This function parses one line from log file, checks if any " from " 
 * is matched. If so, returns the mail address */
void parseQmailFromBytesLine(char *str)
{

	char *p;
	char *email;
	char *domain;
	char *bytes;
	char *savemail;
	char *savebytes;
	char *savedomain;

	p = str;
	if (((strstr(str, " from <>")) != NULL) || ((strstr(str, " bytes ")) == NULL)) {
		(general.from_cnt)++;
		return;  /* null sender */
	}
	/* get bytes */
    	while (strncmp (p, " bytes ", 7))
		p++;
	p += 7;
	 if (strstr(p, "@") == NULL) {
		(general.from_cnt)++;
		return; /*null sender, ignore it */
	 }
	
	lowercase(p);
	bytes = (char *)malloc(16 * (sizeof(char)));
	savebytes = bytes;
	while ((*bytes++ =  *p++) != ' ')
		;
	*(--bytes) = '\0';
	/* get from */
    	while (strncmp (p,"from ", 5))
        	p++;
    	p += 6;
	email = (char *)malloc((strlen(p) + 2) * sizeof(char));
	savemail = email;
	while ((*email++ = *p++) != '@')
		;
	/* get from domain */
	domain = (char *)malloc((strlen(p)  +2) * sizeof(char));
	savedomain = domain;

	while ((*domain++ = *email++ = *p++) != '>')
		;
	*(--email) = '\0';
	*(--domain) = '\0';
	/* lowercase(savedomain);
	lowercase(savemail); */
	checkUser(savedomain, savemail, FROM_MAIL, atol(savebytes));
	(general.from_cnt)++;
	general.from_byte += atol(savebytes);
	free(savebytes);
	free(savemail);
	free(savedomain);
}

void parseQmailToRemoteLine(char *str)
{
	char *p;
	char *email;
	char *domain;
	char *savemail;
	char *savedomain;

    	p = str;
	/* get email */
    	while (strncmp (p," to remote ", 11))
        	p++;
    	p += 11;
	if ((strstr(p, "@")) == NULL) {
		(general.to_cnt)++;
		return; /* null to*/
	}
	lowercase(p);
	email = (char *)malloc((strlen(p) + 2) * sizeof(char));
	savemail = email;

	while ((*email++ = *p++) != '@')
		;
	/* get from domain */
	domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
	savedomain = domain;
	while ((*domain++ = *email++ = *p++) != '\n')
		;
	*(--email) = '\0';
	*(--domain) = '\0';
	checkUser(savedomain, savemail, TO_MAIL, 0);
	(general.to_cnt)++;
	free(savedomain);
	free(savemail);
}

void parseQmailToLocalLine(char *str)
{
	int state  = 0;
	char *p;
	char *email;
	char *domain;
	char *savemail;
	char *savemail2;
	char *savedomain;
	char *vdomain;

    	p = str;
    	while (strncmp (p," to local ",10))
        	p++;
    	p += 10;
	if ((strstr(p, "@")) == NULL) {
		(general.to_cnt)++;
		return;
	}
	lowercase(p);
	email = (char *)malloc((strlen(p) + 2) * sizeof(char));
	savemail = email;  
	while ((*email++ = *p++) != '@')
		;
	domain = (char *)malloc((strlen(p)  +2) * sizeof(char));
	savedomain = domain;
	while (( (*domain++ = *email++ = *p++) != '\n'))
		;
	*(--email) = '\0';
	*(--domain) = '\0';
	vdomain = (char *)malloc((strlen(savedomain) + 2) * (sizeof(char)));
	sprintf(vdomain, "%s-", savedomain);
	if ((strstr(savemail, vdomain)) != NULL)  {
		state = 1;
		while(*savemail++ !='-')
			;
	savemail2 = (char *)malloc((strlen(savemail) + 2) * sizeof(char));
	strcpy(savemail2, savemail);
	}
	/* lowercase(savedomain);
	lowercase(savemail); */
	if (state == 1) {
		checkUser(savedomain, savemail2, TO_MAIL, 0);
		(general.to_cnt)++;
		free(savemail2);
	}
	else {
		checkUser(savedomain, savemail, TO_MAIL, 0);
		(general.to_cnt)++;
		free(savemail);
	}
		free(vdomain);
		free(savedomain);
}
	

/* This function parses one line from log file, checks if any " from " 
 * is matched. If so, returns the mail address */
void parseSendmailFromBytesLine(char *str)
{
	int i = 0, state = 0;
	char *p;
	char *email;
	char *domain;
	char *bytes;
	char *savemail;
	char *savebytes;
	char *savedomain;

	if (((strstr(str, " from=<>")) != NULL) || ((strstr(str, " from=,")) != NULL) ) {
		(general.from_cnt)++;
		return; /* null sender */
	}
	else if (((strstr(str, " from=<")) != NULL) && ((strstr(str, " size=")) != NULL )) {
   	 	p = str;
    		while (strncmp (p,"from=<", 6))
        		p++;
    		p += 6;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') { /* check for @*/
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i;
		if (state == 0) {
			p--;  /*get back first char */
			while ((*email++ = *p++) != '>')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else  { /* state = 1 , means we found @ at from part */
			while (((*email++ = *p++) != '@'))
				;
			/* get from domain */
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != '>')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
			p++;
		}
	}
	/* if line is contain from= */
	/* we use two diffrent method to get email address from "from" line because
	 * there are two kinds of logging method for sendmail */
	else if (((strstr(str, " from=")) != NULL) && ((strstr(str, " size=")) != NULL )) {
    		p = str;
  	  	while (strncmp (p,"from=", 5))
        		p++;
    		p += 5;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != ',')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {  /* state =1 , @ is found */
			while ((*email++ = *p++) != '@')
				;
			/*get from domain */
			domain = (char *)malloc((strlen(p) + 1) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != ',')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
		}
	} /* else if (((strstr(str, " from=")) != NULL) && ((s .....ends here */
	else
		return; /* if we can not find "from=<" or "from=" string in line , return false;*/
	while (strncmp (p," size=", 6))
       		p++;
	p += 6;
	bytes = (char *)malloc(16 * (sizeof(char)));
	savebytes = bytes;
	while (((*bytes++ = *p++) != ',')) { /* go until find "," or " " size=2634,", "size=2634 "  */
                if (*p == ' ' ||  *p == '\n')
                break;
        }
	*(--bytes) = '\0';
	if (state == 1)	{
		checkUser(savedomain, savemail, FROM_MAIL, atoi(savebytes));
		free(savedomain);
	}
	else
		checkUser(hostname, savemail, FROM_MAIL, atoi(savebytes));
	(general.from_cnt)++;
	general.from_byte += atol(savebytes);
	free(savemail);
	free(savebytes);
}

void parseSendmailToLine(char *str) /* ft = from or to */
{
	char *p;
	char *email;
	char *domain;
	char *savemail;
	char *savedomain;
	int state = 0, i = 0;

	if ((strstr(str, " to=<>")) != NULL) {
		(general.to_cnt)++;
		return;
	}

	else if ((strstr(str, " to=<")) != NULL) {
    		p = str;
	/*get email */
    		while (strncmp (p," to=<", 5))
      		  	p++;
  	  	p += 5;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != '>')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {/* state =1 @ is found */
			while ((*email++ = *p++) != '@')
				;
			/*get from domain */
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != '>')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
		}
	}
	else if ((strstr(str, " to=")) != NULL) { 
    		p = str;
		/*get email */
    		while (strncmp (p," to=", 4))
        		p++;
    		p += 4;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != ',')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {
			/*get from domain */
			while ((*email++ = *p++) != '@')
				;
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != ',')
					;
			*(--email) = '\0';
			*(--domain) = '\0';
		}
	}
	else
		return;
	if (state == 1) {
		checkUser(savedomain, savemail, TO_MAIL, 0);
		(general.to_cnt)++;
	       	free (savedomain);
	}
	else {
		checkUser(hostname, savemail, TO_MAIL, 0);
		(general.to_cnt)++;
	}
       	free (savemail);
	return;
}


/* This function parses one line from log file, checks if any " from " 
 * is matched. If so, returns the mail address 
 *
 *
 * EXIM SUPPORT CODE by Marco Erra <mare@erra.myip.org>
 */


void parseEximFromBytesLine(char *str)
{
	int i = 0, state = 0;
	char *p;
	char *email;
	char *domain;
	char *bytes;
	char *savemail;
	char *savebytes;
	char *savedomain;
/*printf("EximFrom\n");*/
	if (((strstr(str, " <= <>")) != NULL) || ((strstr(str, " <=,")) != NULL) ) {
		(general.from_cnt)++;
		return; /* null sender */
	}else if (((strstr(str, " <= <")) != NULL) && ((strstr(str, " S=")) != NULL )) {
   	 	p = str;
    		while (strncmp (p," <= <", 5))
        		p++;
    		p += 5;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ' ') { /* check for @*/
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i;
		if (state == 0) {
			p--;  /*get back first char */
			while ((*email++ = *p++) != '>')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else  { /* state = 1 , means we found @ at from part */
			while (((*email++ = *p++) != '@'))
				;
			/* get from domain */
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != '>')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
			p++;
		}
	}
	/* if line is contain from= */
	/* we use two diffrent method to get email address from "from" line because
	 * there are two kinds of logging method for sendmail */
	else if (((strstr(str, " <= ")) != NULL) && ((strstr(str, " S=")) != NULL )) {
    		p = str;
  	  	while (strncmp (p," <= ", 4))
        		p++;
    		p += 4;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ' ') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != ' ')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {  /* state =1 , @ is found */
			while ((*email++ = *p++) != '@')
				;
			/*get from domain */
			domain = (char *)malloc((strlen(p) + 1) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != ' ')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
		}
	} /* else if (((strstr(str, " <= ")) != NULL) && ((s .....ends here */
	else
		return; /* if we can not find " <= <" or " <= " string in line , return false;*/
	while (strncmp (p," s=", 3))
       		p++;
	p += 3;
	bytes = (char *)malloc(16 * (sizeof(char)));
	savebytes = bytes;
	while (((*bytes++ = *p++) != ' ')) { /* go until find "," or " " size=2634,", "size=2634 "  */
                if (*p == ' ' ||  *p == '\n')
                break;
        }
	*(bytes) = '\0';
/*soma = soma + atoi(savebytes);
printf("SIZE: %d\n", soma);*/
	if (state == 1)	{
		checkUser(savedomain, savemail, FROM_MAIL, atoi(savebytes));
		free(savedomain);
	}
	else
		checkUser(hostname, savemail, FROM_MAIL, atoi(savebytes));
	(general.from_cnt)++;
	general.from_byte += atol(savebytes);
	free(savemail);
	free(savebytes);
}

void parseEximToLine(char *str) /* ft = from or to */
{
	char *p;
	char *email;
	char *domain;
	char *savemail;
	char *savedomain;
	int state = 0, i = 0;

/*printf("EximTo %s\n", str);*/

	if ((strstr(str, " => <>")) != NULL) {
		(general.to_cnt)++;
		return;
	}
	else if ((strstr(str, " => <")) != NULL) {
    		p = str;
	/*get email */
    		while (strncmp (p," => <", 5))
      		  	p++;
  	  	p += 5;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != '>')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {/* state =1 @ is found */
			while ((*email++ = *p++) != '@')
				;
			/*get from domain */
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != '>')
				;
			*(--email) = '\0';
			*(--domain) = '\0';
		}
	}
	else if ((strstr(str, " => ")) != NULL) { 
    		p = str;
		/*get email */
    		while (strncmp (p," => ", 4))
        		p++;
    		p += 4;
		lowercase(p);
		email = (char *)malloc((strlen(p) + 2) * sizeof(char));
		savemail = email;
		while((*p++) != ',') {
			if (*p == '@') {
				state = 1;
				i++;
				break;
			}
			i++;
		}
		p -= i; /* return back */
		if (state == 0) {/* if we can not find @ in from line, ignore it */
			p--;  /*get back first char */
			while ((*email++ = *p++) != ' ')
				;
			*(--email) = '\0';
			strcat(email, "@");
			strcat(email, hostname);
		}
		else {
			/*get from domain */
			while ((*email++ = *p++) != '@')
				;
			domain = (char *)malloc((strlen(p) + 2) * sizeof(char));
			savedomain = domain;
			while ((*domain++ = *email++ = *p++) != ' ')
				;
			*(--email) = '\0';
/*			printf("Char: %c", *domain);*/
			if (*(--email) == '>'){
				*(domain-2) = '\0';
			} else {
				*(--domain) = '\0';
			}
		}
/*printf("Domain %s\n", savedomain);*/
	}
	else
		return;
	if (state == 1) {
		checkUser(savedomain, savemail, TO_MAIL, 0);
		(general.to_cnt)++;
	       	free (savedomain);
	}
	else {
		checkUser(hostname, savemail, TO_MAIL, 0);
		(general.to_cnt)++;
	}
       	free (savemail);
	return;
}

void readEximLogFile(char *fn) 
{	
	FILE *fp;
	char buf[1024];

	if ((fp = fopen(fn, "r")) == NULL) {
		fprintf(stderr, "fopen: %s: %s\n", fn, strerror(errno));
		exit(-1);
	}
	 /* Get the historical values of last read log file's inode number
	    If both inode numbers are the same, we assume that log file 
	    has not been changed (i.e rotated, removed), so we can 
	    go past offset bytes and continue to read new logs */

	while ((fgets(buf, 1024, fp)) != NULL) {
		if ((check_syslog_date_exim(buf)) > 0) {
			if ((strstr(buf, " <= ")) != NULL){  /* if this is from line */
				parseEximFromBytesLine(buf);
			}else if ((strstr(buf, " => ")) != NULL)
				parseEximToLine(buf);
		}
	}
	fclose(fp);
}

int check_syslog_date_exim(char *buf)
{
	unsigned char m[2]= {0};
	unsigned char a[5]= {0};
	int ano = 0, mes = 0, day = 0, i = 0, j, k;

		for (k = 0; buf[k] != '-' && buf[k] != '\n' && buf[k] != EOF; k++)
			ano =  10 * ano + (buf[k] - '0');
		k++;
		for (i = k++; buf[i] != '-' && buf[i] != '\n' && buf[i] != EOF; i++)
			mes =  10 * mes + (buf[i] - '0');
		i++;
		for (j = i++; buf[j] != ' ' && buf[j] != '\n' && buf[j] != EOF; j++)
			day =  10 * day + (buf[j] - '0');
		if ((cur_month == mes) && (day == cur_day )){
/*			printf("Mes: %d - Dia: %d\n", mes, day);*/
			return 1;
		}
		return -1;
}

