#
# Red Hat BIND package .spec file
#

%define VERSION %{version}


%{?!SDB:       %define SDB       0}
%{?!test:      %define test      0}
%{?!bind_uid:  %define bind_uid  25}
%{?!bind_gid:  %define bind_gid  25}
%{?!GSSTSIG:   %define GSSTSIG   1}
%{?!PKCS11:    %define PKCS11    0}
%define        bind_dir          /var/named
%define        chroot_prefix     %{bind_dir}/chroot
#
Summary:  The Berkeley Internet Name Domain (BIND) DNS (Domain Name System) server
Name:     bind
License:  ISC
Version:  9.9.7
Release:  1%{?dist}
#Release:  2%{?dist}
Epoch:    40
Url:      http://www.isc.org/products/BIND/
Buildroot:%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:    System Environment/Daemons
#
Source:   ftp://ftp.isc.org/isc/bind9/%{VERSION}/bind-%{VERSION}.tar.gz
Source1:  named.sysconfig
Source2:  named.init
Source3:  named.logrotate
Source4:  named.NetworkManager
Source5:  rfc1912.txt
Source7:  bind-9.3.1rc1-sdb_tools-Makefile.in
Source8:  dnszone.schema
Source12: README.sdb_pgsql
Source21: Copyright.caching-nameserver
Source25: named.conf.sample
Source28: config-8.tar.bz2
Source30: ldap2zone.c
Source31: named.portreserve
##!! for centos4/5
Source98: named.init.el4
Source99: flexible.m4
#Patch1:   centos5.capability.patch

#
Requires:       bind-libs = %{epoch}:%{version}-%{release}
Requires:       mktemp
Requires(post): grep, chkconfig
Requires(pre):  shadow-utils
Requires(preun):chkconfig
Obsoletes:      bind-config < 30:9.3.2-34.fc6
Provides:       bind-config = 30:9.3.2-34.fc6
Obsoletes:      caching-nameserver < 31:9.4.1-7.fc8
Provides:       caching-nameserver = 31:9.4.1-7.fc8
Obsoletes:      dnssec-conf < 1.22-6
Provides:       dnssec-conf = 1.22-6
BuildRequires:  openssl-devel, libtool, autoconf, pkgconfig, libcap-devel
BuildRequires:  libidn-devel, libxml2-devel
%if %{SDB}
BuildRequires:  openldap-devel, postgresql-devel, sqlite-devel, mysql-devel
%endif
%if %{test}
BuildRequires:  net-tools
%endif
%if %{GSSTSIG}
BuildRequires:  krb5-devel
%endif
# Needed to regenerate dig.1 manpage
BuildRequires: docbook-style-xsl, libxslt
%if "%{?dist}" == ".el6"
Requires:      portreserve
%endif

%description
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named),
which resolves host names to IP addresses; a resolver library
(routines for applications to use when interfacing with DNS); and
tools for verifying that the DNS server is operating properly.

%if %{PKCS11}
%package pkcs11
Summary: Bind PKCS#11 tools for using DNSSEC
Group:   System Environment/Daemons
Requires: engine_pkcs11 opensc
#BuildRequires: opensc-devel

%description pkcs11
This is a set of PKCS#11 utilities that when used together create rsa
keys in a PKCS11 keystore, such as provided by opencryptoki. The keys
will have a label of "zone,zsk|ksk,xxx" and an id of the keytag in hex.
%endif

%if %{SDB}
%package sdb
Summary: BIND server with database backends and DLZ support
Group:   System Environment/Daemons
Requires:bind-libs = %{epoch}:%{version}-%{release}

%description sdb
BIND (Berkeley Internet Name Domain) is an implementation of the DNS
(Domain Name System) protocols. BIND includes a DNS server (named-sdb)
which has compiled-in SDB (Simplified Database Backend) which includes
support for using alternative Zone Databases stored in an LDAP server
(ldapdb), a postgreSQL database (pgsqldb), an sqlite database (sqlitedb),
or in the filesystem (dirdb), in addition to the standard in-memory RBT
(Red Black Tree) zone database. It also includes support for DLZ
(Dynamic Loadable Zones)
%endif

%package libs
Summary:  Libraries used by the BIND DNS packages
Group:    Applications/System
Obsoletes:bind-libbind-devel < 31:9.3.3-4.fc7
Provides: bind-libbind-devel = 31:9.3.3-4.fc7

%description libs
Contains libraries used by both the bind server package as well as the utils
packages.

%package utils
Summary: Utilities for querying DNS name servers
Group:   Applications/System
Requires:bind-libs = %{epoch}:%{version}-%{release}

