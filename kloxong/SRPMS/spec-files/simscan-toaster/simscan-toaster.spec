%define	name simscan
%define	pversion 1.4.0
%define 	bversion 1.4
%define	rpmrelease 8.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
BuildRequires:	automake, autoconf
%define		ccflags %{optflags}
%define		ldflags %{optflags}

############### RPM ################################

%define	debug_package %{nil}
%define	vtoaster %{pversion}
%define	builddate Fri Jun 12 2009




Name:		%{name}-toaster
Summary:	Simscan for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.inter7.com/vpopmail

Source0:	simscan-%{pversion}.tar.gz
Source1:	update-simscan

Source4:	supervise-clamd.run
Source5:	supervise-clamd-log.run

Patch0:		simscan-1.4.0-combined.4.patch.bz2
Patch1:		o_creat.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{pversion}-root
#BuildPreReq:		qmail-toaster >= 1.03-1.2.4, ripmime-toaster
BuildRequires:	qmail-toaster >= 1.03-1.2.4, ripmime
BuildRequires:	mysql-devel, mysql-libs, clamav, ripmime, clamd, spamassassin-toaster 
#Requires:	qmail-toaster >= 1.03-1.2.4, clamav-toaster, ripmime-toaster
#Requires:	qmail-toaster >= 1.03-1.2.4, clamav, ripmime, clamd
Requires:	qmail-toaster >= 1.03-1.2.4, clamav, ripmime, clamd, spamassassin-toaster 

%if %{?fedora}0 > 150 || %{?rhel}0 >60
BuildRequires: clamav-server, clamav-data, clamav-update, clamav-filesystem, clamav, clamav-scanner-systemd, clamav-devel, clamav-lib, clamav-server-systemd
Requires: clamav-server, clamav-data, clamav-update, clamav-filesystem, clamav, clamav-scanner-systemd, clamav-devel, clamav-lib, clamav-server-systemd
%endif

Obsoletes:	clamav-toaster, ripmime-toaster


Packager:	Eric Shubert <eric@datamatters.us>

%define	name simscan
%define	qdir /var/qmail
%define	qbin /var/qmail/bin
%define	qcont /var/qmail/control
%define	qtcp %{_sysconfdir}/tcprules.d/tcp.smtp

# we need to handle that for user selection centos 7 and centos 6
%if %{?fedora}0 > 150 || %{?rhel}0 >60
%define scanuser	clamscan
%else
%define scanuser	clam
%endif

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
SimScan is a simplified scanner for qmail similar to qmail-scanner and qscand.
It uses clamav, trophie, and/or spamassassin.  It also supports attachment
blocking by extension.  Simscan is written entirely in C to ensure maximum
speed.  There are several options to allow simscan to scan per domain, and
reject spam mail.


                Current settings
     ---------------------------------------
     user                  = clamav --> change to clam user
     qmail directory       = /var/qmail
     work directory        = /var/qmail/simscan
     control directory     = /var/qmail/control
     qmail queue program   = /var/qmail/bin/qmail-queue
     clamdscan program     = /usr/bin/clamdscan
     clamav scan           = ON
     trophie scanning      = OFF
     attachement scan      = ON
     ripmime program       = /usr/bin/ripmime
     custom smtp reject    = ON
     drop message          = OFF
     regex scanner         = OFF
     quarantine processing = OFF
     domain based checking = ON
     add received header   = ON
     spam scanning         = ON
     spamc program         = /usr/bin/spamc
     spamc arguments       =
     spamc user            = OFF
     authenticated users scanned = OFF
     spam passthru         = OFF
     spam hits             = 40

                Current simcontrol config
     ----------------------------------------------------------
     :clam=yes,spam=yes,spam_hits=12,attach=.mp3:.src:.bat:.pif
     
     
#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%setup -q -n %{name}-%{pversion}
%patch0 -p1
%patch1 -p1

# Cleanup for gcc
#-------------------------------------------------------------------------------
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------

# Run configure to create makefile
#-------------------------------------------------------------------------------
%configure \
	--enable-user=%scanuser \
	--enable-attach \
	--enable-ripmime=/usr/bin/ripmime \
	--enable-per-domain \
	--enable-spam \
	--enable-spam-hits=40 \
	--enable-received \
	--enable-clamavdb-path=/usr/share/clamav \
	--enable-custom-smtp-rejectn \
	--enable-clamdscan
%{__make}


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# install directories
#-------------------------------------------------------------------------------
install -d %{buildroot}%{qdir}
install -d %{buildroot}%{qdir}/bin
install -d %{buildroot}%{qdir}/control
install -d -m750 %{buildroot}%{qdir}/%{name}
install -d %{buildroot}%{_datadir}/doc/%{name}-%{pversion}

