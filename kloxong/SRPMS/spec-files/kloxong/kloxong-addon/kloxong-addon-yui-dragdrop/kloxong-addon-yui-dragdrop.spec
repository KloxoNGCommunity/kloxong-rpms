%define kloxo /usr/local/lxlabs/kloxo/httpdocs/htmllib
%define productname kloxong-addon
%define packagename yui-dragdrop
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript Framework HTML 
Version: 2.9.0
Release: 3%{?dist}
License: GPL
URL: http://yuilibrary.com/yui/docs/dd/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, lxphp >= 4.0.4
Obsoletes: kloxo-yui-dragdrop, kloxomr-addon-yui-dragdrop

%description
The Drag and Drop Utility allows you to create a draggable interface efficiently, 
buffering you from browser-level abnormalities and enabling you to focus on the 
interesting logic surrounding your particular implementation. This component enables 
you to create a variety of standard draggable objects with just a few lines of code and 
then, using its extensive API, add your own specific implementation logic.

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
%doc README
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.9.0-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.9.0-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 2.9.0-2.lx
- update to new version

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 2.2.2-1
- Initial start of this SPEC
