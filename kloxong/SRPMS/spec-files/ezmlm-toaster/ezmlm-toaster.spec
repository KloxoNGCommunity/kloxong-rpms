%define	name ezmlm
%define	idxversion 0.40
%define	ezmlmversion 0.53
%define 	pversion %{ezmlmversion}.324
%define 	bversion 1.3
%define	rpmrelease 9.kng%{?dist}

%define         release %{bversion}.%{rpmrelease}
%define         apacheuser apache
%define         apachegroup apache
#BuildRequires:  mysql-devel >= 5.0.22, mysql >= 5.0.22
Requires:       mysql >= 5.0.22
BuildRequires: zlib-devel
%if %{?fedora}0 > 150 || %{?rhel}0 > 70
Requires:      libnsl ,	perl
BuildRequires:	perl, libnsl, glibc, libnsl2
%endif
%define	gccver	gcc
%define	ccflags %{optflags}
%define	ldflags %{optflags} -L/lib64 -lnsl

############### RPM ################################

%define		debug_package %{nil}
%define         vtoaster %{pversion}
%define 	basedir %{_datadir}/toaster
%define		dbase mysql
%define		ezroot /usr
%define		builddate Fri Jun 12 2009

Name: 		%{name}-toaster
Summary: 	Qmail Easy Mailing List Manager + IDX patches.
Version: 	%{vtoaster}
Release: 	%{release}
Group: 		Utilities/System
URL: 		http://www.ezmlm.org
License: 	GNU
Buildroot: 	%{_tmppath}/%{name}-%{version}
Packager: 	Jake Vickers <jake@qmailtoaster.com>
Source0: 	ftp://koobera.math.uic.edu/pub/software/ezmlm-%{ezmlmversion}.tar.bz2
Source1: 	ftp://ftp.id.wustl.edu/pub/patches/ezmlm-idx-%{idxversion}.tar.bz2
Source2: 	ezman-%{idxversion}.html.tar.bz2
Summary: 	Qmail Easy Mailing List Manager + IDX patches with %{dbase} database support.
Group: 		Utilities/System 
Obsoletes: 	ezmlm-idx, ezmlm-toaster-doc
Conflicts: 	ezmlm, ezmlm-idx-std, ezmlm-idx-pgsql, ezmlm-idx-mysql

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
ezmlm lets users set up their own mailing lists within qmail's address
hierarchy. A user, Joe, types

   ezmlm-make ~/SOS ~/.qmail-sos joe-sos isp.net

and instantly has a functioning mailing list, joe-sos@isp.net, with all
relevant information stored in a new ~/SOS directory.

ezmlm sets  up joe-sos-subscribe  and joe-sos-unsubscribe for automatic
processing of subscription and  unsubscription requests. Any message to
joe-sos-subscribe  will work;  Joe  doesn't  have to explain any tricky
command formats. ezmlm  will  send  back  instructions  if a subscriber
sends a message to joe-sos-request or joe-sos-help.

ezmlm  automatically  archives new messages. Messages are labelled with
sequence numbers; a subscriber can fetch message 123 by sending mail to
joe-sos-get.123.  The archive  format supports  fast message  retrieval
even when there are thousands of messages.

ezmlm  takes  advantage  of  qmail's  VERPs  to  reliably determine the
recipient address and message number for every incoming bounce message.
It waits ten days  and  then  sends  the  subscriber  a list of message
numbers that bounced.  If that warning bounces, ezmlm sends a probe; if
the probe bounces, ezmlm  automatically removes the subscriber from the
mailing list.

