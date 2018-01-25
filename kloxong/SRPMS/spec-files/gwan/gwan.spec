%define gwanpath /home/gwan
%define productname gwan

Name: %{productname}
Summary: G-WAN Web Server
Version: 4.3.17
Release: 2%{?dist}
License: GPL
URL: http://www.gwan.ch/
Group: Applications/Internet

Source0: %{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: glibc-devel, sqlite-devel

%description
G-WAN powers the next-generation, massively-scalable EON, Inc PaaS 
able to deploy the most demanding Web Applications using 
a variety of programming languages in an elastic, fail-safe, and remarkably efficient Cloud. 

%prep
%setup -q -n %{name}-%{version}

%build

if [ -z "`/usr/bin/id -g gwan 2>/dev/null`" ]; then
	/usr/sbin/groupadd -r gwan  2>&1 || :
fi

if [ -z "`/usr/bin/id -u gwan 2>/dev/null`" ]; then
	/usr/sbin/useradd -r gwan -g gwan  2>&1 || :
fi

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{gwanpath}
%{__cp} -rp * $RPM_BUILD_ROOT%{gwanpath}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 0755 ./gwan.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gwan

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,gwan,gwan,755)
%{gwanpath}
%attr(0755,root,root) /etc/rc.d/init.d/gwan
%attr(0755,gwan,apache) /home/gwan/32/gwan
%attr(0755,gwan,gwan) /home/gwan/64/gwan

%changelog
* Sat Oct 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> 4.3.17-2
- move dir from /opt/gwan to /home/gwan
- change user from apache to gwan
- chmod 775 for gwan file

* Sat Oct 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> 4.3.17-1
- add 'Requires: make' because need to make data.cb (centos 6 not installed it)

