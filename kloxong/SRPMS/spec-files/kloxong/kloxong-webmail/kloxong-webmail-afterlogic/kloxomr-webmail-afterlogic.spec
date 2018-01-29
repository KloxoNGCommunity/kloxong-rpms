%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename afterlogic
%define sourcename afterlogic-webmail

Name: %{productname}-%{packagename}
Summary: Roundcube webmail client
Version: 7.7.2
#Release: 1%{?dist}
Release: 1%{?dist}
License: GPL
URL: http://www.roundcube.net/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.gz
Source1: afterlogic_settings.xml.php
Source2: afterlogic_initial.sql
Source3: afterlogic_inc_settings_path.php

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Provides: webmail
Obsoletes: kloxo-afterlogic, kloxomr-webmail-afterlogic

%description
Roundcube webmail is a browser-based multilingual IMAP client with an 
application-like user interface. It provides full functionality you
expect from an e-mail client, including MIME support, address book,
folder manipulation, message searching and spell checking. 

%prep
%setup -q -n %{sourcename}-%{version}

%post
%{__mv} -f $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/install/installer.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/install/installer.php.bck
%{__rm} -rf $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/@@@install@@@
%{__mv} -f $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/install $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/@@@install@@@
sed -i "s:settings.xml':settings.xml.php':" $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/libraries/afterlogic/common/settings.php

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

install -D -m 755 $RPM_SOURCE_DIR/afterlogic_settings.xml.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/data/settings/afterlogic_settings.xml.php
install -D -m 755 $RPM_SOURCE_DIR/afterlogic_initial.sql $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/data/settings/afterlogic_initial.sql
install -D -m 755 $RPM_SOURCE_DIR/afterlogic_inc_settings_path.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/afterlogic/inc_settings_path.php

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

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.7.2-1.mr
- update to 7.7.2

* Tue Mar 01 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.6.7-1.mr
- update to 7.6.6
- add create database in afterlogic_initial.sql

* Thu Dec 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.6.6-1.mr
- update to 7.6.6

* Thu Oct 08 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.6.2-1.mr
- update to 7.6.2

* Wed Apr 29 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.6.0-3.mr
- update to 7.6.0

* Tue Apr 26 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.5.0-3.mr
- change settings.xml to settings.xml.php for security reason

* Tue Apr 14 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.5.0-1.mr
- update to 7.5.0

* Fri Apr 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.2-5.mr
- fix/mod afterlogic_settings.xml

* Mon Mar 30 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.2-4.mr
- fix sql file (missing create database)

* Fri Mar 27 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.2-3.mr
- update afterlogic_initial.sql (because the old not work)

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.2-2.mr
- fix mv for install dir

* Sun Jan 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.2-1.mr
- update to 7.4.2

* Tue Nov 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.1-1.mr
- update to 7.4.1

* Thu Sep 25 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.4.0.7-2.mr
- fix afterlogic_settings.xml
- update to 7.4.0.7

* Sun Jul 6 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.3.0.3-1.mr
- update to 7.3.0.3

* Sat Mar 1 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 7.2.1-1.mr
- update 7.2.1
- fix mysql data (add skype and facebook column in awm_addr_book)

* Wed Jun 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.1-2.mr
- update to 7.0.2

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 7.0.1-1.mr
- update to 7.0.1

* Mon Mar 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1-4.mr
- set Layout to 'Bottom' instead 'Side'
- set slavehost also to 'localhost'

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 6.5.1-3.mr
- change DefaultTimeFormat to F24 and OutgoingSendingMethod to NoAuth for afterlogic_initial.sql
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Fri Dec 21 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 6.5.1-2.lx
- Initial start of this SPEC
- @@install@@
- incude ready-made setting.xml and initial.sql

