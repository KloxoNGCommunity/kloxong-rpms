%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name mongo
%global real_name php-pecl-mongo
%global basever 1
%global php_base php54

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


Summary:      PHP MongoDB database driver
Name:         %{php_base}-pecl-mongo
Version:      1.6.9
Release:      1%{?dist}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:      %{pecl_name}.ini
%{?el5:BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)}
BuildRequires: %{php_base}-devel
BuildRequires: %{php_base}-pear
BuildRequires: openssl-devel
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if 0%{?php_zend_api:1}
Requires:     %{php_base}(zend-abi) = %{php_zend_api}
Requires:     %{php_base}(api) = %{php_core_api}
%else
Requires:     %{php_base}-api = %{php_apiver}
%endif
Provides:     %{real_name} = %{version}-%{release}
Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     %{php_base}-pecl(%{pecl_name}) = %{version}-%{release}


%description
This package provides an interface for communicating with the MongoDB database
in PHP.


%prep
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure 
%{__make} %{?_smp_mflags}


%install
%{?el5:%{__rm} -rf %{buildroot}}
cd %{pecl_name}-%{version}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__install} -Dm0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install XML package description
%{__install} -Dm0644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%{?el5:%clean}
%{?el5:%{__rm} -rf %{buildroot}}


%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
cd %{pecl_name}-%{version}
# only check if build extension can be loaded

%{_bindir}/php \
    -n -d extension=json.so \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"


%files
%doc %{pecl_name}-%{version}/README.md
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Jun 10 2015 Carl George <carl.george@rackspace.com> - 1.6.9-1.ius
- Latest upstream

* Thu May 14 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.8-1.ius
- Latest upstream

* Wed Apr 29 2015 Carl George <carl.george@rackspace.com> - 1.6.7-1.ius
- Latest upstream

* Mon Mar 30 2015 Carl George <carl.george@rackspace.com> - 1.6.6-1.ius
- Latest upstream

* Tue Mar 17 2015 Carl George <carl.george@rackspace.com> - 1.6.5-1.ius
- Latest upstream
- Add build dependency on openssl-devel

* Mon Mar 02 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.3-1.ius
- Latest upstream

* Wed Feb 11 2015 Carl George <carl.george@rackspace.com> - 1.6.2-1.ius
- Latest upstream

* Thu Feb 05 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.1-1.ius
- Latest sources from upstream

* Thu Jan 29 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.0-1.ius
- Latest sources from upstream

* Tue Nov 11 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.8-1.ius
- Latest sources from upstream

* Tue Sep 16 2014 Carl George <carl.george@rackspace.com> - 1.5.7-1.ius
- Latest sources from upstream
- Move config from a here doc to separate source file

* Thu Jul 31 2014 Carl George <carl.george@rackspace.com> - 1.5.5-1.ius
- Latest sources from upstream

* Wed Jun 18 2014 Carl George <carl.george@rackspace.com> - 1.5.4-1.ius
- Latest sources from upstream

* Fri Jun 06 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.3-1.ius
- Latest sources from upstream

* Wed May 07 2014 Carl George <carl.george@rackspace.com> - 1.5.2-1.ius
- Latest sources from upstream

* Mon Apr 07 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.1-1.ius
- Latest sources from upstream

* Fri Apr 04 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.0-1.ius
- Latest sources from upstream
- update check based on remi's 1.5.0alpha1

* Fri Jan 24 2014 Ben Harper <ben.harper@rackspace.com> - 1.4.5-1.ius
- Latest sources from upstream

* Wed Nov 06 2013 Ben Harper <ben.harper@rackspace.com> - 1.3.2-2
- adding provides per LP bug 1248285

* Mon Dec 31 2012 Ben Harper <ben.harper@rackspace.com> - 1.3.2-1
- porting from EPEL
- upsteam 1.3.2 

* Sat Jul 28 2012 Christof Damian <christof@damian.net> - 1.2.12-1
- upstream 1.2.12

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Christof Damian <christof@damian.net> - 1.2.10-1
- upstream 1.2.10

* Sat Mar  3 2012 Christof Damian <christof@damian.net> - 1.2.9-1
- upstream 1.2.9

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- update to 1.2.7 for php 5.4
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Christof Damian <christof@damian.net> - 1.2.1-1
- upstream 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Christof Damian <christof@damian.net> - 1.0.10-4
- added link to option docs

* Sat Oct 23 2010 Christof Damian <christof@damian.net> - 1.0.10-3
- fix post
- add example config with sensible defaults
- add conditionals for EPEL + fix for check

* Fri Oct 22 2010 Christof Damian <christof@damian.net> - 1.0.10-2
- fixes for package review: requires and warnings

* Wed Oct 20 2010 Christof Damian <christof@damian.net> - 1.0.10-1
- Initial RPM
