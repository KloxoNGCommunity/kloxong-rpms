%global	checkout	1fba865ab73cc98a3109f88d85eb82c1bfc29b37

%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

%define php_base php54
%define real_name php-suhosin
%define name %{php_base}-suhosin

Name:          	%{name} 
Version:        0.9.38
Release:        1%{?dist}
Summary:        Suhosin is an advanced protection system for PHP installations

Group:          Development/Languages
License:        PHP
URL:            http://www.hardened-php.net/suhosin/
# git clone https://github.com/stefanesser/suhosin.git suhosin
# cd suhosin && git checkout %%{checkout} && cd ../
# tar czvf suhosin-%%{version}.tgz ./suhosin/
Source0:        http://download.suhosin.org/suhosin-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       %{real_name} = %{version}
BuildRequires:  %{php_base}-devel
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_apiver}
Requires:       %{php_base}

# FIX ME: This should be removed before/after RHEL 5.6 is out
# See: https://bugs.launchpad.net/ius/+bug/691755


%description
Suhosin is an advanced protection system for PHP installations. It was designed 
to protect servers and users from known and unknown flaws in PHP applications 
and the PHP core.  

%prep
%setup -q -n suhosin-%{version}

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
* Thu May 21 2015 Ben Harper <ben.harper@rackspace.com> - 0.9.38-1.ius
- Latest upstream

* Tue Feb 17 2015 Carl George <carl.george@rackspace.com> - 0.9.37.1-1.ius
- Latest upstream

* Fri Dec 05 2014 Ben Harper <ben.harper@rackspace.com> - 0.9.37-1.ius
- Latest sources from upstream

* Thu Jun 12 2014 Ben Harper <ben.harper@rackspace.com> - 0.9.36-1.ius
- Latest sources from upstream

* Tue Feb 25 2014 Ben Harper <ben.harper@rackspace.com> - 0.9.35-1.ius
- Latest sources from upstream

* Wed Jun 27 2012 Mark McKinstry <mmckinst@nexcess.net> - 0.9.34-20120520.1.ius
- use 0.9.34 from git for PHP 5.4

* Thu Jan 26 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.9.33-1
- Latest sources from upstream

* Mon Oct 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.9.32.1-5
- Adding Providers for php-suhosin

* Fri Aug 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.9.32.1-4
- Rebuilding

* Tue Feb 01 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 0.9.32.1-3
- Removed Obsoletes: php53*

* Fri Dec 17 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.9.32.1-2
- Name change to php53u-suhosin.  Resolves: LP#691755
  Obsoletes php53-suhosin
- Rebuild against php53u-5.3.4

* Mon Jul 27 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.9.32.1-1
- Latest sources from upstream
- Built against php53-5.3.3

* Wed Feb 10 2010 BJ Dierkes <wdierkes@rackspace.com> - 0.9.29-1
- Porting from Fedora 12 to IUS
- Latest sources from upstream

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.9.27-3
- rebuild for new PHP 5.3.0 ABI (20090626)

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
