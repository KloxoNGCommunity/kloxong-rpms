%define 	name daemontools
%define 	pversion 0.76
%define 	bversion 1.3
%define 	rpmrelease 7%{?dist}

%define	release %{bversion}.%{rpmrelease}
%define	ccflags %{optflags}
%define	ldflags %{optflags}


############### RPM ################################

%define	debug_package %{nil}
%define 	cmddir /command
%define 	srvdir /service
%define 	vtoaster %{pversion}
%define	builddate Sun Jun 14 2009

Name:		%{name}-toaster
Summary:	DJB daemontools
Version:	%{vtoaster}
Release:	%{release}
License:	GNU
Group:		System/Servers
URL:		http://cr.yp.to/daemontools.html
Source:		daemontools-%{pversion}.tar.bz2
Source1:	daemontools-%{pversion}-man.tar.bz2
Patch:		daemontools-toaster-errno.patch.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}
Obsoletes:	daemontools-toaster-doc
Packager:	Jake Vickers <jake@qmailtoaster.com>
 
#----------------------------------------------------------------------------------
%description
#----------------------------------------------------------------------------------
Supervise monitors a service. It starts the service and restarts the
service if it dies.  The companion  svc program  stops,  pauses,  or
restarts the service on sysadmin request.  The svstat program prints
a one-line status report.

Multilog saves error  messages to  one or more  logs.  It optionally
timestamps each line and,  for each log,  includes or excludes lines
matching specified patterns.  It automatically rotates logs to limit
the amount of disk space used.   If the disk fills up, it pauses and
tries again, without losing any data.


#----------------------------------------------------------------------------------
%prep
#----------------------------------------------------------------------------------
%define name daemontools
%setup -q -n %{name}-%{pversion}
%patch -p0

#----------------------------------------------------------------------------------
%setup -q -T -D -c -a 1 -n %{name}-%{pversion}
#----------------------------------------------------------------------------------


# Cleanup for gcc
#----------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc

#----------------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# We have gcc written in a temp file
echo "`cat %{_tmppath}/%{name}-%{pversion}-gcc` %{ccflags}"    >src/conf-cc
echo "`cat %{_tmppath}/%{name}-%{pversion}-gcc` -s %{ldflags}" >src/conf-ld

# Delete gcc temp file
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "%{_prefix}" >src/conf-home

package/compile

#----------------------------------------------------------------------------------
%install
#----------------------------------------------------------------------------------

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{cmddir}
mkdir -p %{buildroot}%{srvdir}

