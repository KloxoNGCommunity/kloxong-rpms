#
# PowerDNS server el5/el6 spec file
#
# - to disable devtoolset-2 use --without devtoolset
# - to disable lua use --without lua
#
%{?!rhel:%define rhel 0}
%if 0%{?rhel} == 5
%define hardening no
%else
%define hardening yes
%endif


Summary:		PowerDNS is a Versatile Database Driven Nameserver
Name:			pdns
Version:		4.1.13
Release:		1%{dist}
Epoch:			0
License:		GPLv2
Group:			System Environment/Daemons
URL:			http://www.powerdns.com/
Source0:		http://downloads.powerdns.com/releases/pdns-4.1.13.tar.bz2
Patch0:			pdns-git-init.patch
Patch1:			pdns-4.1.1-disable-secpoll.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%if %{!?_without_devtoolset:1}%{?_without_devtoolset:0}
BuildRequires:		devtoolset-8-gcc devtoolset-8-gcc-c++
BuildRequires:		devtoolset-8-binutils
%endif

BuildRequires:		openssl-devel
BuildRequires:		boost-devel
BuildRequires:		sqlite-devel

%if %{!?_without_lua:1}%{?_without_lua:0}
BuildRequires:		lua-devel
%endif

Provides:		powerdns = %{version}-%{release}
Obsoletes:		pdns-server
Obsoletes:		pdns-server-dnssec-tools
Obsoletes:		pdns-server-backend-bind


%description
PowerDNS is a versatile nameserver which supports a large number
of different backends ranging from simple zonefiles to relational
databases and load balancing/failover algorithms.

%package		backend-bind
Summary:		Bind backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description		backend-bind
The BindBackend parses a Bind-style named.conf and extracts information about
zones from it. It makes no attempt to honour other configuration flags,
which you should configure (when available) using the PDNS native configuration.

%package		backend-mysql
Summary:		MySQL backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		mysql-devel
Obsoletes:		pdns-server-backend-mysql

%description		backend-mysql
This package contains the MySQL backend for the PowerDNS nameserver.

%package		backend-postgresql
Summary:		postgesql backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		postgresql-devel
Obsoletes:		pdns-server-backend-postgresql

%description		backend-postgresql
This package contains the postgesql backend for the PowerDNS nameserver.

%package		backend-sqlite
Summary:		sqlite3 backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		sqlite-devel
Obsoletes:		pdns-server-backend-sqlite3
Obsoletes:		pdns-backend-sqlite3 < 3.4.0-2

%description		backend-sqlite
This package contains the sqlite3 backend for the PowerDNS nameserver.

%package		backend-ldap
Summary:		LDAP backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		openldap-devel
Obsoletes:		pdns-server-backend-ldap

%description		backend-ldap
This package contains the LDAP backend for the PowerDNS nameserver.

%package		backend-lua
Summary:		Lua backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{version}-%{release}
BuildRequires:		lua-devel

%description		backend-lua
This package contains the Lua backent for the PowerDNS nameserver.

%package		backend-mydns
Summary:		MyDNS backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
BuildRequires:		mysql-devel

%description		backend-mydns
This package contains the MyDNS backend for the PowerDNS nameserver.

%package		backend-pipe
Summary:		Pipe/coprocess backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:		pdns-server-backend-pipe

%description		backend-pipe
This package contains the pipe backend for the PowerDNS nameserver. This
allows PowerDNS to retrieve domain info from a process that accepts
questions on stdin and returns answers on stdout.

