%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename egroupware
%define portionname gallery-modules1

Name: %{productname}-%{packagename}-%{portionname}
Summary: EGroupware Community Edition
Version: 1.8.004
Release: 2%{?dist}
License: GPL
URL: http://http://www.egroupware.org/
Group: Applications/Internet

Source0: ftp://ftp.horde.org/pub/horde-webmail/%{packagename}-%{portionname}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Provides: webmail
Obsoletes: kloxo-egroupware-gallery-modules1, kloxomr-webmail-egroupware-gallery-modules1
Requires: kloxong-webmail-egroupware-gallery

%description
EGroupware is a multi-user, web-based groupware suite.
Currently available modules include: email, addressbook, calendar, 
infolog (notes, to-do's, phone calls), content management, wiki, 
project management, tracker, timesheet, knowledge base, CalDAV/CardDAV

%prep
%setup -q -n %{packagename}-%{portionname}-%{version}

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
