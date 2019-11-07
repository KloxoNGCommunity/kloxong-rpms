%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename roundcube
%define sourcename roundcubemail

Name: %{productname}-%{packagename}
Summary: Roundcube webmail client
Version: 1.2.5
#Release: 1%{?dist}
Release: 1%{?dist}
License: GPL
URL: http://www.roundcube.net/
Group: Applications/Internet

Source0: %{sourcename}-%{version}-complete.tar.gz
Source1: roundcube_db.inc.php
Source2: roundcube_main.inc.php
Source3: roundcube_mysql.initial.sql
#Source4: roundcube_mysql.update.sql
Source5: roundcube_config.inc.php
Source6: roundcube_defaults.inc.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Provides: webmail
Obsoletes: kloxo-roundcube, kloxomr-webmail-roundcube

%description
Roundcube webmail is a browser-based multilingual IMAP client with an 
application-like user interface. It provides full functionality you
expect from an e-mail client, including MIME support, address book,
folder manipulation, message searching and spell checking. 

%prep
%setup -q -n %{sourcename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

install -D -m 755 $RPM_SOURCE_DIR/roundcube_db.inc.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/config/roundcube_db.inc.php
install -D -m 755 $RPM_SOURCE_DIR/roundcube_main.inc.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/config/roundcube_main.inc.php
install -D -m 755 $RPM_SOURCE_DIR/roundcube_mysql.initial.sql $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/SQL/roundcube_mysql.initial.sql
#install -D -m 755 $RPM_SOURCE_DIR/roundcube_mysql.update.sql $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/SQL/roundcube_mysql.update.sql
install -D -m 755 $RPM_SOURCE_DIR/roundcube_config.inc.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/config/roundcube_config.inc.php
install -D -m 755 $RPM_SOURCE_DIR/roundcube_defaults.inc.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/roundcube/config/roundcube_defaults.inc.php

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
#%doc README CHANGELOG INSTALL LICENSE UPGRADING
#%doc CHANGELOG INSTALL LICENSE UPGRADING
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.5-1.mr
- update to 1.2.5

* Tue Jul 26 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.0-1.mr
- update to 1.2.0

* Sun Jun 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.2-1.mr
- update to 1.1.2

* Tue Mar 31 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.1-3.mr
- fix sql file (wrong database name)

* Mon Mar 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.1-2.mr
- fix sql file (missing create database)

* Sat Mar 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.1-1.mr
- update to 1.1.1

* Thu Feb 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1.0-1.mr
- update 1.1.0

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.4-1.mr
- update to 1.0.4

* Tue Sep 30 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.3-1.mr
- update to 1.0.3

* Sun Sep 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.2-1.mr
- update to 1.0.2

* Wed Jun 11 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.1-3.mr
- update to 1.0.1

* Tue Mar 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.rc-3.mr
- update to 1.0.rc

* Sun Mar 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.5-2.mr
- fix database (add database name)

* Sun Mar 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 0.9.5-1.mr
- downgrade to 0.9.5 because still trouble with database!

* Sat Mar 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0.rc-1.mr
- update to 1.0-rc

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.8.5-1.mr
- update and rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.8.4-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Mon Nov 26 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 0.8.4-2.lx
- update to 0.8.4

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 0.8.1-1.lx
- update to 0.8.1

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 0.7.1-1
- Initial start of this SPEC
