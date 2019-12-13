%define 	name qmail
%define 	pversion 1.03
%define 	bversion 1.3
%define 	rpmrelease 57.kng%{?dist}


%define	release %{bversion}.%{rpmrelease}
%define	crontab /etc/crontab
%define	rcpath /etc
%define	_initpath /etc/rc.d/init.d
BuildRequires:	openssl-devel >= 0.9.8, krb5-devel >= 1.5
Requires:		openssl >= 0.9.8, sh-utils
BuildRequires:	shadow-utils, bzip2, net-tools
Provides:	smtpdaemon, MTA
Obsoletes:	qmail-toaster-doc
%define	ccflags %{optflags} -DTLS=20060104 -I/home/vpopmail/include
%define	ldflags %{optflags}


############### RPM ################################

%define		debug_package %{nil}
%define		vtoaster %{pversion}
%define		qdir /var/qmail
%define		builddate Thu Feb 24 2011

Name:		%{name}-toaster
Summary:	qmail Mail Transfer Agent
Version:	%{vtoaster}
Release:	%{release}
License:	GNU
Group:		System/Servers
URL:		http://www.qmail.org/

Source:	qmail-%{pversion}.tar.bz2
Source1:	qmail_qmail-aliases
Source3:	qmail_qmail.rc
Source4:	qmail_qmail.init
Source5:	qmail_supervise-pop3.run
Source6:	qmail_supervise-pop3-log.run
Source7:	qmail_supervise-send.run
Source8:	qmail_supervise-send-log.run
Source9:	qmail_supervise-smtp.run
Source10:	qmail_supervise-smtp-log.run
Source19:	qmail_supervise-submission.run
Source20:	qmail_supervise-submission-log.run
Source11:	qmail_gentestcrt.sh
Source12:	qmail_badmimetypes
Source13:	qmail_badloadertypes
Source14:	qmail_badmailfrom
Source15:	qmail_badmailto
Source16:	qmail_dh_key
Source17:	qmail_qmail-default
Source18:	qmail_qmail.init.sus

Source100:	qmail_supervise-smtp-ssl.run
Source101:	qmail_supervise-smtp-ssl-log.run

Source200:	qmail_dkimsign.pl
Source201:	qmail_qmail-remote.new

Source300:	qmail_sendmail-wrapper

Patch0:	qmail_qmailtoaster-1.3.2.patch
Patch1:	qmail_qmailtoaster-chkuser.patch
Patch2:	qmail_qmail-require_auth.patch
Patch3:	qmail_qmail-dk-0.6.beta.2.patch
Patch4:	qmail_qmail-smtpd-spf-qq-reject-logging.patch
Patch5:	qmail_qmail-srs-qt-0.5.patch
Patch6:	qmail_qmailtoaster-big-dns.patch
Patch7:	qmail_qmail-smtpd-linefeed.patch
Patch8:	qmail_qmail-empf.patch

Patch9:	qmail_qmail-vpopmail-devel.patch
Patch10: qmail_qmail-uids.patch

Patch11: qmail_qmail-nocram.patch
Patch12: qmail_splogger-nostamp.patch

Patch20: qmail_qmail-outgoingip_rediff.patch
Patch21: qmail_qmail-outgoingips_rediff.patch

Patch30: qmail_qmailtoaster-any-to-cname.patch

Patch40: qmail-toaster-centos-7-chroot.patch

Requires: ucspi-tcp-toaster >= 0.88
Requires: vpopmail-toaster >= 5.4.17
Requires: libsrs2-toaster >= 1.0.18
Requires: mysql-devel
Requires: mysql-libs


BuildRequires: libvpopmail-devel >= 5.4.17
BuildRequires: mysql-devel

Buildroot:	%{_tmppath}/%{name}-%{version}
#Conflicts:	sendmail, exim, smail, postfix, qmail
Obsoletes:	sendmail, sendmail-cf, sendmail-doc, sendmail-devel
Obsoletes:	exim, smail, postfix, qmail, ssmtp
Obsoletes:	set-toaster, checkpassword, vpopmail

Packager:	Jake Vickers <jake@qmailtoaster.com>

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
qmail is a small, fast, secure replacement for the sendmail package, which is
the program that actually receives, routes, and delivers electronic mail.

qmailtoaster-1.3.2.patch            Thu Feb 24, 2011

~~~~~~~~~~~~~ Patches Applied ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qmail-1.03 patched to netqmail-1.05
-----------------------------------
QMAILQUEUE patch
qmail-local patch
local IP 0.0.0.0 patch
sendmail -f patch

Andrew St. Jean - qregex-starttls-2way-auth-20060305
http://www.arda.homeunix.net/store/qmail/

Frederik Vermeulen - qmail-tls 20060104
http://inoa.net/qmail-tls/

Erwin Hoffman - SMTP-AUTH Version 0.57
http://www.fehcom.de/qmail/

Robert Sander - qmail-remote-auth
http://www.ornl.gov/lists/mailing-lists/qmail/2002/03/msg00091.html

Antonio Nati - chkuser-2.0.9
http://www.interazioni.it/opensource/chkuser/

Chris christophe@saout.de - qmail-spf.rc5 
http://www.saout.de/misc/spf/

Russ Nelson - qmail-1.03-dk-0.54 domainkeys patch
http://www.qmail.org/qmail-1.03-dk-0.54.patch

Jeremy Kister - qmail-dk-0.54-auth patch
http://jeremy.kister.net/code/qmail-dk-0.54-auth.patch

Erwin Hoffmann - warlord-1.3.11  
http://www.fehcom.de/qmail/

Bill Shupp - netqmail-maildir++.patch
http://shupp.org/patches/netqmail-maildir++.patch

Bill Shupp - custom-smtp-reject
http://www.shupp.org/patches/custom.patch

Johannes Erdfelt - big-concurrency patch
http://qmail.org/big-concurrency.patch

Inter7 - qmailtap-1.1 tap
http://www.inter7.com/qmailtap/qmail-tap-1.1.diff

Alexey Loukianov - Log Enhancement Patch

Jean-Paul van de Plasse - REQUIRE_AUTH Patch

Marcelo Coelho - qmail-srs-0.4.patch
http://opensource.mco2.net/qmail/srs/

SMTP Linefeed Patch

Big DNS Patch

Inter7 - eMPF 1.0
http://www.inter7.com/?page=empf-install

%package -n qmail-pop3d-toaster
Summary:	POP3 daemon for qmail
Group:		System/Servers
Requires:	qmail-toaster >= %{pversion}-%{release}
Requires:	vpopmail-toaster >= 5.4.17
Conflicts:	uw-imap, courier-imap, dovecot-toaster, dovecot

%description -n qmail-pop3d-toaster
The qmail-pop3d packages provides POP3 support for qmail mail servers.  If
you need to be able to use POP3 with your qmail server, you should install
this package.


#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q -n qmail-%{pversion}

# Apply composit patch
#-------------------------------------------------------------------------------
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p1
%patch6 -p0
%patch7 -p0
%patch8 -p1

#%patch9 -p1
%patch10 -p1

%patch11 -p1
%patch12 -p1

#%patch20 -p1
%patch21 -p1

