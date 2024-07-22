%define name 	lxphp
%define version 5.2.17
#%define release 0.lxcenter.4
%define release 10%{?dist}
%define brand lxlabs
%define real_name php

Name: %{name}       
Version: %{version}  
Release: %{release}
Summary: a LxCenter customized package for php    
Group: System Environment/Base    
License: PHP License   
URL: http://www.lxcenter.org

#Source0: http://download.lxcenter.org/%{name}/%{name}-%{version}.tar.bz2
Source0: http://www.php.net/distributions/%{real_name}-%{version}.tar.bz2
Source1: php.ini 
Source2: lxphpcli.sh
Source3: lxphpcgi.sh

Patch1: php-5.2.4-gnusrc.patch
Patch2: php-4.3.3-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-4.3.2-libtool15.patch
Patch5: php-5.0.2-phpize64.patch

# Fixes for extension modules
Patch22: php-4.3.11-shutdown.patch

# Functional changes
Patch30: php-5.0.4-dlopen.patch
Patch31: php-5.2.4-easter.patch

# Fixes for tests
Patch51: php-5.0.4-tests-wddx.patch

# New Patches
Patch300: php-5.2.1-PQfreemem.patch 
Patch302: php-5.2.8-oci8-lib64.patch  
Patch310: php-5.2.10-bug47285.patch
#Patch314: php-5.2.13-bug51263.patch
#Patch315: php-5.3.2-bug51192.patch

# Security patches
Patch400: php-5.3.3-CVE-2011-4885.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PHP 5 is a powerful apache module that adds scripting and database connection
capabilities to the apache server. This version includes the "php_cgi" binary
for suExec and stand alone php scripts too.


BuildRequires: rpmlib
BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, expat-devel
BuildRequires: gmp-devel, aspell-devel >= 0.50.0
#BuildRequires: httpd-devel >= 2.0.46-1
BuildRequires: libjpeg-devel, libpng-devel, pam-devel
BuildRequires: libclient-devel, net-snmp-devel, libtidy-devel, pspell-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
BuildRequires: zlib-devel, pcre-devel >= 6.6, readline-devel
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: gdbm-devel, libc-client-devel, libmhash-devel, libmcrypt-devel
BuildRequires: mysql-devel, postgresql-devel, libxslt-devel, ncurses-devel
#BuildRequires: smtpdaemon
Obsoletes: php-dbg, php3, phpfi, stronghold-php, lxphp <= 5.2.1
#Requires: libmhash
#Requires: net-snmp

%pre
if rpm -qa|grep lxphp-5.2.1-400 ; then
    rpm -e lxphp-5.2.1-400.i386 --nodeps
fi

%post
ln -sf /usr/local/%{brand}/ext/php/etc/lxphpcli.sh /usr/bin/lphp.exe
ln -sf /usr/local/%{brand}/ext/php/etc/lxphpcli.sh /usr/bin/lxphp.exe

%prep
#%setup -q
%setup -q -n %{real_name}-%{version} 

#%patch1 -p1 -b .gnusrc
#%patch2 -p1 -b .install
%patch3 -p1 -b .norpath
%patch4 -p1 -b .libtool15
#%patch5 -p1 -b .phpize64
##%patch6 -p1 -b .curl716
##%patch7 -p1 -b .filterm4

%patch22 -p1 -b .shutdown

%patch30 -p1 -b .dlopen
%patch31 -p1 -b .easter

%patch51 -p1 -b .tests-wddx
#%patch300 -p1 -b .PQfreemem
%patch302 -p1 -b .oci8-lib64
%patch310 -p1 -b .bug47285
#%%patch314 -p1 -b .bug51263 
#%%patch315 -p1 -b .bug51192

# Security patches
#%patch400 -p1 -b .cve-2011-4885

%build

