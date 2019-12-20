%if 0%{?rhel} >= 7
# Only works on EL7
%global _hardened_build 1
%endif
%global backends %{nil}


Summary:		PowerDNS is a Versatile Database Driven Nameserver
Name:			pdns
Version:		4.1.8
Release:		1.kng%{dist}
Epoch:			0
License:		GPLv2
Group:			System Environment/Daemons
URL:			http://www.powerdns.com/
Source0:		http://downloads.powerdns.com/releases/%{name}-%{version}.tar.bz2
Patch0:			pdns-git-init.patch
Patch1:			pdns-4.1.1-disable-secpoll.patch
%if 0%{?rhel} < 7
Source1: pdns.init
%endif
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} >= 7
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: systemd
BuildRequires: systemd-units
BuildRequires: systemd-devel

BuildRequires: protobuf-devel
BuildRequires: protobuf-compiler
BuildRequires: p11-kit-devel
BuildRequires: libcurl-devel
BuildRequires: boost-devel
%else
BuildRequires: boost148-devel
BuildRequires: boost148-program-options
BuildRequires: devtoolset-8
%endif


Requires(pre): shadow-utils
BuildRequires: lua-devel 
%define lua_implementation lua

BuildRequires: bison	
BuildRequires: boost-devel	
BuildRequires: gcc-c++	
BuildRequires: libsodium-devel	
BuildRequires: lua-devel	
BuildRequires: openssl-devel	
BuildRequires: protobuf-compiler	
BuildRequires: protobuf-devel		
BuildRequires: libsodium-devel
BuildRequires: bison
BuildRequires: openssl-devel

BuildRequires:		openssl-devel
BuildRequires:		boost-devel
BuildRequires:		sqlite-devel

Provides:		powerdns = %{version}-%{release}
Obsoletes:		pdns-server
Obsoletes:		pdns-server-dnssec-tools
Obsoletes:		pdns-server-backend-bind

%global backends %{backends} bind

%description
The PowerDNS Nameserver is a modern, advanced and high performance
authoritative-only nameserver. It is written from scratch and conforms
to all relevant DNS standards documents.
Furthermore, PowerDNS interfaces with almost any database.

%package tools
Summary: Extra tools for %{name}
Group: System Environment/Daemons

%description tools
This package contains the extra tools for %{name}

%package backend-mysql
Summary: MySQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: mysql-devel
%global backends %{backends} gmysql

%description backend-mysql
This package contains the gmysql backend for %{name}

%package backend-postgresql
Summary: PostgreSQL backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: postgresql-devel
%global backends %{backends} gpgsql

%description backend-postgresql
This package contains the gpgsql backend for %{name}

%package backend-pipe
Summary: Pipe backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} pipe

%description backend-pipe
This package contains the pipe backend for %{name}

%package backend-remote
Summary: Remote backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
%global backends %{backends} remote

%description backend-remote
This package contains the remote backend for %{name}

%package backend-ldap
Summary: LDAP backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: openldap-devel
%global backends %{backends} ldap

%description backend-ldap
This package contains the LDAP backend for %{name}


%package backend-sqlite
Summary: SQLite backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: sqlite-devel
%global backends %{backends} gsqlite3

%description backend-sqlite
This package contains the SQLite backend for %{name}

%if 0%{?rhel} >= 7
%package backend-odbc
Summary: UnixODBC backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: unixODBC-devel
%global backends %{backends} godbc

%description backend-odbc
This package contains the godbc backend for %{name}

%package backend-geoip
Summary: Geo backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: yaml-cpp-devel
%if 0%{?rhel} <= 7
BuildRequires: geoip-devel
%endif
BuildRequires: libmaxminddb-devel
%global backends %{backends} geoip

%description backend-geoip
This package contains the geoip backend for %{name}
It allows different answers to DNS queries coming from different
IP address ranges or based on the geoipgraphic location

%package backend-lmdb
Summary: LMDB backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: lmdb-devel
%global backends %{backends} lmdb

%description backend-lmdb
This package contains the lmdb backend for %{name}

%package backend-tinydns
Summary: TinyDNS backend for %{name}
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: tinycdb-devel
%global backends %{backends} tinydns

%description backend-tinydns
This package contains the TinyDNS backend for %{name}

%package ixfrdist
BuildRequires: yaml-cpp-devel
Summary: A progrm to redistribute zones over AXFR and IXFR
Group: System Environment/Daemons

%description ixfrdist
This package contains the ixfrdist program.
%endif


%prep

%if 0%{?rhel} == 6
%setup -n %{name}-%{version}
%else
%autosetup -p1 -n %{name}-%{version}
%endif

