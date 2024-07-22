%define name 	php52s
%define version 5.2.17
%define release 12%{?dist}
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
Source1: php52s.ini 
Source2: php52s-cli.sh
Source3: php52s-cgi.sh

# Build fixes
Patch1: php-5.2.10-gnurc.patch
Patch2: php-5.2.8-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-5.2.8-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.2.8-recode.patch

# Fixes for extension modules
Patch20: php-4.3.11-shutdown.patch
Patch21: php-5.2.3-macropen.patch

# Functional changes
Patch40: php-5.0.4-dlopen.patch
Patch41: php-5.2.4-easter.patch
Patch42: php-5.2.5-systzdata.patch

# Fixes for tests
Patch60: php-5.2.7-tests-dashn.patch
Patch61: php-5.0.4-tests-wddx.patch

# php-fpm patch
Patch101: fpm.patch

# mail header patch
Patch111: php-5.2.15-mail-header.patch

# CVE
Patch201: php-5.2.17-CVE-2011-2202.patch
Patch202: php-5.2.17-CVE-2011-1938.patch
Patch203: php-5.2.17-CVE-2011-1148.patch
Patch204: php-5.2.17-CVE-2011-0708.patch
Patch205: php-5.2.17-CVE-2011-1092.patch
Patch206: php-5.2.17-CVE-2011-0421.patch

# Backport from 5.3.6
Patch301: php-5.3.6-bug-54055.patch
Patch302: php-5.3.6-bug-53577.patch
Patch303: php-5.2.17-bug-48484.patch
Patch304: php-5.3.6-bug-48607.patch
Patch305: php-5.3.6-bug-53574.patch
Patch306: php-5.3.6-bug-52290.patch
Patch307: php-5.2.17-bug-52063.patch
Patch308: php-5.3.6-bug-53924.patch
Patch309: php-5.3.6-bug-53150.patch
Patch310: php-5.3.6-bug-52209.patch
Patch311: php-5.3.6-bug-47435.patch
Patch312: php-5.3.6-bug-53377.patch
Patch313: php-5.2.17-bug-39847.patch
Patch314: php-5.3.6-39199.patch
Patch315: php-5.3.6-bug-53630.patch
Patch316: php-5.3.6-bug-51336.patch
Patch317: php-5.3.6-bug-53515.patch
Patch318: php-5.3.6-bug-54092.patch
Patch319: php-5.3.6-bug-53903.patch
Patch320: php-5.3.6-bug-54089.patch
Patch321: php-5.3.6-bug-53603.patch
Patch322: php-5.3.6-bug-53854.patch
Patch323: php-5.3.6-bug-53579.patch
Patch324: php-5.3.6-bug-53568.patch
Patch325: php-5.2.17-bug-49072.patch
# 5.3.7
Patch330: php-5.3.7-bug-55399.patch
Patch331: php-5.2.17-bug-55082.patch
Patch332: php-5.3.7-bug-55014.patch
#Patch333: php-5.3.7-bug-54924.patch
Patch334: php-5.3.7-bug-54180.patch
Patch335: php-5.3.7-bug-54137.patch
Patch336: php-5.3.7-bug-53848.patch
Patch337: php-5.3.7-bug-52935.patch
Patch338: php-5.3.7-bug-51997.patch
Patch339: php-5.3.7-bug-50363.patch
Patch340: php-5.3.7-bug-48465.patch
Patch341: php-5.3.7-bug-54529.patch
Patch342: php-5.3.7-bug-52496.patch
Patch343: php-5.3.7-bug-54242.patch
Patch344: php-5.3.7-bug-54121.patch
Patch345: php-5.3.7-bug-53037.patch
Patch346: php-5.3.7-bug-54269.patch
Patch347: php-5.3.7-bug-54601.patch
Patch348: php-5.3.7-bug-54440.patch
Patch349: php-5.3.7-bug-54494.patch
Patch350: php-5.3.7-bug-54221.patch
Patch351: php-5.3.7-bug-52104.patch
Patch352: php-5.3.7-bug-54329.patch
Patch353: php-5.3.7-bug-53782.patch
Patch354: php-5.3.7-bug-54318.patch
Patch355: php-5.3.7-bug-55323.patch
Patch356: php-5.3.7-bug-54312.patch
Patch357: php-5.3.7-bug-51958.patch
Patch358: php-5.3.7-bug-54946.patch
# 5.3.9 backport
Patch359: php-5.2.17-CVE-2011-4566.patch
Patch360: php-5.2.17-bug-60206.patch
Patch361: php-5.2.17-bug-60138.patch
Patch362: php-5.2.17-bug-60120.patch
Patch363: php-5.2.17-bug-55674.patch
Patch364: php-5.2.17-bug-55509.patch
Patch365: php-5.2.17-bug-55504.patch
Patch366: php-5.2.17-bug-52461.patch
Patch367: php-5.2.17-bug-55366.patch
Patch368: php-5.2.17-bug-55273.patch
Patch369: php-5.2.17-bug-52624.patch
Patch370: php-5.2.17-bug-43200.patch
# CVE-2012-0781
Patch371: php-5.2.17-bug-54682.patch
Patch372: php-5.2.17-bug-60455.patch
Patch373: php-5.2.17-bug-60183.patch
Patch374: php-5.2.17-bug-55478.patch
# Bug-319457 CVE-2011-4153
Patch375: php-5.2.17-bug-319457.patch
# Bug-55776 CVE-2012-0788
Patch376: php-5.2.17-bug-55776.patch