%patch30 -p1
# fixing compile error in qmail and centos 7 needs a check that cant be done in a chroot enviroment
%if %{?fedora}0 > 140 || %{?rhel}0 > 60
%patch40 -p1
%endif

%define name qmail

# Remove CRAM-MD5 because qmail-remote-auth doesn't like it
#-------------------------------------------------------------------------------
%{__perl} -pi -e "s|\#define AUTHCRAM||g" qmail-smtpd.c
%{__perl} -pi -e "s|LDK_PATH|%{_libdir}/libdomainkeys.a|g" Makefile



# Cleanup for the gcc
#-------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}


 
# Commenting group and users creation at build and trying to find a work around 
# Add users and groups as per Life With Qmail
#-------------------------------------------------------------------------------
#if [ -z "`/usr/bin/id -g nofiles 2>/dev/null`" ]; then
#	groupadd -g 2107 -r nofiles 2>&1 || :
#fi
#if [ -z "`/usr/bin/id -g qmail 2>/dev/null`" ]; then	
#	groupadd -g 2108 -r qmail 2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u alias 2>/dev/null`" ]; then
#	useradd -u 7790 -r -M -d %{qdir}/alias -s /sbin/nologin -c "qmail alias" -g qmail alias  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmaild 2>/dev/null`" ]; then
#	useradd -u 7791 -r -M -d %{qdir} -s /sbin/nologin -c "qmail daemon" -g qmail qmaild  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmaill 2>/dev/null`" ]; then
#	useradd -u 7792 -r -M -d %{qdir} -s /sbin/nologin -c "qmail logger" -g qmail qmaill  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmailp 2>/dev/null`" ]; then
#	useradd -u 7793 -r -M -d %{qdir} -s /sbin/nologin -c "qmail passwd" -g qmail qmailp  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmailq 2>/dev/null`" ]; then
#	useradd -u 7794 -r -M -d %{qdir} -s /sbin/nologin -c "qmail queue" -g qmail qmailq  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmailr 2>/dev/null`" ]; then
#	useradd -u 7795 -r -M -d %{qdir} -s /sbin/nologin -c "qmail remote" -g qmail qmailr  2>&1 || :
#fi
#if [ -z "`/usr/bin/id -u qmails 2>/dev/null`" ]; then
#	useradd -u 7796 -r -M -d %{qdir} -s /sbin/nologin -c "qmail send" -g qmail qmails  2>&1 || :
#fi

# We may need this to build and in order for qmail-toaster to have access to /home/vpopmail/include/ 
#if [ ! -z "`/usr/bin/id -g vchkpw 2>/dev/null`" ]; then
#	adduser qmail vchkpw 2>&1   || :
#fi


# We have gcc written in a temp file
#-------------------------------------------------------------------------------
echo "`cat %{_tmppath}/%{name}-%{pversion}-gcc` %{ccflags}"    >conf-cc
echo "`cat %{_tmppath}/%{name}-%{pversion}-gcc` -s %{ldflags}" >conf-ld

# Delete gcc temp file
#-------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

make clean
make compile makelib
make it man


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
export PATH="/sbin:/usr/sbin:/bin:/usr/bin"

# install directories
#-------------------------------------------------------------------------------
install -d -o root -g qmail %{buildroot}%{qdir}
install -d -o alias -g qmail %{buildroot}%{qdir}/alias
install -d -g qmail %{buildroot}%{qdir}/control
install -d -g qmail %{buildroot}%{qdir}/owners
install -d -g qmail %{buildroot}%{qdir}/users
install -d -g qmail %{buildroot}%{qdir}/control/domainkeys
install -d -g qmail %{buildroot}%{qdir}/control/tlshosts
install -d -g qmail %{buildroot}%{qdir}/control/tlshosts/exhaustivelist
install -d %{buildroot}%{qdir}/bin
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{qdir}/man
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}

#-------------------------------------------------------------------------------
install -d -m755 -o 0 -g qmail %{buildroot}%{qdir}
for i in bin boot control doc man users; do
  install -d -m755 -o 0 -g qmail %{buildroot}%{qdir}/$i
done

for i in man1 man5 man7 man8; do
  install -d -m755 -o 0 -g qmail %{buildroot}%{qdir}/man/$i
done

for i in cat1 cat5 cat7 cat8; do
  install -d -m755 -o 0 -g qmail %{buildroot}%{qdir}/man/$i
done

#-------------------------------------------------------------------------------
install -d -m700 -o 0 -g 0 %{buildroot}%{qdir}/supervise
for i in send smtp submission pop3 smtp-ssl; do
  install -d -m1751 -o 0 -g qmail %{buildroot}%{qdir}/supervise/$i
  install -d -m751 -o 0 -g qmail %{buildroot}%{qdir}/supervise/$i/log
  install -d -m751 -o 0 -g qmail %{buildroot}%{qdir}/supervise/$i/supervise
done

#-------------------------------------------------------------------------------
install -d -m750 -o qmailq -g qmail %{buildroot}%{qdir}/queue
install -d -m2755 -o alias -g qmail %{buildroot}%{qdir}/alias

install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail
install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail/send
install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail/smtp
install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail/submission
install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail/pop3
install -d -m755 -o qmaill -g 0 %{buildroot}/var/log/qmail/smtp-ssl

# install binaries
#-------------------------------------------------------------------------------
for i in bouncesaying condredirect datemail elq except forward instcheck maildir2mbox maildirmake maildirwatch mailsubj pinq predate preline qail qbiff; do
  install -m755 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/bin
done

for i in qmail-clean qmail-getpw qmail-local qmail-popup qmail-pw2u qmail-remote qmail-rspawn qmail-send splogger; do
  install -m711 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/bin
done

for i in qmail-lspawn qmail-newmrh qmail-newu qmail-start; do
  install -m700 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/bin
done

for i in qmail-dk qmail-queue; do
  install -m4711 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/bin
done

for i in qmail-badmimetypes qmail-badloadertypes qmail-inject qmail-pop3d qmail-qmqpc qmail-qmqpd qmail-qmtpd qmail-qread qmail-qstat qmail-showctl qmail-smtpd qmail-tcpok qmail-tcpto qreceipt qsmhook sendmail spfquery tcp-env srsfilter; do
  install -m755 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/bin
done


# install docs
#-------------------------------------------------------------------------------
for i in BIN.README BLURB BLURB2 BLURB3 BLURB4 CHANGES CHKUSER.changelog CHKUSER.copyright CHKUSER.log_format CHKUSER.readme CHKUSER.running chkuser_settings.h FAQ FILES FILES.warlord HISTORY.warlord INSTALL INSTALL.alias INSTALL.ctl INSTALL.ids INSTALL.maildir INSTALL.mbox INSTALL.vsm INSTALL.warlord INTERNALS PIC.local2alias PIC.local2ext PIC.local2local PIC.local2rem PIC.local2virt PIC.nullclient PIC.relaybad PIC.relaygood PIC.rem2local README README.srs README.auth README.domainkeys README.qregex README.remote-auth README.starttls README.tap README.warlord REMOVE.binmail REMOVE.sendmail SECURITY SYSDEPS THANKS THOUGHTS TODO UPGRADE VERSION ChangeLog.empf README.empf; do
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/doc
done

