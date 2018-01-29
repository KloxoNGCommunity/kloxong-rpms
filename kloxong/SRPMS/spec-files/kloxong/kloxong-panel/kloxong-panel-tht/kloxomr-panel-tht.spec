%define kloxocp /home/kloxo/httpd/cp
%define productname kloxong-panel
%define packagename tht
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Web-based Billing System
Version: 1.2.6
Release: 3%{?dist}
License: GPL
URL: http://thehostingtool.com/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.bz2
Source1: naxes-kloxo-1.0.tar.bz2
Source2: tht_install.sql
Source3: tht_upgrade.sql
Source4: tht_conf.inc.php
Source5: kloxo_reworked.php
Source6: kloxo.php

Patch0: tht-1.2.6_mod.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Obsoletes: kloxomr-panel-tht

%description
TheHostingTool is aiming to provide the next generation in free, hosting applications. 
It provides you, the webhost, near complete automation on everything you want it to do. 
So that means, signup, monthly posts checking, suspension, and termination. 
While it does that, it provides client features, like the client control panel that gives 
the clients the power to manage their account.

%prep
%setup -q -n %{sourcename}-%{version}
%patch0 -p1

tar xvfj %{SOURCE1}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__cp} -rp %{SOURCE2} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/tht_install.sql
%{__cp} -rp %{SOURCE3} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/tht_upgrade.sql
%{__cp} -rp %{SOURCE4} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/tht_conf.inc.php
%{__cp} -rp %{SOURCE4} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/includes/conf.inc.php
%{__cp} -rp $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/naxes-kloxo-1.0/* $RPM_BUILD_ROOT%{kloxocp}/%{packagename}
%{__rm} -rf $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/naxes-kloxo-1.0
%{__cp} -rp %{SOURCE6} $RPM_BUILD_ROOT%{kloxocp}/%{packagename}/includes/servers/kloxo.php

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,apache,apache,755)
%{kloxocp}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.6-3.mr
- use modified kloxo.php instead kloxo_reworked.php

* Tue Apr 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.6-2.mr
- add kloxo.php from tht reworked 1.3.10 and rename to kloxo_reworked.php

* Fri Apr 24 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2.6-1.mr
- Compile TheHostingTool for Kloxo-MR