#we will use the above not hardcoded names
#%setup -q -n pdns-4.1.8
# we use original init script
#%patch0 -p1 -b .init
# not sure why we need this patch
#%patch1 -p1 -b .disable-secpoll

%build
export CPPFLAGS="-DLDAP_DEPRECATED"
# we comment since its not applicable in our version
%if 0%{?rhel} == 6
. /opt/rh/devtoolset-8/enable
%endif

%configure \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --disable-static \
  --disable-dependency-tracking \
  --disable-silent-rules \
  --with-modules='' \
  --with-lua \
# we dont need all so we select  
  --with-dynmodules='%{backends} random' \
  --enable-tools \
# we need to use enable instead of with since we are bellow 4.2
#  --with-libsodium \
  --enable-libsodium \
  --enable-unit-tests \
%if 0%{?rhel} >= 7
  --enable-lua-records \
  --enable-experimental-pkcs11 \
  --enable-systemd \
  --enable-ixfrdist \
%else
#  comments as it not applicable bellow 4.2
  --disable-lua-records \
  --without-protobuf \
  --with-boost=/usr/include/boost148/ LDFLAGS=-L/usr/lib64/boost148 \
  CXXFLAGS=-std=gnu++11
%endif

#we will use the above more feature rich configure
#%configure \
#   --sysconfdir=%{_sysconfdir}/%{name} \
#    --with-sqlite3 \
#    --with-lua=%{!?_without_lua:yes}%{?_without_lua:no} \
#    --enable-hardening=%{hardening} \
#    --with-modules="" \
#    --with-dynmodules="bind gmysql gpgsql gsqlite3 ldap lua mydns pipe remote" \
#    --disable-static \
#    --enable-tools


%{__make} %{?_smp_mflags}

%install
#cleaning up the build just in case
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

make install DESTDIR=%{buildroot}

#%{__make} DESTDIR=%{buildroot} install
#%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la

%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la
%{__rm} -rf %{buildroot}%{_docdir}

%if 0%{?rhel} == 6
%{__install} -D -p %{SOURCE1} %{buildroot}%{_initrddir}/pdns
%endif

# no use for this 
#install -d %{buildroot}%{_sysconfdir}/%{name}/

%{buildroot}/usr/sbin/pdns_server --no-config --config | sed \
  -e 's!# daemon=.*!daemon=no!' \
  -e 's!# guardian=.*!guardian=no!' \
  -e 's!# launch=.*!&\\nlaunch=!' \
  -e 's!# setgid=.*!setgid=pdns!' \
  -e 's!# setuid=.*!setuid=pdns!' \
  > %{buildroot}%{_sysconfdir}/%{name}/pdns.conf
%{__rm} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf-dist
%{__rm} %{buildroot}/usr/bin/stubquery

chmod 600 %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

# fix the config no need for this anymore
#%{__mv} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf-dist %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

# we set the config above another method 
#cat >> %{buildroot}%{_sysconfdir}/%{name}/pdns.conf << EOF
#setuid=pdns
#setgid=pdns
#EOF

chmod 600 %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

%if 0%{?rhel} >= 7
# rename zone2ldap to pdns-zone2ldap (#1193116)
%{__mv} %{buildroot}/%{_bindir}/zone2ldap %{buildroot}/%{_bindir}/pdns-zone2ldap
%{__mv} %{buildroot}/%{_mandir}/man1/zone2ldap.1 %{buildroot}/%{_mandir}/man1/pdns-zone2ldap.1
%endif


# install sysv scripts not needed we use them on setup
#install -d %{buildroot}%{_initrddir}
#install -m755 pdns/pdns.init %{buildroot}%{_initrddir}/pdns

%check
PDNS_TEST_NO_IPV6=1 make %{?_smp_mflags} -C pdns check || (cat pdns/test-suite.log && false)


%pre
getent group pdns >/dev/null || groupadd -r pdns
getent passwd pdns >/dev/null || \
	useradd -r -g pdns -d / -s /sbin/nologin \
	-c "PowerDNS authoritative server user" pdns
exit 0

%if 0%{?rhel} >= 7
if [ "`stat -c '%U:%G' %{_sysconfdir}/%{name}`" = "root:root" ]; then
  chown -R root:pdns /etc/powerdns
  # Make sure that pdns can read it; the default used to be 0600
  chmod g+r /etc/powerdns/pdns.conf
fi
chown -R pdns:pdns /var/lib/powerdns || :
%endif

%post
%if 0%{?rhel} >= 7
%systemd_post pdns.service
%else
/sbin/chkconfig --add pdns
%endif

%preun
%if 0%{?rhel} >= 7
%systemd_preun pdns.service
%else
if [ $1 -eq 0 ]; then
  /sbin/service pdns stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del pdns