install -m 755 command/* %{buildroot}%{_bindir}
install -m 644 %{name}-%{pversion}-man/*.8 %{buildroot}%{_mandir}/man8
for i in `cat package/commands`
do
  ln -s ..%{_bindir}/$i %{buildroot}/command/$i
done



#----------------------------------------------------------------------------------
%clean
#----------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#----------------------------------------------------------------------------------
%files
#----------------------------------------------------------------------------------
%defattr (-,root,root)
%doc src/CHANGES package/README src/TODO
%attr(0755,root,root) %{_bindir}/svscan
%attr(0755,root,root) %{_bindir}/svscanboot
%attr(0755,root,root) %{_bindir}/supervise
%attr(0755,root,root) %{_bindir}/svc
%attr(0755,root,root) %{_bindir}/svok
%attr(0755,root,root) %{_bindir}/svstat
%attr(0755,root,root) %{_bindir}/fghack
%attr(0755,root,root) %{_bindir}/multilog
%attr(0755,root,root) %{_bindir}/pgrphack
%attr(0755,root,root) %{_bindir}/tai64n
%attr(0755,root,root) %{_bindir}/tai64nlocal
%attr(0755,root,root) %{_bindir}/readproctitle
%attr(0755,root,root) %{_bindir}/softlimit
%attr(0755,root,root) %{_bindir}/envuidgid
%attr(0755,root,root) %{_bindir}/envdir
%attr(0755,root,root) %{_bindir}/setlock
%attr(0755,root,root) %{_bindir}/setuidgid
%attr(0755,root,root) %dir %{cmddir}
%attr(0755,root,root) %{cmddir}/*
%attr(0755,root,root) %dir %{srvdir}

%attr(0644,root,root) %{_mandir}/man8/envdir.8.*
%attr(0644,root,root) %{_mandir}/man8/envuidgid.8.*
%attr(0644,root,root) %{_mandir}/man8/fghack.8.*
%attr(0644,root,root) %{_mandir}/man8/multilog.8.*
%attr(0644,root,root) %{_mandir}/man8/pgrphack.8.*
%attr(0644,root,root) %{_mandir}/man8/readproctitle.8.*
%attr(0644,root,root) %{_mandir}/man8/setlock.8.*
%attr(0644,root,root) %{_mandir}/man8/setuidgid.8.*
%attr(0644,root,root) %{_mandir}/man8/softlimit.8.*
%attr(0644,root,root) %{_mandir}/man8/supervise.8.*
%attr(0644,root,root) %{_mandir}/man8/svc.8.*
%attr(0644,root,root) %{_mandir}/man8/svok.8.*
%attr(0644,root,root) %{_mandir}/man8/svscan.8.*
%attr(0644,root,root) %{_mandir}/man8/svscanboot.8.*
%attr(0644,root,root) %{_mandir}/man8/svstat.8.*
%attr(0644,root,root) %{_mandir}/man8/tai64n.8.*
%attr(0644,root,root) %{_mandir}/man8/tai64nlocal.8.*


#----------------------------------------------------------------------------------
%changelog
#----------------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.76-1.3.7.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.76-1.3.6.mr
- add build_cnt_60 and build_cnt_6064

* Sun Jun 14 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.6
- Added Mandriva 2009 x86_64 support
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.6
- Added Fedora 11 x86_64 support
* Thu Jun 11 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.6
- Added Fedora 11 support
* Tue Jun 02 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.6
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.4
- Added Suse 11.1 support
* Sun Feb 08 2009 Jake Vickers <jake@qmailtoaster.com> 0.76-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.3.3
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.76-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.11
- Add Fedora Core 5 support
* Fri Apr 28 2006 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.10
- Cleanup format of spec file - No major changes
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.9
- Add SuSE 10.0 and Mandriva 2006.0 support
* Fri Oct 14 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.8
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.7
- Add CentOS 4 x86_64 support
* Wed Jun 29 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.6
- Add Fedora Core 4 support
* Thu Jun 02 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 0.76-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Sun May 22 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.4
- Remove doc rpm
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Wed Jun 02 2004 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.2
- Add Fedora Core 2 support 
* Sun Apr 18 2004 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.2.1
- Move package without change to new qmailtoaster release 
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.0.6
- Add Trustix 2.0 support
- Add Fedora Core 1 support
* Thu Nov 20 2003 Nick Hemmesch <nick@ndhsoft.com> 0.76-1.0.5
- Fix typo and add errno patch
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.76-1.0.4
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.76-1.0.3
- Conectiva Linux 7.0 support
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.76-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 0.76-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support for new RPM-4.0.4
* Sun Oct 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.76-0.9.2
- Little clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.76-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again.
  They are very basic but they should work now.
- Packages are named with their proper releases and bversion is from now
  part of the rpm release: we will continue upgrading safely.
* Mon Sep 23 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.0.76-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
- Clean-ups
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.76-2
- Deleted Mandrake Release Autodetection (creates problems)
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.0.76-1
- New version: 0.7
- Better macros to detect Mandrake Release
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.0.76-1
- New version: 0.6 toaster.
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.0.76-1
- Doc package is standalone (someone does not ask for man pages)
- Checks for gcc-3.2 (default compiler from now)
- New version: 0.5 toaster.
* Thu Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.0.76-1
- Rebuild against 0.4 toaster
* Tue Aug 02 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.76-3
- No more install -s (creates problems)
* Tue Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.76-2
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
- Little clean-ups.
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.0.76.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-0.76.1mdk
- toaster v. 0.2
- added files attributes
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-0.76.3mdk
- Added tests for gcc-3.1.1
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
- Very soft clean-ups
* Thu Jul 11 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.76-2mdk
- Renamed the package in toster (we are building toaster packages)
* Mon Jul 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.76-1mdk
- First package release