./configure \
	--prefix=/usr/local/%{brand}/ext/php \
	--with-config-file-path=/usr/local/%{brand}/ext/php/etc \
	--with-config-file-scan-dir=/usr/local/%{brand}/ext/php/etc/php.d \
	--with-libdir=%{_lib} \
	--with-jpeg-dir=%{_prefix} \
	--with-gd=shared \
	--with-imap=shared --with-imap-ssl \
	--with-kerberos \
	--with-gdbm \
	--with-zlib=shared \
	--with-gmp=shared \
	--with-mysql=shared,/usr \
	--with-mysqli=shared,/usr/bin/mysql_config \
	--with-pgsql=shared \
	--with-iconv=shared \
	--with-curl=shared,/usr \
	--with-kerberos \
	--with-mhash=shared \
	--with-mcrypt=shared \
	--with-layout=GNU \
	--with-pcre-regex \
	--with-dom-exslt=/usr \
	--with-dom-xslt=/usr \
	--with-dom=/usr \
	--with-expat-dir=/usr \
	--with-regex=system \
	--with-openssl=shared \
	--with-pdo-sqlite=shared \
	--with-pdo-mysql=shared \
	--with-pdo-pgsql=shared \
	--with-pdo \
	--with-sqlite=shared \
	--with-gettext=shared \
	--with-tidy=shared \
	--with-xmlrpc=shared \
	--with-xsl=shared \
	--enable-xml=shared \
	--enable-xmlreader=shared \
	--enable-xmlwriter=shared \
	--with-ncurses=shared \
	--with-bz2=shared \
	--enable-zip=shared \
	--with-readline=shared \
	--with-pspell=shared \
	--with-db4=shared,/usr \
	--with-snmp=shared \
	--enable-calendar=shared \
	--enable-json=shared \
	--with-wddx \
	--without-oci8 \
	--disable-rpath \
	--disable-debug \
	--enable-force-cgi-redirect \
	--enable-fastcgi \
	--enable-mbstring=shared --enable-mbstr-enc-trans \
	--enable-pic \
	--enable-inline-optimization \
	--enable-posix \
	--enable-simplexml \
	--enable-track-vars \
       --enable-discard-path \
	--enable-sysvshm \
	--enable-soap=shared,/usr \
	--enable-sysvsem \
	--enable-sockets \
	--enable-safe-mode \
	--enable-magic-quotes \
	--enable-ftp \
	--enable-exif \
	--enable-bcmath \
	--enable-trans-sid \
	--enable-pcntl=shared \
	--enable-mbregex \
	--enable-dio \
	--enable-shmop \
	--enable-memory-limit

