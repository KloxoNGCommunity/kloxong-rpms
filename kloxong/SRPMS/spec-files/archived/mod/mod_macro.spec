%define modn   macro
%define modv   1.1.11



Summary:       A module for using macros within Apache configs
Name:          mod_%{modn}
Version:       %{modv}
Release:       3%{?dist}
License:       Apache
Group:         System Environment/Daemons
Source0:       http://people.apache.org/~fabien/%{name}/%{name}-%{modv}.tar.gz
URL:           http://people.apache.org/~fabien/%{name}/
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:        Fabien Coelho <mod.macro@coelho.net>
Provides:      httpd-mod(%{modn}) = %{modv}
Provides:      %{name} = %{modv}

BuildRequires: httpd-devel >= 2.2 %{_bindir}/apxs
BuildRequires: libtool
%if 0%{?fedora} > 29 || 0%{?rhel} > 8
BuildRequires:  make
BuildRequires:	gcc
BuildRequires: gcc-c++
%endif


%description
Mod_macro is a third-party module to the Apache HTTP Server, allowing for
the definition and use of macros (configuration templates) within Apache
runtime configuration files. The syntax is a natural extension to Apache
html-like configuration style.


%prep
%setup -q


%build
%{_bindir}/apxs -c %{name}.c

%{__cat} <<EOF >macro.conf
# This is the Apache server configuration file for mod_macro.
#
LoadModule macro_module modules/mod_macro.so
EOF

%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules

%{__install} -m 0755 .libs/%{name}.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
%{__install} -Dp -m 0644 macro.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/macro.conf


%postun
# Restart after erase/upgrade
# /sbin/service httpd condrestart >/dev/null 2>&1 || :


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES INSTALL LICENSE README
%doc *.html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{modn}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Mon Sep 15 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.11-3
- Disable requires to httpd

* Mon Aug 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.11-1
- compile for httpd 2.2 for Kloxo-MR

* Wed Apr 04 2012 Peter Pramberger <peterpramb@member.fsf.org> - 1.1.11-1
- Initial build
