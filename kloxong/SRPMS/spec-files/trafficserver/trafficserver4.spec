# https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%define _hardened_build	1
%define rhelver		%(/usr/lib/rpm/redhat/dist.sh --distnum)
%define rhelarch		%(uname -i)

Summary:	Fast, scalable and extensible HTTP/1.1 compliant caching proxy server
Name:		trafficserver
Version:	4.0.1
Release:	1%{?dist}
License:	ASL 2.0
Group:		System Environment/Daemons
Source0:	http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
Source1:	trafficserver.sysconf
Source2:	trafficserver.service
Source3:	trafficserver.tmpfilesd
URL:		http://trafficserver.apache.org/index.html
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	autoconf, automake, libtool, openssl-devel, tcl-devel, expat-devel
BuildRequires:	pcre-devel, zlib-devel, xz-devel, gcc-c++
BuildRequires:	redhat-rpm-config
ExclusiveArch:	%{ix86} x86_64 ia64 %{arm}
Requires: initscripts
%if %{rhelver} > 6
Requires:		systemd
Requires(postun):	systemd
%else
Requires(post):	chkconfig
Requires(preun):	chkconfig initscripts
Requires(postun):	initscripts
%endif

Patch2:		trafficserver-init_scripts.patch


%description
Apache Traffic Server is a fast, scalable and extensible HTTP/1.1 compliant
caching proxy server.

%prep
%setup -q

## disable for version 4 (especially not work in centos 6)
#%patch2 -p1 -b .patch2

%build
%configure \
	--enable-layout=Gentoo \
	--libdir=%{_libdir}/trafficserver \
	--libexecdir=%{_libdir}/trafficserver/plugins \
	--sysconfdir=%{_sysconfdir}/trafficserver \
	--with-tcl=%{_libdir} \
	--with-user=ats --with-group=ats \
	--disable-silent-rules

make %{?_smp_mflags}