%description utils
Bind-utils contains a collection of utilities for querying DNS (Domain
Name System) name servers to find out information about Internet
hosts. These tools will provide you with the IP addresses for given
host names, as well as other information about registered domains and
network addresses.

You should install bind-utils if you need to get information from DNS name
servers.

%package devel
Summary:  Header files and libraries needed for BIND DNS development
Group:    Development/Libraries
Obsoletes:bind-libbind-devel < 31:9.3.3-4.fc7
Provides: bind-libbind-devel = 31:9.3.3-4.fc7
Requires: bind-libs = %{epoch}:%{version}-%{release}

%description devel
The bind-devel package contains all the header files and libraries
required for development with ISC BIND 9 and BIND 8


%package chroot
Summary:        A chroot runtime environment for the ISC BIND DNS server, named(8)
Group:          System Environment/Daemons
Prefix:         %{chroot_prefix}
Requires(post): grep
Requires(preun):grep
Requires:       bind = %{epoch}:%{version}-%{release}

%description chroot
This package contains a tree of files which can be used as a
chroot(2) jail for the named(8) program from the BIND package.
Based on the code from Jan "Yenya" Kasprzak <kas@fi.muni.cz>

%prep
%setup -q -n %{name}-%{VERSION}
#%patch1

# disable building bin/tests, missing main?
sed -i -e 's/tests //g' bin/Makefile.in
##!! add a libtool macro for centos4/5
cp -fp %{SOURCE99} libtool.m4


%build
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CPPFLAGS="$CPPFLAGS -DDIG_SIGCHASE"
export STD_CDEFINES="$CPPFLAGS"

aclocal -I libtool.m4 --force; autoconf -f

%configure \
  --with-libtool \
  --localstatedir=/var \
  --enable-threads \
  --enable-ipv6 \
  --with-pic \
  --disable-static \
  --disable-openssl-version-check \
%if %{PKCS11}
  --with-pkcs11=%{_libdir}/pkcs11/PKCS11_API.so \
%endif
%if %{SDB}
  --with-dlz-ldap=yes \
  --with-dlz-postgres=yes \
  --with-dlz-mysql=yes \
  --with-dlz-filesystem=yes \
%endif
%if %{GSSTSIG}
  --with-gssapi=yes \
  --disable-isc-spnego \
%endif
  --with-docbook-xsl=%{_datadir}/sgml/docbook/xsl-stylesheets \
%ifarch ppc ppc64
  --disable-atomic \
%endif
  --enable-fixed-rrset \
  --enable-filter-aaaa \
  --enable-rrl \
;
make %{?_smp_mflags}

# Regenerate dig.1 manpage
pushd bin/dig
make man
popd
pushd bin/nsupdate
make man
popd

%if %{test}
%check
if [ "`whoami`" = 'root' ]; then
  set -e
  chmod -R a+rwX .
  pushd bin/tests
  pushd system
  ./ifconfig.sh up
  popd
  make test
  e=$?
  pushd system
  ./ifconfig.sh down
  popd
  popd
  if [ "$e" -ne 0 ]; then
    echo "ERROR: this build of BIND failed 'make test'. Aborting."
    exit $e;
  fi;
else
  echo 'only root can run the tests (they require an ifconfig).'
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

