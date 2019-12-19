%define	name qmailadmin
%define	pversion 1.2.16
%define 	bversion 1.4
%define	rpmrelease 2.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
%define		apacheuser apache
%define		apachegroup apache
BuildRequires: automake
#BuildRequires:	mysql-devel >= 5.0.22, mysql >= 5.0.22, httpd >= 2.2.3, automake
#Requires:	mysql >= 5.0.22, httpd >= 2.2.3,
%define		ccflags %{optflags} 
%define		ldflags %{optflags}

############### RPM ################################

%define	debug_package %{nil}
%define         vtoaster %{pversion}
%define 	basedir %{_datadir}/toaster
%define 	qadmdir %{basedir}/qmailadmin
%define		builddate Sat Feb 18 2012
%{!?spambox:%define spambox 0}

Name:           %{name}-toaster
Summary:	Web Administration for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.inter7.com/qmailadmin
Source0:	qmailadmin-%{pversion}.tar.bz2
Source1:	help.tar.bz2
Patch1: 	qmailadmin-lib-kloxong-qtoaster.patch
Patch2: 	qmailadmin-noroot.patch
Patch3: 	qmailadmin-vpop-devel.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	qmail-toaster >= 1.03, vpopmail-toaster >= 5.4.33
BuildRequires: libvpopmail-devel >= 5.4.17
BuildRequires:  autorespond-toaster >= 2.0.2, ezmlm-toaster >= 0.53.324, bzip2
BuildRequires:	mysql-devel, mysql
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:  bzip2
Requires:	qmail-toaster >= 1.03, vpopmail-toaster >= 5.4.33
Requires:	control-panel-toaster >= 0.2
Requires:	autorespond-toaster >= 2.0.2, ezmlm-toaster >= 0.53.324
Requires:	mysql
Packager:       Bharath Chari <qmailtoaster@arachnis.com> 


%define vdir	/home/vpopmail
%define qdir	/var/qmail

#----------------------------------------------------------------------------
%description
#----------------------------------------------------------------------------
QmailAdmin is a free software package that provides a web interface
for managing a  qmail  system with virtual domains. This version is
for use with the vpopmail program. It provides admin for
adding/deleting users, Aliases, Forwards, Mailing lists and
Autoresponders. Version 0.40 features automatic International language
support via the users language settings on their browser.


            qmailadmin 1.2.15
            Current settings
---------------------------------------
       cgi-bin dir = /usr/share/qmailadmin
          html dir = /usr/share/qmailadmin
         image dir = /usr/share/qmailadmin/images
         image URL = /qmailadmin/images
      template dir = /usr/share/qmailadmin
         qmail dir = /var/qmail
      vpopmail dir = /home/vpopmail
   autorespond dir = /usr/bin
         ezmlm dir = /usr/bin
         ezmlm idx = yes
   mysql for ezmlm = no
              help = yes
      modify quota = yes
   domain autofill = no
 
#----------------------------------------------------------------------------
%prep
#----------------------------------------------------------------------------

%define name qmailadmin
%setup  -q -n %{name}-%{pversion}


#%patch1 -p1
%patch2 -p1
%patch3 -p1

# Cleanup for gcc
#----------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc

# Export compiler flags
#----------------------------------------------------------------------------
export CC="`cat %{_tmppath}/%{name}-%{pversion}-gcc` %{ccflags}"

#----------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------
%{__aclocal}
%{__autoconf}
%{__automake}
./configure \
 --prefix=%{_prefix} \
 --datadir=%{_datadir}/%{name} \
 --enable-htmllibdir=%{_datadir}/%{name} \
 --enable-htmldir=%{_datadir}/%{name} \
 --enable-cgibindir=%{_datadir}/%{name} \
 --enable-imageurl=/%{name}/images \
 --enable-imagedir=%{_datadir}/%{name}/images \
 --enable-cgipath=/qmailadmin/index.cgi \
 --enable-vpopmaildir=%{vdir} \
 --enable-qmaildir=%{qdir} \
 --enable-ezmlmdir=%{_bindir} \
 --enable-autoresponder-path=%{_bindir} \
 --enable-vpopuser=vpopmail \
 --enable-vpopgroup=vchkpw \
 --enable-maxusersperpage=12 \
 --enable-maxaliasesperpage=12 \
 --enable-modify-quota=y \
 --enable-ezmlm-mysql=n \
 --enable-help=y \
