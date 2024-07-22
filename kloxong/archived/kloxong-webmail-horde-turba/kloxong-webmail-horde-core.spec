%define kloxo /home/kloxo/httpd/webmail
%define productname kloxo-webmail
%define packagename horde

Name: %{productname}-%{packagename}
Summary: Horde webmail client
Version: 1.2.11
Release: 9%{?dist}
License: GPL
URL: http://www.horde.org/
Group: Applications/Internet

Source0: ftp://ftp.horde.org/pub/horde-webmail/%{packagename}-core-%{version}.tar.bz2
Source1: horde_conf.php
Source1: horde_groupware.mysql.sql

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Requires: kloxo-webmail-horde-dimp, kloxo-webmail-horde-imp
Requires: kloxo-webmail-horde-ingo, kloxo-webmail-horde-kronolith
Requires: kloxo-webmail-horde-mimp, kloxo-webmail-horde-mnemo
Requires: kloxo-webmail-horde-nag, kloxo-webmail-horde-pear
Requires: kloxo-webmail-horde-turba
Provides: webmail
Obsoletes: kloxong-horde, kloxomr-webmail-horde-core

%description
Horde Groupware Webmail Edition is a free, enterprise ready, browser
based collaboration suite. Users can manage and share calendars,
contacts, tasks and notes with the standards compliant components from
the Horde Project.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Webmail) please visit <http://www.horde.org/>.

%prep
%setup -q -n %{packagename}-core-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

# Do not install this file and directories
%{__rm} -f $RPM_BUILD_ROOT%{kloxo}/%{packagename}/test.php

# Move 2 files into docs
%{__mv} -f COPYING $RPM_BUILD_ROOT%{kloxo}/%{packagename}/docs/
%{__mv} -f README $RPM_BUILD_ROOT%{kloxo}/%{packagename}/docs/

install -D -m 755 $RPM_SOURCE_DIR/horde_conf.php $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/horde/config/horde_conf.php
install -D -m 755 $RPM_SOURCE_DIR/horde_groupware.mysql.sql $RPM_BUILD_ROOT/home/kloxo/httpd/webmail/horde/scripts/sql/horde_groupware.mysql.sql

%post

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
%doc docs/*
%dir %{kloxo}/%{packagename}
%{kloxo}/%{packagename}

%changelog
* Wed Jun 19 2024 John Parnell Pierce <john@luckytanuki.com>
- Change product name back to Kloxo

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.11-9.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.11-9.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Jan 6 2013 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.2.11-8.lx
- include ready-made conf.php (handling deprecated warning)
- split src to core, dimp, imp, ingo, kronolith, mimp, mnemo, nag, pear and turba

* Tue Oct 2 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.2.11-6.lx
- 'pear' also separate rpm

* Tue Oct 2 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.2.11-5.lx
- fix 'Requires'

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.2.11-4.lx
- split package

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.2.11-2.lx
- rename

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 1.2.11-1
- Initial start of this SPEC
