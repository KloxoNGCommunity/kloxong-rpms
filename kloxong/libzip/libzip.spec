# remirepo spec file for libzip and remi-libzip
# renamed for parallel installation, from:
#
# Fedora spec file for libzip
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

## FOR EL-7
##     build as libzip5
## FOR EL-8
##     1st build --with    move_to_opt for SCL
##     2nd build --without move_to_opt for module
## FOR EL-9
##     build as remi-libzip

%global libname libzip
%global soname  5
%bcond_without  tests

%if 0%{?vendeur:1} && 0%{?rhel} >= 8
%bcond_without move_to_opt
%else
%bcond_with    move_to_opt
%endif

%if %{with move_to_opt}
%global _prefix /opt/%{?vendeur:%{vendeur}/}%{libname}
%global __arch_install_post /bin/true
Name:    %{?vendeur:%{vendeur}-}%{libname}
%else
%if 0%{?rhel} == 7
Name:    %{libname}%{soname}
%else
Name:    %{libname}
%endif
%endif

Version: 1.9.2
Release: 3%{?dist}
Summary: C library for reading, creating, and modifying zip archives

License: BSD
URL:     https://libzip.org/
Source0: https://libzip.org/download/libzip-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  zlib-devel >= 1.1.2
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  xz-devel >= 5.2
# for ZSTD_minCLevel
BuildRequires:  libzstd-devel   >= 1.3.6
Requires:       libzstd%{?_isa} >= 1.3.6
%if 0%{?rhel} == 7
BuildRequires:  cmake3 >= 3.0.2
%else
BuildRequires:  cmake >= 3.0.2
%endif
# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
# find regress/ -type f | /usr/lib/rpm/perl.prov
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%if 0%{?rhel} == 7
# RHEL have commands in main package
Provides:  %{libname} =  %{version}-%{release}
%endif
%if %{with move_to_opt}
%if 0%{?rhel} == 8
Obsoletes: php56-libzip < %{version}
Obsoletes: php70-libzip < %{version}
Obsoletes: php71-libzip < %{version}
Obsoletes: php72-libzip < %{version}
Obsoletes: php73-libzip < %{version}
Obsoletes: php74-libzip < %{version}
Obsoletes: php80-libzip < %{version}
Obsoletes: php81-libzip < %{version}
Obsoletes: php82-libzip < %{version}
%endif

# Filter in the /opt installation
%{?filter_from_provides: %filter_from_provides /libzip/d}
%{?filter_from_requires: %filter_from_requires /libzip/d}
%{?filter_setup}

%global __provides_exclude ^(libzip\\.so|cmake|pkgconfig).*$
%global __requires_exclude ^libzip\\.so.*$
%endif


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.
%if "%{name}" != "%{libname}"
%{name} is designed to be installed beside %{libname}.
%endif


%package devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%if 0%{?rhel} == 7
Conflicts: %{libname}-last-devel     <  %{version}
Conflicts: %{libname}-devel          <  %{version}
Provides:  %{libname}-devel          =  %{version}-%{release}
%endif
%if %{with move_to_opt} && 0%{?rhel} == 8
Obsoletes: php56-libzip-devel < %{version}
Obsoletes: php70-libzip-devel < %{version}
Obsoletes: php71-libzip-devel < %{version}
Obsoletes: php72-libzip-devel < %{version}
Obsoletes: php73-libzip-devel < %{version}
Obsoletes: php74-libzip-devel < %{version}
Obsoletes: php80-libzip-devel < %{version}
Obsoletes: php81-libzip-devel < %{version}
Obsoletes: php82-libzip-devel < %{version}
%endif

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:  Command line tools from %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%if 0%{?rhel} == 7
Conflicts: %{libname}-last-tools     <  %{version}
Conflicts: %{libname}-tools          <  %{version}
# RHEL have commands in main package
Conflicts: %{libname}                <  1.1
%endif
%if %{with move_to_opt} && 0%{?rhel} == 8
Obsoletes: php56-libzip-tools < %{version}
Obsoletes: php70-libzip-tools < %{version}
Obsoletes: php71-libzip-tools < %{version}
Obsoletes: php72-libzip-tools < %{version}
Obsoletes: php73-libzip-tools < %{version}
Obsoletes: php74-libzip-tools < %{version}
Obsoletes: php80-libzip-tools < %{version}
Obsoletes: php81-libzip-tools < %{version}
Obsoletes: php82-libzip-tools < %{version}
%endif

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- zipcmp
- zipmerge
- ziptool


