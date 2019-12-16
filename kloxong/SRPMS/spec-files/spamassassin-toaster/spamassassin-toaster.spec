%define	name spamassassin
%define	pversion 3.4.1
%define 	bversion 1.4
%define	rpmrelease 8.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
BuildRequires:	perl >= 5.8.8, perl-Digest-SHA1, perl-HTTP-Parser, openssl-devel
## MR -- exist in 3.4.0
BuildRequires:	perl-devel, perl-NetAddr-IP, perl-Archive-Tar, perl-Mail-SPF, perl-Time-HiRes
BuildRequires:	perl-Geo-IP, perl-IO-Socket-SSL, perl-Razor-Agent
BuildRequires:	perl-Encode-Detect, perl-Net-Patricia, perl-Digest-SHA
BuildRequires:  perl-DBI, perl-Net-DNS-Nameserver, perl-File-Fetch, perl-Mail-DKIM

Requires:	perl-Digest-SHA1, perl-HTTP-Parser, procmail
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
## MR -- exist in 3.4.0
Requires:	perl-NetAddr-IP, perl-Archive-Tar, perl-Mail-SPF, perl-Razor-Agent
Requires:	perl-Geo-IP, perl-IO-Socket-INET6, perl-IO-Socket-SSL, perl-Digest-SHA 
Requires:	perl-Encode-Detect, perl-Net-Patricia, perl-Time-HiRes, perl-Mail-DKIM
Requires: 	perl-DBI, perl-Net-DNS-Nameserver, perl-File-Fetch, wget

%if %{?fedora}0 > 150 || %{?rhel}0 > 60 
BuildRequires: perl-IO-Socket-IP
Requires: perl-IO-Socket-IP
%endif

%if %{?fedora}0 <= 150 || %{?rhel}0 <= 60 
BuildRequires: rh-perl524-perl-IO-Socket-IP
Requires: rh-perl524-perl-IO-Socket-IP
%endif

%define	ccflags %{optflags}
%define	ldflags %{optflags}



############### RPM ################################

%define	debug_package %{nil}
%define	vtoaster %{pversion}
%define	_use_internal_dependency_generator 0
%define	real_name Mail-SpamAssassin
%define	krb5backcompat %([ -a /usr/include/krb5/krb5.h ] && echo 1 || echo 0)

%{!?perl_vendorlib: %define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)}

%define	builddate Fri Oct 07 2011

Name:		%{name}-toaster
Summary:	Spam filter for email which can be invoked from mail delivery agents.
Version:	%{vtoaster}
Release:	%{release}
License:	Apache License
Group:		Applications/Internet
URL:		http://spamassassin.apache.org/
Source0:	%{name}/%{real_name}-%{version}.tar.bz2
Source1:	qmailtoaster.local.cf.bz2

#Source2:	supervise.spamd.run.bz2
#Source3:	supervise.spamd.log.run.bz2
Source2:	supervise.spamd.run
Source3:	supervise.spamd.log.run

Source4:	qmailtoaster.v310.pre.bz2
Source99:	filter-requires-spamassassin.sh


Buildroot:	%{_tmppath}/%{name}-root
Prefix:	%{_prefix}
Requires:	vpopmail-toaster >= 5.4.17, qmail-toaster, gnupg
Obsoletes:	perl-Mail-SpamAssassin, spamassassin, perl-spamassassin
Packager:       Eric Shubert <eric@datamatters.us>

%define	name spamassassin
%define	__find_requires %{SOURCE99}
%define	qdir /var/qmail

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
SpamAssassin provides you with a way to reduce if not completely eliminate
Unsolicited Commercial Email (SPAM) from your incoming email.  It can
be invoked by a MDA such as sendmail or postfix, or can be called from
a procmail script, .forward file, etc.  It uses a genetic-algorithm
evolved scoring system to identify messages which look spammy, then
adds headers to the message so they can be filtered by the user's mail
reading software.  This distribution includes the spamd/spamc components
which create a server that considerably speeds processing of mail.

v310.pre settings
-----------------------------------------------------------
loadplugin Mail::SpamAssassin::Plugin::Pyzor
loadplugin Mail::SpamAssassin::Plugin::AWL
loadplugin Mail::SpamAssassin::Plugin::AutoLearnThreshold
loadplugin Mail::SpamAssassin::Plugin::WhiteListSubject
loadplugin Mail::SpamAssassin::Plugin::MIMEHeader
loadplugin Mail::SpamAssassin::Plugin::ReplaceTags

The custom local.cf for spamassassin-toaster is as follows:
-----------------------------------------------------------
ok_locales all
skip_rbl_checks 1

