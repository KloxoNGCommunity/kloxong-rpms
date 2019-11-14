## MR -- enable this if want create debuginfo
%define  debug_package %{nil}

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} && 0%{?suse_version} >=1210)

%define STEP_VERSION f
%define REAL_VERSION 10.9
%define APPEAR_VERSION 10.9.0

%define _dist_ver %(sh /usr/lib/rpm/redhat/dist.sh)

%define FULL_VERSION %{APPEAR_VERSION}

Summary:	An advanced and secure webserver for Unix
Name:		hiawatha
Version:	%{FULL_VERSION}
Release:	%{STEP_VERSION}.2.kng%{?dist}
Source0:	http://www.hiawatha-webserver.org/files/%{name}-%{REAL_VERSION}.tar.gz
Source1:	%{name}-sysvscript
Source2:	%{name}-systemd

Patch0: 	hiawatha-9.6_maxuploadsize.patch
Patch1000: 	hiawatha-9.6_fix-dirprotect.patch
Patch1001: 	hiawatha-9.6_fix-cgiwrapper.patch
Patch1010: 	hiawatha-9.7_fix-chuck_size.patch
Patch1011: 	hiawatha-9.7_fix-ssl_return.patch
Patch1020: 	hiawatha-9.9_fixaccesslogfile.patch
Patch1030: 	hiawatha-9.11_fix-url-with-space.patch
Patch1031: 	hiawatha-9.11_change_polarssl_to_generic_libpath.patch
Patch1032: 	hiawatha-9.11_asn1parse_of_polarssl.patch
Patch1040: 	hiawatha-9.12_change_polarssl_to_generic_libpath.patch
Patch1041: 	hiawatha-9.12_fix_logrotate.patch
Patch1042: 	hiawatha-9.12_fix_envir_len.patch
Patch1043: 	hiawatha-9.12_fix_merge_chunks.patch
Patch1044: 	hiawatha-9.12_fix_merge_chunks_and_ssl_to_tls.patch
Patch1045: 	hiawatha-9.12_fix_merge_chunks_and_ssl_to_tls_2.patch
Patch1046: 	hiawatha-9.12_fix_logrotate2.patch
Patch1047: 	hiawatha-9.12_add_session_request_patch.patch

Patch1050: 	hiawatha-9.13_change_polarssl_to_generic_libpath.patch
Patch1051: 	hiawatha-9.14_change_polarssl_to_generic_libpath.patch

Patch1060: 	hiawatha-10.2-patch-22.patch

Patch1070: 	hiawatha-10.4_enable-root-user.patch

Patch1071: 	hiawatha-10.5_nobody-99.patch

Patch1080: 	hiawatha-10.9_mbedtls_bignum.patch

License:	GPLv2+
Group:		System Environment/Daemons
URL:		http://www.hiawatha-webserver.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake3 >= 3.0.0
BuildRequires:	make, gcc, glibc-devel, libxml2-devel, libxslt-devel, redhat-rpm-config
Requires:		libxml2,libxslt
Provides:		polarssl, mbedtls
Obsoletes:		polarssl, polarssl-devel, mbedtls, mbedtls-devel

%description
Hiawatha is an advanced and secure webserver for Unix. It has been written
with 'being secure' as its main goal. This resulted in a webserver which
has for example DoS protection, connection control and traffic throttling.
It has of course also thoroughly been checked and tested for buffer overflows.

%prep
#%setup -q
%setup -q -n %{name}-%{REAL_VERSION}
#sed -i -e '/add_subdirectory(polarssl)/d' -e 's| polarssl/include||' -e 's|${POLARSSL_LIBRARY}||' CMakeLists.txt
#sed -i '/^\tpolarssl/d' CMakeFiles.txt
sed -i 's|{CMAKE_INSTALL_FULL_LIBDIR}/hiawatha|{CMAKE_INSTALL_FULL_LIBDIR}|' CMakeLists.txt
sed -i 's|{CMAKE_INSTALL_LIBDIR}/hiawatha|{CMAKE_INSTALL_LIBDIR}|' CMakeLists.txt

#%patch0
#%patch1000 -p1
#%patch1001 -p1
#%patch1010 -p1
#%patch1011 -p1
#%patch1020 -p1

#%patch1030 -p1
#%patch1031 -p1
#%patch1032 -p1
#%patch1040 -p1
#%patch1041 -p1
#%patch1042 -p1
#%patch1043 -p1
#%patch1044 -p1
#%patch1045 -p1
#%patch1046 -p1
#%patch1047 -p1

#%patch1050 -p1
#%patch1051 -p1

#%patch1060 -p1

#%patch1070 -p1
%patch1071 -p1

%if 0%{?__isa_bits} != 64
%patch1080 -p1
%endif

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS
%cmake3 \
      -DCMAKE_INSTALL_PREFIX="" \
      -DCMAKE_INSTALL_BINDIR=%{_bindir} \
      -DCMAKE_INSTALL_SBINDIR=%{_sbindir} \
      -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_MANDIR=%{_mandir} \
      -DCONFIG_DIR=%{_sysconfdir}/hiawatha \
      -DLOG_DIR=%{_localstatedir}/log/hiawatha \
      -DPID_DIR=%{_localstatedir}/run \
      -DWORK_DIR=%{_localstatedir}/cache/hiawatha \
      -DENABLE_CACHE=ON \
      -DENABLE_IPV6=ON \
      -DENABLE_MONITOR=ON \
      -DENABLE_RPROXY=ON \
      -DENABLE_TLS=ON \
      -DENABLE_TOMAHAWK=ON \
      -DENABLE_TOOLKIT=ON \
      -DENABLE_TESTING=OFF \
      -DENABLE_XSLT=on


