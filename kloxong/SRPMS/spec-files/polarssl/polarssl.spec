Name:           polarssl
Version:        1.3.8
Release:        1%{?dist}
Summary:        Light-weight cryptographic and SSL/TLS library

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://polarssl.org/
Source0:        http://polarssl.org/download/%{name}-%{version}-gpl.tgz

Patch0: 	polarssl_pthread_enable.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PolarSSL is a light-weight open source cryptographic and SSL/TLS
library written in C. PolarSSL makes it easy for developers to include
cryptographic and SSL/TLS capabilities in their (embedded)
applications with as little hassle as possible.

%package        utils
Summary:        Utilities for %{name}
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    utils
Cryptographic utilities based on %{name}. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%cmake \
	-DCMAKE_BUILD_TYPE:String="Release" \
	-DUSE_SHARED_POLARSSL_LIBRARY:BOOL=1 \
	-DPOLARSSL_THREADING_PTHREAD:BOOL=1 \
	-DPOLARSSL_THREADING_C:BOOL=1 .
make %{?_smp_mflags} all apidoc

%check
LD_LIBRARY_PATH=$PWD/library ctest --output-on-failure -V

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/polarssl/bin
mv -f $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libexecdir}/polarssl
## MR -- remove png files because make devel more than 10MB
rm -rf apidoc/*.png

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE ChangeLog
%{_libdir}/*

%files utils
%{_libexecdir}/%{name}/

%files devel
%doc apidoc/*
%{_includedir}/%{name}/
%{_libdir}/*

%changelog
* Sun Aug 31 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.8-1
- polarssl 1.3.8

* Sun Jun 01 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.7-1
- polarssl 1.3.7
- recompile for Kloxo-MR

* Wed Nov 06 2013 Mads Kiilerich <mads@kiilerich.com> - 1.3.2-1
- polarssl 1.3.2

* Tue Oct 29 2013 Mads Kiilerich <mads@kiilerich.com> - 1.3.1-1
- polarssl 1.3.1

* Wed Oct 02 2013 Mads Kiilerich <mads@kiilerich.com> - 1.3.0-1
- polarssl 1.3.0

* Wed Oct 02 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.9-1
- polarssl 1.2.9

* Mon Sep 09 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.8-1
- polarssl 1.2.8

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.7-1
- Update 1.2.7 (Fix FTBFS on ARM), cleanup SPEC

* Sun Mar 31 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.6-1
- polarssl-1.2.6
    - TLS and DTLS protocol issue:      CVE-2013-0169  (bug 907589)
    - out-of-bounds comparisons:        CVE-2013-1621  (bug 908423)

* Sun Feb 03 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.5-1
- polarssl-1.2.5

* Thu Jan 31 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.4-1
- polarssl-1.2.4

* Sun Jan 20 2013 Mads Kiilerich <mads@kiilerich.com> - 1.2.3-1
- polarssl-1.2.3

* Sat Jan 19 2013 Mads Kiilerich <mads@kiilerich.com> - 1.1.5-1
- polarssl-1.1.5

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 02 2012 Mads Kiilerich <mads@kiilerich.com> - 1.1.4-1
- polarssl-1.1.4

* Sun Apr 29 2012 Mads Kiilerich <mads@kiilerich.com> - 1.1.3-1
- polarssl-1.1.3

* Sat Apr 28 2012 Mads Kiilerich <mads@kiilerich.com> - 1.1.2-1
- polarssl-1.1.2

* Thu Mar 15 2012 Mads Kiilerich <mads@kiilerich.com> - 1.1.1-1
- polarssl-1.1.1
- Remove old hacks and patches
- New -utils subpackage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 17 2011 Mads Kiilerich <mads@kiilerich.com> - 0.14.3-1
- polarssl-0.14.3

* Tue Feb 22 2011 Mads Kiilerich <mads@kiilerich.com> - 0.14.1-1
- polarssl-0.14.1 bugfix release
- removed doc patch and replaced relevant parts with sed

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Mads Kiilerich <mads@kiilerich.com> - 0.14.0-4
- First official approved package

* Sun Jan 30 2011 Mads Kiilerich <mads@kiilerich.com> - 0.14.0-3
- More specific %%files
- Rename patches to polarssl prefix and show their summary

* Sat Nov 13 2010 Mads Kiilerich <mads@kiilerich.com> - 0.14.0-2
- Fix lib64 issue by updating cmake install patches to use LIB_INSTALL_DIR
- Add comment that patches has been sent upstream

* Wed Sep 15 2010 Mads Kiilerich <mads@kiilerich.com> - 0.14.0-1
- Initial Fedora package
