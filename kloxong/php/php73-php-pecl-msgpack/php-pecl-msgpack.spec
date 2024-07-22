# remirepo spec file for php-pecl-msgpack
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-msgpack
#
# Copyright (c) 2012-2022 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package       php-pecl-msgpack
%endif

%global gh_commit   943d27267fbf6da6b4d225f344f4731aec0c671b
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    msgpack
%global gh_project  msgpack-php
#global gh_date     20171026
%global pecl_name   msgpack
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

%global upstream_version 2.2.0
%global upstream_prever  RC2
%global upstream_lower   RC2

# to use system library
%bcond_with    msgpack

# to disable test suite
%bcond_without tests

Summary:       API for communicating with MessagePack serialization
Name:          %{?scl_prefix}php-pecl-msgpack
License:       BSD
Version:       %{upstream_version}%{?upstream_lower:~%{upstream_lower}}
URL:           https://pecl.php.net/package/msgpack
%if 0%{?gh_date:1}
Release:       0.7.%{gh_date}.%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{pecl_name}-%{version}-%{gh_short}.tar.gz
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz
%endif

BuildRequires: make
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel >= 7.0
BuildRequires: %{?scl_prefix}php-pear
%if %{with msgpack}
BuildRequires: msgpack-devel
%else
Provides: bundled(msgpack) = 3.2.0
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?packager}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
%if "%{php_version}" > "7.3"
Obsoletes:      php73-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.4"
Obsoletes:      php74-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "8.0"
Obsoletes:      php80-pecl-%{pecl_name} <= %{version}
%endif
%endif


%description
This extension provide API for communicating with MessagePack serialization.

MessagePack is an efficient binary serialization format. It lets you exchange
data among multiple languages like JSON but it's faster and smaller.
For example, small integers (like flags or error code) are encoded into a
single byte, and typical short strings only require an extra byte in addition
to the strings themselves.

If you ever wished to use JSON for convenience (storing an image with metadata)
but could not for technical reasons (encoding, size, speed...), MessagePack is
a perfect replacement.

This extension is still EXPERIMENTAL.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       MessagePack developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}


%description devel
These are the files needed to compile programs using MessagePack serializer.


%prep
%setup -qc
%if 0%{?gh_date:1}
mv %{gh_project}-%{gh_commit} NTS
mv NTS/package.xml .
sed -e '/release/s/0.5.6/%{version}%{?gh_date:dev}/' -i package.xml
%else
mv %{pecl_name}-%{upstream_version}%{?upstream_prever} NTS
%endif

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd NTS
%if %{with msgpack}
# use system library
rm -rf msgpack
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MSGPACK_VERSION/{s/.* "//;s/".*$//;p}' php_msgpack.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}%{?gh_date:-dev}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable MessagePack extension module
extension = %{pecl_name}.so

; Configuration options

;msgpack.error_display = On
;msgpack.illegal_key_insert = Off
;msgpack.php_only = On
EOF


%build
%{?dtsenable}

cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
   [ -f $i ]       && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
# Erratic results, segfauilt and mark as XFAIL
rm */tests/034.phpt
%ifarch aarch64
# too slow
rm */tests/035.phpt
%endif

cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with tests}
: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q --show-diff
%endif

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with tests}
: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php -q --show-diff
%endif
%endif


%if 0%{?fedora} < 24 && 0%{?rhel} < 8
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Fri Oct  7 2022 Remi Collet <remi@remirepo.net> - 2.2.0~RC2-1
- update to 2.2.0RC2

* Fri Sep  9 2022 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-8
- ignore 8 failed tests with PHP 8.2

* Thu Jul 28 2022 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-7
- skip one test on aarch64

* Mon Sep  6 2021 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-6
- F35 build

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-4
- rebuild for 8.1.0RC1

* Tue Aug 31 2021 Remi Collet <remi@remirepo.net> - 2.2.0~RC1-1
- update to 2.2.0RC1

