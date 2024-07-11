# remirepo spec file for php-pecl-apcu
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-apcu
#
# Copyright (c) 2013-2023 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%{?scl:%scl_package php-pecl-apcu}

# Defined in Fedora >= 37 and RHEL >= 10, in PHP >= 7.4 for remirepo
%{!?__phpize:      %global __phpize       %{_bindir}/phpize}
%{!?__ztsphpize:   %global __ztsphpize    %{_bindir}/zts-phpize}
%{!?__phpconfig:   %global __phpconfig    %{_bindir}/php-config}
%{!?__ztsphpconfig:%global __ztsphpconfig %{_bindir}/zts-php-config}

%bcond_without     tests

%global gh_commit  b771cd50a7fe519b6aaccbe5dc97594e68e0c88f
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   krakjoe
%global gh_project apcu
%global pecl_name  apcu
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name   40-%{pecl_name}.ini
%global sources    %{pecl_name}-%{version}
%global _configure ../%{sources}/configure

Name:           %{?scl_prefix}php-pecl-apcu
Summary:        APC User Cache
Version:        5.1.22
License:        PHP-3.01
URL:            https://pecl.php.net/package/APCu
Release:        2%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:        %{pecl_name}-5.1.19.ini
Source2:        %{pecl_name}-panel.conf
Source3:        %{pecl_name}.conf.php

Patch0:         %{pecl_name}-php83.patch
Patch1:         %{pecl_name}-tests.patch

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?scl_prefix}php-devel >= 7.0
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Obsoletes:      %{?scl_prefix}php-apcu               < 4.0.0-1
Provides:       %{?scl_prefix}php-apcu               = %{version}
Provides:       %{?scl_prefix}php-apcu%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(apcu)         = %{version}
Provides:       %{?scl_prefix}php-pecl(apcu)%{?_isa} = %{version}

%if "%{?packager}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:      php53-pecl-%{pecl_name} <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:      php54-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "7.1"
Obsoletes:     php71u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php71w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.2"
Obsoletes:     php72u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php72w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.3"
Obsoletes:      php73-pecl-%{pecl_name} <= %{version}
Obsoletes:     php73w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.4"
Obsoletes:      php74-pecl-%{pecl_name} <= %{version}
Obsoletes:     php74w-pecl-%{pecl_name} <= %{version}
%endif
%endif


%description
APCu is userland caching: APC stripped of opcode caching.

APCu only supports userland caching of variables.

The %{?scl_prefix}php-pecl-apcu-bc package provides a drop
in replacement for APC.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       APCu developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

Obsoletes:     %{?scl_prefix}php-pecl-apc-devel          < 4
Provides:      %{?scl_prefix}php-pecl-apc-devel          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-apc-devel%{?_isa}  = %{version}-%{release}

%description devel
These are the files needed to compile programs using APCu.


%if 0%{!?scl:1}
%package -n apcu-panel
Summary:       APCu control panel
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}
Requires:      php(httpd)
Requires:      php-gd
Requires:      httpd

Obsoletes:     apc-panel < 4
Provides:      apc-panel = %{version}-%{release}

%description -n apcu-panel
This package provides the APCu control panel, with Apache
configuration, available on http://localhost/apcu-panel/
%endif


%prep
%setup -qc
%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

cd %{sources}
%patch -P0 -p1 -b.php83
%patch -P1 -p1 -b.pr490

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APCU_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

%if 0%{!?scl:1}
# Fix path to configuration file
sed -e s:apc.conf.php:%{_sysconfdir}/apcu-panel/conf.php:g \
    -i %{sources}/apc.php
%else
# Provide the control panel as doc
sed -e '/"apc.php"/s/role="src"/role="doc"/' -i package.xml
%endif

%build
%{?dtsenable}

cd %{sources}
%{__phpize}

cd ../NTS
%configure \
   --enable-apcu \
   --with-php-config=%{__phpconfig}
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%configure \
   --enable-apcu \
   --with-php-config=%{__ztsphpconfig}
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if 0%{!?scl:1}
# Install the Control Panel
# Pages
install -D -m 644 -p %{sources}/apc.php  \
        %{buildroot}%{_datadir}/apcu-panel/index.php
# Apache config
install -D -m 644 -p %{SOURCE2} \
        %{buildroot}%{_sysconfdir}/httpd/conf.d/apcu-panel.conf
# Panel config
install -D -m 644 -p %{SOURCE3} \
        %{buildroot}%{_sysconfdir}/apcu-panel/conf.php
%endif


# Test & Documentation
cd %{sources}
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f $i ]       && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
   [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}

%{_bindir}/php -n \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   -m | grep 'apcu'

%if %{with tests}
# Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q --show-diff
%endif

%if %{with_zts}
%{__ztsphp} -n \
   -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
   -m | grep 'apcu'