required_score 5
report_safe 0
rewrite_header Subject ***SPAM***

use_pyzor 1

use_auto_whitelist 1

use_bayes 1
use_bayes_rules 1
bayes_auto_learn 1


#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q -n Mail-SpamAssassin-%{version}

%{__cat} <<EOF >sa-update.logrotate     ### SOURCE 6
/var/log/sa-update.log {
    monthly
    notifempty
    missingok
}
EOF

%{__cat} <<EOF >sa-update.crontab       ### SOURCE 7
#
# /var/log/sa-update.log contains a history log of sa-update runs
# stdout goes to log only, stderr goes to log and cron output (email errors)

10 4 * * * root /usr/share/spamassassin/sa-update.cron >>/var/log/sa-update.log | tee -a /var/log/sa-update.log
EOF

%{__cat} <<'EOF' >sa-update.cronscript      ### SOURCE 8
#!/bin/bash

sleep $(expr $RANDOM % 7200)
# Only restart spamd if sa-update returns 0, meaning it updated the rules
#/usr/bin/sa-update && /etc/init.d/spamassassin condrestart > /dev/null
#     --channel saupdates.openprotect.com \
/usr/bin/sa-update --gpgkey D1C035168C1EBC08464946DA258CDB3ABDE9DC10 \
      --channel updates.spamassassin.org \
      || exit $?
svc -d /var/qmail/supervise/spamd /var/qmail/supervise/spamd/log
svc -t /var/qmail/supervise/spamd /var/qmail/supervise/spamd/log
svc -u /var/qmail/supervise/spamd /var/qmail/supervise/spamd/log
EOF

# Cleanup for the compiler
#-------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
%{__perl} Makefile.PL DESTDIR=$RPM_BUILD_ROOT/ SYSCONFDIR=%{_sysconfdir} INSTALLDIRS=vendor ENABLE_SSL=yes < /dev/null

%{__make} %{?krb5backcompat:SSLCFLAGS=-DSPAMC_SSL\ -I /usr/include/krb5} OPTIMIZE="$RPM_OPT_FLAGS"


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall PREFIX=%{buildroot}%{prefix} \
	INSTALLMAN1DIR=%{buildroot}%{_mandir}/man1 \
	INSTALLMAN3DIR=%{buildroot}%{_mandir}/man3 \
	LOCAL_RULES_DIR=%{buildroot}/etc/mail/spamassassin