fi
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun_with_restart pdns.service
%else
if [ $1 -ge 1 ]; then
  /sbin/service pdns condrestart >/dev/null 2>&1 || :
fi
%endif


%files
%doc COPYING README
%{_bindir}/pdns_control
%{_bindir}/pdnsutil
%{_bindir}/zone2sql
%{_bindir}/zone2json
%{_sbindir}/pdns_server
%{_libdir}/%{name}/libbindbackend.so
%{_mandir}/man1/pdns_control.1.gz
%{_mandir}/man1/pdns_server.1.gz
%{_mandir}/man1/zone2sql.1.gz
%{_mandir}/man1/zone2json.1.gz
%{_mandir}/man1/pdnsutil.1.gz
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/librandombackend.so
%config(noreplace) %{_sysconfdir}/%{name}/pdns.conf

%if 0%{?rhel} >= 7
%{_bindir}/pdns-zone2ldap
%{_mandir}/man1/pdns-zone2ldap.1.gz
%{_unitdir}/pdns.service
%{_unitdir}/pdns@.service
%else
%{_bindir}/zone2ldap
%{_mandir}/man1/zone2ldap.1.gz
%{_initrddir}/pdns
%endif

%files tools
%{_bindir}/calidns
%{_bindir}/dnsgram
%{_bindir}/dnsreplay
%{_bindir}/dnsscan
%{_bindir}/dnsscope
%{_bindir}/dnswasher
%{_bindir}/dumresp
%{_bindir}/ixplore
%{_bindir}/pdns_notify
%{_bindir}/nproxy
%{_bindir}/nsec3dig
%{_bindir}/saxfr
%{_bindir}/sdig
%{_mandir}/man1/calidns.1.gz
%{_mandir}/man1/dnsgram.1.gz
%{_mandir}/man1/dnsreplay.1.gz
%{_mandir}/man1/dnsscan.1.gz
%{_mandir}/man1/dnsscope.1.gz
%{_mandir}/man1/dnswasher.1.gz
%{_mandir}/man1/dumresp.1.gz
%{_mandir}/man1/ixplore.1.gz
%{_mandir}/man1/pdns_notify.1.gz
%{_mandir}/man1/nproxy.1.gz
%{_mandir}/man1/nsec3dig.1.gz
%{_mandir}/man1/saxfr.1.gz
%{_mandir}/man1/sdig.1.gz
%{_bindir}/dnsbulktest
%{_bindir}/dnspcap2calidns
%{_bindir}/dnstcpbench
%{_mandir}/man1/dnsbulktest.1.gz
%{_mandir}/man1/dnspcap2calidns.1.gz
%{_mandir}/man1/dnstcpbench.1.gz
%if 0%{?rhel} >= 7
%{_bindir}/dnspcap2protobuf
%{_mandir}/man1/dnspcap2protobuf.1.gz
%endif

%files backend-mysql
%doc modules/gmysqlbackend/schema.mysql.sql
%doc modules/gmysqlbackend/dnssec-3.x_to_3.4.0_schema.mysql.sql
%doc modules/gmysqlbackend/nodnssec-3.x_to_3.4.0_schema.mysql.sql
%{_libdir}/%{name}/libgmysqlbackend.so

%files backend-postgresql
%doc modules/gpgsqlbackend/schema.pgsql.sql
%doc modules/gpgsqlbackend/dnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc modules/gpgsqlbackend/nodnssec-3.x_to_3.4.0_schema.pgsql.sql
%{_libdir}/%{name}/libgpgsqlbackend.so

%files backend-pipe
%{_libdir}/%{name}/libpipebackend.so

%files backend-remote
%{_libdir}/%{name}/libremotebackend.so

%files backend-ldap
%{_libdir}/%{name}/libldapbackend.so

%doc modules/ldapbackend/dnsdomain2.schema
%doc modules/ldapbackend/pdns-domaininfo.schema


%files backend-sqlite
%doc modules/gsqlite3backend/schema.sqlite3.sql
%doc modules/gsqlite3backend/dnssec-3.x_to_3.4.0_schema.sqlite3.sql
%doc modules/gsqlite3backend/nodnssec-3.x_to_3.4.0_schema.sqlite3.sql
%{_libdir}/%{name}/libgsqlite3backend.so

%if 0%{?rhel} >= 7
%files backend-odbc
%doc modules/godbcbackend/schema.mssql.sql
%{_libdir}/%{name}/libgodbcbackend.so

%files backend-geoip
%{_libdir}/%{name}/libgeoipbackend.so

%files backend-lmdb
%{_libdir}/%{name}/liblmdbbackend.so