#php-5.2-max-input-vars patch
Patch400: php-5.2.17-max-input-vars.patch
Patch401: php-5.2.17-bug-323007-2.patch
# Bug-323016 CVE-2012-0831
Patch402: php-5.2.17-bug-323016.patch
# CVE-2012-1823
Patch410: php-5.2.17-CVE-2012-1823.patch
# Bug-61650
Patch421: php-5.2.17-bug-61650.patch
# Bug-61165
#Patch422: php-5.2.17-bug-61165.patch
# Bug-61095
Patch423: php-5.2.17-bug-61095.patch
# Bug-61000
Patch424: php-5.2.17-bug-61000.patch
# Bug-60801
#Patch425: php-5.2.17-bug-60801.patch
# Bug-60569
Patch426: php-5.2.17-bug-60569.patch
# Bug-60227  CVE-2011-1398
Patch427: php-5.2.17-bug-60227.patch
# Bug-60222
Patch428: php-5.2.17-bug-60222.patch
# CVE-2012-1172
Patch429: php-5.2.17-CVE-2012-1172.patch

# CVE-2012-2688
Patch430: php-5.2.17-CVE-2012-2688.patch

Patch431: php-5.2.17-bug-62432.patch
# CVE-2012-3365
Patch432: php-5.2.17-CVE-2012-3365.patch
# CVE-2012-2311
Patch433: php-5.2.17-CVE-2012-2311.patch
#
Patch434: php-5.2.17-bug-61546.patch
Patch435: php-5.2.17-bug-62005.patch
Patch436: php-5.2.17-bug-61730.patch
Patch437: php-5.2.17-bug-61764.patch
Patch438: php-5.2.17-bug-61713.patch
Patch439: php-5.2.17-bug-61948.patch
Patch440: php-5.2.17-bug-62146.patch
Patch441: php-5.2.17-bug-61755.patch
Patch442: php-5.2.17-bug-61961.patch
Patch443: php-5.2.17-bug-62064.patch

Patch444: php-5.2.17-bug-62763.patch
Patch445: php-5.2.17-bug-62839.patch
Patch446: php-5.2.17-bug-62499.patch
Patch447: php-5.2.17-bug-62715.patch
Patch448: php-5.2.17-CVE-2012-0057.patch
# CVE-2012-0789
Patch449: php-5.2.17-bug-53502.patch
# CVE-2011-4153
Patch450: php-5.2.17-CVE-2011-4153.patch
# CVE-2012-2336
Patch451: php-5.2.17-CVE-2012-2336.patch
# CVE-2006-7243
Patch452: php-5.2.17-CVE-2006-7243.patch
# timezonedb.h updated to version 2012.5 (2012e)
Patch453: php-5.2.17-timezone.patch
Patch454: php-5.2.17-bug-62844.patch

Patch455: php-5.2.17-27-maillog.patch

Patch456: php-5.2.17-CVE-2013-1635.patch
Patch457: php-5.2.17-CVE-2013-1643.patch

