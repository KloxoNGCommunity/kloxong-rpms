%global php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %((echo 0; php-config --version 2>/dev/null) | tail -1)

%define real_name php-xcache
%define name php54-xcache

Summary:       PHP accelerator, optimizer, encoder and dynamic content cacher
Name:          %{name}
Version:       3.2.0
Release:       1%{?dist}
License:       BSD
Group:         Development/Languages
Vendor:        IUS Community Project
URL:           http://xcache.lighttpd.net/
Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/xcache-%{version}.tar.gz
Source1:       xcache.ini
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:     php54-eaccelerator php54-pecl-apc
BuildRequires: php54-devel >= 5.1.0

# to force use of autoconf and not autoconf26x
#%if 0%{?rhel} >= 6
BuildRequires: autoconf
#%else
#BuildRequires: autoconf < 2.63
#%endif

Provides:      php-eaccelerator = %{version}-%{release}
Requires:      php54(zend-abi) = %{php_zend_api}
Requires:      php54(api) = %{php_core_api}

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
* Fri Sep 19 2014 Ben Harper <ben.harper@rackspace.com> - 3.2.0-1.ius
- Latest sources from upstream

* Mon Oct 14 2013 Ben Harper <ben.harper@rackspace.com> - 3.1.0-1.ius
- Latest sources from upstream

* Tue Jun 18 2013 Ben Harper <ben.harper@rackspace.com> - 3.0.3-1.ius
- Latest sources from upstream

* Thu Jun 13 2013 Ben Harper <ben.harper@rackspace.com> - 3.0.2-1.ius
- Latest sources from upstream

* Fri Jan 11 2013 Ben Harper <ben.harper@rackspace.com> - 3.0.1-1.ius
- Latest sources from upstream 

* Mon Nov 05 2012 Ben Harper <ben.harper@rackspace.com> -  3.0.0-1.ius
- Latest sources from upstream
- update xcache.ini to load module via extension as zend_extension is not supported
   
* Tue Aug 21 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.0.1-2.ius
- Rebuilding against php54-5.4.6-2.ius as it is now using bundled PCRE.

* Thu Jul 19 2012 Dustin Offutt <dustin.offutt@rackspace.com> - 2.0.1-1.ius
- Latest sources from upstream

* Mon May 14 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.0.0-1.ius
- New package for php54
