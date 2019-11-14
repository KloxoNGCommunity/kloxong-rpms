%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename telaen

Name: %{productname}-%{packagename}
Summary: Telaen webmail
Version: 1.3.2
Release: 3.kng%{?dist}
License: GPL
URL: https://github.com/jimjag/telaen
Group: Applications/Internet

Source0: %{packagename}-%{version}.tar.bz2
Source1: telaen_config.languages.php
Source2: telaen_config.php
Source3: telaen_config.security.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Provides: webmail
Obsoletes: kloxo-telaen, kloxomr-webmail-telaen

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

install -D -m 755 $RPM_SOURCE_DIR/telaen_config.languages.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/telaen/inc/config/config.languages.php.default
install -D -m 755 $RPM_SOURCE_DIR/telaen_config.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/telaen/inc/config/config.php.default
install -D -m 755 $RPM_SOURCE_DIR/telaen_config.security.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/telaen/inc/config/config.security.php.default

%post
if [ ! -d /tmp/telaen ] ; then
	mkdir -p /tmp/telaen
	chown apache:apache /tmp/telaen
fi

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

* Mon Mar 16 2015  Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.2-3.mr
- update iCalcreator.class.php from 2.14 to 2.20.2 (fix no warning if not found .ics file)
- still warning for class.mymonth.php
- fix default configs copy


* Thu Jun 27 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.2-2.mr
- fix config copy

* Wed Jun 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3.2-1.mr
- first compile
