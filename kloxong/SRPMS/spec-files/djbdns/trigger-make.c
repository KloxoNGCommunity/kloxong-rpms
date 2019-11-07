/*****************************************************************************

    runs "make" as root in the directory defined in /etc/djbnotify.conf

*****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define CONFIG "/etc/djbnotify.conf"
#define MAKE "/usr/bin/make"
#define PATH "/usr/bin:/bin:/usr/local/bin"

char *cmd[] = { MAKE , NULL } ;
char *env[] = { "PATH=" PATH , "SHELL=/bin/sh" ,  NULL } ;

void try_this( char *domain, char *server, char *file );


int main ( int argc , char *argv[] )
{
  char *domain = argv[1];

  if ( domain == NULL || *domain == '\0' )
  {
    fprintf( stderr, "Usage: %s domain\n", argv[0] );
    return 1;
  }


  FILE *fd = fopen( CONFIG, "r" );

  if ( fd == NULL )
  {
    fprintf( stdout, "Error opening file %s\n", CONFIG );
    return 1;
  }

  while ( 1 )
  {
    char *linePtr = NULL;
    size_t n = 80;
    int size = getline( &linePtr, &n, fd );

    if ( size < 0 )
    {
      break; /* End of file. */
    }

    if ( size == 0 )
    {
      free( linePtr );
      continue; /* Uninteresting blank line. */
    }

    if ( linePtr[0] == '#' )
    {
      free( linePtr );
      continue; /* Ignore comments in file. */
    }
    
    if ( linePtr[ size - 1 ] == '\n' )
    {
      linePtr[ size - 1 ] = '\0'; /* Zap newline char. */
    }

   char *tdomain = strtok( linePtr, " \t" );

   if ( tdomain == NULL )
   {
     fprintf( stderr, "Can't find domain.\n" );
     return 1;
   }

   char *tserver = strtok( NULL, " \t" );

   if ( tserver == NULL )
   {
     fprintf( stderr, "Can't find server.\n" );
     return 1;
   }

   char *tfile = strtok( NULL, " \t" );

   if ( tfile == NULL )
   {
     fprintf( stderr, "Can't find file.\n" );
     return 1;
   }

   printf( "Domain: %s Server: %s File: %s\n", tdomain, tserver, tfile );

   if ( strcmp( domain, tdomain ) == 0 )
   {
     printf( "Found domain %s\n", domain );
     try_this( tdomain, tserver, tfile );
   }

   free( linePtr );
  }

  fprintf( stderr, "Can't find domain %s\n", domain );
  return 1;
}


void try_this( char *domain_, char *server_, char *file_ )
{
  int slashes_seen = 0;
  int size = strlen( file_ ) - 1;

  /* Find the file directory */
  while ( size >= 0 & slashes_seen != 2 )
  {
    if ( file_[ size ] == '/' )
    {
      slashes_seen++;
    }

    file_[ size ] = '\0'; /* Zap it */
    size--;
  }

  if ( slashes_seen != 2 )
  {
    fprintf( stderr, "Can't back up 2 directories (%s).\n", file_ );
    return;
  }

  printf( "Changing to directory %s\n", file_ );

  if ( chdir ( file_ ) )
  {
    perror ( "chdir" );
    return;
  }

  if ( setuid( 0 ) )
  {
    perror( "setuid" );
    return;
  }

  if ( seteuid( 0 ) )
  {
    perror ( "seteuid" );
    return;
  }

  execve ( cmd[0] , cmd , env );
  perror ( "execve" );
}
