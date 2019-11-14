%define kloxocp /home/kloxo/httpd/cp
%define productname kloxong-panel
%define packagename mywebsql
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript Framework HTML 
Version: 3.7
Release: 1.kng%{?dist}
License: GPL
URL: http://mywebsql.net/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Obsoletes: kloxomr-panel-mywebsql

%description
MyWebSql is an open source, web based, WYSIWYG mysql client written in PHP. 
It utilizes modern day technologies and browsers to provide a fast, 
intuitive querying and editing interface to the mysql databases. 

Simplified Database Web Administration. For MySQL, SQLite and PostgreSQL databases.

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

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 3.7-1.mr
- update to 3.7

* Sat Oct 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 3.6-1.mr
- update to 3.6

* Tue Oct 21 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5-1.mr
- update to 3.5

* Wed Apr 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 3.4-1.mr
- update to 3.4

* Sun Aug 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.3-1.mr
- make rpm for Kloxo-MR
