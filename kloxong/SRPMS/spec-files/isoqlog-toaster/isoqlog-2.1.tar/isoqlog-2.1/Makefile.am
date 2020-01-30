SUBDIRS = htmltemp lang tr

bin_PROGRAMS = isoqlog

isoqlog_SOURCES = Data.c \
	Dir.c \
	Html.c \
	LangCfg.c \
	Parser.c \
	Store.c \
	loadconfig.c \
	main.c

# conf dizini
docdir = $(datadir)/doc/isoqlog
doc_DATA = AUTHORS COPYING ChangeLog FAQ INSTALL NEWS README TODO EnderUNIX README.Turkish

sysconf_DATA = isoqlog.conf-dist isoqlog.domains-dist