%__make %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
#make install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}/var/log/%{name}
install -D -m 644 logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
sed -i 's|/usr/var/log/hiawatha/|/var/log/hiawatha/|' %{buildroot}%{_sysconfdir}/%{name}/hiawatha.conf

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%else
# install SYSV init stuff
%{__mkdir} -p %{buildroot}%{_initrddir}
%{__install} -m755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/cache/hiawatha
%attr(0755,root,root) %dir %{_localstatedir}/log/hiawatha
%{_bindir}/ssi-cgi
%{_sbindir}/cgi-wrapper
%{_sbindir}/wigwam
%{_sbindir}/lefh
%{_libdir}/*
%if %{use_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%{_localstatedir}/www/hiawatha/index.html


%changelog
* Fri May 10 2019 Mustafa Ramadhan <mustafa@bigraf.com> - 10.9.0.f-2
- update to 10.9

* Thu Apr 27 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 10.6.0.f-1
- update to 10.6

* Sat Feb 04 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 10.5.0.f-2
- update to 10.5

* Thu Oct 20 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.4.0.f-2
- enable root user

* Thu Oct 20 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.4.0.f-1
- update to 10.4

* Sun Jun 04 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.3.0.f-1
- update to 10.3

* Mon May 31 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.2.0.f-7
- add patch 22 before 10.3 release

* Mon May 9 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.2.0.f-6
- update to 10.2

* Fri Feb 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 10.1.0.f-6
- update to 10.1

* Wed Dec 9 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 10.0.0.f-6
- update to 10.0

* Sun Oct 17 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.15.0.f-6
- update to 9.15
- use sed instead path for change_polarssl_to_generic_libpath

* Sun Jul 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.14.0.f-6
- update to 9.14

* Tue May 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.13.0.f-6
- update to 9.13

* Thu Apr 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-6
- fix logrotate
- add session request patch

* Wed Apr 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-5
- fix merge chunks (alt)
- change ssl to tls

* Mon Apr 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-4
- fix merge chunks

* Thu Feb 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-3
- fix envir len

* Tue Feb 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-2
- fix logrotate (change ownership from www-data to apache; change rotate to all log)

* Sun Feb 15 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.12.0.f-1
- update

* Fri Feb 06 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.11.0.f-4
- set obsoletes and provides for polarssl because trouble without polarssl in CentOS 6
- change polarssl path from /usr/lib/hiawatha to /usr/lib

* Wed Feb 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.11.0.f-3
- Change Requires and BuildRequires where remove polarssl

* Sat Jan 31 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.11.0.f-2
- fix url with space

* Sun Jan 25 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.11.0.f-1
- update

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.10.1.f-1
- update to 9.10.1

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 9.10.f-1
- update to 9.10

* Tue Dec 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.9.f-3
- back to use Requires and BuildRequires for polarssl

* Tue Dec 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.9.f-2
- fix accesslogfile for accept 'none'

* Mon Dec 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.9.f-1
- update to 9.9
- use built-in polarssl because still trouble for polarssl-1.3.9 compile

* Mon Sep 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.8.f-2
- update to 9.8
- enable 'Requires: polarssl'

* Sun Sep 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.7.p2-1
- add ssl_return patch (problem with keep-alive in reverse-proxy)

* Wed Sep 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.7.p1-1
- add chunk_size patch (problem with keep-alive in reverse-proxy)

* Sun Aug 31 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.7.f-3
- fix hiawatha-sysvscript

* Sun Aug 31 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.7.f-2
- update to 9.7 (already change MaxUploadSize 2048; URLToolkit in .hiawatha)
- mod hiawatha-sysvscript (init) to include '/etc/sysconfig/hiawatha' if exists
- use system/external polarssl with remove built-in polarssl

* Sun Jul 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.7.b-1
- update to 9.7.b (beta; enable urltoolkit in .hiawatha)

* Thu Jun 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.6-2
- add fixdirprotect patch

* Sun Jun 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.6-1
- update to 9.6

* Sat Apr 26 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.5-2
- recompile without patch (because compile bnutils 2.24 for Centos 5 64bit)

* Thu Apr 24 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.5-1
- update to 9.5 (with patch because the same touble like 9.5 with new polarssl)

* Sun Mar 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 9.4-1
- update to 9.4 with patch

* Thu Dec 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3.1-1
- update to 9.3.1

* Mon Dec 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3-2
- patch maxuploadsize from 100 to 2048MB

* Mon Nov 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.3-1
- update to 9.3
- make simple release

* Fri Aug 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.2-7.2
- fix hiawatha init (hiawatha-sysvscript) where change gprinf to 'echo -n'

* Sun Jul 28 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 9.2-7.1
- compile for Centos 5/6
- taken from http://download.opensuse.org/repositories/home:/akauffman/CentOS_CentOS-6/src/
- modified .spec for centos 5 compatilibity
