Name:           mod_rpaf
Version:        0.6
#Release:        2%{?dist}
Release:        4%{?dist}
Summary:        Reverse proxy add forward module for Apache

Group:          System Environment/Daemons
License:        ASL 1.0
URL:            http://stderr.net/apache/rpaf/
Source0:        http://stderr.net/apache/rpaf/download/%{name}-%{version}.tar.gz
Patch0:         mod_rpaf-0.6-Make.patch
Patch1:         mod_rpaf-0.6.path
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
Requires:       httpd

%description
Reverse proxy add forward module for Apache


%prep
%setup -q
%patch0 -p1 -b .makefile
pwd
%patch1 -p0 -b .path


%build
make rpaf-2.0


%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -pm 755 .libs/mod_rpaf-2.0.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README CHANGES
%{_libdir}/httpd/modules/mod_rpaf-2.0.so



%changelog
* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.6-4.mr.el5
- change mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Aug 19 2012 Mustafa Ramadhan (mustafa.ramadhan@lxcenter.org) 0.6-3.lx.el5
- Recompile for lxcenter

* Sun Aug 23 2009 Frolov Denis <d.frolov81 at mail.ru> 0.6-2
- Add path patch

* Mon May 27 2008 Frolov Denis <d.frolov81 at mail.ru> 0.6-1
- Initial build for Red Hat Club Repository