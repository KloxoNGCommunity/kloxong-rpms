%define 	real_name courier-imap
%define 	pversion 4.1.2
%define 	bversion 1.3
%define 	rpmrelease 20.kng%{?dist}

%define		release %{bversion}.kng.%{rpmrelease}
BuildRequires:	gamin-devel, openssl-devel >= 0.9.8, expect >= 5.43.0, gdbm-devel >= 1.8.0
BuildRequires:	gcc-c++, sed, perl
Requires:		openssl >= 0.9.8, chkconfig, fileutils
Requires:		textutils, sh-utils, sed
%define		ccflags %{optflags} -DHAVE_VLOGAUTH
%define		ldflags %{optflags} -L/usr/include

############### RPM ################################
Autoreq: 0
%define	debug_package %{nil}
%define	vtoaster %{pversion}
%define	_qdir /var/qmail
%define	_qtlogdir /var/log/qmail
%define	_spath %{_qdir}/supervise
%define	builddate Fri Jun 12 2009

Name:		%{real_name}-toaster
Summary:	Courier-IMAP is an IMAP server that uses Maildirs
Version:	%{vtoaster}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.courier-mta.org

Source:	courier-imap-%{pversion}.tar.bz2
Source1:	supervise-imap4.run
Source2:	supervise-imap4-log.run
Source3:	supervise-imap4-ssl.run
Source4:	supervise-imap4-ssl-log.run
Source5:	supervise-pop3-ssl.run
Source6:	supervise-pop3-ssl-log.run
Source7:	envconv
Source8:	imapd
Source9:	imapd-ssl
Source10:	pop3d
Source11:	pop3d-ssl

Source12:	supervise-pop3.run
Source13:	supervise-pop3-log.run

BuildRoot:		%{_tmppath}/%{real_name}-%{version}-toaster-buildroot

Requires:		qmail-toaster >= 1.03
Requires:		ucspi-tcp-toaster >= 0.88, daemontools-toaster >= 0.76
Requires:		courier-authlib-toaster
Requires:		fileutils textutils sh-utils sed

BuildRequires:	textutils openssl-devel fileutils perl
BuildRequires:	courier-authlib-toaster

Conflicts:	uw-imap, courier-imap, dovecot
Obsoletes:	courier-imap-toaster-doc, qmail-pop3d-toaster

Provides:	imap, imap-server

Packager:	Jake Vickers <jake@qmailtoaster.com>


#-----------------------------------------------------------------------------
%description
#-----------------------------------------------------------------------------
Courier-IMAP is an IMAP server for Maildir mailboxes.  This package contains
the  standalone  version of the  IMAP server  that's included in the Courier
mail server package.  This  package  is  a  standalone  version for use with
qmail-toaster mail servers.   Do  not  install this package if you intend to
install the full Courier mail server.


#-----------------------------------------------------------------------------
%prep
#-----------------------------------------------------------------------------

%define name courier-imap
%setup -q -n courier-imap-%{pversion}


# Cleanup for the new gcc
#-----------------------------------------------------------------------------

echo "gcc" > %{_tmppath}/%{real_name}-%{pversion}-gcc


#-----------------------------------------------------------------------------
%build
#-----------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}