%package		backend-remote
Summary:		Experimental remotere backend for %{name}
Group:			System Environment/Daemons
Requires:		%{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:		pdns-server-backend-remote

%description		backend-remote
This package contains the remote backend for the PowerDNS nameserver. This
backend provides json based unix socket / pipe / http remoting for powerdns.

%package		tools
Summary:		PowerDNS DNS tools
Group:			Applications/System
Conflicts:		%{name} < %{epoch}:%{version}-%{release}
Conflicts:		%{name} > %{epoch}:%{version}-%{release}
Obsoletes:		pdns-server-tools

%description		tools
This package contains the the PowerDNS DNS tools.


%prep
%setup -q -n pdns-4.1.13
%patch0 -p1 -b .init
%patch1 -p1 -b .disable-secpoll


%build
%if %{!?_without_devtoolset:1}%{?_without_devtoolset:0}
export PATH=/opt/rh/devtoolset-8/root/usr/bin/:$PATH
%endif

%if 0%{?rhel} == 6
. /opt/rh/devtoolset-8/enable
%endif
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --with-sqlite3 \
    --with-lua=%{!?_without_lua:yes}%{?_without_lua:no} \
    --enable-hardening=%{hardening} \
    --with-modules="" \
    --with-dynmodules="bind gmysql gpgsql gsqlite3 ldap lua mydns pipe remote" \
    --disable-static \
    --enable-tools


%{__make} %{?_smp_mflags}


%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.la

install -d %{buildroot}%{_sysconfdir}/%{name}/

# fix the config
%{__mv} %{buildroot}%{_sysconfdir}/%{name}/pdns.conf-dist %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

cat >> %{buildroot}%{_sysconfdir}/%{name}/pdns.conf << EOF
setuid=pdns
setgid=pdns
EOF

chmod 600 %{buildroot}%{_sysconfdir}/%{name}/pdns.conf

# install sysv scripts
install -d %{buildroot}%{_initrddir}
install -m755 pdns/pdns.init %{buildroot}%{_initrddir}/pdns


%pre
getent group pdns >/dev/null || groupadd -r pdns
getent passwd pdns >/dev/null || \
	useradd -r -g pdns -d / -s /sbin/nologin \
	-c "PowerDNS authoritative server user" pdns
exit 0

%post
/sbin/chkconfig --add pdns

%preun
if [ $1 -eq 0 ]; then
    /sbin/service pdns stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del pdns
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service pdns condrestart >/dev/null 2>&1
fi

%files
%doc COPYING INSTALL NOTICE README
%dir %{_sysconfdir}/%{name}/
%dir %{_libdir}/%{name}/
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/%{name}/pdns.conf
%config(noreplace) %attr(0755,root,root) %{_initrddir}/pdns
%{_bindir}/pdns_control
%{_bindir}/pdnsutil
%{_sbindir}/pdns_server
%{_mandir}/man1/pdns_control.1.gz
%{_mandir}/man1/pdns_server.1.gz
%{_mandir}/man1/pdnsutil.1.gz

%files backend-bind
%{_libdir}/%{name}/libbindbackend.so
%doc pdns/bind-dnssec.schema.sqlite3.sql

%files backend-mysql
%{_libdir}/%{name}/libgmysqlbackend.so
%doc %{_defaultdocdir}/%{name}/schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.mysql.sql
%doc %{_defaultdocdir}/%{name}/3.4.0_to_4.1.0_schema.mysql.sql

%files backend-postgresql
%{_libdir}/%{name}/libgpgsqlbackend.so
%doc %{_defaultdocdir}/%{name}/schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/3.4.0_to_4.1.0_schema.pgsql.sql
%doc %{_defaultdocdir}/%{name}/4.1.10_to_4.1.11.schema.pgsql.sql

%files backend-sqlite
%{_libdir}/%{name}/libgsqlite3backend.so
%doc %{_defaultdocdir}/%{name}/schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/nodnssec-3.x_to_3.4.0_schema.sqlite3.sql
%doc %{_defaultdocdir}/%{name}/dnssec-3.x_to_3.4.0_schema.sqlite3.sql

%files backend-ldap
%{_libdir}/%{name}/libldapbackend.so
%doc %{_defaultdocdir}/%{name}/dnsdomain2.schema
%doc %{_defaultdocdir}/%{name}/pdns-domaininfo.schema

%files backend-lua
%{_libdir}/%{name}/libluabackend.so
%doc modules/luabackend/README

%files backend-mydns
%{_libdir}/%{name}/libmydnsbackend.so
%doc %{_defaultdocdir}/%{name}/schema.mydns.sql

%files backend-pipe
%{_libdir}/%{name}/libpipebackend.so

%files backend-remote
%{_libdir}/%{name}/libremotebackend.so

%files tools
%{_bindir}/zone2json
%{_bindir}/zone2ldap
%{_bindir}/zone2sql
 %{_bindir}/calidns
 %{_bindir}/dnsgram
 %{_bindir}/dnsreplay
 %{_bindir}/dnsscan
 %{_bindir}/dnsscope
 %{_bindir}/dnswasher
 %{_bindir}/dumresp
 %{_bindir}/ixplore
 %{_bindir}/nproxy
 %{_bindir}/nsec3dig
 %{_bindir}/pdns_notify
 %{_bindir}/saxfr
 %{_bindir}/sdig
 %{_bindir}/stubquery
%{_mandir}/man1/zone2json.1.gz
%{_mandir}/man1/zone2ldap.1.gz
%{_mandir}/man1/zone2sql.1.gz
 %{_mandir}/man1/calidns.1.gz
 %{_mandir}/man1/dnsgram.1.gz
 %{_mandir}/man1/dnsreplay.1.gz
 %{_mandir}/man1/dnsscan.1.gz
 %{_mandir}/man1/dnsscope.1.gz
 %{_mandir}/man1/dnswasher.1.gz
 %{_mandir}/man1/dumresp.1.gz
 %{_mandir}/man1/ixplore.1.gz
 %{_mandir}/man1/nproxy.1.gz
 %{_mandir}/man1/nsec3dig.1.gz
 %{_mandir}/man1/pdns_notify.1.gz
 %{_mandir}/man1/saxfr.1.gz
 %{_mandir}/man1/sdig.1.gz


%changelog
* Thu Aug 08 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.13-1
- update to version 4.1.13

* Wed Aug 07 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.12-1
- update to version 4.1.12

* Tue Jul 30 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.11-1
- update to version 4.1.11

* Thu Jun 20 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.10-1
- update to version 4.1.10

* Tue Jun 18 2019 Kees Monshouwer <mind04@monshouwer.org> 4.1.9-1
- update to version 4.1.9

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
