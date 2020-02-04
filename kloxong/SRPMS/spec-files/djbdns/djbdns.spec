Name: djbdns
Version: 1.05
Release: 17.4.kng%{?dist}
Group: Utilities/System
URL: http://cr.yp.to/djbns.html
License: Check with djb@koobera.math.uic.edu

#fix for centos 8 build
%global debug_package %{nil}

Requires: make

Source0: http://cr.yp.to/djbdns/djbdns-%{version}.tar.gz
Source1: ftp://innominate.org/gpa/djb/djbdns-1.05-man-20031023.tar.gz
Source2: ZONE.NOTES
Source3: djbdns.init
Source4: TRANSFER.FROM.MASTER.TO.SECONDARIES
Source5: make-data
Source6: push-changes
Source7: Makefile.example
Source8: trigger-make.c
Source9: update-dns
Source10: djbnotify.conf
Source11: update-dns-cache-root
Source12: cache-reload
Source13: djbdns.init.orig
Patch0: http://www.fefe.de/dns/djbdns-1.05-test23.diff
Patch1: query.arpa.patch
Patch2: dnscache.sigpipe.patch
Patch3: nxdomain.patch
Patch4: tcp.servfail.patch
Patch5: oversize.udp.patch
Patch6: dnscache-cache-soa-records.patch
Patch7: dnscache-merge-similar-outgoing-queries.patch
Patch8: tinydns-fix-file-descriptor-leak.patch
Patch9: tinydns-data-semantic-error.patch
Patch10: dnsroots.global.2002-11.patch
Patch11: dnsroots.global.2004-01.patch
Patch12: tinydns-alias-chain-truncation.patch
Patch13: dnscache-cname-handling.patch
Patch14: dnscache-strict-forwardonly.patch
Patch15: axfrdns-tcp-large-packet.patch
Patch30: djbdns-chroot-kloxong-compile.patch
Summary: A Secure DNS server (Domain Name Server).
Packager: david@summersoft.fay.ar.us
#Requires: ucspi-tcp >= 0.88-4
#Requires: daemontools >= 0.76-2
%ifos linux
Requires: /sbin/chkconfig
%endif
#Conflicts: bind
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}
%define _default_patch_fuzz 2
%description
A secure DNS server (Domain Name Server).

%changelog
* Thu Dec 19 2019 Dionysis Kladis <dkstiler@gmail.com> 1.05-17.5
- added a patch to compile properly in chroot enviroment without root 

* Sun Aug 31 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.05-17.5
- add detect '/etc/sysconfig/djbdns' if exists in djbdns.init

* Wed Aug 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.05-17.4
- disable conflict with bind

* Sun Aug 6 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.05-17.3
- add 'Requires: make' because need to make data.cb (centos 6 not installed it)

* Sun Aug 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.05-17.2
- Compile for Kloxo-MR
- change modified djbdns.init for Kloxo-MR purpose
- back to /bin because change path from /bin to /bin will be conflict with spamdyke-utils

* Sun Jul 17 2011 David Summers <david@summersoft.fay.ar.us> 1.05-17
- Updated build for CentOS 6.

* Sun Mar 13 2011 David Summers <david@summersoft.fay.ar.us> 1.05-16
- Change update-dns-cache-root script to check for type of dns cache,
  in the /etc/dns.cache, either djbdns or unbound.

- Fixed to not delete startup script link when just doing upgrade of RPM.

* Mon Feb 14 2011 David Summers <david@summersoft.fay.ar.us> 1.05-15
- Added patch to make-data to parse for IPv6 addresses
  in '.' (SOA,NS,A) Records and '&' (NS,A) Records.

* Mon Jan 31 2011 David Summers <david@summersoft.fay.ar.us> 1.05-14
- Added weekly check for cache update to root servers.

* Sat May 08 2010 David Summers <david@summersoft.fay.ar.us> 1.05-13
- Updated to http://www.fefe.de/dns/djbdns-1.05-test23.diff.
  Also tested and fixed the special ipv6 names and address lookups.
- Updated to djbdns-1.05-man-20031023 man files.
- Added dnscache SIGPIPE patch, recommended by djb.
- Added patch to do NXDOMAIN caching.
- Added TCP SERVFAIL patch, updated for IPV6.
- Added oversize UDP patch.
- Added SOA cache patch.
- Added the dnscache "merge similar outgoing queries" patch.
- Added the tinydns "file descriptor leak" patch.
- Added the tinydns-data "semantic error" patch.
- Added the dnsroots.global 2002-11 and 2004-01 patches.
- Added the tinydns alias-chain-truncation patch.
- Added the dnscache CNAME handling patch.
- Added the dnscache strict forwardonly patch.
- Added the axfrdns TCP large packet patch.

