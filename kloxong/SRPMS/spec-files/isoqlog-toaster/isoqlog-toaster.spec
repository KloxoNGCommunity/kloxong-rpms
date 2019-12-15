%define	name isoqlog
%define	pversion 2.1
%define 	bversion 1.3
%define	rpmrelease 8.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
%define		ccflags %{optflags} 
%define		ldflags %{optflags}
%define		apacheuser apache
%define		apachegroup apache
%define		crontab /etc/crontab

############### RPM ################################

%define	debug_package %{nil}
%define	vtoaster %{pversion}
%define 	basedir %{_datadir}/toaster
%define 	isoqdir %{basedir}/isoqlog
%define	builddate Fri Jun 12 2009

Name:		%{name}-toaster
Summary:	Isoqlog is an MTA log analysis program written in C.
Version:	%{vtoaster}
Release:	%{release}
License:	BSD
Group:		Monitoring
URL:		http://www.enderunix.org/isoqlog/
Source0:	isoqlog-%{pversion}.tar.bz2
Source1:	isoqlog.conf.bz2	
Source2:	cron.sh.bz2
Source3:	toaster-templates.tar.bz2
Patch0:		isoqlog-2.1-fixes.patch.bz2
Patch1:		isoqlog-2.1-errno.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
#BuildPreReq:	qmail-toaster >= 1.03, control-panel-toaster >= 0.2
BuildRequires: qmail-toaster >= 1.03
BuildRequires: automake
#Requires:	qmail-toaster >= 1.03, control-panel-toaster >= 0.5
Requires:	qmail-toaster >= 1.03
Obsoletes:	isoqlog-toaster-doc
Packager:       Jake Vickers <jake@qmailtoaster.com>


#----------------------------------------------------------------------------
%description
#----------------------------------------------------------------------------
Isoqlog is an MTA log analysis program written in C. It is
designed to scan qmail, postfix, sendmail logfiles and
produce usage statistics in HTML format. for viewing through a
browser. It produces Top domains output according to Incoming,
Outgoing, total  mails and  bytes, it keeps your main domain
mail statistics with Days Top Domain, Top Users values for per
day, per month, and years.


#----------------------------------------------------------------------------
%prep
#----------------------------------------------------------------------------
%define name isoqlog

%setup -q -n %{name}-%{pversion}

%patch0 -p0
%patch1 -p1

# CVS cleanup
#----------------------------------------------------------------------------
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

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

./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --datadir=%{basedir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}									


make

#----------------------------------------------------------------------------
%install
#----------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR="%{buildroot}" install

# Write the module into the control panel
cat <<EOF >>$RPM_BUILD_DIR/%{name}-%{pversion}/isoqlog.module


<!-- isoqlog.module -->
<tr>
        <td align="right" width="47%">Usage Statistics per Domain</td>
        <td width="6%">&nbsp;</td>
        <td align="left" width=47%"><input type="button" value="%{name}-%{pversion}" class="inputs" onClick="location.href='/qlogs-toaster/';"></td>
</tr>
<!-- isoqlog.module -->


EOF

THISDIR=`pwd`
install -d %{buildroot}/%{_docdir}/%{name}
install -d %{buildroot}/%{isoqdir}/bin
install -d %{buildroot}/%{basedir}/include
install -m644 isoqlog.module %{buildroot}%{basedir}/include/
bzcat %{SOURCE1} > %{buildroot}/%{_sysconfdir}/%{name}/isoqlog.conf
bzcat %{SOURCE2} > %{buildroot}/%{isoqdir}/bin/cron.sh
mv %{buildroot}/%{basedir}/doc/isoqlog/* %{buildroot}/%{_docdir}/%{name}/
cd %{buildroot}/%{isoqdir}/htmltemp
tar fvxj %{SOURCE3}
cd $THISDIR

%{__perl} -pi -e "s|USR:GRP|%{apacheuser}:%{apachegroup}|g" %{buildroot}/%{isoqdir}/bin/cron.sh


#----------------------------------------------------------------------------
%postun
#----------------------------------------------------------------------------
# Remove cron-job
if [ "$1" = "0" ]; then
  grep -v '* * * * root %{vdir}/bin/clearopensmtp' %{crontab} > %{crontab}.new
  mv -f %{crontab}.new %{crontab}
fi


#----------------------------------------------------------------------------
%post
#----------------------------------------------------------------------------
# Install cron-job
if ! grep '* * * * root %{isoqdir}/bin/cron.sh' %{crontab} > /dev/null; then
  echo "" >> %{crontab}
  echo "58 * * * * root %{isoqdir}/bin/cron.sh 2>&1 > /dev/null" >> %{crontab}
fi


#----------------------------------------------------------------------------
%clean
#----------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#----------------------------------------------------------------------------
%files
#----------------------------------------------------------------------------
%defattr(-,root,root)

# Docs
%attr(0644,root,root) %doc %{_docdir}/%{name}/*

%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/htmltemp
%attr(0644,%{apacheuser},%{apachegroup}) %{isoqdir}/lang/*
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/lang
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/bin
%attr(0644,%{apacheuser},%{apachegroup}) %{isoqdir}/htmltemp/*
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/htmltemp/images
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/htmltemp/library
%attr(0755,root,root) %dir %{_docdir}/%{name}/tr
%attr(0755,root,root) %{isoqdir}/bin/cron.sh
%attr(0644,root,root) %{basedir}/include/*

#----------------------------------------------------------------------------"
%changelog
#----------------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 2.1-1.3.8.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 2.1-1.3.7.mr
- add build_cnt_60 and build_cnt_6064

* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.7
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.7
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.6
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Sat Feb 14 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.5
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.5
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.4
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Fri Feb 23 2007 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.3
- Fix ownership of cron.sh to root:root
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.1-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.1
- Add SuSE 10.1 support
- Set apacheuser and apachegroup correctly in cron.sh
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.10
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.9
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.8
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.7
- Add CentOS 4 x86_64 support
* Fri Sep 22 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.6
- Remove automake config for Mandrake acct build failures
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.5
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 2.1-1.2.4
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Fri May 27 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.3
- Remove doc rpm
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.2
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.1
- Add Fedora Core 2 support
* Wed Feb 11 2004 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.5
- Fix Trustix 2.0 crontab call to fcrontab
- Define crontab
- Define appacheuser and apachegroup
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.4
- Add Fedora Core 1 support
* Tue Nov 25 2003 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.3
- Add Red Hat 9 support
- Add Trustix 2.0 support
- Add Mandrake 9.2 support
- Fix images to images-toaster
* Sun Mar 30 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.1-1.1.2
- Toaster HTML templates (alpha status)
* Sat Mar 29 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.1-1.1.1
- First rpm: everything is OK. Templates are NOT ok.