%if %{with tests}
# Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
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
%{?_licensedir:%license %{sources}/LICENSE}
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


%if 0%{!?scl:1}
%files -n apcu-panel
# Need to restrict access, as it contains a clear password
%attr(550,apache,root) %dir %{_sysconfdir}/apcu-panel
%config(noreplace) %{_sysconfdir}/apcu-panel/conf.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/apcu-panel.conf
%{_datadir}/apcu-panel
%endif


%changelog
* Tue Jun  6 2023 Remi Collet <remi@remirepo.net> - 5.1.22-2
- build out of sources tree
- add upstream patch for 8.3
- add patch for tests when build out of sources tree from
  https://github.com/krakjoe/apcu/pull/490

* Mon Sep 19 2022 Remi Collet <remi@remirepo.net> - 5.1.22-1
- update to 5.1.22

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 5.1.21-3
- rebuild for PHP 8.2.0RC1

* Thu Aug 18 2022 Remi Collet <remi@remirepo.net> - 5.1.21-2
- add upstream patches for PHP 8.2

* Thu Oct  7 2021 Remi Collet <remi@remirepo.net> - 5.1.21-1
- update to 5.1.21

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 5.1.20-5
- rebuild for 8.1.0RC1

* Fri Jul 23 2021 Remi Collet <remi@remirepo.net> - 5.1.20-4
- add upstream patch for PHP 8.1.0beta1

* Wed Jul  7 2021 Remi Collet <remi@remirepo.net> - 5.1.20-3
- add upstream patch for test suite with PHP 8.1

* Thu Jun 10 2021 Remi Collet <remi@remirepo.net> - 5.1.20-2
- temporarily ignore 3 tests with PHP 8.1

* Thu Mar  4 2021 Remi Collet <remi@remirepo.net> - 5.1.20-1
- update to 5.1.20

* Mon Oct  5 2020 Remi Collet <remi@remirepo.net> - 5.1.19-1
- update to 5.1.19

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 5.1.18-7
- rebuild for PHP 8.0.0RC1

* Wed Sep 23 2020 Remi Collet <remi@remirepo.net> - 5.1.18-6
- rebuild for PHP 8.0.0beta4

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 5.1.18-5
- more upstream patches

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 5.1.18-4
- rebuild for PHP 8.0.0beta3

* Wed Aug  5 2020 Remi Collet <remi@remirepo.net> - 5.1.18-3
- rebuild for 8.0.0beta1
- more upstream patches

* Fri Apr 10 2020 Remi Collet <remi@remirepo.net> - 5.1.18-2
- add upstream patch for 8.0

* Mon Oct 28 2019 Remi Collet <remi@remirepo.net> - 5.1.18-1
- update to 5.1.18

* Thu Oct  3 2019 Remi Collet <remi@remirepo.net> - 5.1.17-6
- more upstream patch for test suite

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 5.1.17-5
- rebuild for 7.4.0RC1

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 5.1.17-4
- rebuild for 7.4.0beta1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 5.1.17-3
- rebuild

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 5.1.17-2
- cleanup

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 5.1.17-1
- update to 5.1.17

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 5.1.16-1
- update to 5.1.16

* Fri Dec  7 2018 Remi Collet <remi@remirepo.net> - 5.1.15-1
- update to 5.1.15

* Wed Nov 21 2018 Remi Collet <remi@remirepo.net> - 5.1.14-1
- update to 5.1.14

* Mon Nov 19 2018 Remi Collet <remi@remirepo.net> - 5.1.13-1
- update to 5.1.13

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 5.1.12-3
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 5.1.12-2
- rebuld for 7.3.0alpha4 new ABI

* Mon Jul  9 2018 Remi Collet <remi@remirepo.net> - 5.1.12-1
- update to 5.1.12 (stable)

* Thu Mar  8 2018 Remi Collet <remi@remirepo.net> - 5.1.11-1
- update to 5.1.11 (stable)

* Mon Feb 26 2018 Remi Collet <remi@remirepo.net> - 5.1.10-2
- drop dependency on apcu-bc

* Fri Feb 16 2018 Remi Collet <remi@remirepo.net> - 5.1.10-1
- update to 5.1.10 (stable)

* Tue Jan  2 2018 Remi Collet <remi@fedoraproject.org> - 5.1.9-1
- Update to 5.1.9 (php 7, stable)

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 5.1.8-4
- rebuild for PHP 7.2.0beta1 new API

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 5.1.8-3
- rebuild for 7.2.0alpha2

* Thu Apr 13 2017 Remi Collet <remi@fedoraproject.org> - 5.1.8-2
- drop dependency on apcu-bc with PHP 7.2

* Mon Jan 16 2017 Remi Collet <remi@fedoraproject.org> - 5.1.8-1
- Update to 5.1.8 (php 7, stable)

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-2
- rebuild with PHP 7.1.0 GA