# Set compiler includes
#-----------------------------------------------------------------------------
export CC="`cat %{_tmppath}/%{real_name}-%{pversion}-gcc` %{ccflags}"
export CPPFLAGS=-I%{_includedir}
export COURIERAUTHCONFIG=%{_bindir}/courierauthconfig
[ -f %{_tmppath}/%{real_name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{real_name}-%{pversion}-gcc

%configure \
    --disable-root-check \
    --datadir=%{_datadir}/courier \
    --sysconfdir=%{_sysconfdir}/courier \
    --enable-unicode \
    --with-redhat

# Make
#-----------------------------------------------------------------------------
make


#-----------------------------------------------------------------------------
%install
#-----------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


# Install into buildroot
#-----------------------------------------------------------------------------
	make DESTDIR=%{buildroot} install

# Qmail logs
#-----------------------------------------------------------------------------
mkdir -p %{buildroot}%{_qtlogdir}/imap4
mkdir -p %{buildroot}%{_qtlogdir}/imap4-ssl
mkdir -p %{buildroot}%{_qtlogdir}/pop3
mkdir -p %{buildroot}%{_qtlogdir}/pop3-ssl

# Supervise
#-----------------------------------------------------------------------------
mkdir -p %{buildroot}%{_spath}/imap4/log
mkdir -p %{buildroot}%{_spath}/imap4/supervise
mkdir -p %{buildroot}%{_spath}/imap4/env
mkdir -p %{buildroot}%{_spath}/imap4-ssl/log
mkdir -p %{buildroot}%{_spath}/imap4-ssl/supervise
mkdir -p %{buildroot}%{_spath}/imap4-ssl/env
mkdir -p %{buildroot}%{_spath}/pop3/log
mkdir -p %{buildroot}%{_spath}/pop3/supervise
mkdir -p %{buildroot}%{_spath}/pop3/env
mkdir -p %{buildroot}%{_spath}/pop3-ssl/log
mkdir -p %{buildroot}%{_spath}/pop3-ssl/supervise
mkdir -p %{buildroot}%{_spath}/pop3-ssl/env

install -m700 %{SOURCE1} %{buildroot}%{_spath}/imap4/run
install -m700 %{SOURCE2} %{buildroot}%{_spath}/imap4/log/run
install -m700 %{SOURCE3} %{buildroot}%{_spath}/imap4-ssl/run
install -m700 %{SOURCE4} %{buildroot}%{_spath}/imap4-ssl/log/run
install -m700 %{SOURCE5} %{buildroot}%{_spath}/pop3-ssl/run
install -m700 %{SOURCE6} %{buildroot}%{_spath}/pop3-ssl/log/run

install -m700 %{SOURCE12} %{buildroot}%{_spath}/pop3/run
install -m700 %{SOURCE13} %{buildroot}%{_spath}/pop3/log/run

install -m755 %{SOURCE7} %{buildroot}%{_bindir}/envconv
install -m644 %{SOURCE8} %{buildroot}%{_sysconfdir}/courier/imapd
install -m644 %{SOURCE9} %{buildroot}%{_sysconfdir}/courier/imapd-ssl
install -m644 %{SOURCE10} %{buildroot}%{_sysconfdir}/courier/pop3d
install -m644 %{SOURCE11} %{buildroot}%{_sysconfdir}/courier/pop3d-ssl

# Remove sysV startup - we use qmail to start courier-imap
#-----------------------------------------------------------------------------
[ -f %{buildroot}%{_libexecdir}/imapd.rc ] && rm -f %{buildroot}%{_libexecdir}/imapd.rc
[ -f %{buildroot}%{_libexecdir}/imapd-ssl.rc ] && rm -f %{buildroot}%{_libexecdir}/imapd-ssl.rc
[ -f %{buildroot}%{_libexecdir}/pop3d.rc ] && rm -f %{buildroot}%{_libexecdir}/pop3d.rc
[ -f %{buildroot}%{_libexecdir}/pop3d-ssl.rc ] && rm -f %{buildroot}%{_libexecdir}/pop3d-ssl.rc


#-----------------------------------------------------------------------------
%post
#-----------------------------------------------------------------------------
[ -f %{_tmppath}/setupcourier ] && rm -f %{_tmppath}/setupcourier

# Do not install dummy certificates
#-----------------------------------------------------------------------------
if [ $1 = "1" ]; then
cat <<EOF >>%{_tmppath}/setupcourier
#!/bin/sh
[ -f %{_datadir}/courier/pop3d.pem ] || %{_datadir}/courier/mkpop3dcert >/dev/null 2>&1
[ -f %{_datadir}/courier/imapd.pem ] || %{_datadir}/courier/mkimapdcert >/dev/null 2>&1
EOF
fi

if [ -f %{_tmppath}/setupcourier ]; then
chmod +x %{_tmppath}/setupcourier
%{_tmppath}/setupcourier 2>&1 > /dev/null
rm -f %{_tmppath}/setupcourier
fi;

## MR -- set as inactive if dovecot is 'run' state
if [ -f %{_spath}/dovecot/run ] ; then
	mv -f %{_spath}/pop3/run %{_spath}/pop3/down
	mv -f %{_spath}/pop3/log/run %{_spath}/pop3/log/down
	mv -f %{_spath}/pop3-ssl/run %{_spath}/pop3-ssl/down
	mv -f %{_spath}/pop3-ssl/log/run %{_spath}/pop3-ssl/log/down
	mv -f %{_spath}/imap4/run %{_spath}/imap4/down
	mv -f %{_spath}/imap4/log/run %{_spath}/imap4/log/down
	mv -f %{_spath}/imap4-ssl/run %{_spath}/imap4-ssl/down
	mv -f %{_spath}/imap4-ssl/log/run %{_spath}/imap4-ssl/log/down
fi

#-----------------------------------------------------------------------------
%postun
#-----------------------------------------------------------------------------
if [ $1 = "0" ]; then
  rm -fR %{_spath}/imap4/
  rm -fR %{_spath}/imap4-ssl/
  rm -fR %{_spath}/pop3/
  rm -fR %{_spath}/pop3-ssl/
  rm -fR %{_qtlogdir}/imap4/
  rm -fR %{_qtlogdir}/imap4-ssl/
  rm -fR %{_qtlogdir}/pop3/
  rm -fR %{_qtlogdir}/pop3-ssl/
fi


#-----------------------------------------------------------------------------
%clean
#-----------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{real_name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{real_name}-%{pversion}


#-----------------------------------------------------------------------------
%files
#-----------------------------------------------------------------------------
%defattr(-, -, root)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%attr(0755,root,root) %{_libexecdir}/*
%attr(0755,root,root) %dir %{_datadir}/courier
%attr(0644,root,root) %{_datadir}/courier/*
%attr(0755,root,root) %dir %{_sysconfdir}/courier
%attr(0644,root,root) %{_sysconfdir}/courier/*
%attr(1700,qmaill,qmail) %dir %{_spath}/imap4
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4/env
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4/log
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4/supervise
%attr(1700,qmaill,qmail) %dir %{_spath}/imap4-ssl
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4-ssl/env
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4-ssl/log
%attr(0700,qmaill,qmail) %dir %{_spath}/imap4-ssl/supervise
%attr(1700,qmaill,qmail) %dir %{_spath}/pop3
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3/env
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3/log
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3/supervise
%attr(1700,qmaill,qmail) %dir %{_spath}/pop3-ssl
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3-ssl/env
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3-ssl/log
%attr(0700,qmaill,qmail) %dir %{_spath}/pop3-ssl/supervise
%attr(0751,qmaill,qmail) %{_spath}/imap4/run
%attr(0751,qmaill,qmail) %{_spath}/imap4/log/run
%attr(0751,qmaill,qmail) %{_spath}/imap4-ssl/run
%attr(0751,qmaill,qmail) %{_spath}/imap4-ssl/log/run
%attr(0751,qmaill,qmail) %{_spath}/pop3/run
%attr(0751,qmaill,qmail) %{_spath}/pop3/log/run
%attr(0751,qmaill,qmail) %{_spath}/pop3-ssl/run
%attr(0751,qmaill,qmail) %{_spath}/pop3-ssl/log/run
%attr(0750,qmaill,qmail) %dir %{_qtlogdir}/imap4
%attr(0750,qmaill,qmail) %dir %{_qtlogdir}/imap4-ssl
%attr(0750,qmaill,qmail) %dir %{_qtlogdir}/pop3
%attr(0750,qmaill,qmail) %dir %{_qtlogdir}/pop3-ssl

# docs
#-----------------------------------------------------------------------------
%doc NEWS AUTHORS COPYING imap/BUGS README *.html imap/*.html maildir/*.html
%doc maildir/*.html maildir/*.txt
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man8/*


#-----------------------------------------------------------------------------
%changelog
#-----------------------------------------------------------------------------
* Wed Dec 18 2019 Dionysis Kladis <dkstiler@gmail.com> 0.59.2-1.3.20.kng
- Recompile it for kloxong in copr chroot enviroment

* Fri Jun 17 2015 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.20.mr
- Set to use pop3 (beside pop3-ssl, imap4 and imap4-ssl) instead from qmail-pop3d-toaster
- set no obsolete for dovecot-toaster
- disable requires to maildrop-toaster (may trouble with courier-imap-toaster)

* Mon May 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.19.mr
- set STARTTLS for imapd-ssl and pop3d-ssl

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.18.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Fri Nov 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.17.mr
- add BuildRequires for gamin-devel (libfam) for enable 'IMAP notification'

* Mon Mar 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.16.mr
- back to use .14 based because have a trouble with .15

* Mon Mar 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.15.mr
- like qmail-toaster, also possible without softlimit

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.14.mr
- update run and log run script

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.13.mr
- increase softlimit because have trouble with current value on Centos 6 64bit

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.12.mr
- increase MAXDAEMONS and MAXPERIP value on /etc/courier/imapd (like pop3d)

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.11.mr
- add conflict
- modified run and log run script

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.10.mr
- add build_cnt_60 and build_cnt_6064
- problem with BuildPreReq on centos 6 and then change to BuildRequires

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 3.0.4-1.3.10
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 3.0.4-1.3.10
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 3.0.4-1.3.9
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Increased softlimits for x86_64 distros
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 3.0.4-1.3.8
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 3.0.4-1.3.8
- Added Fedora 9 and 10 support
* Sat Apr 17 2007 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.3.7
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Mon Jan 08 2007 Erik A. Espinoza <espinoza@kabewm.com> 4.1.2-1.3.6
- Commented SSL Cache from pop3d
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 4.1.2-1.3.5
- Upgraded to courier-imap 4.1.2
* Sun Nov 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.1.1-1.3.4
- Enabled unicode support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.1.1-1.3.3
- Added Fedora Core 6 support
* Thu Jun 08 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.1.1-1.3.2
- Upgraded to courier-imap 4.1.1
* Fri Jun 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.1.0-1.3.1
- Upgraded to courier-imap 4.1.0
- Requires courier-authlib
- Added SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.11
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.10
- Add SuSE 10.0 and Mandrive 2006.0 support
- Add authshadow support
* Fri Oct 14 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.7
- Add CentOS 4 x86_64 support
* Wed Jun 29 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.6
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 3.0.8-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Thu May 25 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.8-1.2.4
- Update to courier-imap-3.0.8
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.2
- Update to courier-imap-3.0.4
- Add Fedora Core 2 support
* Wed May 05 2004 Nick Hemmesch <nick@ndhsoft.com> 3.0.3-1.2.1
- Make work with vpopmail-5.4.3
- Set env to show quotas in imap
* Wed Apr 07 2004 Nick Hemmesch <nick@ndhsoft.com> 3.0.3-1.0.6
- Update to Courier-Imap 3.0.3
* Sun Feb 22 2004 Nick Hemmesch <nick@ndhsoft.com> 1.7.3-1.0.5
- By popular demand - no roaming users is default install
- For roaming users with vpopmail use "roaming" switch
* Sun Feb 15 2004 Nick Hemmesch <nick@ndhsoft.com> 1.7.3-1.0.4
- Allow limited roaming users for clients that don't like SMTP-AUTH
- Allow no roaming users with noroam option
* Sat Jan 10 2004 Nick Hemmesch <nick@ndhsoft.com> 1.7.3-1.0.3
- Remove open relay for roaming users in favor of SMTP-AUTH
- Add Fedora Core 1 support
* Sun Nov 23 2003 Nick Hemmesch <nick@ndhsoft.com> 1.7.3-1.0.2
- Fix kerberos lib link for Red Hat 9
- Make patch to fix roaming users with vpopmail
- Add vlogauth def
- Change config so imapv4 compliant clients work
- If this works I will upgrade to latest stable version
- Add Trustix 2.0 support
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.7.3-1.0.1
- Last version 1.7.3
- Clean-ups on SPEC file: compilation banner, better gcc detects
- Detect gcc-3.2.3
- Fixed permissions on supervise dirs (rare bug with high msec security)
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
* Wed Apr 9 2003 David Uhlman <devel_mail@andthengroup.com> 1.7.0-1.0.3
- Fixed courier ssl run scripts to include necessary environment variables.
  Added /bindir/envconv, /qmaildir/supervise/*ssl/env dir to hold envdir vars
* Wed Apr 02 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.7.0-1.0.3
- Clean-ups
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.7.0-1.0.2
- Conectiva Linux 7.0 support
* Sun Feb 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.7.0-1.0.1
- Last version 1.7.0
* Sat Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 1.6.2-1.0.4
- Support for Red Hat 8.0
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.6.2-1.0.3
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Fri Jan 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.6.2-1.0.2
- Fixed bugs in RPM macros, but we need to improve them to support a large
  number of RPM based OS.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.6.2-1.0.1
- Last version of Courier: 1.6.2
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Wed Nov 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.6.1-1.0.1
- Last version of Courier: 1.6.1
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.5.3-0.9.2
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
- Packages are named with their proper releases and bversion is from now
  part of the rpm release: we will continue upgrading safely.
* Mon Sep 23 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.5.3-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
- Clean-ups
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.5.3-1
- New version 1.5.3
* Wed Sep 04 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.5.2-3
- From now we will run imap4, imap4-ssl, pop3-ssl over tcpserver
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.5.2-2
- Deleted Mandrake Release Autodetection (creates problems)
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.5.2-1
- New version: 0.7 toaster.
- Better upgrade capabilities: now uninstallation is clean (no died files)
- Better macros to detect Mandrake Release
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.1.5.2-1
- New version: 0.6 toaster.
- Soft clean-ups for upgrade cleanly.
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.1.5.2-1
- Doc package is standalone (someone does not ask for man pages)
- Checks for gcc-3.2 (default compiler from now)
- New version: 0.5 toaster.
* Tue Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.1.5.2-1
- Rebuild agains 0.4 toaster
- Better upgrade features
* Wed Aug 07 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.5.2-1
- New version (1.5.2)
* Thu Aug 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.5.1-3
- Better dependencies for RedHat
* Thu Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.5.1-2
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
- Soft clean-ups
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.5.1.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-1.5.1.1mdk
- toaster v. 0.2
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.5.1.2mdk
- Added tests for gcc-3.1.1
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
- Deleted all Mandrake dependencies as mandrake-release and so on...
- Deleted chkconfig work (some people told me on RedHat failed) and added
  soft links.
* Thu Jul 11 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.5.1-1mdk
- First Package
