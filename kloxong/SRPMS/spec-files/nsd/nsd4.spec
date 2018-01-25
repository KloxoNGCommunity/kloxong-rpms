Summary: Fast and lean authoritative DNS Name Server
Name: nsd
Version: 4.1.10
Release: 1%{?dist}
License: BSD
Url: http://www.nlnetlabs.nl/%{name}/
Source: http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz
Source1: nsd.init
Source2: nsd.logrotate
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: flex, openssl-devel, libevent-devel
Requires(pre): shadow-utils
Requires: libevent

%description
NSD is a complete implementation of an authoritative DNS name server.
For further information about what NSD is and what NSD is not please
consult the REQUIREMENTS document which is a part of this distribution
(thanks to Olaf).

%prep
%setup -q

%build
%configure --enable-bind8-stats \
    --enable-checking \
    --enable-ratelimit \
    --with-ssl \
    --with-libevent \
    --with-user=%{name} \
    --with-configdir=%{_sysconfdir}/%{name} \
    --with-zonesdir=%{_sysconfdir}/%{name} \
    --with-zonelistfile=%{_localstatedir}/lib/%{name}/zone.list \
    --with-dbfile=%{_localstatedir}/lib/%{name}/nsd.db \
    --with-pidfile=%{_localstatedir}/run/%{name}/%{name}.pid \
    --with-xfrdfile=%{_localstatedir}/lib/%{name}/xfrd.state \
    --with-xfrdir=%{_localstatedir}/lib/%{name}/xfr 

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} nsd-mem
#convert to utf8
iconv -f iso8859-1 -t utf-8 doc/RELNOTES > doc/RELNOTES.utf8
iconv -f iso8859-1 -t utf-8 doc/CREDITS > doc/CREDITS.utf8
mv -f doc/RELNOTES.utf8 doc/RELNOTES
mv -f doc/CREDITS.utf8 doc/CREDITS


%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}%{_initrddir}
install -m 0755 %{SOURCE1} %{buildroot}/%{_initrddir}/nsd
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/nsd
install -d -m 0755 %{buildroot}%{_localstatedir}/run/%{name}
install -d -m 0700 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 0700 %{buildroot}%{_localstatedir}/lib/%{name}/xfr
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0755 nsd-mem %{buildroot}/%{_sbindir}/nsd-mem

mv %{buildroot}%{_sysconfdir}/nsd/nsd.conf.sample %{buildroot}%{_sysconfdir}/nsd/nsd.conf

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-,root,root,-)
%doc doc/*
%doc contrib/nsd.zones2nsd.conf
%attr(0755,root,nsd) %dir %{_sysconfdir}/nsd
%attr(0644,root,nsd) %config(noreplace) %{_sysconfdir}/nsd/nsd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/nsd
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,%{name},%{name}) %dir %{_localstatedir}/run/%{name}
%attr(0755,%{name},%{name}) %dir %{_localstatedir}/lib/%{name}
%attr(0755,%{name},%{name}) %dir %{_localstatedir}/lib/%{name}/xfr
%{_sbindir}/*
%{_mandir}/*/*

%pre
getent group nsd >/dev/null || groupadd -r nsd
getent passwd nsd >/dev/null || \
useradd -r -g nsd -d /etc/nsd -s /sbin/nologin \
        -c "nsd daemon account" nsd
exit 0

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name} 
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%changelog
* Wed Jun 15 2016 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.10-1
- update to 4.1.10
- update nsd4.init

* Mon Mar 28 2016 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.9-1
- update to 4.1.9

* Fri Dec 11 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.7-1
- update to 4.1.7

* Tue Oct 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.6-1
- update to 4.1.6

* Thu Sep 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.5-1
- update to 4.1.5

* Sat Sep 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.4-1
- update to 4.1.4

* Thu Jun 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.3-1
- update to 4.1.3

* Sat Apr 18 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.2-1
- update to 4.1.2

* Tue Feb 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.1-2
- add logrotate

* Tue Feb 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.1-1
- update to 4.1.1

* Thu Oct 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.0-3
- add 'sleep 2' between stop and start in restart

* Thu Oct 02 2014 Mustafa Ramadhan <mustafa@bigraf.com> 4.1.0-2
- first compile for Kloxo-MR

* Tue Sep 23 2014 Takashi Takizawa <taki@cyber.email.ne.jp> - 4.1.0-1
- Updated to 4.1.0

* Thu Jul 17 2014 Takashi Takizawa <taki@cyber.email.ne.jp> - 4.0.3-1
- Updated to 4.0.3

* Tue Feb 05 2013 Paul Wouters <pwouters@redhat.com> - 3.2.15-3
- Updated to 3.2.15 which has support for rate limiting
- Only run nsdc rebuild hourly cronjob when nsd service is running
- Fix nsd.init to return proper return code for 'status' cmd