* Fri Oct 21 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-1
- Update to 5.1.7 (php 7, stable)

* Tue Oct 18 2016 Remi Collet <remi@fedoraproject.org> - 5.1.7-0.1.20161018gitb771cd5
- test for upcoming 5.1.7

* Thu Oct  6 2016 Remi Collet <remi@fedoraproject.org> - 5.1.6-1
- Update to 5.1.6 (php 7, stable)

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-4
- rebuild for PHP 7.1 new API version

* Mon Jul 25 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-3
- add patch for PHP 7.1 and ZTS

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-2
- disable ZTS build with PHP 7.1

* Tue Jun  7 2016 Remi Collet <remi@fedoraproject.org> - 5.1.5-1
- Update to 5.1.5 (php 7, stable)

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> - 5.1.4-1
- Update to 5.1.4 (php 7, stable)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 5.1.3-2
- adapt for F24

* Fri Jan 15 2016 Remi Collet <remi@fedoraproject.org> - 5.1.3-1
- Update to 5.1.3 (stable)

* Sat Jan  9 2016 Remi Collet <remi@fedoraproject.org> - 5.1.2-2
- add upstream patches to fix issues with apcu_inc / apcu_dec
  https://github.com/krakjoe/apcu/issues/158 - negative step hangs
  https://github.com/krakjoe/apcu/issues/164 - huge step performance

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- Update to 5.1.2 (stable)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-0.2
- test build of upcomming 5.1.2

* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-0.1.20151204gitba021db
- test build of upcomming 5.1.2

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0 (beta)

* Fri Nov 20 2015 Remi Collet <remi@fedoraproject.org> - 5.1.0-0.1.20151120gitba683bc
- test build for upcoming 5.1.0

* Fri Nov  6 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.6.20151106gitffb4fc8
- new snapshot

* Fri Nov  6 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.5.20151106gite032e7b
- new snapshot

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.4.20151014git9c361d2
- new snapshot (with apcu and apc extensions)

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.3.20150921gitea10226
- rebuild for PHP 7.0.0RC5 new API version
- new snapshot

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.2.20150921gitea10226
- new snapshot

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 5.0.0-0.1.20150921gita3128da
- update to 5.0.0-dev for PHP 7
- sources from github

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 4.0.7-3
- allow build against rh-php56 (as more-php56)

* Tue Jun  9 2015 Remi Collet <remi@fedoraproject.org> - 4.0.7-2
- upstream fix for the control panel
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 4.0.7-1.1
- Fedora 21 SCL mass rebuild

* Sat Oct 11 2014 Remi Collet <remi@fedoraproject.org> - 4.0.7-1
- Update to 4.0.7

* Sun Aug 24 2014 Remi Collet <remi@fedoraproject.org> - 4.0.6-2
- improve SCL stuff

* Thu Jun 12 2014 Remi Collet <remi@fedoraproject.org> - 4.0.6-1
- Update to 4.0.6 (beta)

* Wed Jun 11 2014 Remi Collet <remi@fedoraproject.org> - 4.0.5-1
- Update to 4.0.5 (beta)
- open https://github.com/krakjoe/apcu/pull/74 (PHP 5.4)

* Sun Jun  8 2014 Remi Collet <remi@fedoraproject.org> - 4.0.4-3
- add build patch for php 5.6.0beta4

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 4.0.4-2
- add numerical prefix to extension configuration file

* Sat Mar 01 2014 Remi Collet <remi@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4 (beta)

* Mon Jan 27 2014 Remi Collet <remi@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3 (beta)
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)
- drop panel sub-package in SCL
- add SCL stuff

* Mon Sep 16 2013 Remi Collet <rcollet@redhat.com> - 4.0.2-2
- fix perm on config dir
- always provides php-pecl-apc-devel and apc-panel

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2

* Fri Aug 30 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-3
- rebuild to have NEVR > EPEL (or Fedora)

* Thu Jul  4 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-2
- obsoletes APC with php 5.5
- restore APC serializers ABI (patch merged upstream)

* Tue Apr 30 2013 Remi Collet <remi@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1
- add missing scriptlet
- fix Conflicts

* Thu Apr 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-2
- fix segfault when used from command line

* Wed Mar 27 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-1
- first pecl release
- rename from php-apcu to php-pecl-apcu

* Tue Mar 26 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.4.git4322fad
- new snapshot (test before release)

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.3.git647cb2b
- new snapshot with our pull request
- allow to run test suite simultaneously on 32/64 arch
- build warning free

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.2.git6d20302
- new snapshot with full APC compatibility

* Sat Mar 23 2013 Remi Collet <remi@fedoraproject.org> - 4.0.0-0.1.git44e8dd4
- initial package, version 4.0.0
