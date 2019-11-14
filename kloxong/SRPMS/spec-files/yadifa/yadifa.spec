## MR -- enable this if want create debuginfo
%define  debug_package %{nil}

%global _hardened_build	1

# version revision
%global revision	6937

%if 0%{?rhel} >= 7
%global _with_systemd	1
%endif
%if 0%{?fedora}
%global _with_systemd	1
%endif

Name:		yadifa
Version:	2.2.5
Release:	1.kng%{?dist}
Summary:	Lightweight authoritative Name Server with DNSSEC capabilities

Group:		System Environment/Daemons
License:	BSD
URL:		http://www.yadifa.eu
Source0:	http://cdn.yadifa.eu/sites/default/files/releases/%{name}-%{version}-%{revision}.tar.gz
Source1:	yadifad.service
Source2:	yadifad.init
Source3:	yadifa.logrotate

BuildRequires:	gcc, coreutils, findutils, make, openssl-devel, sed

Requires:	yadifa-libs = %{version}-%{release}

%if 0%{?_with_systemd}
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
BuildRequires:	systemd
%else
Requires(post):	chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif


%description
YADIFA is a name server implementation developed from scratch by .eu.
It is portable across multiple operating systems and supports DNSSEC,
TSIG, DNS notify, DNS update, IPv6.

%package libs
Summary:	Libraries used by the YADIFA packages
Group:		Applications/System

%description libs
Contains libraries used by YADIFA DNS server

%package tools
Summary:	Remote management client for YADIFA DNS server
Group:		Applications/System

%description tools
Contains utility for YADIFA DNS server remote management

%package devel
Summary:	Header files and libraries needed for YADIFA development
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The yadifa-devel package contains header files and libraries
required for development with YADIFA DNS server


%prep
%setup -q -n %{name}-%{version}-%{revision}

%build
export CPPFLAGS="%{optflags} -DNDEBUG -g"
export LDFLAGS="$LDFLAGS -lssl -lcrypto"

%configure \
    --with-tools \
    --enable-rrl \
    --enable-nsid \
    --enable-ctrl \
    --enable-dynamic-provisioning \
    --enable-shared \
    --disable-static

# don't mess with rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/libtool
# avoid unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/libtool
# adjust build options
sed -i 's|-mtune=native||g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i 's|= -fno-ident|=|g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i 's|= -ansi|=|g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i 's|= -pedantic|=|g' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i '/^YRCFLAGS = -DNDEBUG $(CCOPTIMISATIONFLAGS) -DCMR/d' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i '/^YPCFLAGS = -DNDEBUG $(CCOPTIMISATIONFLAGS) -pg -DCMP/d' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
sed -i '/^YDCFLAGS = -DDEBUG $(DEBUGFLAGS) -DCMD/d' \
    {.,bin/yadifa,lib/dnscore,lib/dnsdb,lib/dnslg,lib/dnszone,sbin/yadifad}/Makefile
# change configuration options
sed -i '/daemon/s|off|on|g' etc/yadifad.conf.example
# adjust additional key options
sed -i 's|^include "keys.conf"|#include "keys.conf"|' etc/yadifad.conf.example
sed -i '/^<\/key>/a \ \n<key>\n \ name \ abroad-admin-key\n \ algorithm \ hmac-md5\n \ secret \ AbroadAdminTSIGKey==\n<\/key>' \
    etc/yadifad.conf.example

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -Dpm 0644 etc/yadifad.conf.example %{buildroot}%{_sysconfdir}/yadifad.conf
mkdir -p %{buildroot}%{_localstatedir}/log/yadifa
rm -f %{buildroot}%{_libdir}/*.la
# rhel6 workaround
rm -rf %{buildroot}%{_defaultdocdir}/yadifa

# bash completion
for comp in yadifa yadifad; do
install -Dpm 0644 etc/${comp}.bash_completion \
    %{buildroot}%{_datadir}/bash-completion/completions/${comp}
done

%if 0%{?_with_systemd}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/yadifad.service
%else
install -Dpm 0755 %{SOURCE2} %{buildroot}%{_initrddir}/yadifad
%endif

install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/yadifa


%post
%if 0%{?_with_systemd}
%systemd_post yadifad.service
%else
/sbin/chkconfig --add yadifad
%endif
exit 0

%preun
%if 0%{?_with_systemd}
%systemd_preun yadifad.service
%else
if [ $1 = 0 ]; then
	/sbin/service yadifad stop > /dev/null 2>&1
	/sbin/chkconfig --del yadifad
fi
%endif
exit 0

%postun
%if 0%{?_with_systemd}
%systemd_postun_with_restart yadifad.service
%else
if [ "$1" -ge "1" ]; then
	/sbin/service yadifad condrestart > /dev/null 2>&1
fi
%endif
exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README
# rhel6 workaround
%doc etc/*.conf.example
%config(noreplace) %{_sysconfdir}/yadifad.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/yadifa
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/yadifad
%if 0%{?_with_systemd}
%{_unitdir}/yadifad.service
%else
%{_initrddir}/yadifad
%endif
%{_localstatedir}/zones
%{_localstatedir}/log/yadifa
%{_sbindir}/yadifad
%{_mandir}/man5/yadifa.*.5*
%{_mandir}/man5/yadifad.*.5*
%{_mandir}/man8/yadifad.8*

%files libs
%{_libdir}/libdnscore.so.3*
%{_libdir}/libdnsdb.so.3*
%{_libdir}/libdnslg.so.2*
%{_libdir}/libdnszone.so.2*

%files tools
%license COPYING
%doc AUTHORS
%{_bindir}/yadifa
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/yadifa
%{_mandir}/man8/yadifa.8*

%files devel
%{_includedir}/dnscore
%{_includedir}/dnsdb
%{_includedir}/dnslg
%{_includedir}/dnszone
%{_libdir}/libdnscore.so
%{_libdir}/libdnsdb.so
%{_libdir}/libdnslg.so
%{_libdir}/libdnszone.so


%changelog
* Mon Aug 07 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 2.2.5-1
- Update to 2.2.5 release

* Sat Dec 24 2016 Denis Fateyev <denis@fateyev.com> - 2.2.3-1
- Update to 2.2.3 release

* Sat Sep 03 2016 Denis Fateyev <denis@fateyev.com> - 2.2.1-1
- Update to 2.2.1 release

* Sat Jul 16 2016 Denis Fateyev <denis@fateyev.com> - 2.2.0-1
- Update to 2.2.0 release

* Tue Feb 23 2016 Denis Fateyev <denis@fateyev.com> - 2.1.6-1
- Update to 2.1.6 release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Denis Fateyev <denis@fateyev.com> - 2.1.5-1
- Update to 2.1.5 release

* Wed Sep 30 2015 Denis Fateyev <denis@fateyev.com> - 2.1.3-1
- Update to 2.1.3 release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Denis Fateyev <denis@fateyev.com> - 2.0.6-1
- Update to 2.0.6 release

* Sun Dec 21 2014 Denis Fateyev <denis@fateyev.com> - 2.0.4-1
- Update to 2.0.4 release

* Sat Oct 18 2014 Denis Fateyev <denis@fateyev.com> - 2.0.0-1
- Update to 2.0.0 release
- New program features added

* Thu Aug 28 2014 Denis Fateyev <denis@fateyev.com> - 1.0.3-2
- Build options clarification
- Minor specfile cleanup

* Sat Aug 16 2014 Denis Fateyev <denis@fateyev.com> - 1.0.3-1
- Initial Fedora RPM release