%if %{spambox}
 --enable-modify-spam \
 --enable-spam-command="|/var/qmail/bin/preline /usr/bin/maildrop -A 'Content-Filter: maildrop-toaster' /etc/mail/mailfilter" \
%endif
 --enable-domain-autofill=n

%{__make}

cp %{SOURCE1} $RPM_BUILD_DIR/%{name}-%{pversion}/help.tar.bz2
tar xvfj $RPM_BUILD_DIR/%{name}-%{pversion}/help.tar.bz2
rm -f $RPM_BUILD_DIR/%{name}-%{pversion}/help.tar.bz2


#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------
rm -Rf %{buildroot}
install -d %{buildroot}%{_datadir}/%{name}

%{__make} DESTDIR=%{buildroot} install-strip 

pushd %{buildroot}%{_datadir}/%{name}
  ln -s qmailadmin index.cgi
popd


# Call qmail from admin-toaster
#------------------------------------------------------------------------------
[ -d %{buildroot}%{basedir}/include ]	|| mkdir -p %{buildroot}%{basedir}/include

cat <<EOF >>%{buildroot}%{basedir}/include/qmailadmin.module


<!-- qmailadmin.module -->
<tr>
	<td align="right" width="47%">Edit Users, mailing lists, forwarders</td>
	<td width="6%">&nbsp;</td>
	<td align="left" width="47%"><input type="button" value="%{name}-%{pversion}" class="inputs" onClick="location.href='/qmailadmin';"></td>
</tr>
<!-- qmailadmin.module -->


EOF


