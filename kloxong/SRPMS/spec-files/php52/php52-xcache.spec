%global php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %((echo 0; php-config --version 2>/dev/null) | tail -1)

%define real_name php-xcache
%define name php52-xcache

Summary:       PHP accelerator, optimizer, encoder and dynamic content cacher
Name:          %{name}
Version:       3.1.0
Release:       2%{?dist}
License:       BSD
Group:         Development/Languages
Vendor:        IUS Community Project
URL:           http://xcache.lighttpd.net/
Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/xcache-%{version}.tar.gz
Source1:       xcache.ini
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:     php52-eaccelerator php52-pecl-apc
BuildRequires: php-devel >= 5.1.0
#BuildRequires: autoconf < 2.63
BuildRequires: autoconf

Provides:      php52-eaccelerator = %{version}-%{release}
Requires:      php52(zend-abi) = %{php_zend_api}
Requires:      php52(api) = %{php_core_api}

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load.

%prep
%setup -q -n xcache-%{version}
%{__rm} -f coverager/common-zh-simplified-gb2312.lang.php

%build
phpize
%configure --enable-xcache \
           --enable-xcache-constant \
           --enable-xcache-optimizer \
           --enable-xcache-coverager \
           --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

%{__install} -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini
sed -i -e 's|/EXT_DIR|%{php_extdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc xcache.ini AUTHORS ChangeLog NEWS README THANKS COPYING
%doc htdocs
%config(noreplace) %{_sysconfdir}/php.d/xcache.ini
%{php_extdir}/xcache.so

%changelog
* Fri Mar 7 2014 Mustafa Ramadhan <mustafa@bigraf.com> -  3.1.0-2.ius
- update to 3.1.0

* Fri Jan 11 2013 Ben Harper <ben.harper@rackspace.com> -  3.0.1-1.ius
- Latest sources from upstream

* Mon Nov 05 2012 Ben Harper <ben.harper@rackspace.com> -  3.0.0-1.ius
- Latest sources from upstream
- update xcache.ini to load module via extension as zend_extension is nsupported

* Thu Jul 19 2012 Dustin Offutt <dustin.offutt@rackspace.com> - 2.0.1-1.ius
- Latest sources from upstream

* Mon Apr 23 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.0.0-1.ius
- Latest sources from upstream

* Mon Jun 06 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.3.2-1.ius
- Latest sources from upstream

* Mon Jan 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.3.0-4.ius
- Porting from bugzilla #563510 to IUS
- Adding Provides tag

* Tue Feb 16 2010 Timon <timosha@gmail.com> - 1.3.0-4
- review notes

* Thu Feb 11 2010 Timon <timosha@gmail.com> - 1.3.0-3
- remove xcache.ini from spec
- remove RHEL lines
- add some configure features
- add doc files
- review fixes

* Wed Feb 10 2010 Timon <timosha@gmail.com> 1.3.0-1
- Updated source to 1.3.0
- First release for Fedora12