* Thu Jun 10 2021 Remi Collet <remi@remirepo.net> - 2.1.2-3
- add patch for test suite with PHP 8.1 from
  https://github.com/msgpack/msgpack-php/pull/156

* Wed Apr 28 2021 Remi Collet <remi@remirepo.net> - 2.1.2-2
- F34 rebuild for https://github.com/remicollet/remirepo/issues/174

* Sat Nov 28 2020 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 2.1.1-3
- rebuild for PHP 8.0.0RC1

* Wed Sep 23 2020 Remi Collet <remi@remirepo.net> - 2.1.1-2
- add upstream patches for PHP 8

* Tue Jul 28 2020 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Fri Feb 28 2020 Remi Collet <remi@remirepo.net> - 2.1.0-1
- update to 2.1.0

* Fri Dec 20 2019 Remi Collet <remi@remirepo.net> - 2.1.0~beta1-1
- update to 2.1.0beta1

* Fri Dec 20 2019 Remi Collet <remi@remirepo.net> - 2.1.0~beta1-0
- test build for upcoming 2.1.0beta1

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 2.0.3-3
- rebuild for 7.4.0RC1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 2.0.3-2
- rebuild

* Thu Dec 20 2018 Remi Collet <remi@remirepo.net> - 2.0.3-1
- update to 2.0.3

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 2.0.3-0.3.20171026.943d272
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 2.0.3-0.2.20171026.943d272
- rebuld for 7.3.0alpha4 new ABI

* Wed Jun 27 2018 Remi Collet <remi@remirepo.net> - 2.0.3-0.1.20171026.943d272
- update to 2.0.3-dev for PHP 7.3 with patches from
  https://github.com/msgpack/msgpack-php/pull/124
  https://github.com/msgpack/msgpack-php/pull/127
- ignore test suite result for now

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 2.0.2-4
- rebuild for PHP 7.2.0beta1 new API

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 2.0.2-3
- rebuild for 7.2.0alpha2

* Fri Apr 14 2017 Remi Collet <remi@remirepo.net> - 2.0.2-2
- add patch for test suite with PHP 7.2 from
  https://github.com/msgpack/msgpack-php/pull/118

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- rebuild for PHP 7.1 new API version

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- ignore more tests with 7.1

* Sat Jun 11 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- add patch for PHP 7.1
  open https://github.com/msgpack/msgpack-php/pull/87

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (php 7, beta)
- use sources from pecl

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (php 7, beta)

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.20151014git75991cf
- new snapshot, version bump to 2.0.0dev

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.7.20151002git7a5bdb1
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.6.20150702gitce27a10
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.5.20150702gitce27a10
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.4.20150702gitce27a10
- new snapshot, rebuild against php 7.0.0beta1

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.3.20150612git95c8dc3
- allow build against rh-php56 (as more-php56)
- rebuild for "rh_layout" (php70)

* Fri Jun 12 2015 Remi Collet <remi@fedoraproject.org> - 0.5.7-0.1.20150612git95c8dc3
- update to 0.5.7dev for PHP 7
- sources from github

* Mon Apr 27 2015 Remi Collet <remi@fedoraproject.org> - 0.5.6-1
- Update to 0.5.6
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-8.1
- Fedora 21 SCL mass rebuild

* Sun Aug 24 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-8
- improve SCL stuff

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-7
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 0.5.5-6
- allow SCL build

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 0.5.5-5
- cleanups
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)

* Thu Jul 18 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-4
- bump release

* Thu Apr 18 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-4
- ExcludeArch: ppc64 (as msgpack)

* Tue Apr  2 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-3
- use system msgpack library headers

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-2
- cleanups

* Wed Feb 20 2013 Remi Collet <remi@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1.1
- also provides php-msgpack

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 0.5.3-1
- update to 0.5.3 (beta)

* Sat Sep 15 2012 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- initial package, version 0.5.2 (beta)

