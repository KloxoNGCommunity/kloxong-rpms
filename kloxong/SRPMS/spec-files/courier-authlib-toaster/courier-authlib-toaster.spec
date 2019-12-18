%define	name courier-authlib
%define	pversion 0.59.2
%define 	bversion 1.3
%define	rpmrelease 13.kng%{?dist}

%define	release %{bversion}.%{rpmrelease}
BuildRequires:	automake, autoconf
%define		ccflags %{optflags} /etc/libvpopmail/lib_deps
%define		ldflags %{optflags}

############### RPM ################################
%define		debug_package %{nil}
%define         vtoaster %{pversion}
%define         _qdir /var/qmail
%define		_spath %{_qdir}/supervise
%define		_qtlogdir /var/log/qmail
%define		builddate Tue Jun 16 2009

Name:		%{name}-toaster
Summary:	courier-authlib for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.courier-mta.org/
Source0:	courier-authlib-%{pversion}.tar.bz2
Source1:	supervise-authlib.run.bz2
Source2:	supervise-authlib-log.run.bz2
Source3:	authdaemonrc.bz2
BuildRoot:	%{_tmppath}/%{name}-%{pversion}-root
BuildRequires:    %{_includedir}/ltdl.h
BuildRequires:	libtool-ltdl-devel, mysql-devel, zlib-devel, gdbm-devel, expect, gcc-c++
BuildRequires:	qmail-toaster >= 1.03-1.3.15
BuildRequires: vpopmail-toaster >= 5.4.17
BuildRequires: libvpopmail-devel >= 5.4.17
Requires:	qmail-toaster >= 1.03-1.3.15, vpopmail-toaster >= 5.4.17
Obsoletes:	courier-imap-toaster < 4
Packager:       Jake Vickers <jake@qmailtoaster.com>
Patch1: courier-authlib-library-toaster-kloxong.patch

%define	name courier-authlib



#------------------------------------------------------------------------------------
%description
#------------------------------------------------------------------------------------
This package, courier-authlib, allows the new courier imap to use vpopmail for authentication.


#------------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------------
%setup -q -n %{name}-%{pversion}

%patch1 -p1

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

%configure \
    --with-mailuser=vpopmail \
    --with-mailgroup=vchkpw \
    --sysconfdir=%{_sysconfdir}/courier \
    --with-authvchkpw \
    --without-authuserdb \
    --without-authpam \
    --without-authldap \
    --without-authpwd \
    --with-authshadow \
    --without-authpgsql \
    --without-authmysql \
    --without-authcustom \
    --without-authpipe \
    --enable-ltdl-install=no \
    --with-ssl \
    --with-redhat



%{__make}

# Delete gcc temp file
#------------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#------------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------------

# Install into buildroot
#-----------------------------------------------------------------------------
        make DESTDIR=%{buildroot} install


# Install default config
#-----------------------------------------------------------------------------
mkdir -p %{buildroot}%{_sysconfdir}/courier
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/courier/authlib/authdaemonrc.bz2
bunzip2 %{buildroot}%{_sysconfdir}/courier/authlib/authdaemonrc.bz2 

# Supervise
#-----------------------------------------------------------------------------
mkdir -p %{buildroot}%{_spath}/authlib/log
mkdir -p %{buildroot}%{_spath}/authlib/env
mkdir -p %{buildroot}%{_spath}/authlib/supervise
mkdir -p %{buildroot}%{_qtlogdir}/authlib

install -m700 %{SOURCE1} %{buildroot}%{_spath}/authlib/run.bz2
bunzip2 %{buildroot}%{_spath}/authlib/run.bz2
install -m700 %{SOURCE2} %{buildroot}%{_spath}/authlib/log/run.bz2
bunzip2 %{buildroot}%{_spath}/authlib/log/run.bz2

#------------------------------------------------------------------------------------
%postun
#------------------------------------------------------------------------------------
if [ $1 = "0" ]; then
  rm -fR %{_spath}/authlib/
  rm -fR %{_qtlogdir}/authlib/
fi


#------------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}


#------------------------------------------------------------------------------------
%files 
#------------------------------------------------------------------------------------
%defattr(-,root,root)
%doc README READM*html README.ldap INSTALL INSTALL.html NEWS NEWS.html auth*.html 
%attr(0755,root,root) %dir %{_libexecdir}/courier-authlib
%attr(0755,root,root) %dir %{_sysconfdir}/courier
%attr(0750,qmaill,qmail) %dir %{_qtlogdir}/authlib
%attr(0755,root,root) %dir %{_localstatedir}/spool/authdaemon
%attr(1700,qmaill,qmail) %dir %{_spath}/authlib
%attr(0700,qmaill,qmail) %dir %{_spath}/authlib/log
%attr(0700,qmaill,qmail) %dir %{_spath}/authlib/env
%attr(0700,qmaill,qmail) %dir %{_spath}/authlib/supervise
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/*
%attr(0755,root,root) %{_libexecdir}/courier-authlib/*
%attr(0644,root,root) %{_sysconfdir}/courier/*
%attr(0751,qmaill,qmail) %{_spath}/authlib/run
%attr(0751,qmaill,qmail) %{_spath}/authlib/log/run
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man8/*


#------------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.13.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Tue Jul 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.12.mr
- don't install mysql*-libs because make conflict between mysql branch!

* Thu Jun 20 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.11.mr
- update run and log run script

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 0.59.2-1.3.10.mr
- add build_cnt_60 and build_cnt_6064

* Tue Jun 16 2009 Jake Vickers <jake@qmailtoaster.com> 0.59.2-1.3.10
- Rolled the courier-authlib package back to 0.59.2 since the new version does not have the 
- required vpopmail patches to function with Qmail. Sorry!
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 0.62.2-1.3.9
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 0.62.2-1.3.9
- Added Mandriva 2009 support
* Wed Apr 22 2009 Jake Vickers <jake@qmailtoaster.com> 0.59.2-1.3.8
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 0.59.2-1.3.7
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 0.59.2-1.3.7
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch 0.59.2-1.3.6
- Upgraded to courier-authlib 0.59.2
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Thu Feb 01 2007 Erik A. Espinoza <espinoza@kabewm.com> 0.59.1-1.3.5
- Upgraded to courier-authlib 0.59.1
* Tue Jan 02 2007 Erik A. Espinoza <espinoza@kabewm.com> 0.59-1.3.4
- Upgraded to courier-authlib 0.59
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.58-1.3.3
- Added Fedora Core 6 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.58-1.3.2
- Fixed libtool-ltdl conflict on FC4
* Mon Jun 05 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 0.58-1.3.1
- Initial Package
- Add SuSE 10.1 support