install -d %{buildroot}%{qdir}/supervise
install -d %{buildroot}%{qdir}/supervise/clamd
install -d %{buildroot}%{qdir}/supervise/clamd/log
install -d %{buildroot}%{qdir}/supervise/clamd/supervise

# install files
#-------------------------------------------------------------------------------
install -m4711 $RPM_BUILD_DIR/%{name}-%{pversion}/%{name} %{buildroot}%{qdir}/bin/%{name}
install -m4755 $RPM_BUILD_DIR/%{name}-%{pversion}/simscanmk %{buildroot}%{qdir}/bin/simscanmk
#if we need those later we should make them set attributes to files
#install -m755  -o root -g root %{SOURCE1} %{buildroot}%{qdir}/bin/update-%{name}.bz2
#bunzip2 %{buildroot}%{qdir}/bin/update-%{name}.bz2
install -m755 %{SOURCE1} %{buildroot}%{qdir}/bin/update-%{name}

#if we need those later we should make them set attributes to files
#install %{SOURCE4} %{buildroot}%{qdir}/supervise/clamd/run.bz2
#bunzip2 %{buildroot}%{qdir}/supervise/clamd/run.bz2
#install %{SOURCE5} %{buildroot}%{qdir}/supervise/clamd/log/run.bz2
#bunzip2 %{buildroot}%{qdir}/supervise/clamd/log/run.bz2

install %{SOURCE4} %{buildroot}%{qdir}/supervise/clamd/down
install %{SOURCE5} %{buildroot}%{qdir}/supervise/clamd/log/down

# install docs
#-------------------------------------------------------------------------------
for i in AUTHORS ChangeLog INSTALL README TODO ssattach.example; do
 install -m644 $RPM_BUILD_DIR/%{name}-%{pversion}/$i %{buildroot}%{_datadir}/doc/%{name}-%{pversion}
done

pushd %{buildroot}%{qdir}/control
  echo ":clam=yes,spam=yes,spam_hits=12,attach=.mp3:.src:.bat:.pif" > simcontrol
popd

#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

./%{qdir}/bin/update-%{name}

# We should not overwrite an exisiting tcp.smtp file in case it has custom items in it
if [ -f /etc/tcprules.d/tcp.smtp ] ; then
  touch /etc/tcprules.d/tcp.smtp.new
  echo '127.:allow,RELAYCLIENT="",DKSIGN="/var/qmail/control/domainkeys/%/private",RBLSMTPD="",NOP0FCHECK="1"' > /etc/tcprules.d/tcp.smtp.new
  echo ':allow,BADMIMETYPE="",BADLOADERTYPE="M",CHKUSER_RCPTLIMIT="50",CHKUSER_WRONGRCPTLIMIT="10",QMAILQUEUE="/var/qmail/bin/simscan",DKSIGN="/var/qmail/control/domainkeys/%/private",NOP0FCHECK="1"' >> /etc/tcprules.d/tcp.smtp.new
  echo ""
  echo "Your existing tcp.smtp file was *not* overwritten, but a new one was created called \"tcp.smtp.new\" that"
  echo "you should look at to ensure no new directives were added that may cause issues with your system."
  echo ""
  sleep 10

else

touch /etc/tcprules.d/tcp.smtp
echo '127.:allow,RELAYCLIENT="",DKSIGN="/var/qmail/control/domainkeys/%/private",RBLSMTPD="",NOP0FCHECK="1"' > /etc/tcprules.d/tcp.smtp
echo ':allow,BADMIMETYPE="",BADLOADERTYPE="M",CHKUSER_RCPTLIMIT="50",CHKUSER_WRONGRCPTLIMIT="10",QMAILQUEUE="/var/qmail/bin/simscan",DKSIGN="/var/qmail/control/domainkeys/%/private",NOP0FCHECK="1"' >> /etc/tcprules.d/tcp.smtp
qmailctl cdb

fi

if [ -f /var/qmail/supervise/clamd/run ]; then
	rm -f /var/qmail/supervise/clamd/run ;
fi

if [ -f /var/qmail/supervise/clamd/log/run ]; then
	rm -f /var/qmail/supervise/clamd/log/run ;
fi

if [ -f /etc/rc.d/init.d/clamav ]; then
	chkconfig clamav off
	service clamav stop
	rm -f /etc/rc.d/init.d/clamav ;
fi

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/%{name}-%{pversion} ] && rm -rf $RPM_BUILD_DIR/%{name}-%{pversion}
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

#-------------------------------------------------------------------------------
%files 
#-------------------------------------------------------------------------------
%defattr(644,clam,clam)
#qdir on install was root,root probably should be clam,root
%attr(0750,clam,root) %dir %{qdir}
#bin was on install root, root again it should be clam,root
%attr(0750,clam,root) %dir %{qdir}/bin
%attr(4711,clam,root) %{qdir}/bin/%{name}
# control was root,root it should be clam,root
%attr(0750,clam,root) %{qdir}/control
%attr(0750,clam,root) %dir %{qdir}/%{name}
%attr(4755,root,root) %{qdir}/bin/simscanmk

