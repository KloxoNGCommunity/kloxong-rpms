%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}



Summary:	Apache module to process security in the webserver config
Name:		mod_process_security
Version:	1.1.4
Release:	2.kng%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://github.com/matsumoto-r/mod_process_security
Source0: https://github.com/matsumotory/%{name}/archive/v%{version}.tar.gz
Source1: mod_process_security.conf
BuildRequires: httpd-devel
BuildRequires: pkgconfig
BuildRequires: libcap-devel


BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global modulesdir %{_libdir}/httpd/modules

%description
%{name} is a suEXEC module for CGI and DSO. Improvement of mod_ruid2(vulnerability) 
and mod_suexec(performance).

%prep
#%setup -q -n %{name}
%setup -q

%build

#%{_sbindir}/apxs -i -c -l cap %{name}.c
%{_httpd_apxs} -c -Wc,"%{optflags} -Wall -pedantic -std=c99" -l cap %{name}.c.c


%install
rm -rf $%{buildroot}
mkdir -p %{buildroot}/%{modulesdir}

install -D -p -m 0755 .libs/mod_process_security.so \
    %{buildroot}%{_httpd_moddir}/mod_process_security.so

install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_httpd_confdir}/mod_process_security.conf
    
#%{_sbindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n %{name} %{name}.la
#%{__install} -Dp -m 0644 process_security.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/process_security.conf

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

