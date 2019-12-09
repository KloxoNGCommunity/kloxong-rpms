Name: qmail-fake
Version: 1.03
Release: 1%{dist}
Group: Networking/Daemons
URL: http://www.qmail.org/
License: Public Domain
Packager: John Pierce <info@kloxong.org>
Summary: Fake Qmail Mail Transfer Agent
Buildroot: %_tmppath/%{name}-%{version}

%description

%prep



%build

%install
mkdir %{buildroot}/var;
mkdir %{buildroot}/var/qmail ;
mkdir %{buildroot}/var/qmail/bin ;
touch %{buildroot}/var/qmail/bin/qmail-newu ;
touch %{buildroot}/var/qmail/bin/qmail-inject ;
touch %{buildroot}/var/qmail/bin/qmail-newmrh ;
touch %{buildroot}/var/qmail/bin/vpopfake ;

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
 Create group and user for build if they don't exist
-------------------------------------------------------------------------------
if [ -z "`/usr/bin/id -g vchkpw 2>/dev/null`" ]; then
	/usr/sbin/groupadd -g 89 -r vchkpw 2>&1 || :
fi

if [ -z "`/usr/bin/id -u vpopmail 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 89 -r -M -d %{vdir}  -s /sbin/nologin -c "Vpopmail User" -g vchkpw vpopmail 2>&1 || :
fi

%preun

%files

%dir %attr(0755,root,qmail) /var/qmail
%dir /var/qmail/bin
%attr(0700,root,qmail) /var/qmail/bin/qmail-newmrh
%attr(0700,root,qmail) /var/qmail/bin/qmail-newu
%attr(0711,root,qmail) /var/qmail/bin/qmail-inject
%attr(0711,root,qmail) /var/qmail/bin/vpopfake

%changelog
* Mon Dec 9 2019 John Pierce <info@kloxong.org>
- Fake qmail to trick vpopmail into thinking it is installed

