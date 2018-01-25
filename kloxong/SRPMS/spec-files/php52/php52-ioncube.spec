%global         php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")
%define         realname ioncube
%define         name php52-ioncube

Name:           %{name}
Version:        4.2
Release:        1%{?dist}
Summary:        PHP ionCube Loader

Group:          Development/Languages
License:        Other
URL:            http://www.ioncube.com
Source0:        http://downloads2.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.bz2

BuildRoot:      %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: php, php-devel
BuildRequires: autoconf, automake, libtool
Requires: %{name}(zend-abi) = %{php_zend_api}
Requires: %{name}(api) = %{php_core_api}

%description
ionCube Loader for php

%prep
%setup -q -n %{realname}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{realname}.ini << 'EOF'
; Enable %{name} zend extension module
zend_extension=/usr/lib64/php/modules/ioncube_loader_lin_5.2.so
EOF

%{__mkdir_p} %{buildroot}%{php_extdir}
%{__install} -m 644 ioncube_loader_lin_5.2.so %{buildroot}%{php_extdir}/ioncube_loader_lin_5.2.so

%clean
%{__rm} -rf %{buildroot}


%preun


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%config(noreplace) %{_sysconfdir}/php.d/%{realname}.ini
%{php_extdir}/ioncube_loader_lin_5.2.so


%changelog
* Sun Mar 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2-1
- compile and rename to php52-ioncube

* Wed Dec 22 2010 Denis Frolov <d.frolov81@mail.ru> - 4.2-1
- update to 4.2

* Wed Sep 03 2010 Denis Frolov <d.frolov81@mail.ru> - 3.3-1
- Initial RPM release.