%install
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# the traffic_shell manual conflict with bash: exit enable,
# so we rename these to ts-enable, ts-exit and ts-disable.
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp doc/man/*.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mv $RPM_BUILD_ROOT/usr/share/man/man1/enable.1 \
$RPM_BUILD_ROOT/usr/share/man/man1/ts-enable.1
mv $RPM_BUILD_ROOT/usr/share/man/man1/disable.1 \
$RPM_BUILD_ROOT/usr/share/man/man1/ts-disable.1
mv $RPM_BUILD_ROOT/usr/share/man/man1/exit.1 \
$RPM_BUILD_ROOT/usr/share/man/man1/ts-exit.1
cat <<EOF > README.fedora
The man-pages for enable, disable and exit was renamed to ts-enable,
ts-disable and ts-exit to avoid conflicts with other man-pages.
EOF

# Remove duplicate man-pages:
rm -rf $RPM_BUILD_ROOT%{_docdir}/trafficserver

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/trafficserver

%if %{rhelver} > 6
install -D -m 0644 -p %{SOURCE2} \
	$RPM_BUILD_ROOT/lib/systemd/system/trafficserver.service
install -D -m 0644 -p %{SOURCE3} \
	$RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/trafficserver.conf
%else
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
mv $RPM_BUILD_ROOT/usr/bin/trafficserver $RPM_BUILD_ROOT/etc/init.d
%endif

# Remove static libs (needs to go to separate -static subpackage if we
# want these:
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/libtsmgmt.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/libtsutil.a

# Don't include libtool archives:
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/libtsmgmt.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/libtsutil.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/plugins/conf_remap.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/plugins/header_filter.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/plugins/regex_remap.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/trafficserver/plugins/stats_over_http.la

#
perl -pi -e 's/^CONFIG.*proxy.config.proxy_name STRING.*$/CONFIG proxy.config.proxy_name STRING FIXME.example.com/' \
	$RPM_BUILD_ROOT/etc/trafficserver/records.config
perl -pi -e 's/^CONFIG.*proxy.config.ssl.server.cert.path.*$/CONFIG proxy.config.ssl.server.cert.path STRING \/etc\/pki\/tls\/certs\//' \
	$RPM_BUILD_ROOT/etc/trafficserver/records.config
perl -pi -e 's/^CONFIG.*proxy.config.ssl.server.private_key.path.*$/CONFIG proxy.config.ssl.server.private_key.path STRING \/etc\/pki\/tls\/private\//' \
	$RPM_BUILD_ROOT/etc/trafficserver/records.config

# The clean section  is only needed for EPEL and Fedora < 13
# http://fedoraproject.org/wiki/PackagingGuidelines#.25clean
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, ats, ats, -)
%doc README CHANGES NOTICE README.fedora LICENSE
%attr(0644, root, root) /usr/share/man/man1/*
%attr(0755,root,root) /usr/bin/traffic*
%attr(0755,root,root) %dir %{_libdir}/trafficserver
%attr(0755,root,root) %dir %{_libdir}/trafficserver/plugins
%attr(0755,root,root) %{_libdir}/trafficserver/*.so.*
%attr(0755,root,root) %{_libdir}/trafficserver/plugins/*.so
%config(noreplace) /etc/trafficserver/*
%if %{rhelver} > 6
%attr(0644, root, root) /lib/systemd/system/trafficserver.service
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/tmpfiles.d/trafficserver.conf
%else
%attr(0755, root, root) /etc/init.d/trafficserver
%endif
%attr(0755, ats, ats) %dir /etc/trafficserver
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/sysconfig/trafficserver
%dir /var/log/trafficserver
%dir /var/run/trafficserver
%dir /var/cache/trafficserver

## specific for version 4 -- no need for version 3
/usr/bin/tspush
/usr/share/man/man3/Apache::TS.3pm.gz
/usr/share/man/man3/Apache::TS::AdminClient.3pm.gz
/usr/share/man/man3/Apache::TS::Config::Records.3pm.gz

%if %{rhelver} >= 6
%{_libdir}/perl5/auto/Apache/TS/.packlist
%{_libdir}/perl5/perllocal.pod
%{_libdir}/trafficserver/plugins/cacheurl.la
%{_libdir}/trafficserver/plugins/gzip.la
%{_libdir}/trafficserver/plugins/libloader.la
/usr/share/perl5/Apache/TS.pm
/usr/share/perl5/Apache/TS/AdminClient.pm
/usr/share/perl5/Apache/TS/Config.pm
/usr/share/perl5/Apache/TS/Config/Records.pm
%else
%{_libdir}/perl5/site_perl/5.8.8/Apache/TS.pm
%{_libdir}/perl5/site_perl/5.8.8/Apache/TS/AdminClient.pm
%{_libdir}/perl5/site_perl/5.8.8/Apache/TS/Config.pm
%{_libdir}/perl5/site_perl/5.8.8/Apache/TS/Config/Records.pm
%{_libdir}/trafficserver/plugins/cacheurl.la
%{_libdir}/trafficserver/plugins/gzip.la
%{_libdir}/trafficserver/plugins/header_rewrite.la
%{_libdir}/trafficserver/plugins/libloader.la
%{_libdir}/perl5/5.8.8/%{rhelarch}-linux-thread-multi/perllocal.pod
%{_libdir}/perl5/site_perl/5.8.8/%{rhelarch}-linux-thread-multi/auto/Apache/TS/.packlist
%endif

%post
/sbin/ldconfig
%if %{rhelver} > 6
%systemd_post trafficserver.service
%else
if [ $1 -eq 1 ] ; then
/sbin/chkconfig --add %{name}
fi
%endif

%pre
getent group ats >/dev/null || groupadd -r ats -g 176 &>/dev/null
getent passwd ats >/dev/null || \
useradd -r -u 176 -g ats -d / -s /sbin/nologin \
	-c "Apache Traffic Server" ats &>/dev/null

%preun
%if %{rhelver} > 6
%systemd_preun trafficserver.service
%else
if [ $1 -eq 0 ] ; then
/sbin/service %{name} stop > /dev/null 2>&1
/sbin/chkconfig --del %{name}
fi
%endif

%postun
/sbin/ldconfig

%if %{rhelver} > 6
%systemd_postun_with_restart trafficserver.service
%else
if [ $1 -eq 1 ] ; then
/sbin/service trafficserver condrestart &>/dev/null || :
fi
%endif


%package devel
Summary: Apache Traffic Server development libraries and header files
Group: Development/Libraries
Requires: trafficserver = %{version}-%{release}
%description devel
The trafficserver-devel package include plug-in development libraries and
header files, and Apache httpd style module build system.

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) /usr/bin/tsxs
%attr(0755,root,root) %dir /usr/include/ts
%attr(0644,root,root) /usr/include/ts/*
%attr(0755,root,root) %dir %{_libdir}/trafficserver
%attr(0755,root,root) %dir %{_libdir}/trafficserver/plugins
%attr(0644,root,root) %{_libdir}/trafficserver/*.so

%changelog
* Thu Oct 3 2013 mustafa@bigraf.com - 4.0.1-1

* Tue Oct 1 2013 mustafa@bigraf.com - 3.2.5-4
- recompile for Kloxo-MR in centos 5 and 6
- specific for rhel/centos

* Sun Aug 25 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.5-3
- bz#994224 Use rpm %configure macro, instead of calling configure
  directly.

* Fri Aug 9 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.5-2
- bz#994224 Pass RPM_OPT_FLAGS as environment variables to configure,
  instead of overriding on make commandline. Thanks Dimitry Andric!

* Thu Aug 1 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.5-1
- Update to v3.2.5 which fixes the following bugs:

  [TS-1923] Fix memory issue caused by resolve_logfield_string()
  [TS-1918] SSL hangs after origin handshake.
  [TS-1483] Manager uses hardcoded FD limit causing restarts forever on traffic_server.
  [TS-1784] Fix FreeBSD block calculation (both RAW and directory)
  [TS-1905] TS hangs (dead lock) on HTTPS POST/PROPFIND requests.
  [TS-1785, TS-1904] Fixes to make it build with gcc-4.8.x.
  [TS-1903] Remove JEMALLOC_P use, it seems to have been deprecated.
  [TS-1902] Remove iconv as dependency.
  [TS-1900] Detect and link libhwloc on Ubuntu.
  [TS-1470] Fix cache sizes > 16TB (part 2 - Don't reset the cache after restart)

* Mon Jun 3 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.4-3
- Harden build with PIE flags, ref bz#955127. 

* Sat Jan 19 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.4-1
- Update to 3.2.4 release candiate

* Fri Jan 4 2013 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.3-1
- Update to v3.2.3. Remove patches no longer needed.

* Fri Aug 24 2012 Václav Pavlín <vpavlin@redhat.com> - 3.2.0-6
- Scriptlets replaced with new systemd macros (#851462)

* Thu Aug 16 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.0-5
- Add patch for TS-1392, to fix problem with SNI fallback.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.0-2
- Remove duplicate man-pages.

* Sat Jun 23 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 3.2.0-1
- Update to v3.2.0

* Sun Jun 10 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 3.0.5-1
- Remove trafficserver-gcc47.patch since it's fixed upstream, TS-1116.
- Join trafficserver-condrestart.patch into trafficserver-init_scripts.patch,
  and clean out not needed junk.

* Fri Apr 13 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 3.0.4-5
- Add hardened build.

* Wed Apr 11 2012 <janfrode@tanso.net> - 3.0.4-4
- Add patch for gcc-4.7 build issues.

* Mon Apr 9 2012 Dan Horák <dan[at]danny.cz> - 3.0.4-3
- switch to ExclusiveArch

* Fri Mar 23 2012 <janfrode@tanso.net> - 3.0.4-2
- Create /var/run/trafficserver using tmpfiles.d on f15+.

* Thu Mar 22 2012 <janfrode@tanso.net> - 3.0.4-1
- Update to new upstream release, v3.0.4.
- remove trafficserver-cluster_interface_linux.patch since this was fixed upstream, TS-845.

* Thu Mar 22 2012 <janfrode@tanso.net> - 3.0.3-6
- Remove pidfile from systemd service file. This is a type=simple
  service, so pidfile shouldn't be needed.

* Wed Mar 21 2012 <janfrode@tanso.net> - 3.0.3-5
- Add systemd support.
- Drop init.d-script on systemd-systems.

* Sun Mar 18 2012 <janfrode@tanso.net> - 3.0.3-3
- change default proxy.config.proxy_name to FIXME.example.com instead of the
  name of the buildhost
- configure proxy.config.ssl.server.cert.path and
  proxy.config.ssl.server.private_key.path to point to the standard /etc/pki/
  locations.

* Tue Mar 13 2012 <janfrode@tanso.net> - 3.0.3-2
- exclude ppc/ppc64 since build there fails, TS-1131.

* Sat Mar 10 2012 <janfrode@tanso.net> - 3.0.3-1
- Removed mixed use of spaces and tabs in specfile.

* Mon Feb 13 2012 <janfrode@tanso.net> - 3.0.3-0
- Update to v3.0.3

* Thu Dec 8 2011 <janfrode@tanso.net> - 3.0.2-0
- Update to v3.0.2
- Fix conderestart in initscript, TS-885.

* Tue Jul 19 2011 <janfrode@tanso.net> - 3.0.1-0
- Update to v3.0.1
- Remove uninstall-hook from trafficserver_make_install.patch, removed in v3.0.1.

* Thu Jun 30 2011 <janfrode@tanso.net> - 3.0.0-6
- Note FIXME's on top.
- Remove .la and static libs.
- mktemp'd buildroot.
- include license

* Mon Jun 27 2011 <janfrode@tanso.net> - 3.0.0-5
- Rename patches to start with trafficserver-.
- Remove odd version macro.
- Clean up mixed-use-of-spaces-and-tabs.

* Wed Jun 23 2011 <janfrode@tanso.net> - 3.0.0-4
- Use dedicated user/group ats/ats.
- Restart on upgrades.

* Thu Jun 16 2011 <zym@apache.org> - 3.0.0-3
- update man pages, sugest from Jan-Frode Myklebust <janfrode@tanso.net>
- patch records.config to fix the crashing with cluster iface is noexist
- cleanup spec file

* Wed Jun 15 2011 <zym@apache.org> - 3.0.0-2
- bump to version 3.0.0 stable release
- cleanup the spec file and patches

* Tue May 24 2011 <yonghao@taobao.com> - 2.1.8-2
- fix tcl linking

* Thu May  5 2011 <yonghao@taobao.com> - 2.1.8-1
- bump to 2.1.8
- comment out wccp

* Fri Apr  1 2011 <yonghao@taobao.com> - 2.1.7-3
- enable wccp and fixed compile warning
- never depends on sqlite and db4, add libz and xz-libs
- fix libary permission, do post ldconfig updates

* Sun Mar 27 2011 <yonghao@taobao.com> - 2.1.7-2
- patch traffic_shell fix

* Tue Mar 22 2011 <yonghao@taobao.com> - 2.1.7-1
- bump to v2.1.7
- fix centos5 building
- drop duplicated patches

* Tue Mar 19 2011 <yonghao@taobao.com> - 2.1.6-2
- fix gcc 4.6 building
- split into -devel package for devel libs
- fix init scripts for rpmlint requirement
- fix install scripts to build in mock, without root privileges

* Tue Mar 01 2011 <yonghao@taobao.com> - 2.1.6-1
- bump to 2.1.6 unstable
- replace config layout name as Fedora

* Thu Nov 18 2010 <yonghao@taobao.com> - 2.1.4
- initial release for public
- original spec file is from neomanontheway@gmail.com