* Fri Nov 23 2012 Paul Wouters <pwouters@redhat.com> - 3.2.14-2
- Updated to 32.14 with minor bugfixes and TCP writev support
- Only run nsdc rebuild hourly cronjob when nsd service is running

* Fri Jul 27 2012 Paul Wouters <pwouters@redhat.com> - 3.2.13-1
- Updated to 3.2.13, addresses VU#517036 CVE-2012-2979
  (note Fedora/EPEL packages are not vulnerable to this)
- Add /var/run/nsd via tmpfiles (rhbz#842021)

* Thu Jul 19 2012 Paul Wouters <pwouters@redhat.com> - 3.2.12-1
- Upgraded to 3.2.12 which fixes CVE-2012-2978 (rhbz#841268)

* Mon Jul 16 2012 Paul Wouters <pwouters@redhat.com> - 3.2.11-1
- Updated to 3.2.11 (support for TLSA, GOST, bugfixes)

* Wed Feb 15 2012 Paul Wouters <pwouters@redhat.com> - 3.2.10-1
- Updated to 3.2.10
- Ship our own nsd.conf instead of hacking the nsd.conf.sample
- Merge in fixed by Tuomo Soini <tis@foobar.fi>
  - Fix %%preun and %%postun to be quiet
  - Fix /etc/nsd permissions to be root:nsd mode 0750
  - Cleanup /etc/sysconfig/nsd
  - Change startup order of nsd so it works with IPv6 on 6to4
  - Revert piddir to be owned by user nsd
  - Initscript cleanup

* Tue Jun  7 2011 Paul Wouters <paul@xelerance.com> - 3.2.8-1
- updated to 3.2.8
- fix /var/run/nsd to be owned by root, not nsd
- fix init status to work as expected (bz#525107)
- fix nsd.conf and nsd.conf.5 to have correct logfile
- fix nsd.init syntax error by piddir change
- fix initscript to create /var/run/nsd if missing (bz#710376)

* Wed Mar 09 2011 Paul Wouters <paul@xelerance.com> - 3.2.7-5
- Updated to 3.2.7
- Fix for nsd.init to report OK/FAILED properly (bz#525107)
- Use ghost directive for /var/run/nsd (bz#656642)
- Removed obsolete --enable-nsid
- Remove bogus chowns for /var/*/nsdhm
- Fix misnamed variable NSD_AUTORELOAD which should be NSD_AUTOREBUILD

* Wed Jan 06 2010 Paul Wouters <paul@xelerance.com> - 3.2.4-1
- Upgraded to 3.2.4. Minor fixes to cron/init/sysconfig scripts

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.3-3
- rebuilt with new openssl

* Thu Aug 20 2009 Ville Mattila <vmattila@csc.fi> - 3.2.3-2
- The 'nsdc patch' and 'nsdc rebuild' commands wrote a %%1 file by mistake

* Mon Aug 17 2009 Paul Wouters <paul@xelerance.com> - 3.2.3-1
-Updated to version 3.2.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 06 2009 Paul Wouters <paul@xelerance.com> - 3.2.2-3
- Fixed /dev/nul which cause a file \%%1 to be written by cron
- Bump for EVR.

* Mon May 18 2009 Paul Wouters <paul@xelerance.com> - 3.2.2-1
- Upgraded to 3.2.2 security release
  http://www.nlnetlabs.nl/publications/NSD_vulnerability_announcement.html

* Thu Apr 09 2009 Ville Mattila <vmattila@csc.fi> - 3.2.1-6
- Make various file paths used by the nsd.init script configurable
  from /etc/sysconfig/nsd.
- Add template /etc/sysconfig/nsd.

* Sun Mar 08 2009 Paul Wouters <paul@xelerance.com> - 3.2.1-5
- nsd used the 'named' subsystem in one call in the init script

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Paul Wouters <paul@xelerance.com> - 3.2.1-3
- Fix init script 'unary operator' error.

* Mon Jan 26 2009 Paul Wouters <paul@xelerance.com> - 3.2.1-1
- Updated to new version 3.2.1

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.0-4
- rebuild with new openssl

* Mon Nov 24 2008 Paul Wouters <paul@xelerance.com> - 3.2.0-3
- Updates summary as per Richard Hughes guidelines

* Mon Nov 10 2008 Paul Wouters <paul@xelerance.com> - 3.2.0-2
- Bump version after pre-release version correction.

* Mon Nov 10 2008 Paul Wouters <paul@xelerance.com> - 3.2.0-1
- 3.2.0-1

* Thu Oct  9 2008 Paul Wouters <paul@xelerance.com> - 3.1.1-1
- updated to 3.1.1

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.0-2
- fix license tag
- fix static user creation

* Mon Jun 30 2008 Paul Wouters <paul@xelerance.com> - 3.1.0-1
- Updated to 3.1.0

* Tue May  6 2008 Paul Wouters <paul@xelerance.com> - 3.0.8-2
- Fix /dev/null redirection [Venkatesh Krishnamurthi]

* Tue May  6 2008 Paul Wouters <paul@xelerance.com> - 3.0.8-1
- Updated to 3.0.8

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.7-3
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Paul Wouters <paul@xelerance.com> - 3.0.7-2
- Rebuild for new libcrypto

* Tue Nov 13 2007 Paul Wouters <paul@xelerance.com> - 3.0.7-1
- Updated to new version
- fix RELNOTES/README to be utf8
- Fix path to nsd.db in cron job.

* Thu Nov  8 2007 Paul Wouters <paul@xelerance.com> - 3.0.6-7
- Modified cron to only rebuild/reload when zone updates
  have been received

* Wed Nov  7 2007 Paul Wouters <paul@xelerance.com> - 3.0.6-6
- Added hourly cron job to do various maintenance tasks
- Added nsd rebuild to create the proper nsd.db file on startup
- Added nsd patch on shutdown to ensure zonefiles are up to date

* Tue Oct  2 2007 Paul Wouters <paul@xelerance.com> - 3.0.6-5
- nsdc update and nsdc notify are no longer needed in initscript.

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 3.0.6-4
- Bump release for upgrade path.

* Fri Sep 14 2007 Paul Wouters <paul@xelerance.com> 3.0.6-3
- Do not include examples from nsd.conf.sample that causes
  bogus network traffic.

* Fri Sep 14 2007 Paul Wouters <paul@xelerance.com> 3.0.6-2
- Change locations of ixfr.db and xfrd.state to /var/lib/nsd
- Enable NSEC3
- Delay running nsdc update until after nsd has started
- Delete xfrd.state on nsd stop
- Run nsdc notify in the background, since it can take
  a very long time when remote servers are unavailable.

* Tue Sep 11 2007 Paul Wouters <paul@xelerance.com> 3.0.6-1
- Upgraded to 3.0.6
- Do not include bind2nsd, since it didn't compile for me

* Fri Jul 13 2007 Paul Wouters <paul@xelerance.com> 3.0.5-2
- Fix init script, bug #245546

* Fri Mar 23 2007 Paul Wouters <paul@xelerance.com> 3.0.5-1
- Upgraded to 3.0.5

* Thu Dec  7 2006 Paul Wouters <paul@xelerance.com> 3.0.3-1
- Upgraded to 3.0.3

* Mon Nov 27 2006 Paul Wouters <paul@xelerance.com> 3.0.2-1
- Upgraded to 3.0.2.
- Use new configuration file nsd.conf. Still needs migration script.
  patch from Farkas Levente <lfarkas@bppiac.hu>

* Mon Oct 16 2006  Paul Wouters <paul@xelerance.com> 2.3.6-2
- Bump version for upgrade path

* Thu Oct 12 2006  Paul Wouters <paul@xelerance.com> 2.3.6-1
- Upgraded to 2.3.6
- Removed obsolete workaround in nsd.init
- Fixed spec file so daemon gets properly restarted on upgrade

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 2.3.5-4
- Rebuild requested for PT_GNU_HASH support from gcc
- Removed dbaccess.c from doc section

* Mon Jun 26 2006 Paul Wouters <paul@xelerance.com> - 2.3.5-3
- Bump version for FC-x upgrade path

* Mon Jun 26 2006 Paul Wouters <paul@xelerance.com> - 2.3.5-1
- Upgraded to nsd-2.3.5

* Sun May  7 2006 Paul Wouters <paul@xelerance.com> - 2.3.4-3
- Upgraded to nsd-2.3.4. 
- Removed manual install targets because DESTDIR is now supported
- Re-enabled --checking, checking patch no longer needed and removed.
- Work around in nsd.init for nsd failing to start when there is no ipv6

* Thu Dec 15 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-7
- chkconfig and attribute  changes as proposed by Dmitry Butskoy

* Thu Dec 15 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-6
- Moved pid file to /var/run/nsd/nsd.pid.
- Use _localstatedir instead of "/var"

* Tue Dec 13 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-5
- Added BuildRequires for openssl-devel, removed Requires for openssl.

* Mon Dec 12 2005 Paul Wouters <paul@xelerance.com> - 2.3.3-4
- upgraded to nsd-2.3.3

* Wed Dec  7 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.2-2
- minor cleanups

* Mon Dec  5 2005 Paul Wouters <paul@xelerance.com> - 2.3.2-1
- Upgraded to 2.3.2. Changed post scripts to comply to Fedora
  Extras policies (eg do not start daemon on fresh install)

* Tue Oct  4 2005 Paul Wouters <paul@xelerance.com> - 2.3.1-1
- Initial version
