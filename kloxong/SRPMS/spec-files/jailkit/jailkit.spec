Summary: Utilities to limit user accounts to specific files using chroot()
Name: jailkit
Version: 2.23
Release: 1.kng%{?dist}
License: Open Source
Group: System Environment/Base
URL: http://olivier.sessink.nl/jailkit/

Source: http://olivier.sessink.nl/jailkit/jailkit-%{version}.tar.bz2
Patch1: jailkit-2.17-makefile.patch
Patch2: jailkit-jk_init-php.patch
Patch3: jailkit-2.23-nosetuid.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: binutils, gcc, make, autoconf, automake
BuildRequires: glibc-devel
BuildRequires: libcap-devel
BuildRequires: python36, python36-devel

%undefine __brp_mangle_shebangs

%description
Jailkit is a set of utilities to limit user accounts to specific files
using chroot() and or specific commands. Setting up a chroot shell,
a shell limited to some specific command, or a daemon inside a chroot
jail is a lot easier using these utilities.

Jailkit has been in use for a while on CVS servers (in a chroot and
limited to cvs), sftp/scp servers (both in a chroot and limited to
sftp/scp as well as not in a chroot but only limited to sftp/scp),
and also on general servers with accounts where the shell accounts
are in a chroot.

%prep
%setup

%prep
%setup -q
%patch1 -p0 -b .makefile
%patch2 -p0
%patch3 -p1 

%build
%configure PYTHONINTERPRETER=/usr/bin/python3
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0755 extra/jailkit %{buildroot}%{_initrddir}/jailkit

#%post
#cat /etc/shells | grep -v jk_chrootsh >/etc/shells
#echo "/usr/bin/jk_chrootsh" >> /etc/shells
#/sbin/chkconfig --add jailkit

#%postun
#cat /etc/shells | grep -v jk_chrootsh >/etc/shells

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/jailkit/
%config %{_initrddir}/jailkit
%caps(cap_sys_chroot=ep) %{_sbindir}/jk_chrootsh
%{_sbindir}/jk_jailuser
%{_sbindir}/jk_socketd
%{_sbindir}/jk_check
%{_sbindir}/jk_cp
%{_sbindir}/jk_list
%{_sbindir}/jk_update
%{_sbindir}/jk_chrootlaunch
%{_sbindir}/jk_init
%{_sbindir}/jk_lsh
%caps(cap_sys_chroot=ep) %{_bindir}/jk_uchroot
%{_datadir}/jailkit/

%changelog
* Thu Jun 20 2024 John Pierce <john@luckytanuki.com>
- upgrade to 2.23

* Sun Feb 2 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.17-1
- recompile for Kloxo-MR and update to 2.17
- add Requeries to python-hashlib

* Wed Apr 17 2013 David Hrbáč <david@hrbac.cz> - 2.15-1
- new upstream release

* Wed Jun 02 2010 Steve Huff <shuff@vecna.org> - 2.11-1
- Updated to release 2.11.

* Thu May 15 2008 Dries Verachtert <dries@ulyssis.org> - 2.5-1
- Updated to release 2.5.

* Tue Sep 12 2006 Dag Wieers <dag@wieers.com> - 2.1-1
- Updated to release 2.1.

* Sun Mar 19 2006 Dag Wieers <dag@wieers.com> - 2.0-1
- Updated to release 2.0.

* Fri May 20 2005 Dag Wieers <dag@wieers.com> - 1.3-1
- Initial package. (using DAR)