# We don't want these
rm -f doc/rfc/fetch
mkdir -p doc/rfc
cp  --preserve=timestamps %{SOURCE5} doc/rfc
gzip -9 doc/rfc/*

# Build directory hierarchy
mkdir -p ${RPM_BUILD_ROOT}/etc/{rc.d/init.d,logrotate.d,NetworkManager/dispatcher.d}
mkdir -p ${RPM_BUILD_ROOT}/etc/portreserve
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/bind
mkdir -p ${RPM_BUILD_ROOT}/var/named/{slaves,data,dynamic}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/{man1,man5,man8}
mkdir -p ${RPM_BUILD_ROOT}/var/run/named
mkdir -p ${RPM_BUILD_ROOT}/var/log

#chroot
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/{dev,etc,var}
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/var/{log,named,run/named,tmp}
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/{pki/dnssec-keys,named}
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}/%{_libdir}/bind
# these are required to prevent them being erased during upgrade of previous
# versions that included them (bug #130121):
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/null
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/random
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/dev/zero
touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/localtime

touch ${RPM_BUILD_ROOT}/%{chroot_prefix}/etc/named.conf
#end chroot

make DESTDIR=${RPM_BUILD_ROOT} install

# Remove unwanted files
rm -f ${RPM_BUILD_ROOT}/etc/bind.keys

%if "%{?dist}" == ".el4"
install -m 755 %SOURCE98 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/named
%else
install -m 755 %SOURCE2 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/named
%endif
install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}/etc/logrotate.d/named
install -m 755 %SOURCE4 ${RPM_BUILD_ROOT}/etc/NetworkManager/dispatcher.d/13-named
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/named
%if %{SDB}
mkdir -p ${RPM_BUILD_ROOT}/etc/openldap/schema
install -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}/etc/openldap/schema/dnszone.schema
install -m 644 %{SOURCE12} contrib/sdb/pgsql/
%endif
install -m 644 %{SOURCE31} ${RPM_BUILD_ROOT}%{_sysconfdir}/portreserve/named

# Files required to run test-suite outside of build tree:
cp -fp config.h ${RPM_BUILD_ROOT}/%{_includedir}/bind9
cp -fp lib/dns/include/dns/forward.h ${RPM_BUILD_ROOT}/%{_includedir}/dns
cp -fp lib/isc/unix/include/isc/keyboard.h ${RPM_BUILD_ROOT}/%{_includedir}/isc

# Remove libtool .la files:
find ${RPM_BUILD_ROOT}/%{_libdir} -name '*.la' -exec '/bin/rm' '-f' '{}' ';';
# /usr/lib/rpm/brp-compress
#

# Ghost config files:
touch ${RPM_BUILD_ROOT}%{_localstatedir}/log/named.log

# configuration files:
tar -C ${RPM_BUILD_ROOT} -xjf %{SOURCE28}
touch ${RPM_BUILD_ROOT}/etc/rndc.key
touch ${RPM_BUILD_ROOT}/etc/rndc.conf
mkdir ${RPM_BUILD_ROOT}/etc/named
install -m 644 bind.keys ${RPM_BUILD_ROOT}/etc/named.iscdlv.key

install -m 644 %{SOURCE5}  ./rfc1912.txt
install -m 644 %{SOURCE21} ./Copyright

# sample bind configuration files for %%doc:
mkdir -p sample/etc sample/var/named/{data,slaves}
install -m 644 %{SOURCE25} sample/etc/named.conf
# Copy default configuration to %%doc to make it usable from system-config-bind
install -m 644 ${RPM_BUILD_ROOT}/etc/named.conf named.conf.default
install -m 644 ${RPM_BUILD_ROOT}/etc/named.rfc1912.zones sample/etc/named.rfc1912.zones
install -m 644 ${RPM_BUILD_ROOT}/var/named/{named.ca,named.localhost,named.loopback,named.empty}  sample/var/named
for f in my.internal.zone.db slaves/my.slave.internal.zone.db slaves/my.ddns.internal.zone.db my.external.zone.db; do
  echo '@ in soa localhost. root 1 3H 15M 1W 1D
  ns localhost.' > sample/var/named/$f;
done
:;

%pre
if [ "$1" -eq 1 ]; then
  /usr/sbin/groupadd -g %{bind_gid} -f -r named >/dev/null 2>&1 || :;
%if "%{?dist}" == ".el6"
  /usr/sbin/useradd  -u %{bind_uid} -r -N -M -g named -s /sbin/nologin -d /var/named -c Named named >/dev/null 2>&1 || :;
%else
  /usr/sbin/useradd  -u %{bind_uid} -r -n -M -g named -s /sbin/nologin -d /var/named -c Named named >/dev/null 2>&1 || :;
%endif
fi;
:;

%post
/sbin/ldconfig
/sbin/chkconfig --add named
if [ "$1" -eq 1 ]; then
  [ -x /sbin/restorecon ] && /sbin/restorecon /etc/rndc.* /etc/named.* >/dev/null 2>&1 ;
  # rndc.key has to have correct perms and ownership, CVE-2007-6283
  [ -e /etc/rndc.key ] && chown root:named /etc/rndc.key
  [ -e /etc/rndc.key ] && chmod 0640 /etc/rndc.key
fi
:;

%preun
if [ "$1" -eq 0 ]; then
  /sbin/service named stop >/dev/null 2>&1 || :;
  /sbin/chkconfig --del named || :;
fi;
:;

%postun
/sbin/ldconfig
if [ "$1" -ge 1 ]; then
  /sbin/service named try-restart >/dev/null 2>&1 || :;
fi;
:;

%if %{SDB}
%post sdb
/sbin/service named try-restart > /dev/null 2>&1 || :;

%postun sdb
/sbin/service named try-restart > /dev/null 2>&1 || :;
%endif

%triggerpostun -n bind -- bind <= 32:9.5.0-20.b1
if [ "$1" -gt 0 ]; then
  [ -e /etc/rndc.key ] && chown root:named /etc/rndc.key
  [ -e /etc/rndc.key ] && chmod 0640 /etc/rndc.key
fi
:;

%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig

# Automatically update configuration from "dnssec-conf-based" to "BIND-based"
%triggerpostun -n bind -- dnssec-conf
[ -r '/etc/named.conf' ] || exit 0
cp -fp /etc/named.conf /etc/named.conf.rpmsave
if grep -Eq '/etc/(named.dnssec.keys|pki/dnssec-keys)' /etc/named.conf; then
  if grep -q 'dlv.isc.org.conf' /etc/named.conf; then
    # DLV is configured, reconfigure it to new configuration
    sed -i -e 's/.*dnssec-lookaside.*dlv\.isc\.org\..*/dnssec-lookaside auto;\
