Name: qmail
Version: 1.03
Release: 9%{org_tag}%{dist}
Group: Networking/Daemons
URL: http://www.qmail.org/
License: Public Domain
Packager: Gavin Carr <gavin@openfusion.com.au>
Source0: http://cr.yp.to/qmail/qmail-1.03.tar.gz
Source1: http://www.din.or.jp/~ushijima/qmail-conf/qmail-conf-0.60.tar.gz
Source2: http://cr.yp.to/djbdns/djbdns-1.05.tar.gz
Source3: http://sourceforge.net/projects/qmhandle/qmhandle-1.3.2.tar.gz
Patch0: http://www.qmail.org/moni.csi.hu/pub/glibc-2.3.1/qmail-1.03.errno.patch
Patch1: http://www.qmail.org/moni.csi.hu/pub/glibc-2.3.1/qmail-1.03.qmail_local.patch
Patch2: http://www.qmail.org/qmailqueue.patch
# http://www.ckdhr.com/ckd/qmail-103.patch
Patch3: qmail-1.03-dns-large-results.patch
Patch10: http://www.qmail.org/moni.csi.hu/pub/glibc-2.3.1/djbdns-1.05.errno.patch
Summary: Qmail Mail Transfer Agent
Provides: MTA
Provides: smtpdaemon
Provides: pop3daemon
Provides: qmtpdaemon
Provides: qmqpdaemon
Conflicts: sendmail
BuildRequires: qmail-build-environment
BuildRequires: ucspi-tcp >= 0.88-2
BuildRequires: groff
Requires: ucspi-tcp >= 0.88-2
Requires: daemontools
Buildroot: %_tmppath/%{name}-%{version}

%description
Qmail is a small, fast, secure replacement for the sendmail package, which 
is the program that actually receives, routes, and delivers electronic mail.

This is the Open Fusion qmail package, consisting of the vanilla qmail 1.03 
source with a minimal set of patches applied: currently errno (for glibc 
2.3.1), qmail-local, qmail-queue, and dns-large-results. It also includes 
Tetsu Ushijima's qmail-conf utilities and Michele Beltrame's qmhandle. 
Package originally based on Bruce Guenther's qmail+patches rpm (from 
http://untroubled.org).

%prep
%setup
%setup -T -D -a 1 
%setup -T -D -a 2 
%setup -T -D -a 3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd djbdns-1.05
%patch10 -p1
cd ..

%build
make compile makelib
make it man
cd qmail-conf-0.60
echo '/usr' > conf-ucspi-tcp
make -f Makefile.ini djbdns=../djbdns-1.05
make

%install
export PATH="/sbin:/usr/sbin:/bin:/usr/bin"
/bin/rm -rf $RPM_BUILD_ROOT
mkdir -p -m 0755 $RPM_BUILD_ROOT/usr/lib
mkdir -p -m 0755 $RPM_BUILD_ROOT/usr/sbin
for i in alias bin boot control doc service users; do
  mkdir -p -m 0755 $RPM_BUILD_ROOT/var/qmail/$i
done
for i in cat1 cat5 cat7 cat8 man1 man5 man7 man8; do
  mkdir -p -m 0755 $RPM_BUILD_ROOT/var/qmail/man/$i
done
mkdir -p -m 0750 $RPM_BUILD_ROOT/var/qmail/queue
for i in todo mess lock; do
  mkdir -p -m 0750 $RPM_BUILD_ROOT/var/qmail/queue/$i
done
for i in pid intd bounce info local remote; do
  mkdir -p -m 0700 $RPM_BUILD_ROOT/var/qmail/queue/$i
done
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do
  mkdir -p -m 0750 $RPM_BUILD_ROOT/var/qmail/queue/mess/$i
  mkdir -p -m 0700 $RPM_BUILD_ROOT/var/qmail/queue/info/$i
  mkdir -p -m 0700 $RPM_BUILD_ROOT/var/qmail/queue/local/$i
  mkdir -p -m 0700 $RPM_BUILD_ROOT/var/qmail/queue/remote/$i
