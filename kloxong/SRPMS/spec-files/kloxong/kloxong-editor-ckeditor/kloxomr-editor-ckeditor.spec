%define kloxo /usr/local/lxlabs/kloxo/httpdocs/editor
%define productname kloxong-editor
%define packagename ckeditor
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript WYSIWYG Editor 
Version: 4.5.11
Release: 1%{?dist}
License: GPL
URL: http://ckeditor.com/
Group: Applications/Internet

Source0: %{sourcename}_%{version}_full.tar.gz
Source1: kloxo.js

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, lxphp >= 4.0.4
Obsoletes: kloxo-ckeditor, kloxomr-addon-ckeditor, kloxomr7-editor-ckeditor, kloxomr-editor-ckeditor

%description
CKEditor is a text editor to be used inside web pages. It's a WYSIWYG editor, which 
means that the text being edited on it looks as similar as possible to the results 
users have when publishing it. It brings to the web common editing features found on 
desktop editing applications like Microsoft Word and OpenOffice.


%prep
%setup -q -n %{sourcename}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__mv} -f $RPM_BUILD_ROOT%{kloxo}/%{packagename}/config.js $RPM_BUILD_ROOT%{kloxo}/%{packagename}/config.js.original
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{kloxo}/%{packagename}/kloxo.js

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,lxlabs,lxlabs,755)
#%doc CHANGES.html INSTALL.html LICENSE.html
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Thu Jun 07 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 4.5.11-1.mr
- update

* Sat Sep 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.5.3-1.mr
- update

* Thu Feb 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.7-1.mr
- update

* Mon Dec 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.6-1.mr
- update to 4.4.6

* Sun Oct 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.5-1.mr
- update to 4.4.5

* Sun Jul 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.3-1.mr
- update to 4.4.3

* Fri Jun 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.2-1.mr
- update to 4.4.2

* Fri Jun 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.1-3.mr
- change custom config to kloxo.js and fix content (change to full from body)

* Wed Jun 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.1-2.mr
- move to editor dir

* Thu Jun 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.4.1-1.mr
- update to 4.4.1, add custom config.js and no obsoletes for fckeditor

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2.1-2.mr
- fix obsolote entry

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.2.1-1.mr
- update to 4.2.1

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.6.4-3.mr
- change conflict with obsolete

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.6.4-2.mr
- rename rpm

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.6.4-1.mr
- update to new version

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 3.6.2-1
- Initial start of this SPEC
