%define kloxo /home/kloxo/httpd/webmail
%define productname kloxong-webmail
%define packagename rainloop
%define sourcename rainloop-webmail

Name: %{productname}-%{packagename}
Summary: Rainloop webmail client
Version: 1.12.1
Release: 1.kng%{?dist}
License: GPL
URL: http://rainloop.net/
Group: Applications/Internet
# Use rainloop community version and repackage zip to tarball eg rainloop-community-1.11.0.203.zip -> rainloop-1.11.0.203.tar.gz
Source0: %{sourcename}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 4.0.4, php-mbstring
#Requires: /usr/sbin/sendmail
Provides: webmail

Obsoletes: kloxomr-webmail-rainloop

%description
Rainloop webmail is simple, modern & fast web-based email client

%prep
%setup -q -n %{sourcename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
#%doc README CHANGELOG INSTALL LICENSE UPGRADING
#%doc CHANGELOG INSTALL LICENSE UPGRADING
%{kloxo}/%{packagename}

%changelog
* Mon Feb 3 2020 John Parnell Pierce <john@luckytanuki.com> 1.12.1-1
- upgrade

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> 1.11.0.203-1
- update
* Tue Apr 05 2016 Mustafa Ramadhan <mustafa@bigraf.com> 1.9.4.402-1
- update
* Sun Sep 14 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.6.9.164-1
- First compile for Kloxo-MR
