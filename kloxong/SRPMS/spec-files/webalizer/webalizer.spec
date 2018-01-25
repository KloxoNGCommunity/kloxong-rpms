%define ver 2.23
%define patchlevel 08

%if 0%{?fedora} < 18
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

Name: webalizer
Summary: A flexible Web server log file analysis program
Group: Applications/Internet
Version: %{ver}_%{patchlevel}
Release: 1%{?dist}
URL: http://www.mrunix.net/webalizer/
License: GPLv2+
Source0: ftp://ftp.mrunix.net/pub/webalizer/%{name}-%{ver}-%{patchlevel}-src.tar.bz2
Source1: webalizer.conf
Source2: webalizer.cron
Source3: webalizer-httpd.conf
Source4: webalizer.sysconfig
Patch4: webalizer-2.21-02-underrun.patch
Patch6: webalizer-2.23-05-confuser.patch
Patch9: webalizer-2.23-05-groupvisit.patch
Patch10: webalizer-2.23-05-outputngraph.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gd-devel, %{db_devel}, bzip2-devel
Requires(pre): /usr/sbin/useradd
#Requires: httpd, crontabs
Requires: crontabs

%description
The Webalizer is a Web server log analysis program. It is designed to
scan Web server log files in various formats and produce usage
statistics in HTML format for viewing through a browser. It produces
professional looking graphs which make analyzing when and where your
Web traffic is coming from easy.

%prep
%setup -q -n %{name}-%{ver}-%{patchlevel}
#%patch4 -p1 -b .underrun
#%patch6 -p1 -b .confuser
#%patch9 -p1 -b .groupvisit
%patch10 -p1 -b .outputngraph

%build
CPPFLAGS="-I%{_includedir}/db4" ; export CPPFLAGS
CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS -D_GNU_SOURCE" ; export CFLAGS
%configure --enable-dns --with-dblib=/lib --enable-bz2

make %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/www/usage \
         $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/webalizer

make DESTDIR=$RPM_BUILD_ROOT install

install -p -m 644 $RPM_SOURCE_DIR/webalizer.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 644 *.png $RPM_BUILD_ROOT%{_localstatedir}/www/usage
install -p -m 755 $RPM_SOURCE_DIR/webalizer.cron \
         $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/00webalizer
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 $RPM_SOURCE_DIR/webalizer-httpd.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/webalizer.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 644 $RPM_SOURCE_DIR/webalizer.sysconfig \
        $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/webalizer

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/webalizer.conf.sample

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/adduser -c "Webalizer" -u 67 \
    -s /sbin/nologin -r -d %{_localstatedir}/www/usage webalizer 2>/dev/null || :

