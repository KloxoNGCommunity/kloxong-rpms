%define kloxo /home/kloxo/httpd/webmail
%define productname kloxomr-webmail
%define packagename t-dah

Name: %{productname}-%{packagename}
Summary: T-dah webmail
Version: 3.2.0.2.3
Release: 4%{?dist}
License: GPL
URL: http://tdah.us/
Group: Applications/Internet

Source0: %{packagename}-%{version}.tar.bz2
Source1: t-dah_config.php
Source2: t-dah_config.paths.php
Source3: t-dah_config.mail.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Provides: webmail
Obsoletes: kloxo-t-dah

%description
T-dah is an Open Sourced Universal Webmail origially developed by Aldoir Ventura 
under the name Uebimiau in which we picked up late in 2007. 

It is free and can be installed on any server that supports PHP.

%prep
%setup -q -n %{packagename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

install -D -m 755 $RPM_SOURCE_DIR/t-dah_config.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/t-dah/inc/config/t-dah_config.php
install -D -m 755 $RPM_SOURCE_DIR/t-dah_config.paths.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/t-dah/inc/config/t-dah_config.paths.php
install -D -m 755 $RPM_SOURCE_DIR/t-dah_config.mail.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/t-dah/inc/config/t-dah_config.mail.php

%post

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
%dir %{kloxo}/%{packagename}
%{kloxo}/%{packagename}

%changelog
* Mon Mar 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.2.0-2.3-4.mr
- set host to 'localhost'

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.2.0-2.3-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.2.0-2.3-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Jan 6 2013 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.2.0-2.3-2.lx
- first create kloxo-t-dah rpm
