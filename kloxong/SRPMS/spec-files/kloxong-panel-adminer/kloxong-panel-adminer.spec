%define kloxocp /home/kloxo/httpd/cp
%define productname kloxong-panel
%define packagename adminer
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript Framework HTML 
Version: 4.7.1
Release: 1.kng%{?dist}
License: GPL
URL: http://www.adminer.org/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.gz
Source1: index_adminer.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Obsoletes: kloxomr-panel-adminer

%description
Adminer (formerly phpMinAdmin) is a full-featured database management tool written in PHP.
Conversely to phpMyAdmin, it consist of a single file ready to deploy to the target server.
Adminer is available for MySQL, PostgreSQL, SQLite, MS SQL and Oracle.

%prep
%setup -q -n %{sourcename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__cp} -rp %{SOURCE1} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/index.php

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,apache,apache,755)
%{kloxocp}/%{packagename}

%changelog
* Thu Jun 06 2019 Mustafa Ramadhan <mustafa@bigraf.com> - 4.7.1-1.mr
- update 4.7.1
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 4.3.1-1.mr
- update 4.3.1

* Sun Aug 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2.2-1.mr
- update 4.2.2

* Sat Mar 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2.1-1.mr
- update 4.2.1

* Thu Feb 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2.0-1.mr
- update 4.2.0

* Wed Apr 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.1.0-1.mr
- update 4.1.0

* Sun Aug 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.7.1-2.mr
- add index_adminer.php (to process compile and rename adminer.php to index.php)

* Sun Aug 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.7.1-1.mr
- make rpm for Kloxo-MR
