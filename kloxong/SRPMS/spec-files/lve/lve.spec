Name: lve
Version: 0.7.3
Release: 2%{?dist}
Summary: Light virtualisation solution
License: GPL
Group: System Environment/Kernel
Source: lve-kmod-%{version}.tar.bz2
Provides: lve-kmod-common = %{version}
# temp disabled
#Requires: kmod-lve >= 0.7
Requires(pre): /usr/sbin/groupadd
BuildRequires: libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# %doc README COPYING TODO net-examples scripts
# ===================================================

%description
LVE provides light virtualization solution.

%package -n liblve
Summary: LVE kernel module API library
Group: Development/Libraries
Requires: lve = %{version}-%{release}

%description -n liblve
LVE API library

%package -n liblve-devel
Summary: LVE kernel module API library
Group: Development/Libraries
Provides: lve-devel
Requires: liblve = %{version}-%{release}
Obsoletes: lve-devel

%package -n liblve-devel-static
Summary: LVE kernel module API library
Group: Development/Libraries
Requires: liblve-devel = %{version}-%{release}

%description -n liblve-devel
LVE API library

%description -n liblve-devel-static
LVE API static library

%prep

%setup -n lve-kmod-%{version}
# ln -s /usr/share/libtool/ltmain.sh `pwd`/usrc/ltmain.sh
cp autogen.sh usrc/autogen.sh
cd usrc
./autogen.sh
%configure

%build
cd usrc
libtoolize
make
cd ..

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"
# udev rule
mkdir -p ${RPM_BUILD_ROOT}/%{_includedir}/lve/
mkdir -p ${RPM_BUILD_ROOT}/etc/udev/rules.d
install -m 0600 etc/60-lve.rules ${RPM_BUILD_ROOT}/etc/udev/rules.d
install -m 0644 usrc/src/lve-ctl.h ${RPM_BUILD_ROOT}/%{_includedir}/lve/

# autoload module
mkdir -p ${RPM_BUILD_ROOT}/etc/init.d/
install -m 0755 etc/lve-kmod ${RPM_BUILD_ROOT}/etc/init.d/lve
#
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig/
install -m 0644 etc/lve ${RPM_BUILD_ROOT}/etc/sysconfig/

cd usrc
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/liblve.la

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%pre
getent group lve >/dev/null || /usr/sbin/groupadd -r lve

%post
/sbin/chkconfig --add lve

%preun
if [ $1 = 0 ]; then
    /sbin/service lve stop > /dev/null 2>&1
    /sbin/chkconfig --del lve
fi

%post -n liblve -p /sbin/ldconfig
%postun -n liblve -p /sbin/ldconfig

%posttrans -n liblve
/sbin/ldconfig

%files
%defattr(-,root,root)
/etc/udev/rules.d/60-lve.rules
/etc/init.d/lve
/etc/sysconfig/lve

%files -n liblve-devel
%defattr(-,root,root)
%{_libdir}/liblve.so
%{_includedir}/lve/*.h

%files -n liblve-devel-static
%defattr(-,root,root)
%{_libdir}/liblve.a

%files -n liblve
%defattr(-,root,root)
%{_libdir}/liblve.so.*

# ===================================================
%changelog
* Wed Sep 15 2010 Igor Seletskiy <iseletsk@cloudlinux.com> 0.7.3-1
- Using /etc/container/securelve.mp to define mount points

* Thu Sep 9 2010 Igor Seletskiy <iseletsk@cloudlinux.com> 0.7.2-1
- Added SecureLVE

* Fri Aug 20 2010 Alexey Lyashkov <umka@sevcity.net> 0.7.1-2
- Fixed -devel subpackage

* Fri Aug 20 2010 Alexey Lyashkov <umka@sevcity.net> 0.7.1-1
- Fixed backward compatibility with LVE 0.6
- Fixed access issue for /dev/lve for euid 0

* Tue Aug 10 2010 Sergey Vakula <svakula@cloudlinux.com>
  - call ldconfig in %posttrans

* Fri Jul 30 2010 Leonid Kanter <lkanter@cloudlinux.com>
  - call ldconfig in %post

* Fri Jun 08 2010 Sergey Vakula <svakula@cloudlinux.com>
  - split liblve-devel to liblve-devel and liblve-devel-static

* Fri Jun 06 2010 Sergey Vakula <svakula@cloudlinux.com>
  - revert change of lve_enter prototype

* Fri Apr 16 2010 Alexey Fomenko <alexey.fomenko@asplinux.ru>
  - test build lve 0.7

* Mon Apr 12 2010 Alexey Fomenko <alexey.fomenko@asplinux.ru>
  - last fix to disable lve_destroy

* Wed Mar 10 2010 Alexey Fomenko <alexey.fomenko@asplinux.ru> 
  - [#Bug 129] i686 kernel panics

* Fri Feb 26 2010 Alexey Fomenko <alexey.fomenko@asplinux.ru> 
  - [#Bug 55] Необходимо добавить lve команду &quot;flush&quot; для удаления default setupedcontexts

* Thu Feb 18 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 95] correctly convert CPU percentage limit set based on number of cores

* Wed Feb 17 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Feature 97] add limits of enter's into LVE context

* Tue Feb 02 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 9] incorrectly set groups

* Tue Feb 02 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 33] make access to /dev/lve hiden

* Tue Feb 02 2010 Automatic Change Log Generator <alexey_com@ukr.net> 
  - [#Feature 74] Allow to disable ability to switch user context on system level

* Fri Jan 29 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 101] /proc/lve/list does not contain any header until the first lve is created

* Mon Jan 25 2010 Andrew Perepechko <anserper@ya.ru> 
  - [#Bug 63] all processes killed, but one still shows via lveps -p

* Fri Jan 22 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Feature 68] improve performance of lve calls

* Fri Jan 22 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 99] Kernel error while trying to access the file on virtual host

* Fri Jan 22 2010 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 23] improve performance of do fairsched mvpr(current):

* Wed Dec 30 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 20] using slab to allocate VE structure to avod memory fragmentation

* Sun Dec 27 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 65] panic with access to /proc/lve/list

* Sun Dec 27 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 24] variuos troubles with CPU limiting.

* Sun Dec 27 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Feature 15] add kernel<>userland API more secure.

* Sun Dec 27 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Feature 60] LVE need to use tree to find context.

* Sat Dec 26 2009 Alexey Lyashkov <umka@sevcity.net> 
  - [#Bug 64] lve should use lve  prefix instead of ve 


