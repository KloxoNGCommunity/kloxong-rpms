# norootforbuild

Name:           maradns
Summary:        An authoritative and recursive DNS server made with security in mind
Version:        2.0.07d
Release:        1.kng%{?dist}
License:        BSD (Two-clause)
Group:          Productivity/Networking/DNS/Servers
Url:            http://www.maradns.org/download/2.0/snap
Source:         maradns-%{version}.tar.bz2
Patch1:         maradns-1.1.59-rpm.patch
Patch2:         maradns-suse-install.patch
Patch3:         maradns-init-script.patch
#Requires:       ps gawk grep findutils logrotate
Requires:       gawk grep findutils logrotate
#BuildRequires:  sed rsyslog logrotate ps gawk grep coreutils findutils fdupes binutils
BuildRequires:  sed rsyslog logrotate gawk grep coreutils findutils binutils
BuildRoot:      /var/tmp/%{name}-buildroot

%description
MaraDNS is an authoritative and recursive DNS server made with 
security and embedded systems in mind.  More information is at 
http://www.maradns.org
===
Copyright (c) 2002-2011 Sam Trenholme and others
TERMS
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
This software is provided 'as is' with no guarantees of correctness or
fitness for purpose.
===

%prep
%setup -q -n maradns-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%__sed -i -e 's|FLAGS =|FLAGS = $(RPM_OPT_FLAGS)|g' build/Makefile.linux
%__sed -i -e 's|make FLAGS=-O2|make FLAGS="$(RPM_OPT_FLAGS)"|g' build/Makefile.linux
make 

%install
rm -fr $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/doc
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man5
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/maradns
mkdir -p $RPM_BUILD_ROOT/etc/init.d
make install
cp build/rpm.mararc $RPM_BUILD_ROOT/etc/mararc
mkdir -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/usr/doc $RPM_BUILD_ROOT/usr/share/doc
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share/man
#%fdupes $RPM_BUILD_ROOT/usr/share
strip --strip-all $RPM_BUILD_ROOT/usr/sbin/maradns
strip --strip-all $RPM_BUILD_ROOT/usr/sbin/zoneserver
strip --strip-all $RPM_BUILD_ROOT/usr/sbin/Deadwood
strip --strip-all $RPM_BUILD_ROOT/usr/bin/getzone
strip --strip-all $RPM_BUILD_ROOT/usr/bin/fetchzone
strip --strip-all $RPM_BUILD_ROOT/usr/bin/askmara
strip --strip-all $RPM_BUILD_ROOT/usr/bin/duende

cd $RPM_BUILD_ROOT/usr/share
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /usr/share/doc/maradns-%{version}
%doc /usr/share/doc/maradns-%{version}/*

/usr/sbin/maradns
/usr/sbin/rcmaradns
/usr/sbin/zoneserver
/usr/sbin/rczoneserver
/usr/sbin/Deadwood
/usr/sbin/rcdeadwood

/usr/bin/getzone
/usr/bin/fetchzone
/usr/bin/askmara
/usr/bin/duende

/usr/share/man/man1/Deadwood.1*
/usr/share/man/man1/askmara.1*
/usr/share/man/man1/getzone.1*
/usr/share/man/man1/fetchzone.1*
/usr/share/man/man8/maradns.8*
/usr/share/man/man8/zoneserver.8*
/usr/share/man/man8/duende.8*
/usr/share/man/man5/csv1.5*
/usr/share/man/man5/csv2.5*
/usr/share/man/man5/csv2_txt.5*
/usr/share/man/man5/mararc.5*

%dir /etc/maradns
%dir /etc/maradns/logger
%config /etc/mararc
%config /etc/dwood3rc
%config /etc/maradns/db.example.net

/etc/init.d/maradns
/etc/init.d/maradns.zoneserver
/etc/init.d/maradns.deadwood

%preun
%stop_on_removal maradns.deadwood
%stop_on_removal maradns.zoneserver
%stop_on_removal maradns
exit 0
 
%post
%{fillup_and_insserv -f maradns}
exit 0
 
%postun
%insserv_cleanup
%restart_on_update maradns.deadwood
%restart_on_update maradns.zoneserver
%restart_on_update maradns
exit 0

%changelog
* Thu Jan 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.0.7d-1.mr
- update to 2.0.7d

* Wed Aug 7 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.0.7b-1.mr
- update to 2.0.7b
- recompile for centos (disable requires for fdupes and ps)

* Tue Apr 24 2012 webcd...a@t...online.de
Updated source
* Wed Jun 15 2011 fwdsbs.to.11df@xoxy.net
- custom package created

