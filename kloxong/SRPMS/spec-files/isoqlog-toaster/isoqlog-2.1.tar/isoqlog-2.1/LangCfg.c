#include "LangCfg.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#include <sys/types.h>
#include <sys/stat.h>


extern int errno;

void loadLang(char *langfile) 
{
	FILE *fd;
	char buf[BUFSIZE];
	char keyword[KEYSIZE];
	char value[VALSIZE];
	char *cp1, *cp2;
	char *variables[] = { "Invalid",
		"L_Average",
		"L_Creationtime",
		"L_Daily",
		"L_Day",
		"L_Domain",
		"L_Encoding",
		"L_Mail",
		"L_Main_Page",
		"L_Month",
		"L_Monthly",
		"L_Number",
		"L_Received",
		"L_Receiver",
		"L_Sender",
		"L_Sent",
		"L_Size",
		"L_Stats",
		"L_Top",
		"L_Total",
		"L_Year",
		"L_Yearly"
	};

	int i, key, line, keyword_nums = sizeof(variables)/sizeof(char *);

	
	if ((fd = fopen(langfile, "r")) == NULL) {
		fprintf(stderr, "loadLang: cannot open language configuration file %s, exiting...\n", langfile);
		exit(-1);
	}
	line = 0;
	while ((fgets(buf, BUFSIZE, fd)) != NULL) {
		line++;
		if (buf[0] == '#') 
			continue;
		if ((strlen(buf)) <= 1)
			continue;

		cp1 = buf;
		cp2 = keyword;
		while (isspace((int)*cp1)) 
			cp1++;
		while (isgraph((int)*cp1) && (*cp1 != '=')) 
			*cp2++ = *cp1++;
		*cp2 = '\0';
		cp2 = value;
		while ((*cp1 != '\0') && (*cp1 !='\n') && (*cp1 !='='))
			cp1++;
		cp1++; 
		while (isspace((int)*cp1))
			cp1++; 
		if (*cp1 == '"') 
			cp1++;
		while ((*cp1 != '\0') && (*cp1 !='\n') && (*cp1 !='"'))
			*cp2++ = *cp1++;
		*cp2-- = '\0';
		if (keyword[0] =='\0' || value[0] =='\0')
			continue;
		key = 0;
		for (i = 0; i < keyword_nums; i++) {
			if ((strcmp(keyword, variables[i])) == 0) {
				key = i;
				break;
			}
		}

		switch(key) {
		case 0:
			fprintf(stderr, "Illegal Keyword: %s\n", keyword);
			break;
		case 1:
			strncpy(L_Average, value, VALSIZE);
			break;
		case 2:
			strncpy(L_Creationtime, value, VALSIZE);
			break;
		case 3:
			strncpy(L_Daily, value, VALSIZE);
			break;
		case 4:
			strncpy(L_Day, value, VALSIZE);
			break;
		case 5:
			strncpy(L_Domain, value, VALSIZE);
			break;
		case 6:
			strncpy(L_Encoding, value, VALSIZE);
			break;
		case 7:
			strncpy(L_Mail, value, VALSIZE);
			break;
		case 8:
			strncpy(L_Main_Page, value, VALSIZE);
			break;
		case 9:
			strncpy(L_Month, value, VALSIZE);
			break;
		case 10:
			strncpy(L_Monthly, value, VALSIZE);
			break;
		case 11:
			strncpy(L_Number, value, VALSIZE);
			break;
		case 12:
			strncpy(L_Received, value, VALSIZE);
			break;
		case 13:
			strncpy(L_Receiver, value, VALSIZE);
			break;
		case 14:
			strncpy(L_Sender, value, VALSIZE);
			break;
		case 15:
			strncpy(L_Sent, value, VALSIZE);
			break;
		case 16:
			strncpy(L_Size, value, VALSIZE);
			break;
		case 17:
			strncpy(L_Stats, value, VALSIZE);
			break;
		case 18:
			strncpy(L_Top, value, VALSIZE);
			break;
		case 19:
			strncpy(L_Total, value, VALSIZE);
			break;
		case 20:
			strncpy(L_Year, value, VALSIZE);
			break;
		case 21:
			strncpy(L_Yearly, value, VALSIZE);
			break;
		}
	}
	fclose(fd);
}
