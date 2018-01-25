%define debug_package %{nil}
Name:           libowfat
Version:        0.28
Release:        4%{?dist}
Summary:        Reimplementation of libdjb 

Group:          System Environment/Libraries
License:        GPLv2
URL:            http://www.fefe.de/libowfat/
Source0:        http://dl.fefe.de/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.28-byteh.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
This library is a reimplementation of libdjb, which means that it provides
Daniel Bernstein's interfaces (with some extensions).

It contains wrappers around memory allocation, buffered I/O, routines for
formatting and scanning, a full DNS resolver, several socket routines,
wrappers for socket functions, mkfifo, opendir, wait, and an abstraction
around errno.  It also includes wrappers for Unix signal functions and a
layer of mmap and sendfile.

The library is available for use with the diet libc.


%package        devel
Summary:        Reimplementation of libdjb
Group:          Development/Libraries
Provides:       %{name}-static = %{version}-%{release}


%description    devel
This library is a reimplementation of libdjb, which means that it provides
Daniel Bernstein's interfaces (with some extensions).

It contains wrappers around memory allocation, buffered I/O, routines for
formatting and scanning, a full DNS resolver, several socket routines,
wrappers for socket functions, mkfifo, opendir, wait, and an abstraction
around errno.  It also includes wrappers for Unix signal functions and a
layer of mmap and sendfile.

The library is available for use with the diet libc.


%prep
%setup -q
%patch0 -p1

sed -i '/^CFLAGS/d' GNUmakefile

%build
make -f GNUmakefile %{?_smp_mflags} \
     CFLAGS="%{optflags} -I." 


%install
rm -rf %{buildroot}

make -f GNUmakefile install \
        prefix="%{buildroot}%{_prefix}" \
        LIBDIR="%{buildroot}%{_libdir}" \
        INCLUDEDIR="%{buildroot}%{_includedir}/%{name}" \
        MAN3DIR="%{buildroot}%{_mandir}/man3"


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files devel
%defattr(-,root,root,-)
%doc README TODO COPYING CHANGES
%{_libdir}/%{name}.a
%{_prefix}/include/%{name}
%{_mandir}/man3/**


%changelog
* Sat Oct 24 2009 Simon Wesp <cassmodiah@edoraproject.org> - 0.28-4
- Rebuild without dietlibc usage
- No package (in Fedora-Repo) requires libowfat at this time

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 19 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.28-2
- Honor optflags
- Add parallel build
- Correct libdir paths for dietlibc-integration 
- Cosmetical Issues

* Tue Mar 17 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 0.28-1
- New upstream release

* Sun Aug 24 2008 Simon Wesp <cassmodiah@fedoraproject.org> - 0.27-1
- Initial release