%prep
%setup -q -n %{libname}-%{version}
: ========== BUILD in %{_prefix} ==========

# unwanted in package documentation
rm INSTALL.md

# drop skipped test which make test suite fails (cmake issue ?)
sed -e '/clone-fs-/d' \
%if 0%{?rhel} == 7
    -e '/add_from_stdin/d' \
%endif
    -i regress/CMakeLists.txt


%build
%if 0%{?rhel} == 7
sed -e 's/COMMAND cmake /COMMAND cmake3 /' -i CMakeLists.txt regress/CMakeLists.txt
%cmake3 \
%else
%cmake . \
%endif
  -DENABLE_COMMONCRYPTO:BOOL=OFF \
  -DENABLE_GNUTLS:BOOL=OFF \
  -DENABLE_MBEDTLS:BOOL=OFF \
  -DENABLE_OPENSSL:BOOL=ON \
  -DENABLE_WINDOWS_CRYPTO:BOOL=OFF \
  -DENABLE_BZIP2:BOOL=ON \
  -DENABLE_LZMA:BOOL=ON \
  -DENABLE_ZSTD:BOOL=ON \
  -DBUILD_TOOLS:BOOL=ON \
  -DBUILD_REGRESS:BOOL=ON \
  -DBUILD_EXAMPLES:BOOL=OFF \
  -DBUILD_DOC:BOOL=ON \
  .

%if 0%{?cmake_build:1}
%cmake_build
%else
make %{?_smp_mflags}
%endif


%install
mkdir -p %{buildroot}%{_licensedir}

%if 0%{?cmake_install:1}
%cmake_install
%else
make install DESTDIR=%{buildroot} INSTALL='install -p'
%endif

%if %{with move_to_opt}
mkdir -p %{buildroot}%{_datadir}/licenses
mkdir -p %{buildroot}%{_datadir}/doc
%endif

%check
%if %{with tests}
%if 0%{?ctest:1}
%ctest
%else
make check
%endif
%else
: Test suite disabled
%endif


%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif


%files
%license LICENSE
%{_libdir}/libzip.so.%{soname}*
%if %{with move_to_opt}
%dir %{_prefix}
%dir %{_mandir}
%dir %{_libdir}
%dir %{_libdir}
%dir %{_datadir}
%dir %{_datadir}/licenses
%endif

%files tools
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptool
%{_mandir}/man1/zip*
%if %{with move_to_opt}
%dir %{_bindir}
%dir %{_mandir}/man1
%endif

%files devel
%doc AUTHORS THANKS *.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_libdir}/cmake/libzip
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*
%if %{with move_to_opt}
%dir %{_includedir}
%dir %{_mandir}/man3
%dir %{_libdir}/pkgconfig
%dir %{_libdir}/cmake
%dir %{_datadir}/doc
%endif


%changelog
* Wed Jun 29 2022 Remi Collet <remi@remirepo.net> - 1.9.2-3
- switch to libzip5 on EL-7

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.9.2-2
- don't obsolete libzip5 and php*-libzip for now

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.9.2-1
- update to 1.9.2
- also build as remi-libzip for EL-7 and EL-8

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.9.0-2
- add upstream patch for zip_file_is_seekable reported as
  https://github.com/nih-at/libzip/issues/297
  https://github.com/nih-at/libzip/issues/301

* Tue Jun 14 2022 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0

* Mon Nov  8 2021 Remi Collet <remi@remirepo.net> - 1.8.0-3
- build as remi-libzip for EL-9

* Mon Jun 21 2021 Remi Collet <remi@remirepo.net> - 1.8.0-2
- ensure libzstd >= 1.3.6 is used

* Sat Jun 19 2021 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0
- enable zstd compression support

* Thu Nov  5 2020 Remi Collet <remi@remirepo.net> - 1.7.3-2
- adapt for SCL build

