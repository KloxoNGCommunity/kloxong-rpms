%define major_ver 1.5
%define minor_ver 6

Name: monkey
Summary: Small WebServer
Version: %{major_ver}.%{minor_ver}
Release: 1%{?dist}
Group: System Environment/Daemons
License: GPLv2
URL: http://www.monkey-project.com/
Source0: http://monkey-project.com/releases/%{major_ver}/monkey-%{version}.tar.gz
#Source0: monkey-%{version}.tar.bz2

BuildRequires: jemalloc-devel
Requires: jemalloc

#BuildRequires: polarssl-devel
#Requires: polarssl

%description
Monkey is a lightweight and powerful web server and development ostack for
GNU/Linux. It has been designed to be very scalable with low memory and CPU
consumption, the perfect solution for embedded devices.

%prep
%setup -q

%build
./configure \
	--default-port=80 \
	--default-user=apache \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}/monkey \
	--bindir=%{_prefix}/bin \
	--mandir=%{_mandir}/man1 \
	--plugdir=%{_libdir}/monkeyd/plugins \
	--datadir=/var/www/html \
	--libdir=%{_libdir} \
	--enable-shared \
	--enable-plugins=auth,cgi,cheetah,dirlisting,fastcgi,liana,logger,mandril,proxy_reverse \
	--safe-free

make %{?_smp_mflags}

%install
#cleaning and make some dirs
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_var}/log/%{name}
%{__install} -d %{buildroot}%{_var}/www/%{name}/cgi-bin
#configure and make.
%{__make} install DESTDIR=%{buildroot}

#changing username
%{__sed} -i 's/User nobody/User monkey/g' \
	%{buildroot}/%{_sysconfdir}/%{name}/monkey.conf
#changing port to default for webserver (80)
%{__sed} -i 's/Port 2001/Port 80/g' \
	%{buildroot}/%{_sysconfdir}/%{name}/monkey.conf
#changing original path of pid to /var/run
%{__sed} -i 's/PidFile \/var\/log\/monkey\/monkey.pid/PidFile \/var\/run\/monkey.pid/g' \
	%{buildroot}/%{_sysconfdir}/%{name}/monkey.conf
%{__sed} -i 's/PIDFILE=\"\/var\/log\/monkey\/monkey.pid\"/PIDFILE=\"\/var\/run\/monkey.pid\"/g' \
	%{buildroot}/%{_bindir}/banana
#banana to init.d
%{__mkdir} -p %{buildroot}%{_initrddir}
#rename banana to monkey
%{__mv} -f %{buildroot}%{_bindir}/banana %{buildroot}%{_initrddir}/monkey
%{__sed} -i 's/banana/monkey/g' %{buildroot}%{_initrddir}/monkey
%{__sed} -i 's/Banana/Monkey/g' %{buildroot}%{_initrddir}/monkey

%clean
%{__rm} -rf %{buildroot}

%pre
getent group monkey  > /dev/null || groupadd -r monkey -g 80
getent passwd monkey > /dev/null || \
  useradd -r -g monkey -d %{_var}/www/%{name}  -s /sbin/nologin \
  -c "Monkey HTTP Daemon" monkey -u 80
exit 0


%post -p /sbin/ldconfig

%postun
#clean trash files
%{__kill} -9 $(cat  %{_var}/run/%{name}.pid)> /dev/null 2>&1
%{__rm} -rf %{_var}/run/%{name}.pid > /dev/null 2>&1
%{__rmdir} %{_var}/log/%{name} > /dev/null 2>&1
%{__rmdir} %{_sysconfdir}/%{name} > /dev/null 2>&1
%{__userdel} monkey

%files
%{_bindir}/%{name}
%{_bindir}/mk_passwd
%{_libdir}/monkeyd
%{_sysconfdir}/monkey
%{_mandir}/man1/*
%{_includedir}/*.h
%{_libdir}/lib*
%{_libdir}/pkgconfig/%{name}.pc
/var/www/html/*
%{_initrddir}/monkey

%changelog
* Mon Jun 22 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 1.5.6-1
- First compile for Kloxo-MR
- update for 1.5.6
- enable all plugins except mbedtls

* Wed Feb 05 2014 Huaren Zhong <huaren.zhong@gmail.com> - 1.4.0
- Rebuild for Fedora
* Wed Nov 16 2011 Alexander Khrukin <akhrukin@mandriva.org> 0.21.0-1
+ Revision: 730913
- imported package monkey
