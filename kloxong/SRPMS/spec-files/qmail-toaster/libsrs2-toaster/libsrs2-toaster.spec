%define	name libsrs2
%define	pversion 1.0.18
%define 	bversion 1.3
%define	rpmrelease 7%{?dist}

%define		release %{bversion}.%{rpmrelease}
BuildRequires:	openssl-devel
%define		ccflags %{optflags}
%define		ldflags %{optflags}

############### RPM ################################

%define		debug_package %{nil}
%define         vtoaster %{pversion}
%define		builddate Fri Jun 12 2009

Name:		%{name}-toaster
Summary:	libsrs2 for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	SRS Library
Group:		System Environment/Libraries
URL:		http://www.libsrs2.org/
Source0:	libsrs2-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{pversion}-root
Packager:       Jake Vickers <jake@qmailtoaster.com>

%define	name libsrs2

#------------------------------------------------------------------------------------
%description
#------------------------------------------------------------------------------------
SRS implementation library.
 

#------------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------------
%setup -q -n %{name}-%{pversion}


# Cleanup for gcc
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc


perl -pi -e's/CFLAGS=/CFLAGS=%{optflags} -fPIC /' Makefile


#----------------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}


./configure --prefix=%{_prefix} --libdir=%{_libdir}
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

# Delete gcc temp file
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#------------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------------

# install directories
#------------------------------------------------------------------------------------
rm -rf %{buildroot}

# install files
#------------------------------------------------------------------------------------
make DESTDIR=%{buildroot} install

#------------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#------------------------------------------------------------------------------------
%files 
#------------------------------------------------------------------------------------
%defattr(-,root,root,-)
%doc ChangeLog INSTALL README NEWS AUTHORS COPYING
%{_libdir}/libsrs2.so*
%{_libdir}/libsrs2.a
%{_libdir}/libsrs2.la
%{_bindir}/srs
%{_prefix}/include/srs2.h


#------------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.0.18-1.3.7.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.0.18-1.3.6.mr
- add build_cnt_60 and build_cnt_6064

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.0.18-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Tue Jun 02 2009 Jake Vickers <jake@qmailtoaster.com> 1.0.18-1.3.6
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 1.0.18-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.0.18-1.3.4
- Added Suse 11.1 support
* Sun Feb 08 2009 Jake Vickers <jake@qmailtoaster.com> 1.0.18-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.0.18-1.3.3
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Fri Jan 12 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.0.18-1.3.2
- Minor corrections for 64-bit, Fedora
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.0.18-1.3.1
- Initial Package
