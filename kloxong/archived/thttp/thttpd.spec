%define webroot /var/www/thttpd

Summary: Tiny, turbo, throttleable lightweight http server
Name: thttpd
Version: 2.25b
#Release: 12%{?dist}.1
Release: 13%{?dist}
License: BSD
Group: System Environment/Daemons
URL: http://www.acme.com/software/thttpd/
Source0: http://www.acme.com/software/thttpd/thttpd-%{version}.tar.gz
Source1: thttpd.init
Source2: thttpd.logrotate
Source10: index.html
Source11: thttpd_powered_3.png
Source12: powered_by_fedora.png
Patch0: thttpd-2.25b-CVE-2005-3124.patch
Patch1: thttpd-2.25b-fixes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Thttpd is a very compact no-frills httpd serving daemon that can handle
very high loads.  While lacking many of the advanced features of
Apache, thttpd operates without forking and is extremely efficient in
memory use.  Basic support for cgi scripts, authentication, and ssi is
provided for.  Advanced features include the ability to throttle traffic.

Available rpmbuild rebuild options :
--with : indexes showversion expliciterrors


%prep
%setup
%patch0 -p1 -b .CVE-2005-3124
%patch1 -p1 -b .fixes


%build
%configure
# Hacks :-)
%{__perl} -pi -e 's/-o bin -g bin//g' Makefile
%{__perl} -pi -e 's/.*chgrp.*//g; s/.*chmod.*//g' extras/Makefile
# Config changes
%{!?_with_indexes:        %{__perl} -pi -e 's/#define GENERATE_INDEXES/#undef GENERATE_INDEXES/g' config.h}
%{!?_with_showversion:    %{__perl} -pi -e 's/#define SHOW_SERVER_VERSION/#undef SHOW_SERVER_VERSION/g' config.h}
%{!?_with_expliciterrors: %{__perl} -pi -e 's/#define EXPLICIT_ERROR_PAGES/#undef EXPLICIT_ERROR_PAGES/g' config.h}
%{__make} %{?_smp_mflags} WEBDIR=%{webroot}/html CGIBINDIR=%{webroot}/cgi-bin \
    CCOPT="%{optflags} -D_FILE_OFFSET_BITS=64"


%install
%{__rm} -rf %{buildroot}

# Prepare required directories
%{__mkdir_p} %{buildroot}%{webroot}/{cgi-bin,html,logs}
%{__mkdir_p} %{buildroot}%{_mandir}/man{1,8}
%{__mkdir_p} %{buildroot}%{_sbindir}

# Install init script and logrotate entry
%{__install} -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/thttpd
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/thttpd

# Main install
%{__make} install BINDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}%{_mandir} \
    WEBDIR=%{buildroot}%{webroot}/html \
    CGIBINDIR=%{buildroot}%{webroot}/cgi-bin

# Rename htpasswd in case apache is installed too
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mv} %{buildroot}%{_sbindir}/htpasswd \
        %{buildroot}%{_bindir}/thtpasswd
%{__mv} %{buildroot}%{_mandir}/man1/htpasswd.1 \
        %{buildroot}%{_mandir}/man1/thtpasswd.1

# Install the default index.html and related files
%{__install} -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} \
    %{buildroot}%{webroot}/html/

# Install a default configuration file
%{__cat} << EOF > %{buildroot}%{_sysconfdir}/thttpd.conf
# BEWARE : No empty lines are allowed!
# This section overrides defaults
dir=%{webroot}/html
chroot
user=thttpd         # default = nobody
logfile=/var/log/thttpd.log
pidfile=/var/run/thttpd.pid
# This section _documents_ defaults in effect
# port=80
# nosymlink         # default = !chroot
# novhost
# nocgipat
# nothrottles
# host=0.0.0.0
# charset=iso-8859-1
EOF


%clean
%{__rm} -rf %{buildroot}


%pre
/usr/sbin/groupadd -r www &>/dev/null || :
/usr/sbin/useradd -s /bin/false -c "Web server user" \
    -d %{webroot} -M -r -g www thttpd &>/dev/null || :

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add thttpd
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service thttpd stop &>/dev/null || :
    /sbin/chkconfig --del thttpd
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service thttpd condrestart &>/dev/null || :
fi


