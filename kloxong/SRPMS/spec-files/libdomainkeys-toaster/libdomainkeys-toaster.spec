%define	name libdomainkeys
%define	pversion 0.69
%define 	bversion 1.3
%define	rpmrelease 1.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
BuildRequires:	openssl-devel
BuildRequires:	perl
%define		ccflags %{optflags}
%define		ldflags %{optflags}

############### RPM ################################

%define		debug_package %{nil}
%define         vtoaster %{pversion}
%define		builddate Fri Jun 12 2009

Name:		%{name}-toaster
Summary:	ripMIME for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	Yahoo! DomainKeys Public License
Group:		System Environment/Libraries
URL:		http://domainkeys.sourceforge.net/
Source0:	libdomainkeys-%{version}.tar.gz
Patch0:	libdomainkeys-openssl-1.1.patch
Patch1:	libdomainkeys-0.69.diff
BuildRoot:	%{_tmppath}/%{name}-%{pversion}-root
Provides:	libdomainkeys-devel = %{pversion}
Obsoletes:	libdomainkeys
Packager:       Jake Vickers <jake@qmailtoaster.com>

%define	name libdomainkeys

#------------------------------------------------------------------------------------
%description
#------------------------------------------------------------------------------------
DomainKey Implementor's library.
 

#------------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------------
%setup -q -n %{name}-%{pversion}
%patch0 -p1
%patch1 -p0

# Cleanup for gcc
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc

perl -pi -e's|CFLAGS=|CFLAGS=%{optflags} -fPIC |' Makefile
#this is a hack to work later we should use patch 
%if %{?fedora}0 > 140 || %{?rhel}0 > 60
perl -pi -e's/`cat dns.lib`/-lresolv /' Makefile
%else
echo -- "-lresolv" > dns.lib
%endif

#----------------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}


make UNAME=Linux

# Delete gcc temp file
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#------------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------------

# install directories
#------------------------------------------------------------------------------------
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}

# install files
#------------------------------------------------------------------------------------
install -p domainkeys.h dktrace.h %{buildroot}%{_includedir}
install -p libdomainkeys.a %{buildroot}%{_libdir}
install -p dknewkey dktest %{buildroot}%{_bindir}

#------------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#------------------------------------------------------------------------------------
%files 
#------------------------------------------------------------------------------------
%defattr(-,root,root,-)
%doc README CHANGES *.html
%{_bindir}/*

%{_includedir}/*
%{_libdir}/libdomainkeys.a


#------------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------------
* Tue Dec 10 2019 Dionysis Kladis <dkstiler@gmail.com> 0.68-1.3.7.kng
- Work around to compile in centos 7 inside a Copr container

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.68-1.3.7.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.68-1.3.6.mr
- add build_cnt_60 and build_cnt_6064

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 0.68-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Tue Jun 02 2009 Jake Vickers <jake@qmailtoaster.com> 0.68-1.3.6
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 0.68-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 0.68-1.3.4
- Added Suse 11.1 support
* Sun Feb 08 2009 Jake Vickers <jake@qmailtoaster.com> 0.68-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 0.68-1.3.3
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.68-1.3.2
- Added Fedora Core 6 support
* Fri Jun 02 2006 Nick Hemmesch <nick@ndhsoft.com> 0.68-1.3.1
- Make compatible with all supported distros
- Add SuSE 10.1 support
* Sun May 07 2006 Nick Hemmesch <nick@ndhsoft.com> 0.68-1.0.1
- Initial build
