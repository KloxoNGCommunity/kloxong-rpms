%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename egroupware

Name: %{productname}-%{packagename}
Summary: EGroupware Community Edition
Version: 1.8.004
Release: 2%{?dist}
License: GPL
URL: http://http://www.egroupware.org/
Group: Applications/Internet

Source0: ftp://ftp.horde.org/pub/horde-webmail/%{packagename}-core-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Provides: webmail
Requires: kloxong-webmail-egroupware-addressbook, kloxong-webmail-egroupware-admin
Requires: kloxong-webmail-egroupware-calendar, kloxong-webmail-egroupware-egw-pear
Requires: kloxong-webmail-egroupware-filemanager, kloxong-webmail-egroupware-gallery
Requires: kloxong-webmail-egroupware-infolog, kloxong-webmail-egroupware-phpfreechat
Requires: kloxong-webmail-egroupware-polls, kloxong-webmail-egroupware-projectmanager
Requires: kloxong-webmail-egroupware-sitemgr, kloxong-webmail-egroupware-timesheet
Requires: kloxong-webmail-egroupware-tracker, kloxong-webmail-egroupware-wiki
Obsoletes: kloxo-egroupware, kloxomr-webmail-egroupware-core

%description
EGroupware is a multi-user, web-based groupware suite.
Currently available modules include: email, addressbook, calendar, 
infolog (notes, to-do's, phone calls), content management, wiki, 
project management, tracker, timesheet, knowledge base, CalDAV/CardDAV

%prep
%setup -q -n %{packagename}-core-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%post

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
%dir %{kloxo}/%{packagename}
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.8.004-2.mr
- rename rpm

* Sun Jan 6 2013 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.8.004-2.mr
- first create  EGroupware Community Edition for Kloxo-MR
