Summary:	Apache module to define variables in the webserver config
Name:		mod_define
Version:	2.2
Release:	3%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		http://people.apache.org/~rjung/mod_define/
Source0:	%{name}/%{name}-%{version}.tar.bz2
Source1:      define.conf
BuildRequires:	httpd-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global modulesdir %{_libdir}/httpd/modules

%description
%{name} is an Apache module which allows one to define variables in the web
server configuration files and to use again later in the files.  This allows
one to build configurations which are easier to understand and maintain.

%prep
#%setup -q -n %{name}
%setup -q

%build
%{_sbindir}/apxs -c %{name}.c

%{__cat} <<EOF >define.conf
# This is the Apache server configuration file for mod_define.
#
LoadModule define_module modules/mod_define.so
EOF


%install
rm -rf $%{buildroot}
mkdir -p %{buildroot}/%{modulesdir}
%{_sbindir}/apxs -i -S LIBEXECDIR=%{buildroot}/%{modulesdir} -n %{name} %{name}.la
%{__install} -Dp -m 0644 define.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/define.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README mod_define.html
%{modulesdir}/%{name}.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/define.conf


%changelog
* Thu Aug 07 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.2-3.mr
- Add define.conf

* Mon Aug 04 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.2-1.mr
- compile for httpd 2.2 for Kloxo-MR
- update to 2.2

* Thu Feb 09 2012 [simoN] <simontdd@psu.edu> 2.1-1.dsel
- initial RPM package - v2.1
