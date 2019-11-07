## MR -- enable this if want create debuginfo
%define  debug_package %{nil}

%define hiawathapath /
%define productname hiawatha
%define packagename addons
%define sourcename %{packagename}

Summary:	An advanced and secure webserver for Unix
Name:		%{productname}-%{packagename}
Version:	1.5
Release:	1%{?dist}
Source0:	hiawatha-addons-%{version}.tar.bz2
License:	GPLv2+
Group:		System Environment/Daemons
URL:		http://www.hiawatha-webserver.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

%description
Hiawatha is an advanced and secure webserver for Unix. It has been written
with 'being secure' as its main goal. This resulted in a webserver which
has for example DoS protection, connection control and traffic throttling.
It has of course also thoroughly been checked and tested for buffer overflows.

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT/%{hiawathapath}
%{__cp} -rp * $RPM_BUILD_ROOT/%{hiawathapath}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,apache,apache,755)
%{hiawathapath}


%changelog
* Sat Jan 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.5-1
- update howto and manual

* Sat Jan 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.4-1
- mod urltoolkit (add 'Do')

* Wed Oct 22 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.3-1
- add urltoolkit

* Mon Oct 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.2-1
- change /home to /opt path

* Mon Oct 18 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 1.1-1
- Fix cakephp toolkit

* Sun Aug 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 1.0-1
- compile hiawatha-addons (docs and urltoolkit)