make %{_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

for mod in bz2 calendar curl gd gettext gmp imap iconv json mbstring mcrypt mhash mysql mysqli \
	ncurses openssl pcntl pdo_sqlite pdo_mysql pdo_pgsql pgsql pspell readline \
	snmp soap sqlite tidy xml xmlreader xmlrpc xmlwriter xsl zip zlib ; do

	install -D -m 755 modules/${mod}.so $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/lib/${mod}.so
done

# Doc
install -D -m 755 sapi/cli/php.1 $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/man/man1/php.1

# Binary
install -D -m 755 sapi/cli/php $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/php
install -D -m 755 sapi/cli/php $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/bin/php
install -D -m 755 sapi/cgi/php-cgi $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/bin/php_cgi

# php.ini
install -D -m 755 $RPM_SOURCE_DIR/php.ini $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/php.ini
install -D -m 755 $RPM_SOURCE_DIR/lxphpcgi.sh $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/lxphpcgi.sh
install -D -m 755 $RPM_SOURCE_DIR/lxphpcli.sh $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/lxphpcli.sh

mkdir $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/php.d

for mod in bz2 curl gd gettext gmp imap iconv json mbstring mcrypt mhash mysql mysqli \
	ncurses openssl pcntl pdo_sqlite pdo_mysql readline \
	snmp soap sqlite tidy xml xmlreader xmlrpc xmlwriter xsl zip zlib ; do

cat > $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF

done

for mod in calendar pdo_pgsql pgsql pspell ; do

cat > $RPM_BUILD_ROOT/usr/local/%{brand}/ext/php/etc/php.d/${mod}.nonini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF

done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

# Modules
/usr/local/%{brand}/ext/php/lib

#for mod in bz2 calendar curl gd gettext gmp imap iconv json mbstring mcrypt mhash mysql mysqli \
#	ncurses openssl pcntl pdo_sqlite pdo_mysql pdo_pgsql pgsql pspell readline \
#	snmp soap sqlite tidy xml xmlreader xmlrpc xmlwriter xsl zip zlib ; do

#	/usr/local/%{brand}/ext/php/lib/${mod}.so
#done

/usr/local/%{brand}/ext/php/lib/bz2.so
/usr/local/%{brand}/ext/php/lib/calendar.so
/usr/local/%{brand}/ext/php/lib/curl.so
/usr/local/%{brand}/ext/php/lib/gd.so
/usr/local/%{brand}/ext/php/lib/gettext.so
/usr/local/%{brand}/ext/php/lib/gmp.so
/usr/local/%{brand}/ext/php/lib/imap.so
/usr/local/%{brand}/ext/php/lib/iconv.so
/usr/local/%{brand}/ext/php/lib/json.so
/usr/local/%{brand}/ext/php/lib/mbstring.so
/usr/local/%{brand}/ext/php/lib/mcrypt.so
/usr/local/%{brand}/ext/php/lib/mhash.so
/usr/local/%{brand}/ext/php/lib/mysql.so
/usr/local/%{brand}/ext/php/lib/mysqli.so
/usr/local/%{brand}/ext/php/lib/ncurses.so
/usr/local/%{brand}/ext/php/lib/openssl.so
/usr/local/%{brand}/ext/php/lib/pcntl.so
/usr/local/%{brand}/ext/php/lib/pdo_sqlite.so
/usr/local/%{brand}/ext/php/lib/pdo_mysql.so
/usr/local/%{brand}/ext/php/lib/pdo_pgsql.so
/usr/local/%{brand}/ext/php/lib/pgsql.so
/usr/local/%{brand}/ext/php/lib/pspell.so
/usr/local/%{brand}/ext/php/lib/readline.so
/usr/local/%{brand}/ext/php/lib/snmp.so
/usr/local/%{brand}/ext/php/lib/soap.so
/usr/local/%{brand}/ext/php/lib/sqlite.so
/usr/local/%{brand}/ext/php/lib/tidy.so
/usr/local/%{brand}/ext/php/lib/xml.so
/usr/local/%{brand}/ext/php/lib/xmlreader.so
/usr/local/%{brand}/ext/php/lib/xmlrpc.so
/usr/local/%{brand}/ext/php/lib/xmlwriter.so
/usr/local/%{brand}/ext/php/lib/xsl.so
/usr/local/%{brand}/ext/php/lib/zip.so
/usr/local/%{brand}/ext/php/lib/zlib.so

# Doc
/usr/local/lxlabs/ext/php/man/
/usr/local/lxlabs/ext/php/man/man1/
/usr/local/lxlabs/ext/php/man/man1/php.1
%config /usr/local/lxlabs/ext/php/man/man1/php.1

# Binary
/usr/local/lxlabs/ext/php/php
/usr/local/lxlabs/ext/php/bin/
/usr/local/lxlabs/ext/php/bin/php
/usr/local/lxlabs/ext/php/bin/php_cgi

# Conf
/usr/local/lxlabs/ext/php/etc
%config /usr/local/lxlabs/ext/php/etc/php.ini


%defattr(-, root, root)
%doc CODING_STANDARDS CREDITS INSTALL LICENSE NEWS
%doc Zend/ZEND_* 

%defattr(-, root, root)
%doc
%changelog
* Sun Jun 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-10.mr
- fix for missing sqlite.ini
- deactive calendar, pgsql, pdo_pgsql and pspell with using .noini

* Wed Jun 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-9.mr
- add net-snmp requires
- mod/fix lxphpcli and lxphpcgi

* Fri Jan 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-8.mr
- recompile
- centos 6 error for patch 2, 5 and 400

* Sun Jan 6 2013 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-8.lx.el5
- add net-snmp-devel
- remove smtpdaemon

* Mon Dec 24 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-7.lx.el5
- fix modified command for remove old lxphp.i386
- move some modules to shared
- create symlink for lphp.exe and lxphp.exe
- add security patchs (base on php52 from ius repo)

* Mon Dec 17 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-6.lx.el5
- modified command for remove old lxphp.i386

* Mon Sep 24 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-5.lx.el5
- fixed bug (forgot source: for additional files

* Mon Sep 24 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-4.lx.el5
- modified php.ini and add script php-cli and php-cgi
- standard modules already embedded including mysql and pqsql module

* Thu Sep 20 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-3.lx.el5
- Modified for 5.2.17

* Mon Sep 17 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> 5.2.17-2.lx.el5
- Modified for 5.2.17

* Thu Feb 11 2011 Danny Terweij <d.terweij@lxcenter.org> 5.2.17-0.lxcenter.4
- Obsolete lxphp-5.2.1-400 i386 package
* Thu Feb 11 2011 Danny Terweij <d.terweij@lxcenter.org> 5.2.17-0.lxcenter.3
- Replace php.ini
- Replace php.1
* Thu Feb 11 2011 Danny Terweij <d.terweij@lxcenter.org> 5.2.17-0.lxcenter.2
- Fix php.ini
- Upgrade to PHP 5.2.17
* Thu Jan 04 2011 Danny Terweij <d.terweij@lxcenter.org> 5.2.16-0.lxcenter.1
- Repackaged at build system
- Upgrade to PHP 5.2.16
* Thu Nov 25 2010 Angel Guzman <angel.guzman@lxcenter.org> 5.2.14-0lxcenter3
- Upgrade to PHP 5.2.14 

