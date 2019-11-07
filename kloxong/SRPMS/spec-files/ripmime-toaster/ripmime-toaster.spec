%define	name ripmime
%define	pversion 1.4.0.6
%define 	bversion 1.3
%define	rpmrelease 8%{?dist}

%define		release %{bversion}.%{rpmrelease}
BuildRequires:	automake, autoconf
%define		ccflags %{optflags}
%define		ldflags %{optflags}

############### RPM ################################

%define	debug_package %{nil}
%define	vtoaster %{pversion}
%define	builddate Fri Jun 12 2009

Name:		%{name}-toaster
Summary:	ripMIME for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	BSD
Group:		Networking/Other
URL:		http://www.pldaniels.com/ripmime/
Source0:	ripmime-%{pversion}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{pversion}-root
BuildRequires:	qmail-toaster >= 1.03-1.3.1
Requires:	qmail-toaster >= 1.03-1.3.1
Packager:       Jake Vickers <jake@qmailtoaster.com>

%define	name ripmime

#------------------------------------------------------------------------------------
%description
#------------------------------------------------------------------------------------
ripMIME has a single sole pupose, to extract the attached files out of a
MIME package.
 

#------------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------------
%setup -q -n %{name}-%{pversion}


# Cleanup for the compiler
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc

#----------------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# Run configure to create makefile
#------------------------------------------------------------------------------------
%{__make}

# Delete gcc temp file
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#------------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------------

# install directories
#------------------------------------------------------------------------------------
install -d -o root -g root %{buildroot}%{_bindir}
install -d -o root -g root %{buildroot}%{_mandir}/man1
install -d -o root -g root %{buildroot}%{_datadir}/doc/%{name}-%{pversion}

# install files
#------------------------------------------------------------------------------------
install -m755 -o root -g root $RPM_BUILD_DIR/%{name}-%{pversion}/ripmime %{buildroot}%{_bindir}
install -m755 -o root -g root $RPM_BUILD_DIR/%{name}-%{pversion}/ripmime.1 %{buildroot}%{_mandir}/man1


# install docs
#------------------------------------------------------------------------------------
for i in CHANGELOG CONTRIBUTORS INSTALL LICENSE README TODO; do
 install -m644 -o 0 -g 0 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{_datadir}/doc/%{name}-%{pversion}
done

#------------------------------------------------------------------------------------
%post
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#------------------------------------------------------------------------------------
%files 
#------------------------------------------------------------------------------------
%defattr(-,root,root)
%doc %attr(0644,root,root) %{_datadir}/doc/%{name}-%{pversion}/*
%attr(0755,root,root) %{_bindir}/ripmime
%attr(0644,root,root) %{_mandir}/man1/*


#------------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0.6-1.3.8
- cleanup spec based on toaster github (without define like build_cnt_60)

* Thu Jul 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0.6-1.3.7
- change BuildPreReq to BuildRequires (centos 6 deprecated issue)

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0.6-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Thu Jun 11 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0.6-1.3.6
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0.6-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Mon Feb 16 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0.6-1.3.4
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0.6-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.4.0.6-1.3.3
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.0.6-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.4.0.6-1.3.1
- Initial Package
- Includes SuSE 10.1 support
