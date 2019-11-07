Summary:	Apache module to process security in the webserver config
Name:		mod_process_security
Version:	1.0
Release:	2%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://github.com/matsumoto-r/mod_process_security
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	httpd-devel, libcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global modulesdir %{_libdir}/httpd/modules

%description
%{name} is a suEXEC module for CGI and DSO. Improvement of mod_ruid2(vulnerability) 
and mod_suexec(performance).

%prep
#%setup -q -n %{name}
%setup -q

%build
%{_sbindir}/apxs -i -c -l cap %{name}.c

%{__cat} <<EOF >process_security.conf
# This is the Apache server configuration file for mod_process_security.
#
LoadModule process_security_module modules/mod_process_security.so


#<IfModule process_security.c>
#    PSExAll On
#    PSExCGI On
#    PSExtensions .php .pl .py
#    PSIgnoreExtensions .html .css
#    ## MR - use this one
#    PSMinUidGid 200 200
#    ## MR - or use default by module
#    PSDefaultUidGid
#    PSRootEnable On
#</IfModule>
EOF


%install
rm -rf $%{buildroot}
mkdir -p %{buildroot}/%{modulesdir}
%{_sbindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n %{name} %{name}.la
%{__install} -Dp -m 0644 process_security.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/process_security.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{modulesdir}/%{name}.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/process_security.conf


%changelog
* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0-2.mr
- add BuildRequires to libcap-devel

* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0-1.mr
- first compile for Kloxo-MR