done
# Setup queue special files
touch $RPM_BUILD_ROOT/var/qmail/queue/lock/sendmutex
chmod 0600 $RPM_BUILD_ROOT/var/qmail/queue/lock/sendmutex
dd if=/dev/zero of=$RPM_BUILD_ROOT/var/qmail/queue/lock/tcpto bs=1024 count=1
chmod 0644 $RPM_BUILD_ROOT/var/qmail/queue/lock/tcpto
mknod -m 0622 $RPM_BUILD_ROOT/var/qmail/queue/lock/trigger p 
# Install binaries
install -m 0700 qmail-lspawn qmail-start qmail-newu qmail-newmrh $RPM_BUILD_ROOT/var/qmail/bin
install -m 0711 qmail-queue qmail-getpw qmail-local qmail-remote qmail-rspawn qmail-clean qmail-send splogger qmail-pw2u $RPM_BUILD_ROOT/var/qmail/bin
install -m 0755 qmail-inject predate datemail mailsubj qmail-showctl qmail-qread qmail-qstat qmail-tcpto qmail-tcpok qmail-pop3d qmail-popup qmail-qmqpc qmail-qmqpd qmail-qmtpd qmail-smtpd sendmail tcp-env qreceipt qsmhook qbiff forward preline condredirect bouncesaying except maildirmake maildir2mbox maildirwatch qail elq pinq $RPM_BUILD_ROOT/var/qmail/bin
# Install boot scripts
install -m 0755 home home+df proc proc+df binm1 binm1+df binm2 binm2+df binm3 binm3+df $RPM_BUILD_ROOT/var/qmail/boot
cat <<EOD > $RPM_BUILD_ROOT/var/qmail/rc
#!/bin/sh
#
# Using qmail-local to deliver to ~/Maildir/ by default (no splogger).
#

exec env - PATH="/var/qmail/bin:$PATH" qmail-start ./Maildir/

EOD
chmod 755 $RPM_BUILD_ROOT/var/qmail/rc
# Install docs
install -m 0644 README BIN.README BLURB* CHANGES FAQ UPGRADE SENDMAIL INSTALL* TEST* REMOVE* PIC* $RPM_BUILD_ROOT/var/qmail/doc
# Install man pages
install -m 0644 *.1 $RPM_BUILD_ROOT/var/qmail/man/man1
install -m 0644 *.5 $RPM_BUILD_ROOT/var/qmail/man/man5
install -m 0644 *.7 $RPM_BUILD_ROOT/var/qmail/man/man7
install -m 0644 *.8 $RPM_BUILD_ROOT/var/qmail/man/man8
# Install qmail-conf binaries
install -m 0755 qmail-conf-0.60/qmail*conf $RPM_BUILD_ROOT/var/qmail/bin
# Install qmhandle
install -m 0755 qmhandle-1.3.2/qmHandle $RPM_BUILD_ROOT/var/qmail/bin/qmhandle
install -m 0644 qmhandle-1.3.2/README $RPM_BUILD_ROOT/var/qmail/doc/README.qmhandle

# Create sendmail links
pushd $RPM_BUILD_ROOT/usr/lib
  ln -sf /var/qmail/bin/sendmail 
popd
pushd $RPM_BUILD_ROOT/usr/sbin
  ln -sf /var/qmail/bin/sendmail 
popd

# Install some extra configuration programs
pushd $RPM_BUILD_ROOT/var/qmail/alias
  echo '&root' >.qmail-postmaster
  echo '&root' >.qmail-mailer-daemon
  touch .qmail-root
  chmod 644 .qmail*
popd

pushd $RPM_BUILD_ROOT/var/qmail/control
  touch defaultdomain locals me plusdomain rcpthosts
  chmod 644 defaultdomain locals me plusdomain rcpthosts
popd

%clean
rm -rf $RPM_BUILD_ROOT

# Pre/Post-install Scripts #####################################################
%pre
PATH="/sbin:/usr/sbin:$PATH" export PATH
add_user() { grep "^$1:" /etc/passwd >/dev/null || useradd -d "$4" -u "$2" -g "$3" -M -r -s /bin/true "$1"; }
add_group() { grep "^$1:" /etc/group >/dev/null || groupadd -g "$2" "$1"; }

add_group nofiles 350
add_group qmail   351

add_user alias  350 nofiles /var/qmail/alias
add_user qmaild 351 nofiles /var/qmail
add_user qmaill 352 nofiles /var/qmail
add_user qmailp 353 nofiles /var/qmail
add_user qmailq 354   qmail /var/qmail
add_user qmailr 355   qmail /var/qmail
add_user qmails 356   qmail /var/qmail

%post
PATH="/sbin:/usr/sbin:$PATH" export PATH
# Binaries
if ! [ -s /var/qmail/control/me ]; then
  hostname > /var/qmail/control/me
  hostname > /var/qmail/control/locals
fi
# Startup initial services
if ! [ -d /var/qmail/service/qmail ]; then
  /var/qmail/bin/qmail-delivery-conf qmaill /var/qmail/service/qmail
  echo 999999 > /var/qmail/service/qmail/log/env/MAXFILESIZE
fi
[ -L /service/qmail ] || ln -sf /var/qmail/service/qmail /service
[ -L /var/log/qmail ] || ln -sf /var/qmail/service/qmail/log/main /var/log/qmail
[ -L /service/qmail ] && svc -u /service/qmail 
[ -d /service/qmail/log ] && svc -u /service/qmail/log

%preun
if [ $1 -gt 0 ]; then exit 0; fi

for svc in pop3d qmail qmqpd qmtpd qread qstat smtpd; do
  if [ -L /service/$svc ]; then
    svc -d /service/$svc /service/$svc/log
    rm -f /service/$svc
  fi
