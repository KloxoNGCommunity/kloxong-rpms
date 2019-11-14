%define kloxo /usr/local/lxlabs/kloxo/httpdocs/editor
%define productname kloxong-addon
%define packagename fckeditor
%define sourcename %{packagename}

Name: %{productname}-%{packagename}
Summary: Javascript WYSIWYG Editor 
#Version: 2.4.3
Version: 2.6.8
Release: 7.kng%{?dist}
License: GPL
URL: http://ckeditor.com/
Group: Applications/Internet

Source0: %{sourcename}-%{version}.tar.bz2

#BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, lxphp >= 4.0.4
Obsoletes: kloxo-fckeditor

%description
FCKEditor is a text editor to be used inside web pages. It's a WYSIWYG editor, which 
means that the text being edited on it looks as similar as possible to the results 
users have when publishing it. It brings to the web common editing features found on 
desktop editing applications like Microsoft Word and OpenOffice.


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
#%doc _documentation.html htaccess.txt license.txt _upgrade.html _whatsnew.html
%doc _documentation.html license.txt _upgrade.html _whatsnew.html _whatsnew_history.html
%{kloxo}/%{packagename}

%changelog
* Wed Jun 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-7.mr
- move to editor dir

* Thu Jun 19 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-6.mr
- no obsoletes for fckeditor

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-5.mr
- fix obsolote entry

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-4.mr
- change conflict with obsolete

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.6.8-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 2.6.8-1.lx
- update to new version

* Sun Feb 19 2012 Danny Terweij <contact@lxcenter.org> - 2.4.3-1
- Initial start of this SPEC