* Sat Apr 10 2010 David Summers <david@summersoft.fay.ar.us> 1.05-12
- Switched back to SSH/SCP of master to secondary.

* Fri Mar 05 2010 David Summers <david@summersoft.fay.ar.us> 1.05-11
- Added new zone_transfer_notify_server, zone_transfer_notify_client scripts.
- Took out old attempt attempt at immediate zone notification (from -10).

* Sat Sep 06 2008 David Summers <david@summersoft.fay.ar.us> 1.05-10
- Took out CRON daily script to transfer secondaries (from -8) and added
  djbdns_adduser script and examples to allow ssh/scp file transfers to
  secondaries from the dns Makefile script.

  Example scripts found in the /user/share/doc/djbdns-1.05 directory:
  TRANSFER.FROM.MASTER.TO.SECONDARIES
  Makefile.master
  Makefile.secondary

* Wed Nov 21 2007 David Summers <david@summersoft.fay.ar.us> 1.05-9
- Build changes only.  Changed IPV6 diff to be bunzip'ed so we can see
  future changes.

* Tue Aug 21 2007 David Summers <david@summersoft.fay.ar.us> 1.05-8
- Added CRON daily script to transfer secondaries.
  Config file is /etc/djbdns.secondaries which has a list of directories,
  Zone Names, and IP addresses for zones to be transferred.

* Sat Apr 23 2005 David Summers <david@summersoft.fay.ar.us> 1.05-7
- Fix start/stop sequence to only do one start/stop for each service instead
  of multiple ones.

* Tue Jan 20 2004 David Summers <david@summersoft.fay.ar.us> 1.05-6
- Compiles and runs on Solaris 9.

* Wed Sep 03 2003 David Summers <david@summersoft.fay.ar.us> 1.05-5
- Fixed RedHat 9 compile error problem with "errno" variable.
- Now requires ucspi-tcp >= 0.88-4 and daemontools >= 0.76-2 which fix the same
  problem with those other packages.

* Fri Feb 21 2003 David Summers <david@summersoft.fay.ar.us> 1.05-4
- Make sure we require ucspi-tcp >= 0.88-3 and daemontools >= 0.76-1.

* Tue Feb 11 2003 David Summers <david@summersoft.fay.ar.us> 1.05-3
- Start up right after networking and shutdown right before networking.

* Tue Aug 13 2002 David Summers <david@summersoft.fay.ar.us> 1.05-2
- Changed from ip6.int to ip6.arpa per RFC3152.

* Sun Aug 11 2002 David Summers <david@summersoft.fay.ar.us> 1.05-1
- Release 1.
- Added IPV6 patch.
- Added man pages.
- Added ZONE.NOTES crib notes.

%prep
%setup -q -a 1

# IPV6 patch
%patch0 -p1

# QUERY ARPA PATCH
%patch1 -p0

# SIGPIPE PATCH
%patch2 -p0

# NXDOMAIN patch
%patch3 -p1

# TCP SERVFAIL patch
%patch4 -p0

# OVERSIZE UDP patch
%patch5 -p0

# SOA CACHE patch
%patch6 -p1

# DNSCACHE merge similar outgoing queries patch
%patch7 -p1

# tinydns fix file descriptor leak patch.
%patch8 -p0

# tinydns-data semantic error patch.
%patch9 -p0

# dnsroots.global 2002-11 patch.
%patch10 -p0

# dnsroots.global 2004-01 patch.
%patch11 -p2

# tinydns alias chain truncation patch
%patch12 -p1

# dnscache CNAME handling patch.
%patch13 -p1

# dnscache strict forwardonly patch
%patch14 -p1

# axfrdns tcp large packet patch.
%patch15 -p0

# disablind chkshgr check on compile we later need to check it on install 
%patch30 -p1

# Move binaries to /bin
echo "/" > conf-home

# Get ready to compile trigger-make.c
cp %{SOURCE8} .

%build
make

cc trigger-make.c -o trigger-make

%install
/bin/rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/etc/init.d
#mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
%ifnos linux
mkdir -p $RPM_BUILD_ROOT/etc/rc3.d
%endif
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man5
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man8

# Install DJBDNS programs.
cp dnscache-conf $RPM_BUILD_ROOT/bin
cp tinydns-conf  $RPM_BUILD_ROOT/bin
cp walldns-conf  $RPM_BUILD_ROOT/bin
cp rbldns-conf   $RPM_BUILD_ROOT/bin
cp pickdns-conf  $RPM_BUILD_ROOT/bin
cp axfrdns-conf  $RPM_BUILD_ROOT/bin

cp dnscache      $RPM_BUILD_ROOT/bin
cp tinydns       $RPM_BUILD_ROOT/bin
cp walldns       $RPM_BUILD_ROOT/bin
cp rbldns        $RPM_BUILD_ROOT/bin
cp pickdns       $RPM_BUILD_ROOT/bin
cp axfrdns       $RPM_BUILD_ROOT/bin