for i in qreceipt condredirect mailsubj except maildirmake preline tcp-env bouncesaying maildir2mbox qbiff forward maildirwatch; do
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.1 %{buildroot}%{qdir}/man/man1
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.0 %{buildroot}%{qdir}/man/cat1
done

for i in qmail-users maildir qmail-header envelopes mbox tcp-environ qmail-control qmail-log addresses dot-qmail; do
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.5 %{buildroot}%{qdir}/man/man5
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.0 %{buildroot}%{qdir}/man/cat5
done

for i in qmail-limits forgeries qmail; do
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.7 %{buildroot}%{qdir}/man/man7
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.0 %{buildroot}%{qdir}/man/cat7
done

for i in qmail-badmimetypes qmail-badloadertypes qmail-tcpto qmail-qread splogger qmail-start qmail-qmqpc qmail-newu qmail-tcpok qmail-pop3d qmail-inject qmail-clean qmail-getpw qmail-command qmail-showctl qmail-rspawn qmail-smtpd qmail-qmqpd qmail-qstat qmail-pw2u qmail-qmtpd qmail-queue qmail-popup qmail-lspawn qmail-newmrh qmail-local qmail-send qmail-remote; do
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.8 %{buildroot}%{qdir}/man/man8
  install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/$i.0 %{buildroot}%{qdir}/man/cat8
done

install -m644 -o 0 -g qmail $RPM_BUILD_DIR/%{name}-%{pversion}/qmail-dk.8 %{buildroot}%{qdir}/man/man8

# install boot
#-------------------------------------------------------------------------------
for i in home home+df binm1 binm2+df proc+df binm2 binm3 proc binm3+df binm1+df; do
  install -m755 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{qdir}/boot
done

# build the queue
#-------------------------------------------------------------------------------
for i in bounce info intd local lock mess pid remote todo; do
  install -d %{buildroot}%{qdir}/queue/$i
done

for d in info local mess remote; do
  for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do
    install -d %{buildroot}%{qdir}/queue/$d/$i
  done
done

# the rest
#-------------------------------------------------------------------------------
touch %{buildroot}%{qdir}/queue/lock/sendmutex
touch %{buildroot}%{qdir}/queue/lock/tcpto

# trigger will be changed to a named pipe in the %post section
# this is because fuse-unionfs doesn't handle named pipes (yet)
#mkfifo -m 0622 %{buildroot}%{qdir}/queue/lock/trigger
touch %{buildroot}%{qdir}/queue/lock/trigger

install -m755 instcheck %{buildroot}%{qdir}/bin
install -m755 config-fast %{buildroot}%{qdir}/bin

install -m755 %{SOURCE3} %{buildroot}%{qdir}/rc

mkdir -p %{buildroot}/var/log/qmail/{smtp,smtp-ssl,submission,pop3,send}

mkdir -p %{buildroot}%{_initpath}
install -m755 %{SOURCE4} %{buildroot}%{_initpath}/qmail

### MR -- for dkimsign.pl and qmail-remote.new
install -m755 %{SOURCE200} %{buildroot}%{qdir}/bin/dkimsign.pl
install -m755 %{SOURCE201} %{buildroot}%{qdir}/bin/qmail-remote.new

### MR -- for replace sendmail-wrapper to sendmail
install -m755 %{SOURCE300} %{buildroot}%{qdir}/bin/sendmail-wrapper

mv -f %{buildroot}%{qdir}/bin/sendmail %{buildroot}%{qdir}/bin/sendmail-qmail

# configure qmail /var/qmail/control/*
#-------------------------------------------------------------------------------
touch %{buildroot}%{qdir}/control/smtproutes
touch %{buildroot}%{qdir}/control/policy

pushd %{buildroot}%{qdir}/control
  touch defaultdomain me plusdomain rcpthosts defaulthost
  echo "localhost" > locals
  echo "60" > concurrencyremote
  echo "100" > concurrencyincoming
  echo "20971520" > databytes
  echo "1000000" > logsize
  echo "100" > logcount
  echo "86400" > queuelifetime
  echo "3" > spfbehavior
  echo "Welcome to Qmail Toaster Ver. %{bversion} SMTP Server" > smtpgreeting
  echo "-r zen.spamhaus.org" > blacklists
  chmod 644 *
popd

# Make users dir and files
#-------------------------------------------------------------------------------
pushd %{buildroot}%{qdir}/users
  touch assign cdb
  chmod 644 *
  echo "." > assign
popd

# sendmail compatability and qmailctl links
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}

pushd %{buildroot}%{_sbindir}
  ln -s ../..%{qdir}/bin/sendmail sendmail
popd
pushd %{buildroot}%{_libdir}
  ln -s ../..%{qdir}/bin/sendmail sendmail
popd
pushd %{buildroot}%{_bindir}
  ln -s ../..%{_initpath}/qmail qmailctl
popd

pushd %{buildroot}%{qdir}/bin
  ln -sf sendmail-wrapper sendmail
popd

# Make supervise
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{qdir}/supervise/send/log
mkdir -p %{buildroot}%{qdir}/supervise/smtp/log
mkdir -p %{buildroot}%{qdir}/supervise/submission/log
mkdir -p %{buildroot}%{qdir}/supervise/pop3/log
mkdir -p %{buildroot}%{qdir}/supervise/smtp-ssl/log

install -m700 %{SOURCE5} %{buildroot}%{qdir}/supervise/pop3/run
install -m700 %{SOURCE6} %{buildroot}%{qdir}/supervise/pop3/log/run
install -m700 %{SOURCE7} %{buildroot}%{qdir}/supervise/send/run
install -m700 %{SOURCE8} %{buildroot}%{qdir}/supervise/send/log/run
install -m700 %{SOURCE9} %{buildroot}%{qdir}/supervise/smtp/run
install -m700 %{SOURCE10} %{buildroot}%{qdir}/supervise/smtp/log/run
install -m700 %{SOURCE19} %{buildroot}%{qdir}/supervise/submission/run
install -m700 %{SOURCE20} %{buildroot}%{qdir}/supervise/submission/log/run
install -m700 %{SOURCE100} %{buildroot}%{qdir}/supervise/smtp-ssl/run
install -m700 %{SOURCE101} %{buildroot}%{qdir}/supervise/smtp-ssl/log/run

install -m644 %{SOURCE12} %{buildroot}%{qdir}/control/badmimetypes
install -m644 %{SOURCE13} %{buildroot}%{qdir}/control/badloadertypes
install -m644 %{SOURCE14} %{buildroot}%{qdir}/control/badmailfrom
install -m644 %{SOURCE15} %{buildroot}%{qdir}/control/badmailto
install -m755 %{SOURCE16} %{buildroot}%{qdir}/bin/dh_key
install -m644 %{SOURCE17} %{buildroot}%{qdir}/control/defaultdelivery

# Make /etc/tcprules.d/qmail-smtp
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sysconfdir}/tcprules.d