Patch458: php-5.2.17-bug-64895.patch
Patch459: php-5.2.17-bug-64726.patch
Patch460: php-5.2.17-bug-64458.patch
Patch461: php-5.2.17-CVE-2013-4113.patch
Patch462: php-5.2.17-CVE-2013-4073.patch
Patch463: php-5.2.17-CVE-2013-4248-UML.patch
Patch464: php-5.2.17-CVE-2013-6420.patch

# libxml 2.9.x patch
Patch500: libxml29_compat.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PHP 5 is a powerful apache module that adds scripting and database connection
capabilities to the apache server. This version includes the "php-cgi" binary
for suExec and stand alone php scripts too.


BuildRequires: rpmlib
BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, expat-devel
BuildRequires: gmp-devel, aspell-devel >= 0.50.0
BuildRequires: libjpeg-devel, libpng-devel, pam-devel
BuildRequires: libclient-devel, net-snmp-devel, libtidy-devel, pspell-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
BuildRequires: zlib-devel, pcre-devel >= 6.6, readline-devel
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: gdbm-devel, libc-client-devel, mhash-devel, libmcrypt-devel
BuildRequires: libxslt-devel, ncurses-devel, libxml2-devel
#BuildRequires: mysql-devel, postgresql-devel, smtpdaemon
#BuildRequires: httpd-devel >= 2.0.46-1
Obsoletes: php-dbg, php3, phpfi, stronghold-php, lxphp
Requires: mhash, net-snmp

%post
ln -sf /opt/php52s/etc/php52s-cli.sh /usr/bin/lphp.exe
ln -sf /opt/php52s/etc/php52s-cli.sh /usr/bin/lxphp.exe
ln -sf /opt/php52s/etc/php52s-cli.sh /usr/bin/php52s

%prep
#%setup -q
%setup -q -n %{real_name}-%{version} 

#%patch1 -p1 -b .gnusrc
%patch2 -p1 -b .install
%patch3 -p1 -b .norpath
%patch4 -p1 -b .phpize64
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode

%patch20 -p1 -b .shutdown
%patch21 -p1 -b .macropen

%patch40 -p1 -b .dlopen
%patch41 -p1 -b .easter
%patch42 -p1 -b .systzdata

%patch60 -p1 -b .tests-dashn
%patch61 -p1 -b .tests-wddx

#%patch101 -p1 -b .php-fpm
%patch111 -p1 -b .mail-header

%patch201 -p1 -b .CVE-2011-2202
%patch202 -p1 -b .CVE-2011-1938
%patch203 -p1 -b .CVE-2011-1148
%patch204 -p1 -b .CVE-2011-0708
%patch205 -p1 -b .CVE-2011-1092
%patch206 -p1 -b .CVE-2011-0421

# Bugfix backport from 5.3.6
%patch301 -p1 -b .bug-54055
%patch302 -p1 -b .bug-53577
%patch303 -p1 -b .bug-48484
%patch304 -p1 -b .bug-48607
%patch305 -p1 -b .bug-53574
%patch306 -p1 -b .bug-52290
%patch307 -p1 -b .bug-52063
%patch308 -p1 -b .bug-53924
%patch309 -p1 -b .bug-53150
%patch310 -p1 -b .bug-52209
%patch311 -p1 -b .bug-47435
%patch312 -p1 -b .bug-53377
%patch313 -p1 -b .bug-39847
%patch314 -p1 -b .bug-39199
%patch315 -p1 -b .bug-53630
%patch316 -p1 -b .bug-51336
%patch317 -p1 -b .bug-53515
%patch318 -p1 -b .bug-54092
%patch319 -p1 -b .bug-53903
%patch320 -p1 -b .bug-54089
%patch321 -p1 -b .bug-53603
%patch322 -p1 -b .bug-53854
%patch323 -p1 -b .bug-53579
%patch324 -p1 -b .bug-53568
%patch325 -p1 -b .bug-49072
# Bugfix backport from 5.3.7
%patch330 -p1 -b .bug-55399
%patch331 -p1 -b .bug-55082
%patch332 -p1 -b .bug-55014
#accert %patch333 -p1 -b .bug-54924
%patch334 -p1 -b .bug-54180
%patch335 -p1 -b .bug-54137
%patch336 -p1 -b .bug-53848
%patch337 -p1 -b .bug-52935
#%patch338 -p1 -b .bug-51997
%patch339 -p1 -b .bug-50363
%patch340 -p1 -b .bug-48465
%patch341 -p1 -b .bug-54529
%patch342 -p1 -b .bug-52496
%patch343 -p1 -b .bug-54242
%patch344 -p1 -b .bug-54121
%patch345 -p1 -b .bug-53037
%patch346 -p1 -b .bug-54269
%patch347 -p1 -b .bug-54601
%patch348 -p1 -b .bug-54440
%patch349 -p1 -b .bug-54494
%patch350 -p1 -b .bug-54221
%patch351 -p1 -b .bug-52104
%patch352 -p1 -b .bug-54329
#%patch353 -p1 -b .bug-53782
%patch354 -p1 -b .bug-54318
#soap %patch355 -p1 -b .bug-55323
%patch356 -p1 -b .bug-54312
%patch357 -p1 -b .bug-51958
%patch358 -p1 -b .bug-54946
%patch359 -p1 -b .CVE-2011-4566
%patch360 -p1 -b .bug-60206
%patch361 -p1 -b .bug-60138
%patch362 -p1 -b .bug-60120
%patch363 -p1 -b .bug-55674
%patch364 -p1 -b .bug-55509
%patch365 -p1 -b .bug-55504
%patch366 -p1 -b .bug-52461
%patch367 -p1 -b .bug-55366
%patch368 -p1 -b .bug-55273
%patch369 -p1 -b .bug-52624
%patch370 -p1 -b .bug-43200
%patch371 -p1 -b .bug-54682
%patch372 -p1 -b .bug-60455
%patch373 -p1 -b .bug-60183
%patch374 -p1 -b .bug-55478
%patch375 -p1 -b .bug-319457
%patch376 -p1 -b .bug-55776

