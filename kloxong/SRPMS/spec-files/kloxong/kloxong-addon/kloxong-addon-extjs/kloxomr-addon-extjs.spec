%define kloxo /usr/local/lxlabs/kloxo/httpdocs/htmllib
%define productname kloxomr-addon
%define packagename extjs
%define sourcename ext

Name: %{productname}-%{packagename}
Summary: Javascript Framework
Version: 1.1
Release: 4%{?dist}
License: GPL
URL: http://www.extjs.com/
Group: Applications/Internet

# Where to get old versions
# http://www.sencha.com/learn/legacy/Ext_Version_Archives 
# Repacked to tar.gz
Source0: %{sourcename}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, lxphp >= 4.0.4
Obsoletes: kloxo-extjs

%description
JavaScript Framework for HTML

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
%doc INCLUDE_ORDER.txt license.txt
%{kloxo}/%{packagename}

%changelog
* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 1.1-2.lx
- rename

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 1.1-1
- Initial start of this SPEC