* Wed Jul 15 2020 Remi Collet <remi@remirepo.net> - 1.7.3-1
- update to 1.7.3
- drop patch merged upstream

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 1.7.2-2
- test build for upstream fix

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 1.7.2-1
- update to 1.7.2
- fix installation layout using patch from
  https://github.com/nih-at/libzip/pull/190
- fix pkgconfig usability using patch from
  https://github.com/nih-at/libzip/pull/191

* Sun Jun 14 2020 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 1.7.0-1
- update to 1.7.0
- really enable lzma support (excepted on EL-6)
- patch zipconf.h to re-add missing LIBZIP_VERSION_* macros

* Mon Feb  3 2020 Remi Collet <remi@remirepo.net> - 1.6.1-1
- update to 1.6.1

* Fri Jan 24 2020 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0
- enable lzma support (excepted on EL-6)

* Tue Mar 12 2019 Remi Collet <remi@remirepo.net> - 1.5.2-1
- update to 1.5.2
- add all explicit cmake options to ensure openssl is used
  even in local build with other lilbraries available

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1
- drop dependency on zlib-devel and bzip2-devel no more
  referenced in libzip.pc
- drop rpath patch merged upstream

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 1.5.0-2
- add dependency on zlib-devel and bzip2-devel #1556068

* Mon Mar 12 2018 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0
- use openssl for cryptography instead of bundled custom AES implementation

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.4.0-5
- missing BR on C compiler
- drop ldconfig scriptlets (F28+)

* Fri Jan  5 2018 Remi Collet <remi@remirepo.net> - 1.4.0-3
- add upstream patch and drop multilib hack

* Tue Jan  2 2018 Remi Collet <remi@remirepo.net> - 1.4.0-2
- re-add multilib hack #1529886

* Sat Dec 30 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0
- switch to cmake
- add upstream patch for lib64

* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2

* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.3.1-2
- add upstream patch for regression in 1.3.1

* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1
- drop multilib header hack
- change URL to https://libzip.org/

* Fri Oct  6 2017 Remi Collet <remi@fedoraproject.org> - 1.3.0-2
- test build

* Mon Sep  4 2017 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- add dependency on bzip2 library
- ignore 3 tests failing on 32-bit

* Sun Feb 19 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- rename to libzip5 for new soname

* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3

* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1-1
- update to 1.1
- new ziptool command
- add fix for undefined optopt in ziptool.c (upstream)

* Thu Jan 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- libzip obsoletes libzip-last

* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- soname bump from .2 to .4
- drop ziptorrent
- create "tools" sub package
- rename to libzip-last to allow parallel installation

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-5
- actually apply patch (using %%autosetup)

* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-4
- CVE-2015-2331: integer overflow when processing ZIP archives (#1204676,#1204677)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Remi Collet <remi@fedoraproject.org> - 0.11.2-1
- update to 0.11.2
- run test during build

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-3
- replace php patch with upstream one

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-2
- include API-CHANGES and LICENSE in package doc

* Thu Aug 08 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-1
- update to 0.11.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-5
- fix typo in multiarch (#866171)

* Wed Sep 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-4
- Warning about conflicting contexts for /usr/lib64/libzip/include/zipconf.h versus /usr/include/zipconf-64.h (#853954)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-2
- spec cleanup, better multilib fix

* Wed Mar 21 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-1
- update to 0.10.1 (security fix only)
- fixes for CVE-2012-1162 and CVE-2012-1163

* Sun Mar 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-2
- try to fix ARM issue (#799684)

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-1
- update to 0.10
- apply patch with changes from php bundled lib (thanks spot)
- handle multiarch headers (ex from MySQL)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-2
- Cleaned up pkgconfig deps which are now automatically handled by RPM.

* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-1
- Updated to libzip 0.9.3

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.9-4
- Use bzipped upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- libzip-0.9

* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.8-5
- rebuild for new gcc-4.3

* Fri Jan 11 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.8-4
- use better workaround for removing rpaths

* Tue Nov 20 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-3
- require pkgconfig in devel subpkg
- move api description to devel subpkg
- keep timestamps in %%install
- avoid lib64 rpaths 

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-2
- Change License to BSD

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-1
- Initial version for Fedora