ezmlm is easy for users to control. Joe can edit ~/SOS/text/* to change
any of the administrative  messages  sent to subscribers. He can remove
~/SOS/public and ~/SOS/archived to  disable  automatic subscription and
archiving. He can put  his  own  address  into ~/SOS/editor to set up a
moderated mailing list.  He  can edit ~/SOS/{headeradd,headerremove} to
control  outgoing  headers.  ezmlm  has  several  utilities to manually
inspect and manage mailing lists.

ezmlm uses Delivered-To  to  stop  forwarding  loops,  Mailing-List  to
protect other mailing  lists against false  subscription  requests, and
real  cryptographic  cookies  to  protect  normal  users  against false
subscription  requests.  ezmlm   can   also  be  used  for  a  sublist,
redistributing messages from another list.

ezmlm is reliable, even in the face  of system crashes.  It writes each
new subscription and each new message safely to disk  before it reports
success to qmail.

ezmlm doesn't mind huge mailing lists.  Lists  don't  even  have to fit
into memory.  ezmlm  hashes   the  subscription  list  into  a  set  of
independent files  so that it can handle subscription requests quickly.
ezmlm uses qmail for blazingly fast parallel SMTP deliveries.

The IDX  patches  add:  Indexing,  (Remote)  Moderation,  digest,  make
patches, multi-language, MIME, global interface, MySQL database support.

#-------------------------------------------------------------------------------
%package	-n ezmlm-cgi-toaster
#-------------------------------------------------------------------------------
Summary:	Ezmlm cgi-bin
Group:		Networking/Other
Requires:	%{name} >= %{pversion}-%{release}
#Requires:	control-panel-toaster >= 0.2

#Requires:	httpd >= 2.0.40

#-------------------------------------------------------------------------------
%description	-n ezmlm-cgi-toaster
#-------------------------------------------------------------------------------
Ezmlm cgi to query via apache mail archives.2

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%define name ezmlm
%setup -q -T -b 0 -n ezmlm-%{ezmlmversion}
%setup -D -T -a 1 -n ezmlm-%{ezmlmversion}

[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc
[ -f %{_tmppath}/%{name}-%{pversion}-gcc32 ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc32

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-%{gccver}

mv -f ezmlm-idx-%{idxversion}/* .
patch -s < idx.patch


#-------------------------------------------------------------------------------
%build 
#-------------------------------------------------------------------------------


RC=%{_sysconfdir}/ezmlm/ezmlmrc

sed -e 's{^#define TXT_ETC_EZMLMRC \"/etc/ezmlmrc\"{#define TXT_ETC_EZMLMRC \"$RC\"{' idx.h > idx.h.tmp

mv idx.h.tmp idx.h


# Fix lib include in Makefile
#-------------------------------------------------------------------------------
perl -pi -e 's|`head -1 conf-sqlld`|-L/usr/lib/mysql -lnsl -lm -lz|g' Makefile
/sbin/ldconfig

# We have gcc written in a temp file
#-------------------------------------------------------------------------------
echo "%{gccver} %{ccflags}"    >conf-cc
echo "%{gccver} %{ldflags}" >conf-ld

echo %{ezroot}/bin > conf-bin
echo %{ezroot}/man > conf-man

# GLIBC fix
#-------------------------------------------------------------------------------
echo "Fixing errno.h for new GLIBC"
echo "#include <errno.h>" >> error.h

make 
make it install


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
[ -d %{buildroot}/%{ezroot}/bin ]		|| mkdir -p %{buildroot}/%{ezroot}/bin
[ -d %{buildroot}/%{ezroot}/man ]		|| mkdir -p %{buildroot}/%{ezroot}/man
[ -d %{buildroot}/%{_sysconfdir}/ezmlm ]	|| mkdir -p %{buildroot}/%{_sysconfdir}/ezmlm
[ -d %{buildroot}/%{basedir}/cgi-bin ] 		|| mkdir -p %{buildroot}%{basedir}/cgi-bin

sed '/cat/d' MAN > MAN.tmp
mv MAN.tmp MAN

./install %{buildroot}/%{ezroot}/bin < BIN
./install %{buildroot}/%{ezroot}/man < MAN

# Fix css
#-------------------------------------------------------------------------------
perl -pi -e 's|/ezcgi.css|/scripts/styles.css|g' $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezcgirc

cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.en_US %{buildroot}/%{_sysconfdir}/ezmlm/ezmlmrc
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.en_US %{buildroot}/%{_sysconfdir}/ezmlm/ezmlmrc.dist
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.it %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.cs %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.da %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.de %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.es %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.fr %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlmrc.ru %{buildroot}/%{_sysconfdir}/ezmlm/
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezmlm-cgi %{buildroot}/%{basedir}/cgi-bin/ezmlm.cgi
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezcgirc %{buildroot}/%{_sysconfdir}/ezmlm/ezcgirc
cp $RPM_BUILD_DIR/ezmlm-%{ezmlmversion}/ezcgirc %{buildroot}/%{_sysconfdir}/ezmlm/ezcgirc.dist

tar fvxj $RPM_SOURCE_DIR/ezman-%{idxversion}.html.tar.bz2


#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------

[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{ezmlmversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{ezmlmversion}
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc
[ -f %{_tmppath}/%{name}-%{pversion}-gcc32 ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc32


#-------------------------------------------------------------------------------
%files -n ezmlm-cgi-toaster
#-------------------------------------------------------------------------------
%defattr (-,root,root)
%attr(0755,root,root) %dir %{basedir}/cgi-bin
%config(noreplace) %{_sysconfdir}/ezmlm/ezcgirc
%config %{_sysconfdir}/ezmlm/ezcgirc.dist
%attr(6755,vpopmail,vchkpw) %{basedir}/cgi-bin/ezmlm.cgi


#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ezmlm/ezmlmrc
%config %{_sysconfdir}/ezmlm/ezmlmrc.dist
%config %{_sysconfdir}/ezmlm/ezmlmrc.it
%config %{_sysconfdir}/ezmlm/ezmlmrc.cs
%config %{_sysconfdir}/ezmlm/ezmlmrc.da
%config %{_sysconfdir}/ezmlm/ezmlmrc.de
%config %{_sysconfdir}/ezmlm/ezmlmrc.es
%config %{_sysconfdir}/ezmlm/ezmlmrc.fr
%config %{_sysconfdir}/ezmlm/ezmlmrc.ru
%{ezroot}/bin/*

# docs
%doc BLURB CHANGES* FAQ.idx INSTAL*  README*
%doc THANKS TODO UPGRADE.idx VERSION
%doc DOWNGRADE.idx ezmlmrc ezmlmrc.[a-zA-Z]*  ezman*
%doc qmail-*.tar.gz
%{ezroot}/man/*/*