cp tinydns-get   $RPM_BUILD_ROOT/bin
cp tinydns-data  $RPM_BUILD_ROOT/bin
cp tinydns-edit  $RPM_BUILD_ROOT/bin
cp rbldns-data   $RPM_BUILD_ROOT/bin
cp pickdns-data  $RPM_BUILD_ROOT/bin
cp axfr-get      $RPM_BUILD_ROOT/bin

cp dnsip         $RPM_BUILD_ROOT/bin
cp dnsip6        $RPM_BUILD_ROOT/bin
cp dnsipq        $RPM_BUILD_ROOT/bin
cp dnsip6q       $RPM_BUILD_ROOT/bin
cp dnsname       $RPM_BUILD_ROOT/bin
cp dnstxt        $RPM_BUILD_ROOT/bin
cp dnsmx         $RPM_BUILD_ROOT/bin
cp dnsfilter     $RPM_BUILD_ROOT/bin
cp random-ip     $RPM_BUILD_ROOT/bin
cp dnsqr         $RPM_BUILD_ROOT/bin
cp dnsq          $RPM_BUILD_ROOT/bin
cp dnstrace      $RPM_BUILD_ROOT/bin
cp dnstracesort  $RPM_BUILD_ROOT/bin

cp dnsroots.global $RPM_BUILD_ROOT/etc/

# Install man pages.
cp djbdns-man/*.1 $RPM_BUILD_ROOT/usr/share/man/man1
cp djbdns-man/*.5 $RPM_BUILD_ROOT/usr/share/man/man5
cp djbdns-man/*.8 $RPM_BUILD_ROOT/usr/share/man/man8

# Copy ZONE.NOTES
cp %{SOURCE2} .

# Install startup scripts
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/init.d/djbdns
chmod a+rx $RPM_BUILD_ROOT/etc/init.d/djbdns
%ifnos linux
ln -s ../init.d/djbdns $RPM_BUILD_ROOT/etc/rc3.d/K86djbdns
ln -s ../init.d/djbdns $RPM_BUILD_ROOT/etc/rc3.d/S14djbdns
%endif

# Install configuration file
#touch $RPM_BUILD_ROOT/etc/sysconfig/djbdns

# Install doc files
cp %{SOURCE4} .

# Install make-data
cp %{SOURCE5} $RPM_BUILD_ROOT/bin

# Install push-changes
cp %{SOURCE6} $RPM_BUILD_ROOT/bin

# Install Makefile.example
cp %{SOURCE7} .

# Install trigger-make
cp trigger-make $RPM_BUILD_ROOT/bin

# Install update-dns
cp %{SOURCE9} $RPM_BUILD_ROOT/bin

# Install djbnotify.conf file.
cp %{SOURCE10} $RPM_BUILD_ROOT/etc

# Install update-dns-cache-root
mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cp %{SOURCE11} $RPM_BUILD_ROOT/etc/cron.weekly

# Install cache-reload
mkdir -p $RPM_BUILD_ROOT/bin
cp %{SOURCE12} $RPM_BUILD_ROOT/bin/cache-reload

%pre
if [ "$1"x = "1"x ]; then
%ifos linux
   /usr/sbin/useradd -r dnscache
   /usr/sbin/useradd -r dnslog
   /usr/sbin/useradd -r tinydns
   /usr/sbin/useradd -r axfrdns
   sleep 1;
%else
   /usr/sbin/useradd -d /root dnscache
   /usr/sbin/useradd -d /root dnslog
   /usr/sbin/useradd -d /root tinydns
   /usr/sbin/useradd -d /root axfrdns
   sleep 1;
%endif
fi

%post
if [ "$1"x = "1"x ]; then
%ifos linux
   /sbin/chkconfig --add djbdns
%endif

fi

%preun
/etc/init.d/djbdns stop

%ifos linux
if [ "$1"x = "0"x ]; then
   /sbin/chkconfig --del djbdns
fi
%endif

%postun
if [ "$1"x = "0"x ]; then
   /usr/sbin/userdel dnscache
   /usr/sbin/userdel dnslog
   /usr/sbin/userdel tinydns
   /usr/sbin/userdel axfrdns
fi

%clean
# Clean up after compiling and installing.
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES README TINYDNS TODO VERSION ZONE.NOTES
%doc TRANSFER.FROM.MASTER.TO.SECONDARIES
%doc Makefile.example
/etc/init.d/djbdns
/etc/cron.weekly/update-dns-cache-root
%ifnos linux
/etc/rc3.d/*
%endif
#%config /etc/sysconfig/djbdns
%config /etc/djbnotify.conf
%config /etc/dnsroots.global
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*
%attr(0755,root,root)/bin/trigger-make
/bin/*