bindkeys-file "\/etc\/named.iscdlv.key";/' /etc/named.conf
  fi
  sed -i -e '/.*named\.dnssec\.keys.*/d' -e '/.*pki\/dnssec-keys.*/d' \
    /etc/named.conf
  /sbin/service named try-restart > /dev/null 2>&1 || :;
fi

%post chroot
if [ "$1" -gt 0 ]; then
  [ -e %{chroot_prefix}/dev/random ] || \
    /bin/mknod %{chroot_prefix}/dev/random c 1 8
  [ -e %{chroot_prefix}/dev/zero ] || \
    /bin/mknod %{chroot_prefix}/dev/zero c 1 5
  [ -e %{chroot_prefix}/dev/null ] || \
    /bin/mknod %{chroot_prefix}/dev/null c 1 3
  rm -f %{chroot_prefix}/etc/localtime
  cp /etc/localtime %{chroot_prefix}/etc/localtime
  if ! grep -q '^ROOTDIR=' /etc/sysconfig/named; then
    echo 'ROOTDIR=/var/named/chroot' >> /etc/sysconfig/named
    /sbin/service named try-restart > /dev/null 2>&1 || :;
  fi
fi;
:;

%posttrans chroot
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
  [ -x /sbin/restorecon ] && /sbin/restorecon %{chroot_prefix}/dev/* > /dev/null 2>&1;
fi;
:;

%preun chroot
if [ "$1" -eq 0 ]; then
  rm -f %{chroot_prefix}/dev/{random,zero,null}
  rm -f %{chroot_prefix}/etc/localtime
  if grep -q '^ROOTDIR=' /etc/sysconfig/named; then
    # NOTE: Do NOT call `service named try-restart` because chroot
    # files will remain mounted.
    START=no
    [ -e /var/lock/subsys/named ] && START=yes
    /sbin/service named stop > /dev/null 2>&1 || :;
    sed -i -e '/^ROOTDIR=.*/d' /etc/sysconfig/named
    if [ "x$START" = xyes ]; then
      /sbin/service named start > /dev/null 2>&1 || :;
    fi
  fi
fi
:;

%clean
rm -rf ${RPM_BUILD_ROOT}
:;

%files
%defattr(-,root,root,-)
%{_libdir}/bind
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/named
%config(noreplace) %attr(-,root,named) %{_sysconfdir}/named.iscdlv.key
%config(noreplace) %attr(-,root,named) %{_sysconfdir}/named.root.key
%{_sysconfdir}/rc.d/init.d/named
%{_sysconfdir}/NetworkManager/dispatcher.d/13-named
%{_sysconfdir}/portreserve/named
%{_sbindir}/arpaname
%{_sbindir}/ddns-confgen
%{_sbindir}/genrandom
%{_sbindir}/named-journalprint
%{_sbindir}/nsec3hash
%{_sbindir}/dnssec*
%{_sbindir}/named-check*
%{_sbindir}/lwresd
%{_sbindir}/named
%{_sbindir}/rndc*
%{_sbindir}/named-compilezone
%{_sbindir}/isc-hmac-fixup
%{_bindir}/bind9-config
%{_mandir}/man1/arpaname.1*
%{_mandir}/man1/bind9-config.1*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/named.8*
%{_mandir}/man8/lwresd.8*
%{_mandir}/man8/dnssec*.8*
%{_mandir}/man8/named-checkconf.8*
%{_mandir}/man8/named-checkzone.8*
%{_mandir}/man8/named-compilezone.8*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man8/ddns-confgen.8*
%{_mandir}/man8/genrandom.8*
%{_mandir}/man8/named-journalprint.8*
%{_mandir}/man8/nsec3hash.8*
%{_mandir}/man8/isc-hmac-fixup.8*
%doc CHANGES COPYRIGHT README named.conf.default
%doc doc/arm doc/misc doc/rfc
%doc sample/
%doc Copyright
%doc rfc1912.txt

