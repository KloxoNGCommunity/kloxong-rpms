%define kloxo /usr/local/lxlabs/kloxo/httpdocs/thirdparty
%define productname kloxomr-thirdparty
%define packagename sshterm-applet

Name: %{productname}-%{packagename}
Summary: SSHTerm SSH access for webpages
Version: 0.2.2
Release: 4%{?dist}
License: GPL
URL: http://lxcenter.org/
Group: Applications/Internet
Source0: %{packagename}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: lxphp
Provides: sshterm
Obsoletes: kloxo-sshterm-applet, kloxomr7-thirdparty-sshterm-applet

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
* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.2.2-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 0.2.2-1.lx
- change to version 0.2.2 - the last sshtools.com product version before change to j2ssh

* Sun Mar 11 2012 Danny Terweij <contact@lxcenter.org> - 0.0.1-1
- Initial start of this SPEC
- Source is unknown just packed current dir and set version to 0.0.1