# Make online help
#------------------------------------------------------------------------------
install -d %{buildroot}%{_datadir}/%{name}/images/help
cp -R $RPM_BUILD_DIR/%{name}-%{pversion}/help/* %{buildroot}%{_datadir}/%{name}/images/help/


#----------------------------------------------------------------------------
%clean
#----------------------------------------------------------------------------
[ -n %{buildroot} -a %{buildroot} ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}
rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#----------------------------------------------------------------------------
%files
#----------------------------------------------------------------------------
%defattr(-,root,root)

# Docs
#------------------------------------------------------------------------------
%doc AUTHORS BUGS ChangeLog COPYING FAQ INSTALL NEWS README* TODO TRANSLATORS

# Dirs
#------------------------------------------------------------------------------
%attr(0755,root,root) %dir %{_datadir}/%{name}
%attr(0755,root,root) %dir %{_datadir}/%{name}/html
%attr(0755,root,root) %dir %{_datadir}/%{name}/lang
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_datadir}/%{name}/images

# Files
#------------------------------------------------------------------------------
%attr(0644,root,root) %{_datadir}/%{name}/html/*
%attr(0644,root,root) %{_datadir}/%{name}/lang/*
%attr(-,%{apacheuser},%{apachegroup}) %{_datadir}/%{name}/images/*
%attr(0644,root,root) %{basedir}/include/qmailadmin.module
%attr(6755,vpopmail,vchkpw) %{_datadir}/%{name}/index.cgi
%attr(6755,vpopmail,vchkpw) %{_datadir}/%{name}/qmailadmin


#------------------------------------------------------------------------------
%changelog
#------------------------------------------------------------------------------
* Tue Aug 22 2017 Mustafa Ramadhan <mustafa@bigraf.com> 1.2.16-1.4.2.mr
- recompile without BuildRequires mysql and httpd

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.2.16-1.4.1.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.2.16-1.4.0.mr
- add build_cnt_60 and build_cnt_6064

* Wed Aug 01 2012 Eric Shubert <eric@datamatters.us> 1.2.16-1.4.0
- Bharath Chari updated to 1.2.16, added dependencies
* Sat Jan 22 2011 Jake Vickers <jake@qmailtoaster.com> 1.2.15-1.3.9
- Updated to version 1.2.15
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.12-1.3.8
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.12-1.3.8
- Added Mandriva 2009 support
* Tue May 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.12-1.3.7
- Updated qmailadmin to version 1.2.12
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.11-1.3.6
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.11-1.3.5
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 1.2.11-1.3.5
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.2.11-1.3.4
- Update to qmailadmin-1.2.11
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2.9-1.3.3
- Added Fedora Core 6 support
* Sat Oct 28 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2.9-1.3.2
- Added definition to enable spambox
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.13
- Add Fedora Core 5 support
* Sun Apr 30 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.12
- Removed spam filtering account breaks quota enforcement
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.11
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.10
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.9
- Add CentOS 4 x86_64 support
* Wed Sep 21 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.9-1.2.8
- Update to qmailadmin-1.2.9
* Thu Aug 25 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.8-1.2.7
- Update to qmailadmin-1.2.8
- Add user selectable maildrop filtering
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.7-1.2.6
- Add Fedora Core 4 support
* Wed Jun 08 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.7-1.2.5
- Update to qmailadmin-1.2.7 and add online help
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.2.1-1.2.4
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Changed Mandrake 9.1,9.2 and 10.0 to apache-2x so all spec files has the same requirements.
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 1.2.1-1.2.3
- Add Fedora Core 3 support
- Add CentOS support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 1.2.1-1.2.2
- Add Fedora Core 2 support
* Thu May 13 2004 Nick Hemmesch <nick@ndhsoft.com> 1.2.1-1.2.1
- Update to version 1.2.1
- Relocate qmailadmin to datadir
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 1.0.6-1.0.8
- Add Fedora Core 1 support
* Sun Nov 23 2003 Nick Hemmesch <nick@ndhsoft.com> 1.0.6-1.0.7
- Add Trustix 2.0 support
- Fix images to images-toaster
- Patch template.c to fix
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-1.0.6
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-1.0.5
- Conectiva Linux 7.0 support
- Better managing of apache user (related to distro)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 1.0.6-1.0.4
- Support for Red Hat 8.0
* Wed Feb 05 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-1.0.3
- Support for Red Hat 8.0 thanks to Andrew.J.Kay
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-0.9.2
- Soft clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 1.0.6-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.1.0.6-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.0.6-3
- Quota Fix
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.0.6-2
- Deleted Mandrake Release Autodetection (creates problems)
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.1.0.6-1
- New version: 0.7 toaster.
- Installation directly depends on apache-toaster-conf (that provides httpd
  configurations for all web packages)
- Better macros to detect Mandrake Release
* Thu Aug 13 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.6.1.0.6-1
- New version: 0.6 toaster.
* Mon Aug 12 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.5.1.0.6-1
- Checks for gcc-3.2 (default compiler from now)
- New version: 0.5 toaster.
* Thu Aug 08 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.4.1.0.6-1
- New version 1.0.6
- Better RedHat dependecies
- Rebuild against 0.4 toaster
* Thu Jul 30 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.0.4-2
- Now packages have got 'no sex': you can rebuild them with command line
  flags for specifics targets that are: RedHat, Trustix, and of course
  Mandrake (that is default)
* Sun Jul 28 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.3.1.0.4.1mdk
- toaster v. 0.3: now it is possible upgrading safely because of 'pversion'
  that is package version and 'version' that is toaster version
* Thu Jul 25 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.2-1.0.4.1mdk
- Fixed path images in cgi
- Changed /cgi-bin/ un /mail/
* Mon Jul 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.0.4.4mdk
- Added index.html to explain what toaster do (to be finished)
* Thu Jul 18 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.1-1.0.4.3mdk
- Added toaster version (we will need to mantain it too): is vtoaster 0.1
- Added tests to make gcc to be 3.1.1
- Very soft clean-ups.
* Wed Jul 17 2002 Miguel Beccari <miguel.beccari@clikka.com 1.0.4-2mdk
- Better SPEC (improvements and cleans)
* Tue Jul 16 2002 Miguel Beccari <mighi@clikka.com> 1-0-4 1mdk
- First package.