# Setup default /etc/tcprules.d/qmail-smtp
#-------------------------------------------------------------------------------
cat <<EOFqmail-smtp >%{buildroot}%{_sysconfdir}/tcprules.d/tcp.smtp
127.:allow,RELAYCLIENT="",DKSIGN="/var/qmail/control/domainkeys/%/private"
:allow,BADMIMETYPE="",BADLOADERTYPE="M",CHKUSER_RCPTLIMIT="50",CHKUSER_WRONGRCPTLIMIT="10",DKSIGN="/var/qmail/control/domainkeys/%/private"
EOFqmail-smtp

# Make skel dirs
#-------------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sysconfdir}/skel/Maildir/{cur,new,tmp}
echo "./Maildir/" > %{buildroot}%{_sysconfdir}/skel/.qmail

find %{buildroot}%{qdir}/man -type f -exec bzip2 -9f {} \;

# Build TLS certificate
#-------------------------------------------------------------------------------
cat %{SOURCE11} > ./makecert.sh
chmod +x ./makecert.sh
yes "" | ./makecert.sh
cat ./server.crt ./server.key > %{buildroot}%{qdir}/control/servercert.pem
rm -rf ./server.crt ./server.key
 
pushd %{buildroot}%{qdir}/control
  ln -s servercert.pem clientcert.pem
popd


#-------------------------------------------------------------------------------
%pre
#-------------------------------------------------------------------------------

# Add users and groups as per Life With Qmail
#-------------------------------------------------------------------------------
echo " Adding qmailtoaster users and groups."
if [ -z "`/usr/bin/id -g nofiles 2>/dev/null`" ]; then
	/usr/sbin/groupadd -g 2107 -r nofiles 2>&1 || :
fi
if [ -z "`/usr/bin/id -g qmail 2>/dev/null`" ]; then	
	/usr/sbin/groupadd -g 2108 -r qmail 2>&1 || :
fi

