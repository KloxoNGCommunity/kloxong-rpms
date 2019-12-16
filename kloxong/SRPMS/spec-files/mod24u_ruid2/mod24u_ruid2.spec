%define debug_package %{nil}

%define apxs $(which apxs)

%define real_name mod_ruid2

Name: mod24u_ruid2
Version: 0.9.8
#Release: 1%{?dist}
Release: 3.kng%{?dist}
Summary: Suexec module for apache

Group: System Environment/Daemons
License: ASL 2.0
URL: http://space.dl.sourceforge.net/project/mod-ruid/
Source0: http://space.dl.sourceforge.net/project/mod-ruid/mod_ruid2/%{real_name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{real_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: httpd >= 2.4, libcap-devel, httpd-devel
#Requires: httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
# Hardcode httpd-mm value for copr build
Requires:	httpd-mmn = 20120211x8664
Requires: httpd >= 2.4
Obsoletes: mod_ruid


%description
With this module, all httpd process run under user's access right, not nobody or
apache. mod_ruid2 is similar to mod_suid2, but has better performance than 
mod_suid2 because it doesn`t need to kill httpd children after one request.
It makes use of kernel capabilites and after receiving a new request suids 
again. If you want to run apache modules, i.e. WebDAV, PHP, and so on under 
user's right, this module is useful.


%prep
%setup -n %{real_name}-%{version}


%build
%{apxs} -a -l cap -c mod_ruid2.c


%install
rm -rf %{buildroot}
install -D -p -m 0755 .libs/mod_ruid2.so \
    %{buildroot}%{_libdir}/httpd/modules/mod_ruid2.so


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_ruid2.so



%changelog
* Fri Jun 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.8-3.mr
- recompile with rename to mod24u_ruid2

* Fri Aug 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.8-1.mr
- update to 0.9.8

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.7-3.mr
- change mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Aug 19 2012 Mustafa Ramadhan (mustafa.ramadhan@lxcenter.org) 0.9.7-2.lx.el5
- Update to 0.9.7 and recompile for lxcenter

* Thu Sep 08 2011 Denis Frolov <d.frolov81@mail.ru> 0.9.4-1
- update to mod_ruid2 0.9.4

* Thu Sep 22 2008 Denis Frolov <d.frolov81@mail.ru> 0.6-1
- Initial RPM release.
