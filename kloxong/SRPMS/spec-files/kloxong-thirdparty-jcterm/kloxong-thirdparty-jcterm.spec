%define kloxo /usr/local/lxlabs/kloxo/httpdocs/thirdparty
%define productname kloxong-thirdparty
%define packagename jcterm

Name: %{productname}-%{packagename}
Summary: JCTerm SSH access for webpages
Version: 0.0.10
Release: 2.kng%{?dist}
License: GPL
URL: http://lxcenter.org/
Group: Applications/Internet
Source0: %{packagename}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: lxphp
Provides: jcterm
Obsoletes: kloxomr7-thirdparty-jcterm, kloxomr-thirdparty-jcterm

%description
SSHTerm provides web based SSH access console (java applet)

%prep
%setup -q -n %{packagename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Wed Dec 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.0.10-1.mr
- First compile jcterm (alternative for sshterm-applet) for Kloxo-MR