if [ -z "`/usr/bin/id -u alias 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7790 -r -M -d %{qdir}/alias -s /sbin/nologin -c "qmail alias" -g qmail alias  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmaild 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7791 -r -M -d %{qdir} -s /sbin/nologin -c "qmail daemon" -g qmail qmaild  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmaill 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7792 -r -M -d %{qdir} -s /sbin/nologin -c "qmail logger" -g qmail qmaill  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailp 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7793 -r -M -d %{qdir} -s /sbin/nologin -c "qmail passwd" -g qmail qmailp  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailq 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7794 -r -M -d %{qdir} -s /sbin/nologin -c "qmail queue" -g qmail qmailq  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmailr 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7795 -r -M -d %{qdir} -s /sbin/nologin -c "qmail remote" -g qmail qmailr  2>&1 || :
fi
if [ -z "`/usr/bin/id -u qmails 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 7796 -r -M -d %{qdir} -s /sbin/nologin -c "qmail send" -g qmail qmails  2>&1 || :
fi

if [ -f /tmp/qmail/var/qmail/control/tlshosts/exhaustivelist ]; then
	rm -rf /tmp/qmail/var/qmail/control/tlshosts/exhaustivelist
fi

#we may need this to have access to /home/vpopmail/include/ 
#if [ ! -z "`/usr/bin/id -g vchkpw 2>/dev/null`" ]; then
#	/usr/sbin/adduser qmail vchkpw 2>&1   || :
#fi

#-------------------------------------------------------------------------------
%preun
#-------------------------------------------------------------------------------

if [ "$1" = 0 ]; then

# Make qmail stop
chkconfig --del qmail

# Remove users and groups
userdel alias 2> /dev/null
userdel qmaild 2> /dev/null
userdel qmaill 2> /dev/null
userdel qmailp 2> /dev/null
userdel qmailq 2> /dev/null
userdel qmailr 2> /dev/null
userdel qmails 2> /dev/null
groupdel nofiles 2> /dev/null
groupdel qmail 2> /dev/null	
echo " Removing qmail-toaster users and groups."

# Remove cron job
grep -v ' * * * root %{qdir}/bin/dh_key' %{crontab} > %{crontab}.new
mv -f %{crontab}.new %{crontab}
echo " Removing TLS key cron job."

# Remove qmail man path
if [ -f /etc/man.config ]; then
  grep -v 'MANPATH  /var/qmail/man' /etc/man.config > /etc/man.config.new
  mv -f /etc/man.config.new /etc/man.config
  echo " Removing qmail-toaster from MANPATH."
fi

fi


#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

#mv -f %{qdir}/bin/qmail-queue %{qdir}/bin/qmail-queue.orig
#ln -s %{qdir}/bin/qmail-dk %{qdir}/bin/qmail-queue
#chmod 4711 %{qdir}/bin/qmail-queue.orig

if [ -f %{_bindir}/dkimsign.pl ] ; then
	rm -f %{_bindir}/dkimsign.pl
fi

ln -s %{qdir}/bin/dkimsign.pl %{_bindir}/dkimsign.pl

if [ -f %{qdir}/bin/qmail-queue.orig ] ; then
	### MR -- re-use 'old' qmail-queue
	rm -f %{qdir}/bin/qmail-queue
	mv -f %{qdir}/bin/qmail-queue.orig %{qdir}/bin/qmail-queue
fi

mv -f %{qdir}/bin/qmail-remote %{qdir}/bin/qmail-remote.orig
mv -f %{qdir}/bin/qmail-remote.new %{qdir}/bin/qmail-remote

if [ $1 = "1" ]; then

# Get hostname and parse it for following operations
#-------------------------------------------------------------------------------
defaultHost=`hostname -s`
defaultHostname=`hostname -f`
defaultDomain=`hostname -f | perl -ne "s/.*\.([a-z0-9-]+\.[a-z]+)$/\1/i;" -e "print lc"`

echo $defaultHostname > %{qdir}/control/me

#echo $defaultDomain > %{qdir}/control/defaultdomain
#echo $defaultDomain > %{qdir}/control/defaulthost
#echo $defaultDomain > %{qdir}/control/plusdomain

echo $defaultHostname > %{qdir}/control/defaultdomain
echo $defaultHostname > %{qdir}/control/defaulthost
echo $defaultHostname > %{qdir}/control/plusdomain

echo $defaultHostname >> %{qdir}/control/rcpthosts
echo $defaultHostname >> %{qdir}/control/locals
echo "$defaultHostname - Welcome to Qmail Toaster Ver. %{bversion} SMTP Server" > %{qdir}/control/smtpgreeting

# Make postmaster the default address for aliases
#-------------------------------------------------------------------------------
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-postmaster
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-mailer-daemon
echo "&postmaster@$defaultDomain"	> %{qdir}/alias/.qmail-root
chown alias:nofiles %{qdir}/alias/.qmail*
chmod 644 %{qdir}/alias/.qmail*

# Compile default tcp.smtp
#-------------------------------------------------------------------------------
  if [ -f /usr/bin/tcprules ]; then
    echo "Compiling default cdb files in %{_sysconfdir}/tcprules.d..."
    %{_sysconfdir}/rc.d/init.d/qmail cdb
  fi

fi

# Add qmail man dir to man path
#-------------------------------------------------------------------------------
if [ -f /etc/man.config ]; then
   if ! grep 'MANPATH  /var/qmail/man' /etc/man.config > /dev/null; then
     echo " Adding qmail-toaster to MANPATH."
     echo "MANPATH  /var/qmail/man" >> /etc/man.config
   fi
fi

# Install cron-job to keep temp keys current
#-------------------------------------------------------------------------------
if ! grep ' * * * root %{qdir}/bin/dh_key' %{crontab} > /dev/null; then
  echo " Adding cron job for TLS keys."
  echo "" >> %{crontab}
  echo "01 01 * * * root %{qdir}/bin/dh_key 2>&1 > /dev/null" >> %{crontab}
fi

# Create queue/lock/trigger, but only if not installing in a sandbox
# This is necessary because fuse-unionfs does not (yet) support fifo files.
#-------------------------------------------------------------------------------
if [ ! -f /boot/.qtp-sandbox ]; then
  echo " Creating queue/lock/trigger named pipe."
  rm -f %{qdir}/queue/lock/trigger
  mkfifo -m 0622 %{qdir}/queue/lock/trigger
  chown qmails:qmail %{qdir}/queue/lock/trigger
else
  echo " NOT Creating queue/lock/trigger named pipe."
fi

./%{qdir}/bin/qmail-badmimetypes
echo " Compiling badmimetypes."
./%{qdir}/bin/qmail-badloadertypes
echo " Compiling badloadertypes."

touch %{qdir}/control/tlsserverciphers
rm -fr %{qdir}/control/tlsclientciphers 2>&1 > /dev/null
echo " Making tlsserverciphers."
./%{_bindir}/openssl ciphers > %{qdir}/control/tlsserverciphers
chown root:qmail %{qdir}/control/tlsserverciphers
chmod 644 %{qdir}/control/tlsserverciphers

echo " Linking tlsserverciphers to tlsclientciphers."
ln -s %{qdir}/control/tlsserverciphers %{qdir}/control/tlsclientciphers

echo " Making dh_keys."
./%{qdir}/bin/dh_key

# Make start
chkconfig --add qmail
chkconfig qmail on

if [ "$(id -g postfix|grep postfix)" != "" ] ; then
  groupdel postfix
fi

if [ "$(id -u postfix|grep postfix)" != "" ] ; then
  userdel postfix
fi

if [ "$(id -g vchkpw|grep vchkpw)" != "" ] ; then
  groupadd -g 89 vchkpw
fi

if [ "$(id -u vpopmail|grep vpopmail)" != "" ] ; then
  useradd -u 89 -g 89 vpopmail -s '/sbin/nologin'
fi


#-------------------------------------------------------------------------------
%postun
#-------------------------------------------------------------------------------

if [ "$1" = 0 ]; then
 rm -f  /var/qmail/control/*.cdb
 rm -fR %{qdir}/supervise/send/
 rm -fR %{qdir}/supervise/smtp/
 rm -fR %{qdir}/supervise/pop3/
 rm -fR %{qdir}/supervise/smtp-ssl/
 rm -fR /var/log/qmail/send/
 rm -fR /var/log/qmail/smtp/
 rm -fR /var/log/qmail/pop3/
 rm -fR /var/log/qmail/smtp-ssl/
fi

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------

%defattr(-,-,qmail)
# /usr/bin
# /var/qmail/bin

# config (system)
#-------------------------------------------------------------------------------
%attr(0755,root,root) %config(noreplace) %{_initpath}/qmail
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tcprules.d/tcp.smtp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/skel/.qmail

# directories
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %dir %{qdir}
%attr(2755,alias,qmail) %dir %{qdir}/alias
%attr(0755,root,qmail) %dir %{qdir}/bin
%attr(0755,root,qmail) %dir %{qdir}/boot
%attr(0755,root,qmail) %dir %{qdir}/control
%attr(0755,root,qmail) %dir %{qdir}/control/domainkeys
%attr(0755,root,qmail) %dir %{qdir}/control/tlshosts
%attr(0755,root,qmail) %dir %{qdir}/control/tlshosts/exhaustivelist
%attr(0755,root,qmail) %dir %{qdir}/doc
%attr(0755,root,qmail) %dir %{qdir}/man
%attr(0755,root,qmail) %dir %{qdir}/man/cat1
%attr(0755,root,qmail) %dir %{qdir}/man/cat5
%attr(0755,root,qmail) %dir %{qdir}/man/cat7
%attr(0755,root,qmail) %dir %{qdir}/man/cat8
%attr(0755,root,qmail) %dir %{qdir}/man/man1
%attr(0755,root,qmail) %dir %{qdir}/man/man5
%attr(0755,root,qmail) %dir %{qdir}/man/man7
%attr(0755,root,qmail) %dir %{qdir}/man/man8
%attr(0750,qmailq,qmail) %dir %{qdir}/queue

%attr(0700,qmaill,qmail) %dir %{qdir}/supervise
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/send
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/send/log
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/send/supervise
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/smtp
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/smtp/log
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/smtp/supervise
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/submission
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/submission/log
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/submission/supervise
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/smtp-ssl
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/smtp-ssl/log
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/smtp-ssl/supervise

%attr(0755,root,qmail) %dir %{qdir}/users
%attr(0750,qmaill,qmail) %dir /var/log/qmail
%attr(0750,qmaill,qmail) %dir /var/log/qmail/smtp
%attr(0750,qmaill,qmail) %dir /var/log/qmail/send
%attr(0750,qmaill,qmail) %dir /var/log/qmail/smtp-ssl
%attr(0750,qmaill,qmail) %dir /var/log/qmail/submission

%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/cur
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/new
%attr(0755,root,root) %dir %{_sysconfdir}/skel/Maildir/tmp

# config (qmail)
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/badloadertypes
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/badmimetypes
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/badmailfrom
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/badmailto
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/blacklists
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencyincoming
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/concurrencyremote
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/databytes
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/defaultdelivery
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/defaultdomain
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/defaulthost
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/locals
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/logcount
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/logsize
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/plusdomain
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/queuelifetime
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/rcpthosts
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/servercert.pem
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/smtpgreeting
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/smtproutes
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/spfbehavior
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/me
%attr(0644,root,qmail) %config(noreplace) %{qdir}/control/policy
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/assign
%attr(0644,root,qmail) %config(noreplace) %{qdir}/users/cdb
%attr(0755,root,qmail) %{qdir}/rc

# symlinks (sendmail & domainkeys)
#-------------------------------------------------------------------------------
%attr(-,root,qmail) %{_libdir}/sendmail
%attr(-,root,qmail) %{_sbindir}/sendmail
%attr(-,root,qmail) %{_bindir}/qmailctl
%attr(-,root,qmail) %{qdir}/control/clientcert.pem
#%attr(-,root,qmail) %{qdir}/bin/qmail-queue

# supervise
#-------------------------------------------------------------------------------
%attr(0751,qmaill,qmail) %{qdir}/supervise/send/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/send/log/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/smtp/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/smtp/log/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/submission/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/submission/log/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/smtp-ssl/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/smtp-ssl/log/run

# cat pages
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qdir}/man/cat1/*
%attr(0644,root,qmail) %{qdir}/man/cat5/*
%attr(0644,root,qmail) %{qdir}/man/cat7/*
%attr(0644,root,qmail) %{qdir}/man/cat8/*

# qmail queue
#-------------------------------------------------------------------------------
%attr(0700,qmails,qmail) %dir %{qdir}/queue/bounce
%attr(0700,qmails,qmail) %dir %{qdir}/queue/info
%attr(0700,qmails,qmail) %{qdir}/queue/info/*
%attr(0700,qmailq,qmail) %dir %{qdir}/queue/intd
%attr(0700,qmails,qmail) %dir %{qdir}/queue/local
%attr(0700,qmails,qmail) %{qdir}/queue/local/*
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/lock
%attr(0600,qmails,qmail) %{qdir}/queue/lock/sendmutex
%attr(0644,qmailr,qmail) %{qdir}/queue/lock/tcpto
%attr(-,qmails,qmail) %{qdir}/queue/lock/trigger
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/mess
%attr(0750,qmailq,qmail) %{qdir}/queue/mess/*
%attr(0700,qmailq,qmail) %dir %{qdir}/queue/pid
%attr(0700,qmails,qmail) %dir %{qdir}/queue/remote
%attr(0700,qmails,qmail) %{qdir}/queue/remote/*
%attr(0750,qmailq,qmail) %dir %{qdir}/queue/todo

# boot files
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %{qdir}/boot/home
%attr(0755,root,qmail) %{qdir}/boot/home+df
%attr(0755,root,qmail) %{qdir}/boot/binm1
%attr(0755,root,qmail) %{qdir}/boot/binm2+df
%attr(0755,root,qmail) %{qdir}/boot/proc+df
%attr(0755,root,qmail) %{qdir}/boot/binm2
%attr(0755,root,qmail) %{qdir}/boot/binm3
%attr(0755,root,qmail) %{qdir}/boot/proc
%attr(0755,root,qmail) %{qdir}/boot/binm3+df
%attr(0755,root,qmail) %{qdir}/boot/binm1+df

# binaries/bin
#-------------------------------------------------------------------------------
%attr(0755,root,qmail) %{qdir}/bin/bouncesaying
%attr(0755,root,qmail) %{qdir}/bin/condredirect
%attr(0755,root,qmail) %{qdir}/bin/config-fast
%attr(0755,root,qmail) %{qdir}/bin/datemail
%attr(0755,root,qmail) %{qdir}/bin/dh_key
%attr(0755,root,qmail) %{qdir}/bin/elq
%attr(0755,root,qmail) %{qdir}/bin/except
%attr(0755,root,qmail) %{qdir}/bin/forward
%attr(0755,root,qmail) %{qdir}/bin/instcheck
%attr(0755,root,qmail) %{qdir}/bin/maildir2mbox
%attr(0755,root,qmail) %{qdir}/bin/maildirmake
%attr(0755,root,qmail) %{qdir}/bin/maildirwatch
%attr(0755,root,qmail) %{qdir}/bin/mailsubj
%attr(0755,root,qmail) %{qdir}/bin/pinq
%attr(0755,root,qmail) %{qdir}/bin/predate
%attr(0755,root,qmail) %{qdir}/bin/preline
%attr(0755,root,qmail) %{qdir}/bin/qail
%attr(0755,root,qmail) %{qdir}/bin/qbiff
%attr(0755,root,qmail) %{qdir}/bin/qmail-badloadertypes
%attr(0755,root,qmail) %{qdir}/bin/qmail-badmimetypes
%attr(0711,root,qmail) %{qdir}/bin/qmail-clean
%attr(04711,qmailq,qmail) %{qdir}/bin/qmail-dk
%attr(0711,root,qmail) %{qdir}/bin/qmail-getpw
%attr(0755,root,qmail) %{qdir}/bin/qmail-inject
%attr(0711,root,qmail) %{qdir}/bin/qmail-local
%attr(0700,root,qmail) %{qdir}/bin/qmail-lspawn
%attr(0700,root,qmail) %{qdir}/bin/qmail-newmrh
%attr(0700,root,qmail) %{qdir}/bin/qmail-newu
%attr(0711,root,qmail) %{qdir}/bin/qmail-pw2u
%attr(0755,root,qmail) %{qdir}/bin/qmail-qread
%attr(0755,root,qmail) %{qdir}/bin/qmail-qstat
%attr(04711,qmailq,qmail) %{qdir}/bin/qmail-queue
%attr(0711,root,qmail) %{qdir}/bin/qmail-remote
%attr(0711,root,qmail) %{qdir}/bin/qmail-rspawn
%attr(0711,root,qmail) %{qdir}/bin/qmail-send
%attr(0755,root,qmail) %{qdir}/bin/qmail-showctl
%attr(0755,root,qmail) %{qdir}/bin/qmail-smtpd
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmqpc
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmqpd
%attr(0755,root,qmail) %{qdir}/bin/qmail-qmtpd
%attr(0700,root,qmail) %{qdir}/bin/qmail-start
%attr(0755,root,qmail) %{qdir}/bin/qmail-tcpok
%attr(0755,root,qmail) %{qdir}/bin/qmail-tcpto
%attr(0755,root,qmail) %{qdir}/bin/qreceipt
%attr(0755,root,qmail) %{qdir}/bin/qsmhook
%attr(0755,root,qmail) %{qdir}/bin/sendmail
%attr(0755,root,qmail) %{qdir}/bin/spfquery
%attr(0755,root,qmail) %{qdir}/bin/srsfilter
%attr(0711,root,qmail) %{qdir}/bin/splogger
%attr(0755,root,qmail) %{qdir}/bin/tcp-env

%attr(0755,root,root) %{qdir}/bin/dkimsign.pl
%attr(0755,root,qmail) %{qdir}/bin/qmail-remote.new

%attr(0755,root,qmail) %{qdir}/bin/sendmail-qmail
%attr(0755,root,qmail) %{qdir}/bin/sendmail-wrapper

# man pages
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qdir}/man/man1/qreceipt.1*
%attr(0644,root,qmail) %{qdir}/man/man1/condredirect.1*
%attr(0644,root,qmail) %{qdir}/man/man1/mailsubj.1*
%attr(0644,root,qmail) %{qdir}/man/man1/except.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildirmake.1*
%attr(0644,root,qmail) %{qdir}/man/man1/preline.1*
%attr(0644,root,qmail) %{qdir}/man/man1/tcp-env.1*
%attr(0644,root,qmail) %{qdir}/man/man1/bouncesaying.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildir2mbox.1*
%attr(0644,root,qmail) %{qdir}/man/man1/qbiff.1*
%attr(0644,root,qmail) %{qdir}/man/man1/forward.1*
%attr(0644,root,qmail) %{qdir}/man/man1/maildirwatch.1*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-users.5*
%attr(0644,root,qmail) %{qdir}/man/man5/maildir.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-header.5*
%attr(0644,root,qmail) %{qdir}/man/man5/envelopes.5*
%attr(0644,root,qmail) %{qdir}/man/man5/mbox.5*
%attr(0644,root,qmail) %{qdir}/man/man5/tcp-environ.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-control.5*
%attr(0644,root,qmail) %{qdir}/man/man5/qmail-log.5*
%attr(0644,root,qmail) %{qdir}/man/man5/addresses.5*
%attr(0644,root,qmail) %{qdir}/man/man5/dot-qmail.5*
%attr(0644,root,qmail) %{qdir}/man/man7/qmail-limits.7*
%attr(0644,root,qmail) %{qdir}/man/man7/forgeries.7*
%attr(0644,root,qmail) %{qdir}/man/man7/qmail.7*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-badloadertypes.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-badmimetypes.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-dk.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-tcpto.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qread.8*
%attr(0644,root,qmail) %{qdir}/man/man8/splogger.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-start.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmqpc.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmqpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qmtpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-newu.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-tcpok.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-inject.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-clean.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-getpw.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-command.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-showctl.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-rspawn.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-smtpd.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-qstat.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-pw2u.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-queue.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-popup.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-lspawn.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-newmrh.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-local.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-send.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-remote.8*
%attr(0644,root,qmail) %{qdir}/man/man8/qmail-pop3d.8*

# qmail docs
#-------------------------------------------------------------------------------
%attr(0644,root,qmail) %{qdir}/doc/*

# qmail-pop3d
#-------------------------------------------------------------------------------
%files -n qmail-pop3d-toaster
%defattr(-,-,qmail)
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/pop3
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/pop3/log
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/pop3/supervise
%attr(0751,qmaill,qmail) %{qdir}/supervise/pop3/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/pop3/log/run
%attr(0750,qmaill,qmail) %dir /var/log/qmail/pop3
%attr(0755,root,qmail) %{qdir}/bin/qmail-pop3d
%attr(0711,root,qmail) %{qdir}/bin/qmail-popup


#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Thu Jul 27 2017 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.57.mr
- recompile without atomic repo

* Wed Apr 12 2017 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.56.mr
- add qmail_qmailtoaster-any-to-cname.patch

* Sun May 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.55.mr
- remove change IP in smtp/smtp-ssl/submission because wrong and use outgoingips as alternative

* Sat May 02 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.54.mr
- fix outgoingips patch
- add outgoingip patch (just for archive; may conflict with outgoingips patch)

* Tue Apr 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.53.mr
- replace sendmail-wrapper file

* Tue Apr 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.52.mr
- possible execute other script from sendmail-wrapper

* Wed Apr 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.51.mr
- mod sendmail-wrapper to possible ban for subdir under pwd

* Sun Apr 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.50.mr
- possible set ip and hostname for smtp, smtp-ssl and submission

* Sat Mar 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.49.mr
- change from Conflicts to Obsoletes for postfix, exim, sendmail, ssmtp, smail

* Sun Mar 22 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.48.mr
- fix sendmail-wrapper

* Tue Mar 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.47.mr
- fix sendmail-wrapper (wrong compare to pwd)

* Thu Jan 29 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.46.mr
- modified sendmail-wrapper to make possible ban certain website

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.45.mr
- cleanup spec based on toaster github (without define like build_cnt_60)
- rename ougoingips to outgoingip

* Thu Dec 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.44.mr
- mod/fix sendmail-wrapper

* Sat Dec 13 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.43.mr
- mod sendmail-wrapper

* Thu Dec 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.41.mr
- add sendmail-wrapper for find out php mail() caller

* Fri Nov 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.40.mr
- add vpopmail-devel.patch qmail-uids.patch and qmail-outgoingips.patch

* Wed Oct 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.39.mr
- disable sslv2 and sslv3

* Mon Mar 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.38.mr
- back to use .34 because have a trouble if using .36/.37 based
- hostname for defaultdomain/defaulthost/plusdomain
- mod qmail run for smtp/smtp-ssl/submission for with/-out soflimit and spamdyke 5.x

* Wed Jan 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.34.mr
- fix issue related to dkimsign.pl and qmail-remote.new (again)

* Wed Jan 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.33.mr
- fix issue related to dkimsign.pl and qmail-remote.new

* Mon Jan 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.32.mr
- add dkimsign.pl and qmail-remote.new

* Fri Jan 17 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.31.mr
- add norecordio in control will be disable recordio

* Thu Jan 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.30.mr
- fix conflict if spamdyke together with rblsmtpd

* Tue Dec 10 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.29.mr
- fix control/tlshosts/exhaustivelist from file to directory

* Mon Dec 9 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.28.mr
- using text instead their .bz2
- mod run for smtp/smtp-ssl/submission for spamdyke/rblsmtpd
- add control/tlshosts/exhaustivelist for handle tls issue (error:140943FC)

* Thu Jul 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.27.mr
- change BuildPreReq to BuildRequires (centos 6 deprecated issue)
- don't install mysql*-libs because make conflict between mysql branch!

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.26.mr
- update run and log run script

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.25.mr
- increase softlimit because have trouble with current value on Centos 6 64bit

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.24.mr
- enable again softlimit 'rule' (for 32bit vs 64bit)

* Thu Jun 13 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.23.mr
- add smtp-ssl (port 465) and modified run and log run script

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.03-1.3.22.mr
- add build_cnt_60 and build_cnt_6064

* Thu Mar 08 2012 Eric Shubert <ejs@shubes.net> 1.03-1.3.22
- Reverted chkuser to enable user extensions
- Modified chkuser to enable mailman extensions
* Thu Feb 24 2011 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.21
- Updated chkuser to 2.0.9
- Re-diff'ed the patch file
- enabled ALL extra allow chars in addresses
- Disabled rcpt MX address checking
* Wed Sep 30 2009 Eric Shubert <ejs@shubes.net> 1.03-1.3.20
- Fixed problem with named pipe not being contained in package list
* Mon Aug 17 2009 Eric Shubert <ejs@shubes.net> 1.03-1.3.19
- Modified to not create named pipe when installed in a sandbox
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.18
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Tue Jun 02 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.18
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.17
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Increased softlimits for x86_64 distros
- Added eMPF patch to the package
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.16
- Added Suse 11.1 support
* Sun Feb 08 2009 Jake Vickers <jake@qmailtoaster.com> 1.03-1.3.16
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.15
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Fri Feb 23 2007 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.14
- Adapt qmail-103 big dns patch for qmailtoaster - qmailtoaster-big-dns.patch
- Added qmail-smtpd-linefeed.patch thanks to Jean-Paul van de Plasse
* Wed Jan 31 2007 Jean-Paul van de Plasse <jeanpaul@i-serve.nl> 1.03-1.3.13
- Fixed an error in the supervise submission run script
* Fri Jan 12 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.12
- Upgraded to SRS Patch 0.5. Fixed for gcc 4.x and above
* Thu Jan 11 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.11
- Upgraded to SRS Patch 0.4. No longer optional.
- Changed default blacklist to zen.spamhaus.org from sbl.spamhaus.org
* Mon Jan 08 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.10
- Added SRS Patch, must --define 'srs 1' during compile
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.03-1.3.9
- Added various logging patches from Alexey Loukianov
* Wed Nov 08 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.8
- Added REQUIRE_AUTH patch, thanks to Jean-Paul van de Plasse
- Enabled Submission port 587.
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.7
- Added Fedora Core 6 support
* Sat Sep 09 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.6
- Commented out everything in badmimetypes/badloadertypes
- Fixed bug in qmailctl (cont had smtpd instead of smtp)
* Sat Jul 08 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.5
- Enabled "*" and "$" in chkuser for mailing list support
* Sun Jul 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.03-1.3.4
- Enabled SRS support in chkuser_settings.h
- Disabled MyDoom sig in badmimetypes
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.3
- Correct badmailfrom patterns - Thanks to Paul Oehler
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.2
- Testing complete and found to be stable
- Add Fedora Core 5 support
* Sun Apr 30 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.3.1
- Totally new test project
- Build-01
- This build is patched only to net-qmail-1.05 with
- TLS, smtp-auth, qmail-remote-auth and qmregex 
- Build-02
- Add chkuser 2.0.8b
- Build-03
- Add netqmail-maildir++
- Build-04
- fix chkuser-2.0 to tarpit and check for valid sender MX record
- Build-05
- Add custom-smtp-reject, oversize-dns, big-concurrency 
- Build-06
- Add warlock-1.3.11
- Build-07
- Add qmail-spf-rc5
- Build-08
- Add qmail-dk-0.54 domainkeys and qmail-dk-0.54-auth
- Build-09
- Add qmail-tap-1.1
- Build-10
- Move qmail-queue to qmail-queue.orig
- Configure qmail-dk link to qmail-queue
* Wed Apr 28 2006 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.11
- Add qmailtoaster-1.2.1.patch
- See description for a list of applied patches
- Fixed MTA provides for distros
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.10
- Add SuSE 10.0 and Mandriva 2006.0 support
- Add chkconfig support
* Fri Oct 14 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.8
- Add CentOS 4 x86_64 support
* Wed Jun 29 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.7
- Add Fedora Core 4 support
* Sun Jun 19 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.6
- Update patches - add qmail-tap ver 2
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.03-1.2.5
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Add Obsoletes:	qmail-toaster-doc 
* Thu May 25 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.4
- Update patches - add SPF, chkuser 2.0, spamthrottle, Warlord
- filtering
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.3
- Add Fedora Core 3 support
- Add CentOS 4 support
* Wed Jun 02 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.2
- Add Fedora Core 2 support
* Mon Apr 19 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.2.1
- patch to netqmail-1.05
- Update patches - add qmail-smtpd-virusscan
- Change methods for creating groups and users
- Cleanup runlevel s-links
- Remove cron job with preun
* Sun Feb 22 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.15
- Make dh and rsa temp key cron job silent
- Set default mfcheck = 1
* Sun Feb 15 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.14
- Add dh and rsa temp keys
- Add cron job for temp keys
* Fri Jan 23 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.13
- Fix qmail-remote for TLS and add patch list to description
- Set softlimits
* Thu Jan 08 2004 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.12
- Add Trustix 2.0 support
- Add Fedora Core 1 support
- New TLS and SMTP-AUTH patch that works with RedHat and Fedora
* Sat Nov 29 2003 Nick Hemmesch <nick@ndhsoft.com. 1.03-1.0.11
- Fixed overmaildirquota.c - will work on new patches later aaarg :(
* Fri Nov 28 2003 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.10
- Bad build with big patch and chkuser - revertet back with fixes
* Wed May 27 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.9
- Build self-signed certificate for TLS
* Sat Apr 26 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.8
- Clean-ups on SPEC file: compilation banner, better gcc detects
- Detect gcc-3.2.3
- Fixed permission on supervise dirs (rare bug with high msec security)
- Revisited spamcontrol patch (http://www.ltn.net/enrique)
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
* Wed Apr 02 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.7
- Clean-ups
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.6
- Conectiva Linux 7.0 support
- Big DNS patch (was missing???)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 1.03-1.0.5
- Support for Red Hat 8.0
* Sun Feb 09 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.4
- Fixed SMTP-AUTH (smtp run script call vpopmail user)
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.3
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Fri Jan 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.2
- Fixed bugs in RPM macros, but we need to improve them to support a large
  number of RPM based OS.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1.0.1
- Added new daemons qmail-qmqpc, qmail-qmqpd, qmail-qmtpd. Maybe in future we
  will use it.
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-0.9.2
- TLS patch
- qmail-queue patch
- qmail-pop3d maildir++ quota support
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
- Packages are named with their proper releases and bversion is from now
  part of the rpm release: we will continue upgrading safely.
- Better macros in post unistall
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.03-2
- New set of patches
* Mon Sep 23 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.03-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
- Clean-ups
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-5
- In supervise script now using tcpserver with -R flag: Do not attempt
  to obtain $TCPREMOTEINFO from  the  remote  host.
  This speeds up connections from hosts behind misconfigured firewalls
  with port 113 (identd) closed - that are really really a lot -.
- Full support for smtp over SSL.
* Wed Sep 04 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-4
- Fixed hostname in pop3 tcpserver script
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-3
- Deleted Mandrake Release Autodetection (creates problems)
* Wed Aug 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-2
- Fixed init.d restart option
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.03-1
- New version: 0.7 toaster.
- All sources are now bz2 compressed.
- Auth working 100%
- Better macros to detect Mandrake Release
- Minor clean-ups.
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.1.03-1
- New version: 0.6 toaster./bin/qmail-newu
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.1.03-1
- Doc package is standalone (someone does not ask for man pages)
- Checks for gcc-3.2 (default compiler from now)
- New version: 0.5 toaster.
* Tue Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.1.03-1
- Rebuild against 0.4 toaster
- Revisited instructions after installed the rpm
* Tue Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03-3
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
* Mon Jul 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03.2mdk
- Added bettere controls in supervise/smtp/run
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.03.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-1.03.1mdk
- toaster v. 0.2 (rebuild against ucspi-tcp-toaster v. 0.2)
- More controls on users creation/deletion
- Added /var/qmail/control/blacklists to add anti UCE
- Added controls in supervise/smtp/run to accept mail ONLY from hosts
  with reverse IP (anti-spam rule)
- Added some instructions in post installation
* Mon Jul 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.03.5mdk
- Tested the part that creates qmail users (for RedHat users): we use
  useradd -r flag to create systems account. That is, an user with an
  UID  lower  than  value  of UID_MIN defined in /etc/login.defs
- Some clean-ups
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.03.4mdk
- Added tests for gcc-3.1.1
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
- Deleted all Mandrake dependencies as mandrake-release and so on...
- Deleted chkconfig work (some people told me on RedHat failed) and added
  soft links.
- Added SMTP greatings with toaster banner.
* Wed Jul 10 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-3mdk
- Corrected /var/qmail/assign file (had to have a "." in it)
- Added stuff to create qmail users and groups (people seems not
  to like Mandrake: so we need to be able to create users and groups).
- Better tuning on supervise (adjusted softlimit to 3200000)
- Complete integration (and dependecing) from qmail-pop3d and vpopmail
* Tue Jul 02 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-2mdk
- Tuned supervise to work as better as possible.
- Changed the package names in toaster (we will build toaster packages)
- Added more /var/qmail/control files (but I know I can do more...)
* Tue Jun 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.03-1mdk
- First RPM package (it is based on the great Vincent Danen's SRPM).
  I hope to do a good job too.