#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.53.324-1.3.9.mr
- cleanup spec based on toaster github (without define like build_cnt_60)
- disable Requires to apache/httpd

* Tue Jul 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.53.324-1.3.8.mr
- without mysql request (make less conflict with mysql branch)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.53.324-1.3.7.mr
- add build_cnt_60 and build_cnt_6064
- Remove -lmysqlclient

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 0.53.324-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 0.53.324-1.3.6
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 0.53.324-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 0.53.324-1.3.4
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 0.53.324-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 17 2007 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.3.3
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.53.324-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.11
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.10
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.8
- Add CentOS 4 x86_64 support
* Mon Sep 26 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.7
- Fix compiled definition for Mandrake 10.2
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.6
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 0.5-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Fri May 27 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.4
- Remove doc package
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.2.2
- Add Fedora Core 2 support
* Mon Jan 12 2004 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.0.9
- Trustix fix - dep apache 2.0.40 instead of httpd by Christian Dietrich
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.0.8
- Add Fedora Core 1 support
* Sun Nov 23 2003 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.0.7
- Add Trustix 2.0 support
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-1.0.6
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-1.0.5
- Conectiva Linux 7.0 support
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 0.53.324-1.0.4
- Support for Red Hat 8.0
* Wed Feb 05 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-1.0.3
- Support for Red Hat 8.0 thanks to Andrew.J.Kay
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-0.9.2
- Soft clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.53.324-0.8.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.0.53.324-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.53.324-4
- Cleans and patches on ezmlm.cgi: we use toaster css
* Fri Sep 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.53.324-3
- Default language is English (no more Italian)
- Added localized configuration (was missed)
- Changed dependencing from apache-conf-toaster in toaster-control-panel
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.53.324-2
- Deleted Mandrake Release Autodetection (creates problems)
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.53.324-1
- New version: 0.7 toaster.
- Installation directly depends on apache-conf-toaster (that provides httpd
  configurations for all web packages)
- Better macros to detect Mandrake Release
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.0.53.324-1
- New version: 0.6 toaster
- We have ezmlm.cgi (it was missed in previous packages)
- Configuration files are in /etc/ezmlm (no more in /etc)
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.0.53.324-1
- New version: 0.5 toaster
- Doc package is standalone (someone does not ask for man pages)
- Checks for gcc-3.2 (default compiler from now)
* Tue Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.0.53.324-1
- Rebuild against 0.4 toaster
* Thu Aug 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.53.324-3
- Better dependencies for RedHat
* Thu Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.53.324-2
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
- Soft clean-ups to SPEC file.
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.53.324.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-0.53.324.1mdk
- toaster v. 0.2
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-0.53.324.3mdk
- Added tests for gcc-3.1.1
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
  soft links.
* Thu Jul 11 2002 Miguel Beccari <mighi@clikka.com> 0.53.324-2mdk
- Renamed the package in toster (we are building a toaster series
  of packages)
* Fri Jul 05 2002 Miguel Beccari <mighi@clikka.com> 0.53.324-1mdk
- First RPM package.