%files
%defattr(-, root, root, 0755)
%doc README TODO
%config %{_sysconfdir}/rc.d/init.d/thttpd
%config(noreplace) %{_sysconfdir}/logrotate.d/thttpd
%config(noreplace) %{_sysconfdir}/thttpd.conf
%{_bindir}/thtpasswd
%attr(2755, root, www) %{_sbindir}/makeweb
%{_sbindir}/syslogtocern
%{_sbindir}/thttpd
%attr(2775, thttpd, www) %dir %{webroot}/
%attr(2775, thttpd, www) %dir %{webroot}/cgi-bin/
# We don't want those default cgi-bin programs
%exclude %{webroot}/cgi-bin/*
%attr(2775, thttpd, www) %dir %{webroot}/html/
%attr(2664, thttpd, www) %{webroot}/html/*
%attr(2775, thttpd, www) %dir %{webroot}/logs/
%{_mandir}/man?/*


%changelog
* Fri Jan 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> 2.25b-13.mr
- recompile

* Sun Aug 19 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 2.25b-13.lx.el5
- Recompile.

* Thu Apr  9 2009 Matthias Saou <http://freshrpms.net/> 2.25b-12.1
- Fix thttpd-2.25b-CVE-2005-3124.patch (#483733).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 2.25b-12
- FC6 rebuild.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.25b-11
- Include "fixes" patch from Debian (#191095) to fix thtpasswd and makeweb.
- Rename htpasswd as thtpasswd instead of htpasswd.thttpd.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.25b-10
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 2.25b-9
- Rebuild for new gcc/glibc.
- Remove prever stuff, 2.25b final has been around for while now.

* Mon Nov  7 2005 Matthias Saou <http://freshrpms.net/> 2.25b-8
- Add patch from Gentoo to fix CVE-2005-3124 (#172469, Ville Skyttä).
- Minor cosmetic spec file changes.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.25b
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Jan 20 2005 Matthias Saou <http://freshrpms.net/> 2.25b-5
- Compile with -D_FILE_OFFSET_BITS=64 to support > 2GB log files.

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 2.25b-4
- Bump release to provide Extras upgrade path.
- Re-brand Fedora where it was freshrpms previously.

* Thu Jul 10 2004 Dag Wieers <dag@wieers.com> - 2.25b-3
- Fixed location of service in logrotate conf. (Peter Bieringer)

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 2.25b-2
- Rebuild for Fedora Core 2.

* Mon Apr 26 2004 Matthias Saou <http://freshrpms.net/> 2.25b-2
- Add logrotate entry, it needs to restart thttpd completely because
  of the permissions dropped after opening the log file :-(

* Sun Jan  4 2004 Matthias Saou <http://freshrpms.net/> 2.25b-1
- Update to 2.25b.

* Tue Nov 11 2003 Matthias Saou <http://freshrpms.net/> 2.24-1
- Update to 2.24 final.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 2.23-0.beta1.3
- Rebuild for Fedora Core 1.
- Escaped the %%install and others later in this changelog.

* Wed Oct 22 2003 Matthias Saou <http://freshrpms.net/>
- Added build options and now default to no indexes, explicit errors or
  showing version.

* Mon Nov  4 2002 Matthias Saou <http://freshrpms.net/>
- Update to 2.23beta1.

* Fri May  4 2001 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup for Red Hat 7.
- New, clean initscript.
- Built the latest 2.21b version since 2.20b won't compile even with kgcc.
- Custom config file based on the contrib/redhat one.

* Wed Sep 13 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.20

* Mon Sep 11 2000 Bennett Todd <bet@rahul.net>
  - added thttpd.conf, took config info out of init script
  - switched to logging in /var/log, used pidfile

* Thu Jun 15 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.19

* Thu May 18 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.18

* Fri Mar 17 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.17

* Mon Feb 28 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.16

* Thu Feb 03 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.15

* Thu Jan 21 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.14

* Thu Jan  6 2000 Jef Poskanzer <jef@acme.com>
  - Updated to 2.13

* Mon Jan  3 2000 Bennett Todd <bet@rahul.net>
  - updated to 2.12, tweaked to move thttpd.init into tarball

* Mon Dec 13 1999 Bennett Todd <bet@mordor.net>
  - Updated to 2.09

* Fri Dec 10 1999 Bennett Todd <bet@mordor.net>
  - Updated to 2.08

* Wed Nov 24 1999 Bennett Todd <bet@mordor.net>
  - updated to 2.06, parameterized Version string in source url
  - changed to use "make install", simplified %%files list

* Wed Nov 10 1999 Bennett Todd <bet@mordor.net>
  - Version 2.05, reset release to 1
  - dropped bugfix patch since Jef included that
  - streamlined install

* Sun Jul 25 1999 Bennett Todd <bet@mordor.net>
  - Release 4, added mime type swf

* Mon May  3 1999 Bennett Todd <bet@mordor.net>
  - Release 2, added patch to set cgi-timelimit up to 10 minutes
    fm default 30 seconds

* Wed Feb 10 1999 Bennett Todd <bet@mordor.net>
  - based on 2.00-2, bumped to 2.04, reset release back to 1
  - fixed a couple of broken entries in %%install to reference %{buildroot}
  - simplified %%files to populate /usr/doc/... with just [A-Z]* (TODO had gone
    away, this simplification makes it liklier to be trivially portable to
    future releases).
  - added %%doc tags for the man pages

