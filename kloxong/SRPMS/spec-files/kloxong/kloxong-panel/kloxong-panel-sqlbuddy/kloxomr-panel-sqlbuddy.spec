%define kloxocp /home/kloxo/httpd/cp
%define productname kloxong-panel
%define packagename sqlbuddy
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript Framework HTML 
Version: 1.3.3
Release: 1%{?dist}
License: GPL
URL: http://sqlbuddy.com/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Obsoletes: kloxomr-panel-sqlbuddy

%description
SQL Buddy ? Web based MySQL administration.

%prep
%setup -q -n %{sourcename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxocp}/%{packagename}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,apache,apache,755)
%{kloxocp}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun Aug 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.3-1.mr
- make rpm for Kloxo-MR