%patch400 -p1 -b .php-5.2-max-input-vars
%patch401 -p1 -b .bug-323007
#%patch402 -p1 -b .bug-323016

%patch410 -p1 -b .CVE-2012-1823

%patch421 -p1 -b .bug-61650
#%patch422 -p1 -b .bug-61165
%patch423 -p1 -b .bug-61095
%patch424 -p1 -b .bug-61000
#%patch425 -p1 -b .bug-60801
%patch426 -p1 -b .bug-60569
%patch427 -p1 -b .bug-60227
%patch428 -p1 -b .bug-60222
%patch429 -p1 -b .CVE-2012-1172
%patch430 -p1 -b .CVE-2012-2688
%patch431 -p1 -b .bug-62432
%patch432 -p1 -b .CVE-2012-3365
%patch433 -p1 -b .CVE-2012-2311
%patch434 -p1 -b .bug-61546
%patch435 -p1 -b .bug-62005
%patch436 -p1 -b .bug-61730
%patch437 -p1 -b .bug-61764
%patch438 -p1 -b .bug-61713
%patch439 -p1 -b .bug-61948
%patch440 -p1 -b .bug-62146
%patch441 -p1 -b .bug-61755
%patch442 -p1 -b .bug-61961
%patch443 -p1 -b .bug-62064
%patch444 -p1 -b .bug-62763
%patch445 -p1 -b .bug-62839
%patch446 -p1 -b .bug-62499
%patch447 -p1 -b .bug-62715
%patch448 -p1 -b .CVE-2012-0057
%patch449 -p1 -b .bug-53502
%patch450 -p1 -b .CVE-2011-4153
%patch451 -p1 -b .CVE-2012-2336
%patch452 -p1 -b .CVE-2006-7243
%patch453 -p1 -b .timezone
%patch454 -p1 -b .bug-62844
#%patch455 -p1 -b .maillog

%patch456 -p1 -b .CVE-2013-1635
%patch457 -p1 -b .CVE-2013-1643

%patch458 -p1 -b .bug-64895
%patch459 -p1 -b .bug-64726
%patch460 -p1 -b .bug-64458

%patch461 -p1 -b .CVE-2013-4113
%patch462 -p1 -b .CVE-2013-4073
%patch463 -p1 -b .CVE-2013-4248-UML
%patch464 -p1 -b .CVE-2013-6420

# Libxml2 2.9.x patch
%patch500 -p0

%build

./configure \
	--prefix=/opt/php52s \
	--with-config-file-path=/opt/php52s/etc \
	--with-config-file-scan-dir=/opt/php52s/etc/php.d \
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

	install -D -m 755 modules/${mod}.so $RPM_BUILD_ROOT/opt/php52s/lib/${mod}.so