# Hide configuration
%defattr(0640,root,named,0750)
%dir %{_sysconfdir}/named
%dir %{_localstatedir}/named
%config(noreplace) %verify(not link) %{_sysconfdir}/named.conf
%config(noreplace) %verify(not link) %{_sysconfdir}/named.rfc1912.zones
%config %verify(not link) %{_localstatedir}/named/named.ca
%config %verify(not link) %{_localstatedir}/named/named.localhost
%config %verify(not link) %{_localstatedir}/named/named.loopback
%config %verify(not link) %{_localstatedir}/named/named.empty
%defattr(0660,named,named,0770)
%dir %{_localstatedir}/named/slaves
%dir %{_localstatedir}/named/data
%dir %{_localstatedir}/named/dynamic
%ghost %{_localstatedir}/log/named.log
%defattr(0640,root,named,0750)
%ghost %config(noreplace) %{_sysconfdir}/rndc.key
# ^- rndc.key now created on first install only if it does not exist
# %verify(not size,not md5) %config(noreplace) %attr(0640,root,named) /etc/rndc.conf
# ^- Let the named internal default rndc.conf be used -
#    rndc.conf not required unless it differs from default.
%ghost %config(noreplace) %{_sysconfdir}/rndc.conf
# ^- The default rndc.conf which uses rndc.key is in named's default internal config -
#    so rndc.conf is not necessary.
%config(noreplace) %{_sysconfdir}/logrotate.d/named
%defattr(-,named,named,-)
%dir %{_localstatedir}/run/named

%if %{SDB}
%files sdb
%defattr(-,root,root,-)
%{_mandir}/man1/zone2ldap.1*
%doc contrib/sdb/ldap/README.ldap contrib/sdb/ldap/INSTALL.ldap contrib/sdb/pgsql/README.sdb_pgsql
%dir %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/schema/dnszone.schema
%{_sbindir}/named-sdb
%{_sbindir}/zone2ldap
%{_sbindir}/ldap2zone
%{_sbindir}/zonetodb
%{_sbindir}/zone2sqlite
%endif

%files libs
%defattr(-,root,root,-)
%{_libdir}/*so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/dig
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_mandir}/man1/host.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/nslookup.1*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*so
%{_includedir}/bind9
%{_includedir}/dns
%{_includedir}/dst
%{_includedir}/isc
%{_includedir}/isccc
%{_includedir}/isccfg
%{_includedir}/lwres
%{_mandir}/man1/isc-config.sh.1*
%{_mandir}/man3/lwres*
%{_bindir}/isc-config.sh

%files chroot
%defattr(-,root,root,-)
%ghost %{chroot_prefix}/dev/null
%ghost %{chroot_prefix}/dev/random
%ghost %{chroot_prefix}/dev/zero
%ghost %{chroot_prefix}/etc/localtime
%defattr(0640,root,named,0750)
%dir %{chroot_prefix}
%dir %{chroot_prefix}/dev
%dir %{chroot_prefix}/etc
%dir %{chroot_prefix}/etc/named
%dir %{chroot_prefix}/etc/pki
%dir %{chroot_prefix}/etc/pki/dnssec-keys
%dir %{chroot_prefix}/var
%dir %{chroot_prefix}/var/run
%dir %{chroot_prefix}/var/named
%dir %{chroot_prefix}/usr
%dir %{chroot_prefix}/%{_libdir}
%dir %{chroot_prefix}/%{_libdir}/bind
%ghost %config(noreplace) %{chroot_prefix}/etc/named.conf
%defattr(0660,named,named,0770)
%dir %{chroot_prefix}/var/run/named
%dir %{chroot_prefix}/var/tmp
%dir %{chroot_prefix}/var/log

%if %{PKCS11}
%files pkcs11
%defattr(-,root,root,-)
%doc README.pkcs11
%{_sbindir}/pkcs11-destroy
%{_sbindir}/pkcs11-keygen
%{_sbindir}/pkcs11-list
%{_mandir}/man8/pkcs11*
%endif

%changelog
* Thu Jan 15 2014 Denis Frolov <d.frolov81@mail.ru> 40:9.9.4-P2
- update

* Fri Sep 20 2013 Carl Byington <carl@five-ten-sg.com> 32:9.9.4-0.3
- add patch to build on centos5

