%define  debug_package %{nil}

%global gitcommit 333ff99
Name:           fcgiwrap
Version:        1.1.0
Release:        1%{?dist}
Summary:        Simple FastCGI wrapper for CGI scripts
License:        MIT
URL:            http://nginx.localdomain.pl/
Group:          System Environment/Daemons

Source: %name-%version.tar
Patch0: %name-%version.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      autoconf
BuildRequires:      fcgi-devel
Requires:           spawn-fcgi

%description
fcgiwrap is a simple server for running CGI applications over FastCGI.
It hopes to provide clean CGI support to Nginx (and other web servers
that may need it).


%prep
%setup -q
%patch0 -p1

%build
autoreconf -i
%configure --prefix=""
make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%files
%doc README.rst
%{_sbindir}/fcgiwrap
%{_mandir}/man8/fcgiwrap.8*

%changelog
* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.1.0-1
- first compile for Kloxo-MR
- use fcgi-devel instead libfcg-devel
- add BuildRoot

* Fri Feb 08 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.1.0-1
- new upstream release.

* Fri Jan 11 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3.20120908-1
- Change version to increase monotonously.

* Wed Jan  9 2013 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3-3.gitb9f03e6377
- Make the rpm relocatable.

* Tue Dec 25 2012 Hiroaki Nakamura <hnakamur@gmail.com> - 1.0.3-2.gitb9f03e6377

* Tue Jan 31 2012 Craig Barnes <cr@igbarn.es> - 1.0.3-1.git1328862
- Initial package