done

# Doc
install -D -m 755 sapi/cli/php.1 $RPM_BUILD_ROOT/opt/php52s/man/man1/php.1

# Binary
#install -D -m 755 sapi/cli/php $RPM_BUILD_ROOT/opt/php52s/php
install -D -m 755 sapi/cli/php $RPM_BUILD_ROOT/opt/php52s/bin/php
install -D -m 755 sapi/cgi/php-cgi $RPM_BUILD_ROOT/opt/php52s/bin/php-cgi

# php.ini
install -D -m 755 $RPM_SOURCE_DIR/php52s.ini $RPM_BUILD_ROOT/opt/php52s/etc/php.ini
install -D -m 755 $RPM_SOURCE_DIR/php52s-cgi.sh $RPM_BUILD_ROOT/opt/php52s/etc/php52s-cgi.sh
install -D -m 755 $RPM_SOURCE_DIR/php52s-cli.sh $RPM_BUILD_ROOT/opt/php52s/etc/php52s-cli.sh

mkdir $RPM_BUILD_ROOT/opt/php52s/etc/php.d

for mod in bz2 curl gd gettext gmp imap iconv json mbstring mcrypt mhash mysql mysqli \
	ncurses openssl pcntl pdo_sqlite pdo_mysql readline \
	snmp soap sqlite tidy xml xmlreader xmlrpc xmlwriter xsl zip zlib ; do

cat > $RPM_BUILD_ROOT/opt/php52s/etc/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF

done

for mod in calendar pdo_pgsql pgsql pspell ; do

cat > $RPM_BUILD_ROOT/opt/php52s/etc/php.d/${mod}.nonini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF

done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

# Modules
/opt/php52s/lib

/opt/php52s/lib/bz2.so
/opt/php52s/lib/calendar.so
/opt/php52s/lib/curl.so
/opt/php52s/lib/gd.so
/opt/php52s/lib/gettext.so
/opt/php52s/lib/gmp.so
/opt/php52s/lib/imap.so
/opt/php52s/lib/iconv.so
/opt/php52s/lib/json.so
/opt/php52s/lib/mbstring.so
/opt/php52s/lib/mcrypt.so
/opt/php52s/lib/mhash.so
/opt/php52s/lib/mysql.so
/opt/php52s/lib/mysqli.so
/opt/php52s/lib/ncurses.so
/opt/php52s/lib/openssl.so
/opt/php52s/lib/pcntl.so
/opt/php52s/lib/pdo_sqlite.so
/opt/php52s/lib/pdo_mysql.so
/opt/php52s/lib/pdo_pgsql.so
/opt/php52s/lib/pgsql.so
/opt/php52s/lib/pspell.so
/opt/php52s/lib/readline.so
/opt/php52s/lib/snmp.so
/opt/php52s/lib/soap.so
/opt/php52s/lib/sqlite.so
/opt/php52s/lib/tidy.so
/opt/php52s/lib/xml.so
/opt/php52s/lib/xmlreader.so
/opt/php52s/lib/xmlrpc.so
/opt/php52s/lib/xmlwriter.so
/opt/php52s/lib/xsl.so
/opt/php52s/lib/zip.so
/opt/php52s/lib/zlib.so

# Doc
/opt/php52s/man/
/opt/php52s/man/man1/
/opt/php52s/man/man1/php.1
%config /opt/php52s/man/man1/php.1

# Binary
#/opt/php52s/php
/opt/php52s/bin/
/opt/php52s/bin/php
/opt/php52s/bin/php-cgi

# Conf
/opt/php52s/etc
%config /opt/php52s/etc/php.ini


%defattr(-, root, root)
%doc CODING_STANDARDS CREDITS INSTALL LICENSE NEWS
%doc Zend/ZEND_* 

%defattr(-, root, root)
%doc
%changelog
* Thu Apr 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-12.mr
- recompile with dependencies to mysql55 (because mysql 5.5 in centos 6 already remove my centalt)

* Sat Feb 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-11.mr
- disable BuildRequires to mysql-devel and postgresql-devel
- add more patches (without php-fpm patches)

* Fri Jul 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> 5.2.17-10.mr
- change for lxphp to php52s
- change path from /usr/local/lxlabs/ext/php to /opt/php52s

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