chmod 755 %{buildroot}%{_bindir}/* # allow stripping


[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

find $RPM_BUILD_ROOT/usr -type f -print |
        sed "s@^$RPM_BUILD_ROOT@@g" |
        grep -v perllocal.pod |
        grep -v "\.packlist" > %{name}-%{version}-filelist
if [ "$(cat %{name}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
find $RPM_BUILD_ROOT%{perl_vendorlib}/* -type d -print |
        sed "s@^$RPM_BUILD_ROOT@%dir @g" >> %{name}-%{version}-filelist

rm -f %{buildroot}%{_sysconfdir}/mail/spamassassin/local.cf
rm -f %{buildroot}%{_sysconfdir}/mail/spamassassin/init.pre

%{__install} -Dp -m0644 sa-update.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/sa-update
%{__install} -Dp -m0600 sa-update.crontab %{buildroot}%{_sysconfdir}/cron.d/sa-update
%{__install} -Dp -m0744 sa-update.cronscript %{buildroot}%{_datadir}/spamassassin/sa-update.cron


# Dirs
#-------------------------------------------------------------------------------
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}/etc/cron.hourly
install -d %{buildroot}/etc/mail/spamassassin
install -d %{buildroot}%{qdir}/supervise/spamd
install -d %{buildroot}%{qdir}/supervise/spamd/log
install -d %{buildroot}%{qdir}/supervise/spamd/supervise
install -d %{buildroot}/var/log/qmail
install -d %{buildroot}/var/log/qmail/spamd

#files
#-------------------------------------------------------------------------------
rm -f %{buildroot}%{_sysconfdir}/mail/spamassassin/local.cf
rm -f %{buildroot}%{_sysconfdir}/mail/spamassassin/v310.pre
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/mail/spamassassin/local.cf.bz2
bunzip2 %{buildroot}%{_sysconfdir}/mail/spamassassin/local.cf.bz2

#install -m 0644 %{SOURCE2} %{buildroot}%{qdir}/supervise/spamd/run.bz2
#bunzip2 %{buildroot}%{qdir}/supervise/spamd/run.bz2
#install -m 0644 %{SOURCE3} %{buildroot}%{qdir}/supervise/spamd/log/run.bz2
#bunzip2 %{buildroot}%{qdir}/supervise/spamd/log/run.bz2
install -m 0644 %{SOURCE2} %{buildroot}%{qdir}/supervise/spamd/run
install -m 0644 %{SOURCE3} %{buildroot}%{qdir}/supervise/spamd/log/run

install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/mail/spamassassin/v310.pre.bz2
bunzip2 %{buildroot}%{_sysconfdir}/mail/spamassassin/v310.pre.bz2
install -m 0644 $RPM_BUILD_DIR/%{real_name}-%{pversion}/rules/v312.pre %{buildroot}%{_sysconfdir}/mail/spamassassin/v312.pre
install -m 0644 $RPM_BUILD_DIR/%{real_name}-%{pversion}/rules/v320.pre %{buildroot}%{_sysconfdir}/mail/spamassassin/v320.pre

#-------------------------------------------------------------------------------
%pre
#-------------------------------------------------------------------------------

# remove qtp-sa-update cron job if it exists
if [ -f /etc/cron.daily/qtp-sa-update ]; then
  rm -f /etc/cron.daily/qtp-sa-update
fi

#-------------------------------------------------------------------------------
%preun
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

# get rules for upgrade or new install
/usr/bin/sa-update --gpgkey D1C035168C1EBC08464946DA258CDB3ABDE9DC10 \
      || echo "sa-update return code $?"

#-------------------------------------------------------------------------------
%postun
#-------------------------------------------------------------------------------

if [ $1 = "0" ]; then
  rm -fR /var/qmail/supervise/spamd/
  rm -fR /var/log/qmail/spamd/
fi
#-------------------------------------------------------------------------------
# triggerin is executed after spamassassin is installed, if simscan is installed
# *and* after simscan is installed while spamassassin is installed
#-------------------------------------------------------------------------------
%triggerin -- simscan-toaster
#-------------------------------------------------------------------------------
if [ -x /var/qmail/bin/update-simscan ]; then
  /var/qmail/bin/update-simscan
fi

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{real_name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{real_name}-%{pversion}
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

#-------------------------------------------------------------------------------
%files -f %{name}-%{version}-filelist
#-------------------------------------------------------------------------------
%defattr(-,root,root)

# Docs
%doc LICENSE CREDITS Changes README TRADEMARK UPGRADE
%doc USAGE sample-nonspam.txt sample-spam.txt

# Dirs
%attr(0755,root,root) %dir %{_sysconfdir}/mail/spamassassin
%attr(1700,qmaill,qmail) %dir %{qdir}/supervise/spamd
%attr(0700,qmaill,qmail) %dir %{qdir}/supervise/spamd/log
%attr(0755,qmaill,qmail) %dir %{qdir}/supervise/spamd/supervise
#%attr(0700,qmaill,qmail) %dir /var/log/qmail
%attr(0755,qmaill,qmail) %dir /var/log/qmail/spamd

# Files
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/local.cf
%config            %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v310.pre
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v312.pre
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v320.pre
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v330.pre
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/cron.d/sa-update
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/logrotate.d/sa-update
## MR -- exist in 3.4.0
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v340.pre
## MR -- exist in 3.4.1
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mail/spamassassin/v341.pre


%{_datadir}/spamassassin/

%attr(0751,qmaill,qmail) %{qdir}/supervise/spamd/run
%attr(0751,qmaill,qmail) %{qdir}/supervise/spamd/log/run

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Fri Sep 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> 3.4.1-1.4.7.mr
- update to 3.4.1

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 3.4.0-1.4.6.mr
- cleanup spec based on toaster github (without define like build_cnt_60)
- add '-i 0.0.0.0' in run filr to fix/escape perl(IO::Socket::INET6) create socket

* Wed Aug 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> 3.4.0-1.4.5.mr
- update to 3.4.0

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> 3.3.2-1.4.4.mr
- update run and log run script

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 3.3.2-1.4.3.mr
- add build_cnt_60 and build_cnt_6064

* Sun Jul 29 2012 Eric Shubert <eric@datamatters.us> 3.3.2-1.4.3
- Fixed bug with removing qtp-sa-update
* Sat Jul 28 2012 Eric Shubert <eric@datamatters.us> 3.3.2-1.4.2
- Uncommented sa-update cron job (thanks to Aleksander P)
- Removed stdout output from sa-update.cron (log output only)
- Removed /etc/cron.daily/qtp-sa-update (thanks to Aleksander P)
* Thu Jul 26 2012 Eric Shubert <eric@datamatters.us> 3.3.2-1.4.1
- Added cron job to run sa-update (courtesy of repoforge)
- Added sa-update.log, logrotate conf (courtesy of repoforge)
- Added sa-update to %post
* Tue Jul 24 2012 Eric Shubert <eric@datamatters.us> 3.3.2-1.4.0
- Bumped QMT version to 1.4.0
- Added trigger to update simscan
- Removed DomainKeys plugin from v310.pre
* Fri Oct 07 2011 Jake Vickers <jake@qmailtoaster.com> 3.3.2-1.3.18
- Updated spamassassin to version 3.3.2
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 3.2.5-1.3.17
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 3.2.5-1.3.17
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 3.2.5-1.3.16
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Fixed a bug in installation of /etc/mail/spamassassin files that may have
- caused it to no build/install on certain systems
* Mon Feb 16 2009 Jake Vickers <jake@qmailtoaster.com> 3.2.5-1.3.15
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 3.2.5-1.3.15
- Added Fedora 9 and 10 support
* Fri Jul 11 2008 Erik A. Espinoza <espinoza@kabewm.com> 3.2.5-1.3.14
- Upgraded to SpamAssassin 3.2.5
* Sun Feb 04 2008 Erik A. Espinoza <espinoza@kabewm.com> 3.2.4-1.3.13
- Upgraded to SpamAssassin 3.2.4
* Thu Aug 09 2007 Erik A. Espinoza <espinoza@kabewm.com> 3.2.3-1.3.12
- Upgraded to SpamAssassin 3.2.3
* Tue Aug 07 2007 Erik A. Espinoza <espinoza@kabewm.com> 3.2.2-1.3.11
- Upgraded to SpamAssassin 3.2.2
* Mon Jun 18 2007 Erik A. Espinoza <espinoza@kabewm.com> 3.2.1-1.3.10
- Upgraded to SpamAssassin 3.2.1
* Mon May 21 2007 Erik A. Espinoza <espinoza@kabewm.com> 3.2.0-1.3.9
- Upgraded to SpamAssassin 3.2.0
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 3.1.8-1.3.8
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Sat Feb 24 2007 Erik A. Espinoza <espinoza@kabewm.com> 3.1.8-1.3.7
- Upgraded to SpamAssassin 3.1.8
- Made local.cf, v310.pre and v312.pre into config for easier upgrades
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.7-1.3.6
- Added Fedora Core 6 support
- Changed "required_hits" to "required_score" as the old option has been deprecated
* Sat Oct 14 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.7-1.3.5
- Upgraded to SpamAssassin 3.1.7
* Sat Oct 07 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.6-1.3.4
- Upgraded to SpamAssassin 3.1.6
- Removed "-L", local checks only setting
* Sun Sep 10 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.5-1.3.3
- Upgraded to SpamAssassin 3.1.5
* Sat Aug 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.4-1.3.2
- Upgraded to SpamAssassin 3.1.4
* Tue Jun 06 2006 John Li <jli@jlisbz.com> 3.1.3-1.3.1
- Upgraded to SpamAssassin 3.1.3
- Ticked branch to 1.3
* Sun May 28 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.2-1.2.16
- Upgraded to spamassassin 3.1.2
* Tue May 16 2006 Nick Hemmesch <nick@ndhsoft.com> 3.1.1-1.2.15
- Added SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 3.1.1-1.2.14
- Added Fedora Core 5 support
* Sun Apr 30 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.1-1.2.13
- Fixed spec file to clean build root properly
- Reoved spam-sync cron job
* Tue Apr 10 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.1-1.2.12
- Updated to spamassassin 3.1.1
* Tue Dec 06 2005 Nick Hemmesch <nick@ndhsoft.com> 3.1.0-1.2.11
- Fix bayes_auto_learn and sa-learn functions
- Update local.cf and v310.pre
- Add sa-learn --sync call to cron.hourly
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 3.1.0-1.2.10
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.9
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.8
- Add CentOS 4 x86_64 support
* Mon Sep 26 2005 Nick Hemmesch <nick@ndhsoft.com> 3.1.0-1.2.7
- Update local.cf and dirs for spamassassin 3.1.0
* Tue Sep 20 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 3.1.0-1.2.6
- Upgraded to spamassassin 3.1.0
* Thu Jul 28 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.5
- Fix auto-whitelist - change from a dir to a file
* Mon Jul 04 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.4
- Fix perl-forward-compat problem with rht90 
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.4
- Add support for Fedora Core 4
* Sun Jun 19 2005 Nick Hemmesch <nick@ndhsoft.com> 3.0.4-1.2.3
- Update to spamassassin-3.0.4
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 3.0.1-1.2.2
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Mon May 30 2005 Nick Hemmesch <nick@ndhsoft.com> - 3.0.1-1.2.1
- Intitial build to work with qmail-toaster and simscan-toaster