%files backend-tinydns
%{_libdir}/%{name}/libtinydnsbackend.so

%files ixfrdist
%{_bindir}/ixfrdist
%{_mandir}/man1/ixfrdist.1.gz
%{_mandir}/man5/ixfrdist.yml.5.gz
%{_sysconfdir}/%{name}/ixfrdist.example.yml
%{_unitdir}/ixfrdist.service
%{_unitdir}/ixfrdist@.service
%endif

%changelog
* Fri Dec 20 2019 Dionysis Kladis <dkstiler@gmail.com> 4.1.8-1.kng
- Fixign hardcoded paths
- fix spec file to woth without input
- make the spec file compatible with centos 6 and centos 7 based on pdns original repo
- included the original init from pdns repo and handling it 

* Fri Mar 22 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.8-1
- update to version 4.1.8

* Mon Mar 18 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.7-1
- update to version 4.1.7

* Wed Jan 30 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.6-1
- update to version 4.1.6

* Tue Nov 06 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.5-1
- update to version 4.1.5

* Wed Aug 29 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.4-1
- update to version 4.1.4

* Thu May 24 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.3-1
- update to version 4.1.3

* Mon May 07 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.2-1
- update to version 4.1.2

* Fri Feb 16 2018 Kees Monshouwer <mind04@monshouwer.org> 4.1.1-1
- update to version 4.1.1

* Thu Nov 30 2017 Kees Monshouwer <mind04@monshouwer.org> 4.1.0-1
- update to version 4.1.0

* Mon Nov 27 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.5-1
- update to version 4.0.5

* Thu Jun 22 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.4-1
- update to version 4.0.4
- remove el5 specific parts from spec file

* Tue Jan 17 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.3-1
- update to version 4.0.3

* Fri Jan 13 2017 Kees Monshouwer <mind04@monshouwer.org> 4.0.2-1
- update to version 4.0.2

* Fri Jul 29 2016 Kees Monshouwer <mind04@monshouwer.org> 4.0.1-1
- update to version 4.0.1

* Mon Jul 11 2016 Kees Monshouwer <mind04@monshouwer.org> 4.0.0-1
- update to version 4.0.0
- add ixplore, sdig and dnspcap2protobuf to tools
- rename pdnssec to pdnsutil
- remove geo backend

* Thu Aug 27 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.6-1
- update to version 3.4.6

* Tue Jun 09 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.5-1
- update to version 3.4.5

* Thu Apr 23 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.4-1
- update to version 3.4.4

* Mon Mar 02 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.3-1
- update to version 3.4.3

* Tue Feb 03 2015 Kees Monshouwer <mind04@monshouwer.org> 3.4.2-1
- update to version 3.4.2
- move all manpages to section 1
- markdown based documentation

* Thu Oct 30 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.1-1
- update to 3.4.1
- disable security status polling by default https://github.com/PowerDNS/pdns/blob/master/pdns/docs/security-poll.md

* Sat Oct 11 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.0-2
- reorder spec file
- rename backend-sqlite3 to backend-sqlite
- add lua backend

* Tue Sep 30 2014 Kees Monshouwer <mind04@monshouwer.org> 3.4.0-1
- Update to 3.4.0
- Rename package from pdns-server to pdns
- Changed user from powerdns to pdns
- Changed module location
- New and migration .sql files after the schema change
- Add saxfr to pdns-tools
- Bind backend is now a dynmodule
- Add mydns backend

* Mon Jan 20 2014 Kees Monshouwer <mind04@monshouwer.org> 3.3.1-2
- Fix pdns-tools dependency problem

* Tue Dec 17 2013 Kees Monshouwer <mind04@monshouwer.org> 3.3.1-1
- Update to 3.3.1

* Mon Jul 08 2013 Kees Monshouwer <mind04@monshouwer.org> 3.3-2
- Add remote backend

* Fri Jul 05 2013 Kees Monshouwer <mind04@monshouwer.org> 3.3-1
- Update to 3.3
- Add geo backend

* Thu Jan 17 2013 Kees Monshouwer <mind04@monshouwer.org> 3.2-1
- Update to 3.2
- Add sqlite3 backend

* Wed Sep 05 2012 Kees Monshouwer <mind04@monshouwer.org> 3.1-2
- Fix powerdns user and primary group creation
- Improve spec file

* Fri May 04 2012 Kees Monshouwer <mind04@monshouwer.org> 3.1-1
- Update to 3.1

* Sun Jan 08 2012 Kees Monshouwer <mind04@monshouwer.org> 3.0.1-1
- Update to 3.0.1

* Fri Jul 22 2011 Kees Monshouwer <mind04@monshouwer.org> 3.0-1
- Initial build for PowerDNS 3.0