%files
%defattr(-,root,root)
%doc README
%{_mandir}/man1/*.1*
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/webalizer.conf
%{_sysconfdir}/cron.daily/00webalizer
%config(noreplace) %{_sysconfdir}/httpd/conf.d/webalizer.conf
%config(noreplace) %{_sysconfdir}/sysconfig/webalizer
%attr(-, webalizer, root) %dir %{_localstatedir}/www/usage
%attr(-, webalizer, root) %dir %{_localstatedir}/lib/webalizer
%attr(-, webalizer, root) %{_localstatedir}/www/usage/*.png

%changelog
* Fri Sep 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.23_08-1.mr
- update to 2.23-08

* Tue Jun 02 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.23_05-6.mr
- fix html (remove th) and graph (remove bevel)

* Sat Feb 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.23_05-5.mr
- remove httpd as Requires

* Tue Jul 02 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.23_05-4.mr
- recompile

* Wed Apr 25 2012 Joe Orton <jorton@redhat.com> - 2.23_05-4
- build (conditionally) against libdb-devel

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23_05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.23_05-2
- Rebuild for new libpng

* Thu Jul 14 2011 Joe Orton <jorton@redhat.com> - 2.23_05-1
- update to 2.23_05

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21_02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 17 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.21_02-4
- Don't run cronjob unless configured in /etc/sysconfig/webalizer (merge review #298203)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21_02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Joe Orton <jorton@redhat.com> 2.21_02-2
- update to 2.21-02 (thanks to Robert Scheck)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20_01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  5 2008 Joe Orton <jorton@redhat.com> 2.20_01-1
- update to 2.20_01

* Mon Jul 14 2008 Joe Orton <jorton@redhat.com> 2.01_10-37
- rebuild for new BDB

* Thu Feb  7 2008 Joe Orton <jorton@redhat.com> 2.01_10-36
- fix build with new glibc, use _GNU_SOURCE 

* Thu Feb  7 2008 Joe Orton <jorton@redhat.com> 2.01_10-35
- use %%{_localestatedir}, remove tabs, require httpd not
  webserver, mark webalizer.conf config(noreplace) (#226536)

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 2.01_10-34
- clarify License tag

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 2.01_10-33
- rebuild

* Mon Mar 19 2007 Joe Orton <jorton@redhat.com> 2.01_10-32
- spec file cleanups (#226536):
 * convert to UTF-8
 * fix BuildRoot, Summary
 * add Requires(pre) for shadow-utils, remove Prereqs
 * trim BuildRequires to png-devel, db4-devel
 * use smp_mflags in make
 * use sysconfdir macro throughout
 * preserve file timestamps on installation

* Mon Jan 29 2007 Joe Orton <jorton@redhat.com> 2.01_10-31
- rebuild to pick up new db4 soname

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.01_10-30.1
- rebuild

* Fri Jun 16 2006 Joe Orton <jorton@redhat.com> 2.01_10-30
- add patch set from Jarkko Ala-Louvesniemi (#187344, #187726, #188248)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.01_10-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.01_10-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Joe Orton <jorton@redhat.com> 2.01_10-29
- run with -Q from cron (#120913)
- remove ancient trigger and post scriptlets
- only read webalizer.conf from $PWD if owner matches user (#158174)

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 2.01_10-28
- rebuild

* Mon Jan 24 2005 Joe Orton <jorton@redhat.com> 2.01_10-27
- don't package /etc/webalizer.conf.sample (#145980)

* Fri Nov 19 2004 Joe Orton <jorton@redhat.com> 2.01_10-26
- rebuild

* Wed Aug 18 2004 Joe Orton <jorton@redhat.com> 2.01_10-25
- rebuild

* Fri Jun 18 2004 Alan Cox <alan@redhat.com>
- Added IPv6 patch from PLD c/o Robert Scheck
- Added tests to trap bogus logfiles with negative times/dates
- Fixed leap seconds

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Mar 27 2004 Joe Orton <jorton@redhat.com> 2.0_10-22
- allow access to /usage from ::1 and 127.0.0.1 by default
- require crontabs

* Sun Mar 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- keep apps owned by root:root

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 12 2004 Florian La Roche <Florian.LaRoche@redhat.de> 2.0_10-19
- add an "exit 0" to post script

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 2.01_10-18
- update default config

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 2.01_10-17
- add fix for #111433

* Fri Nov 28 2003 Joe Orton <jorton@redhat.com> 2.01_10-16
- merge from Taroon

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Fri Aug  1 2003 Joe Orton <jorton@redhat.com> 2.01_10-15.ent
- support large (>2gb) log files on 32-bit platforms
- move default output directory to /var/www/usage
- add conf.d/webalizer.conf to add alias for /usage
- only allow access to usage stats from localhost by default
- change default config: don't ignore out-of-sequence log entries,
  count .php and .shtml as "page" extensions.

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 
- rebuilt

* Wed Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 05 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix owner in /var/www/html/usage for "rpm -Va"

* Tue May 06 2003 Phil Knirsch <pknirsch@redhat.com> 2.01_10-12
- Bumped release and rebuilt due to new gd version.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.01_10-11
- rebuilt

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 2.01_10-10
- requires webserver (bug #74006)
- unpackaged file issue

* Tue Jul 02 2002 Than Ngo <than@redhat.com> 2.01_10-9
- fix a bug in post

* Mon Jul 01 2002 Than Ngo <than@redhat.com> 2.01_10-8
- fix a bug in pre (bug #67634)

* Wed Jun 27 2002 Than Ngo <than@redhat.com> 2.01_10-7
- add shadow-utils in prereq 

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Than Ngo <than@redhat.com> 2.01_10-5
- fixed bug #62062, #64392, #63685

* Thu May 30 2002 Nalin Dahyabhai <nalin@redhat.com> 2.01_10-4
- fixup some linkage problems (was getting db2, which shouldn't happen)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.01_10-2
- Use db4

* Wed Apr 17 2002 Than Ngo <than@redhat.com> 2.01_10-1
- 2.01_10 fixes a posible buffer overflow bug in DNS resolver code

* Thu Mar 21 2002 Preston Brown <pbrown@redhat.com>
- put transient files in /var/lib/webalizer
- removed sysconfig runtime option.  Remove the package or cron script if 
  you do not want it to run (#59752)
- make default quiet operation

* Mon Feb 25 2002 Than Ngo <than@redhat.com> 2.01_09-5
- allows multiple partial log files to be used instead of one huge one.(bug #60295)

* Wed Feb 21 2002 Than Ngo <than@redhat.com> 2.01_09-4
- add function to enable/disable webalizer (bug #59752)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 14 2001 Than Ngo <than@redhat.com> 2.01_09-2
- make cron jobs quiet (bug #56249)

* Wed Oct 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.01_09-1
- Update to 2.01-09, fixing security bugs

* Thu Sep 20 2001 Than Ngo <than@redhat.com> 2.01_06-13
- update config file (bug #53881)

* Sun Sep 16 2001 Than Ngo <than@redhat.com> 2.01_06-12
- add patch from author to fix Webalizer dumps core when MangleAgents is set to 1

* Mon Jul 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove empty post
- Mark the crontab file as config(noreplace) 

* Fri Jul 13 2001 Than Ngo <than@redhat.com> 2.01_06-10
- fix build dependencies (bug #48939)
- Copyright->License

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- add missing icons (bug #43220)

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Fri May 18 2001 Than Ngo <than@redhat.com>
- don't run webalizer when access log file is empty (Bug #41322)

* Wed Feb 14 2001 Tim Powers <timp@redhat.com>
- enable dns-lookups (patched to use correct db header) (bug #27612)

* Thu Feb  1 2001 Tim Powers <timp@redhat.com>
- make the cronjob called 00webalizer, so that it runs before everything else

* Wed Jan 31 2001 Tim Powers <timp@redhat.com>
- fixed bug 25351, where webalizer was being run after apache is
  logrotated.

* Tue Oct 17 2000 Than Ngo <than@redhat.com>
- update to 2.01-06

* Tue Oct 17 2000 Than Ngo <than@redhat.com>
- fixed wrong OutputDir (bug #19180)

* Thu Aug 3 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Sun Jun 19 2000 Karsten Hopp <karsten@redhat.de>
- rebuild for 7.0
- changed mandir
- changed graph output to png instead of gif
- changed path to apache root (/var/www)

* Mon Nov 08 1999 Bernhard Rosenkränzer <bero@redhat.com>
- handle RPM_OPT_FLAGS

* Tue Sep 28 1999 Preston Brown <pbrown@redhat.com>
- updated for Secure Web Server 3.1

* Mon May 03 1999 Preston Brown <pbrown@redhat.com>
- initial build for Secure Web Server 3.0
