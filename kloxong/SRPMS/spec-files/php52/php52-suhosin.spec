%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define	realname php-suhosin
%define	name php52-suhosin

Name:           %{name}
Version:        0.9.33
Release:        3%{?dist}
Summary:        Suhosin is an advanced protection system for PHP installations

Group:          Development/Languages
License:        PHP
URL:            http://www.hardened-php.net/suhosin/
Source0:        http://download.suhosin.org/suhosin-%{version}.tgz
Patch0:         suhosin-0.9.33-php-5.2.17.patch
BuildRoot:      %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)
Epoch:          2

BuildRequires:  php-devel
Requires:       %{name}(zend-abi) = %{php_zend_api}
Requires:       %{name}(api) = %{php_apiver}

%description
Suhosin is an advanced protection system for PHP installations. It was designed 
to protect servers and users from known and unknown flaws in PHP applications 
and the PHP core.  

%prep
%setup -q -n suhosin-%{version}
%patch0 -p1


%build
%{_bindir}/phpize
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# install configuration
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%{__cp} suhosin.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d/suhosin.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changelog 
%doc CREDITS
%config(noreplace) %{_sysconfdir}/php.d/suhosin.ini
%{php_extdir}/suhosin.so

%changelog
* Sun Mar 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.33-1
- compile and rename to php52-suhosin

* Mon Jan 23 2012 Denis Frolov <d.frolov81@mail.ru> - 0.9.33-1
- Update to 0.9.33

* Thu Sep 02 2010 Denis Frolov <d.frolov81@mail.ru> - 0.9.32.1-1
- Update to 0.9.32.1

* Mon Mar 29 2010 Denis Frolov <d.frolov81@mail.ru> - 0.9.31-1
- Update to 0.9.31

* Sun Mar 28 2010 Denis Frolov <d.frolov81@mail.ru> - 0.9.30-1
- Update to 0.9.30

* Sun Mar 08 2010 Denis Frolov <d.frolov81@mail.ru> - 0.9.29-3
- Rebuild for php 5.3.2

* Wed Nov 25 2009 Denis Frolov <d.frolov81@mail.ru> - 0.9.29-2
- Rebuild for php 5.3.1

* Thu Sep 01 2009 Denis Frolov <d.frolov81@mail.ru> - 0.9.29-1
- Update to 0.9.29

* Fri Jul 03 2009 Denis Frolov <d.frolov81@mail.ru> - 0.9.27-2
- Rebuilt for CentOS 5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.27-1
- Update to version 0.9.27

* Thu Aug 7 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.25-1
- Update to version 0.9.25

* Wed Jun 18 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.24-1
- Update to version 0.9.24

* Tue Apr 29 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.23-1
- Update to version 0.9.23
- Some specfile updates for review

* Fri Jan 4 2008 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-2
- Use short name for license

* Wed Dec 5 2007 Bart Vanbrabant <bart.vanbrabant@zoeloelip.be> 0.9.22-1
- Initial packaging of 0.9.22