done

%files
%defattr(-,root,qmail)

%dir %attr(0755,root,qmail) /var/qmail
%dir /var/qmail/bin
/var/qmail/bin/bouncesaying
/var/qmail/bin/condredirect
/var/qmail/bin/datemail
/var/qmail/bin/elq
/var/qmail/bin/except
/var/qmail/bin/forward
/var/qmail/bin/maildir2mbox
/var/qmail/bin/maildirmake
/var/qmail/bin/maildirwatch
/var/qmail/bin/mailsubj
/var/qmail/bin/pinq
/var/qmail/bin/predate
/var/qmail/bin/preline
/var/qmail/bin/qail
/var/qmail/bin/qbiff
%attr(0711,root,qmail) /var/qmail/bin/qmail-clean
%attr(0711,root,qmail) /var/qmail/bin/qmail-getpw
/var/qmail/bin/qmail-inject
%attr(0711,root,qmail) /var/qmail/bin/qmail-local
%attr(0700,root,qmail) /var/qmail/bin/qmail-lspawn
%attr(0700,root,qmail) /var/qmail/bin/qmail-newmrh
%attr(0700,root,qmail) /var/qmail/bin/qmail-newu
/var/qmail/bin/qmail-pop3d
%attr(0711,root,qmail) /var/qmail/bin/qmail-popup
%attr(0711,root,qmail) /var/qmail/bin/qmail-pw2u
/var/qmail/bin/qmail-qmqpc
/var/qmail/bin/qmail-qmqpd
/var/qmail/bin/qmail-qmtpd
/var/qmail/bin/qmail-qread
/var/qmail/bin/qmail-qstat
%attr(04711,qmailq,qmail) /var/qmail/bin/qmail-queue
%attr(0711,root,qmail) /var/qmail/bin/qmail-remote
%attr(0711,root,qmail) /var/qmail/bin/qmail-rspawn
%attr(0711,root,qmail) /var/qmail/bin/qmail-send
/var/qmail/bin/qmail-showctl
/var/qmail/bin/qmail-smtpd
%attr(0700,root,qmail) /var/qmail/bin/qmail-start
/var/qmail/bin/qmail-tcpok
/var/qmail/bin/qmail-tcpto
/var/qmail/bin/qreceipt
/var/qmail/bin/qsmhook
%attr(0711,root,qmail) /var/qmail/bin/splogger
/var/qmail/bin/tcp-env
/var/qmail/bin/sendmail
%config %attr(0755,root,qmail) /var/qmail/rc
/var/qmail/bin/qmail-*-conf
/var/qmail/bin/qmhandle

%dir %attr(2755,alias,qmail) /var/qmail/alias
%config %attr(0644,alias,qmail) /var/qmail/alias/.qmail*
%config /var/qmail/control/*
%config /var/qmail/users

%dir %attr(0750,qmailq,qmail) /var/qmail/queue
%attr(0700,qmails,qmail) /var/qmail/queue/bounce
%attr(0700,qmails,qmail) /var/qmail/queue/info
%attr(0700,qmailq,qmail) /var/qmail/queue/intd
%attr(0700,qmails,qmail) /var/qmail/queue/local
%attr(0750,qmailq,qmail) /var/qmail/queue/mess
%attr(0700,qmailq,qmail) /var/qmail/queue/pid
%attr(0700,qmails,qmail) /var/qmail/queue/remote
%attr(0750,qmailq,qmail) /var/qmail/queue/todo

%dir %attr(0750,qmailq,qmail) /var/qmail/queue/lock
%attr(0600,qmails,qmail) /var/qmail/queue/lock/sendmutex
%attr(0644,qmailr,qmail) /var/qmail/queue/lock/tcpto
%attr(0622,qmails,qmail) /var/qmail/queue/lock/trigger

/var/qmail/service
/var/qmail/boot

/usr/lib/sendmail
/usr/sbin/sendmail

%docdir /var/qmail/man
%docdir /var/qmail/doc
/var/qmail/man/*
/var/qmail/doc/*

%changelog
* Thu Aug 21 2014 Gavin Carr <gavin@openfusion.com.au> 1.03-9
- Update included qmhandle to v1.3.2.

* Fri Sep 02 2011 Gavin Carr <gavin@openfusion.com.au> 1.03-8
- More minor cleanups to get building in mock environment.

* Fri Aug 03 2007 Gavin Carr <gavin@openfusion.com.au> 1.03-5
- More minor spec file cleanups when rebuilding for centos5.

* Wed Mar 30 2005 Gavin Carr <gavin@openfusion.com.au> 1.03-4
- Fixed up some missing files and attributes.

* Thu Mar 17 2005 Gavin Carr <gavin@openfusion.com.au> 1.03-3
- Cleaned up various permissions and %post niggles.

# arch-tag: 9b3e0d55-d240-4bc0-9ee7-89786ad486b2