%attr(0755,root,root) %{qdir}/bin/update-%{name}
%attr(4711,clam,root) %{qdir}/bin/%{name}
%attr(0644,root,root) %dir %{_datadir}/doc/%{name}-%{pversion}
%attr(0644,root,root) %{_datadir}/doc/%{name}-%{pversion}/*


%attr(0644,clam,root) %config(noreplace) %{qdir}/control/simcontrol

%attr(0755,qmaill,qmail)  %dir %{qdir}/supervise
%attr(1700,qmaill,qmail)  %dir %{qdir}/supervise/clamd
%attr(0700,qmaill,qmail)  %dir %{qdir}/supervise/clamd/log
%attr(0755,qmaill,qmail)  %dir %{qdir}/supervise/clamd/supervise

%attr(0751,qmaill,qmail) %{qdir}/supervise/clamd/down
%attr(0751,qmaill,qmail) %{qdir}/supervise/clamd/log/down

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Mon Dec 16 2019 Dionysis Kladis <dkstiler@gmail.com> 1.4.0-1.4.8.kng
- Fix install section moving permitions to files section in accordance with copr directives
- Adding missing depedencies for centos 6 and centos 7
- Adding an if statement to configure properly the user for centos 7

* Sat Mar 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.8.mr
- set no 'requires' for clamav, clamd and ripmime (need manual install)

* Fri Mar 13 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.7.mr
- change user from clamav to clam because clamav from epel using clam user
- fix using ripmime (from epel) instead ripmime-toaster

* Tue Mar 03 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.6.mr
- rename run file to down because using clamd service and high cpu usage for clamd supervise

* Sun Mar 01 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.5.mr
- add missing clamd as dependencies
- set user as clam instead clamav in clamd run

* Sat Feb 28 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.4.mr
- using ripmime (from epel) instead ripmime-toaster

* Mon Feb 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.3.mr
- change multilog to splogger

* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.2.mr
- cleanup spec based on toaster github (without define like build_cnt_60)
- user clamav (from epel) instead clamav-toaster
- add 'run' and 'log-run' files of clamav-toaster to here

* Thu Jul 4 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.1.mr
- change BuildPreReq to BuildRequires (centos 6 deprecated issue)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 1.4.0-1.4.0.mr
- add build_cnt_60 and build_cnt_6064

* Mon Mar 26 2012 Eric Shubert <ejs@shubes.net> 1.4.0-1.4.0
- Changed jms1 combined 3 patch to combined 4 patch
- Set o+s on simscanmk file so that non-root users can run it
- Added update-simscan script for running simscanmk from freshclam etc.
- Modified simcontrol file to be %config(noreplace)
* Thu Aug 13 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.8
- Changed minor version number to align with version changes and scripts
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.1
- Changed spec file so that tcp.smtp file is no longer overwritten and a tcp.smtp.new is created
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Thu Jun 11 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.1
- Added Mandriva 2009 support
- Increased spam_hits to 40 from the original 20
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 1.4.0-1.3.0
- Merged the fork into the main QMT trunk. Thanks to Steve for the package and testing.
- Added Suse 11.1, Fedora 9, Fedora 9 x86_64, Fedora 10, and Fedora 10 x86_64 support
- Patched simscanmk.c to compile with new distro compiler flags (O_CREAT error)
* Wed May 7 2008 Steve Huff <shuff@vecna.org> 1.4.0-1.4.0
- Updated to simscan 1.4.0
- Added John Simpson's patch to support varying ClamAV update file locations
  (http://qmail.jms1.net/simscan/)
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.3.6
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
- Removed DKVERIFY - domainkeys now only signs outgoing mail
* Sat Mar 03 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.5
- Skipped RBL checks on localhost
- Modified DKVERIFY to safer defaults
* Thu Jan 11 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.4
- Added fix to allow building with ClamAV 0.90rc2 and above, which doesn't use daily.cvd and main.cvd
* Mon Jan 08 2007 Erik A. Espinoza <espinoza@kabewm.com> 1.3.1-1.3.3
- Upgraded to Simscan 1.3.1
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.3.1
- Added per domain and spam hits to config
- Added SuSE 10.1 support
* Thu May 18 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 1.2-1.2.8
- Enabled simscan in configure line
- Added ripmime-toaster to Requires line
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 1.2-1.2.7
- Update to simscan-1.2
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.6
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.5
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.4
- Add CentOS 4 x86_64 support
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.3
- Add support for Fedora Core 4
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 1.1-1.2.2
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Sat May 28 2005 Nick Hemmesch <nick@ndhsoft.com> 1.1-1.2.1
- Initial simscan-toaster build
