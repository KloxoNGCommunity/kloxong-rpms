%define	name qmailmrtg
%define	pversion 4.2
%define 	bversion 1.3
%define	rpmrelease 8.kng%{?dist}

%define		release %{bversion}.%{rpmrelease}
%define		apacheuser apache
%define		apachegroup apache
%define		crontab /etc/crontab
%define		outputdir %{basedir}/htdocs/mrtg
#Requires:	vixie-cron, crontabs >= 1.10, httpd >= 2.2.2, php >= 5.1.6, mrtg
Requires:	vixie-cron, crontabs >= 1.10, mrtg
%define		ccflags %{optflags}
%define		ldflags %{optflags}

############### RPM ################################

%define		debug_package %{nil}
%define         vtoaster %{pversion}
%define 	basedir %{_datadir}/toaster
%define 	mrtgdir %{basedir}/mrtg
%define		builddate Fri Jun 12 2009

Name:		%{name}-toaster
Summary:	Mrtg for qmail-toaster
Version:	%{vtoaster}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://dev.prodigysolutions.com
Source0:	qmailmrtg7-%{pversion}.tar.bz2
Source1:	index.php.bz2
Patch0:		qmailmrtg7-modernize-code.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	qmail-toaster >= 1.03
Requires:	qmail-toaster >= 1.03, control-panel-toaster >= 0.2
Packager:       Jake Vickers <jake@qmailtoaster.com>

#-------------------------------------------------------------------
%description
#-------------------------------------------------------------------
Qmail MRTG Stat collector 


#-------------------------------------------------------------------
%prep
#-------------------------------------------------------------------
[ -n %{buildroot} -a %{buildroot} ] && rm -rf %{buildroot}


#-------------------------------------------------------------------
%setup -q -n qmailmrtg7-%{pversion}
#-------------------------------------------------------------------

# We need to patch for modern compilers
%patch0 -p1

# Try detecting newest gcc (some distributions have got more then one compiler)
# and write it on a temp file 

[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc

if   [ -x /usr/bin/gcc-3.2.3 ]; then
	echo "/usr/bin/gcc-3.2.3" > %{_tmppath}/%{name}-%{pversion}-gcc
elif   [ -x /usr/bin/gcc-3.2.2 ]; then
	echo "/usr/bin/gcc-3.2.2" > %{_tmppath}/%{name}-%{pversion}-gcc
elif   [ -x /usr/bin/gcc-3.2.1 ]; then
	echo "/usr/bin/gcc-3.2.1" > %{_tmppath}/%{name}-%{pversion}-gcc
elif [ -x /usr/bin/gcc-3.2 ]; then
        echo "/usr/bin/gcc-3.2" > %{_tmppath}/%{name}-%{pversion}-gcc
elif [ -x /usr/bin/gcc-3.1.1 ]; then
        echo "/usr/bin/gcc-3.1.1" > %{_tmppath}/%{name}-%{pversion}-gcc
else
	echo "gcc" > %{_tmppath}/%{name}-%{pversion}-gcc
fi

#-------------------------------------------------------------------
%build
#-------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

# Write the module for the control panel
#-------------------------------------------------------------------
cat <<EOF >>$RPM_BUILD_DIR/qmailmrtg7-%{pversion}/qmailmrtg.module


<!-- qmailmrtg.module -->
<tr>
	<td align="right" width="47%">MTA statistics</td>
	<td width="6%">&nbsp;</td>
	<td align="left" width=47%"><input type="button" value="qmailmrtg7-%{pversion}" class="inputs" onClick="location.href='/stats-toaster/';"></td>
</tr>
<!-- qmailmrtg.module -->


EOF
#"-------------------------------------------------------------------

# We have gcc written in a temp file
export CC="`cat %{_tmppath}/%{name}-%{pversion}-gcc` %{ccflags}"

$CC checkq.c -o checkq
./checkq
$CC -s -O qmailmrtg7.c -o qmailmrtg


#-------------------------------------------------------------------
%install
#-------------------------------------------------------------------
install -d %{buildroot}%{_sysconfdir}/cron.d/
install -d %{buildroot}%{mrtgdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{basedir}/htdocs/mrtg
install -d %{buildroot}%{basedir}/include
install -m755 qmailmrtg %{buildroot}%{_bindir}/qmailmrtg
install -m644 %{SOURCE1} %{buildroot}%{basedir}/htdocs/mrtg/
install -m644 qmailmrtg.module %{buildroot}%{basedir}/include/
bunzip2 %{buildroot}%{basedir}/htdocs/mrtg/index.php.bz2

cat <<EOF >>%{buildroot}%{mrtgdir}/qmailmrtg.cfg
# config by Oden Eriksson <oden@d-srv.com>

Refresh: 600
Interval: 10
WriteExpires: Yes

# where to save the output.
WorkDir: %{outputdir}

#############################################################

Title[messages]: FQDN - Qmail (throughput)
MaxBytes[messages]: 10000
AbsMax[messages]: 20000
Options[messages]: gauge
Target[messages]: \`/usr/bin/qmailmrtg m /var/log/qmail/send\`
PageTop[messages]: <font face=arial size=3><B>FQDN</B> - Qmail (throughput)</font><br>
ShortLegend[messages]: Messages
YLegend[messages]: Messages
Legend1[messages]: Total messages
LegendI[messages]: &nbsp;Deliveries:
LegendO[messages]: &nbsp;Attempts:
WithPeak[messages]: ymwd

#-------------------------------------------------------------------

Title[queue-size]: FQDN - Qmail (queue size)
MaxBytes[queue-size]: 10000
AbsMax[queue-size]: 100000
Options[queue-size]: gauge
Target[queue-size]: \`/usr/bin/qmailmrtg q /var/qmail/queue\`
PageTop[queue-size]: <font face=arial size=3><B>FQDN</B> - Qmail (queue size)</font><br>
ShortLegend[queue-size]: Messages
YLegend[queue-size]: Messages
Legend1[queue-size]: Messages
LegendI[queue-size]: &nbsp;Messages:
LegendO[queue-size]: &nbsp;Unprocessed Messages:
WithPeak[queue-size]: ymwd

#-------------------------------------------------------------------

Title[clamd]: FQDN - clamd
MaxBytes[clamd]: 10000
AbsMax[clamd]: 100000
Options[clamd]: gauge
Target[clamd]: \`/usr/bin/qmailmrtg C /var/log/qmail/clamd\`
PageTop[clamd]: <font face=arial size=3><B>FQDN ClamAV</B></font><br>
ShortLegend[clamd]: Msg
YLegend[clamd]: Viruses
Legend1[clamd]: Total Viruses;
LegendI[clamd]: Found&nbsp;
LegendO[clamd]: Errors:&nbsp;
WithPeak[clamd]: ymwd

#-------------------------------------------------------------------

Title[spamd]: FQDN - spamd
MaxBytes[spamd]: 10000
AbsMax[spamd]: 100000
Options[spamd]: gauge
Target[spamd]: \`/usr/bin/qmailmrtg S /var/log/qmail/spamd\`
PageTop[spamd]: <font face=arial size=3><B>FQDN SpamAssassin</B></font><br>
ShortLegend[spamd]: Messages
YLegend[spamd]: Spam/hour
Legend1[spamd]: Total Spam;
LegendI[spamd]: Clean&nbsp;
LegendO[spamd]: Spam:&nbsp;
WithPeak[spamd]: ymwd

#-------------------------------------------------------------------

Title[concurrency]: FQDN - Qmail (concurrency)
MaxBytes[concurrency]: 500
AbsMax[concurrency]: 10000
Options[concurrency]: gauge
Target[concurrency]: \`/usr/bin/qmailmrtg c /var/log/qmail/send\`
PageTop[concurrency]: <font face=arial size=3><B>FQDN</B> - Qmail (concurrency)</font><br>
ShortLegend[concurrency]: Concurrency
YLegend[concurrency]: Concurrency
Legend1[concurrency]: Concurrency
LegendI[concurrency]: &nbsp;Local:
LegendO[concurrency]: &nbsp;Remote:
WithPeak[concurrency]: ymwd

#-------------------------------------------------------------------

Title[messstatus]: FQDN - Qmail (Success/Failures)
MaxBytes[messstatus]: 10000
AbsMax[messstatus]: 100000
Options[messstatus]: gauge
Target[messstatus]: \`/usr/bin/qmailmrtg s /var/log/qmail/send\`
PageTop[messstatus]: <font face=arial size=3><B>FQDN</B> - Qmail (Success/Failures)</font><br>
ShortLegend[messstatus]: Messages
YLegend[messstatus]: Messages
Legend1[messstatus]: Messages
LegendI[messstatus]: &nbsp;Success:
LegendO[messstatus]: &nbsp;Failures:
WithPeak[messstatus]: ymwd

#-------------------------------------------------------------------

Title[bytes]: FQDN - Qmail (Bytes Transfered)
MaxBytes[bytes]: 200000
AbsMax[bytes]: 10000000
Options[bytes]: gauge
Target[bytes]: \`/usr/bin/qmailmrtg b /var/log/qmail/send\`
PageTop[bytes]: <font face=arial size=3><B>FQDN</B> - Qmail (Bytes Transfered)</font><br>
ShortLegend[bytes]: kB
YLegend[bytes]: kB
Legend1[bytes]: kB
LegendI[bytes]: &nbsp;kB:
LegendO[bytes]: &nbsp;kB:
WithPeak[bytes]: ymwd

#-------------------------------------------------------------------

Title[smtp]: FQDN - Qmail (smtp concurrency)
MaxBytes[smtp]: 100
AbsMax[smtp]: 500
Options[smtp]: gauge
Target[smtp]: \`/usr/bin/qmailmrtg t /var/log/qmail/smtp\`
PageTop[smtp]: <font face=arial size=3><B>FQDN</B> - Qmail (smtp)</font><br>
ShortLegend[smtp]: smtp
YLegend[smtp]: smtp
Legend1[smtp]: smtp
LegendI[smtp]: &nbsp;smtp:
LegendO[smtp]: 
WithPeak[smtp]: ymwd

#-------------------------------------------------------------------

Title[smtpad]: FQDN - smtp (allow/deny)
MaxBytes[smtpad]: 1000
AbsMax[smtpad]: 10000
Options[smtpad]: gauge
Target[smtpad]: \`/usr/bin/qmailmrtg a /var/log/qmail/smtp\`
PageTop[smtpad]: <font face=arial size=3><B>FQDN</B> - smtp (allow/deny)</font><br>
ShortLegend[smtpad]: Smtp
YLegend[smtpad]: Smtp
Legend1[smtpad]: Smtp
LegendI[smtpad]: &nbsp;Allow:
LegendO[smtpad]: &nbsp;Deny:
WithPeak[smtpad]: ymwd

#-------------------------------------------------------------------

Title[pop3]: FQDN - Qmail (pop3)
MaxBytes[pop3]: 100
AbsMax[pop3]: 500
Options[pop3]: gauge
Target[pop3]: \`/usr/bin/qmailmrtg t /var/log/qmail/pop3\`
PageTop[pop3]: <font face=arial size=3><B>FQDN</B> - Qmail (pop3)</font><br>
ShortLegend[pop3]: pop3
YLegend[pop3]: pop3
Legend1[pop3]: pop3
LegendI[pop3]: &nbsp;pop3:
LegendO[pop3]: 
WithPeak[pop3]: ymwd

#-------------------------------------------------------------------

Title[pop3ad]: FQDN - pop3 (allow/deny)
MaxBytes[pop3ad]: 1000
AbsMax[pop3ad]: 10000
Options[pop3ad]: gauge
Target[pop3ad]: \`/usr/bin/qmailmrtg a /var/log/qmail/pop3\`
PageTop[pop3ad]: <font face=arial size=3><B>FQDN</B> - pop3 (allow/deny)</font><br>
ShortLegend[pop3ad]: Pop3
YLegend[pop3ad]: Pop3
Legend1[pop3ad]: Pop3
LegendI[pop3ad]: &nbsp;Allow:
LegendO[pop3ad]: &nbsp;Deny:
WithPeak[pop3ad]: ymwd

#-------------------------------------------------------------------

Title[imap4]: FQDN - Qmail (imap4)
MaxBytes[imap4]: 100
AbsMax[imap4]: 500
Options[imap4]: gauge
Target[imap4]: \`/usr/bin/qmailmrtg t /var/log/qmail/imap4\`
PageTop[imap4]: <font face=arial size=3><B>FQDN</B> - Qmail (imap4)</font><br>
ShortLegend[imap4]: imap4
YLegend[imap4]: imap4
Legend1[imap4]: imap4
LegendI[imap4]: &nbsp;imap4:
LegendO[imap4]: 
WithPeak[imap4]: ymwd

#-------------------------------------------------------------------

Title[imap4ad]: FQDN - imap4 (allow/deny)
MaxBytes[imap4ad]: 1000
AbsMax[imap4ad]: 10000
Options[imap4ad]: gauge
Target[imap4ad]: \`/usr/bin/qmailmrtg a /var/log/qmail/imap4\`
PageTop[imap4ad]: <font face=arial size=3><B>FQDN</B> - imap4 (allow/deny)</font><br>
ShortLegend[imap4ad]: Imap4
YLegend[imap4ad]: Imap4
Legend1[imap4ad]: Imap4
LegendI[imap4ad]: &nbsp;Allow:
LegendO[imap4ad]: &nbsp;Deny:
WithPeak[imap4ad]: ymwd

#-------------------------------------------------------------------

Title[imap4-ssl]: FQDN - Qmail (imap4-ssl)
MaxBytes[imap4-ssl]: 100
AbsMax[imap4-ssl]: 500
Options[imap4-ssl]: gauge
Target[imap4-ssl]: \`/usr/bin/qmailmrtg t /var/log/qmail/imap4-ssl\`
PageTop[imap4-ssl]: <font face=arial size=3><B>FQDN</B> - Qmail (imap4-ssl)</font><br>
ShortLegend[imap4-ssl]: imap4-ssl
YLegend[imap4-ssl]: imap4-ssl
Legend1[imap4-ssl]: imap4-ssl
LegendI[imap4-ssl]: &nbsp;imap4-ssl:
LegendO[imap4-ssl]: 
WithPeak[imap4-ssl]: ymwd

#-------------------------------------------------------------------

Title[imap4-sslad]: FQDN - imap4-ssl (allow/deny)
MaxBytes[imap4-sslad]: 1000
AbsMax[imap4-sslad]: 10000
Options[imap4-sslad]: gauge
Target[imap4-sslad]: \`/usr/bin/qmailmrtg a /var/log/qmail/imap4-ssl\`
PageTop[imap4-sslad]: <font face=arial size=3><B>FQDN</B> - imap4-ssl (allow/deny)</font><br>
ShortLegend[imap4-sslad]: Imap4-ssl
YLegend[imap4-sslad]: Imap4-ssl
Legend1[imap4-sslad]: Imap4-ssl
LegendI[imap4-sslad]: &nbsp;Allow:
LegendO[imap4-sslad]: &nbsp;Deny:
WithPeak[imap4-sslad]: ymwd

#-------------------------------------------------------------------

Title[pop3-ssl]: FQDN - Qmail (pop3-ssl)
MaxBytes[pop3-ssl]: 100
AbsMax[pop3-ssl]: 500
Options[pop3-ssl]: gauge
Target[pop3-ssl]: \`/usr/bin/qmailmrtg t /var/log/qmail/pop3-ssl\`
PageTop[pop3-ssl]: <font face=arial size=3><B>FQDN</B> - Qmail (pop3-ssl)</font><br>
ShortLegend[pop3-ssl]: pop3-ssl
YLegend[pop3-ssl]: pop3-ssl
Legend1[pop3-ssl]: pop3-ssl
LegendI[pop3-ssl]: &nbsp;pop3-ssl:
LegendO[pop3-ssl]: 
WithPeak[pop3-ssl]: ymwd

#-------------------------------------------------------------------

Title[pop3-sslad]: FQDN - pop3-ssl (allow/deny)
MaxBytes[pop3-sslad]: 1000
AbsMax[pop3-sslad]: 10000
Options[pop3-sslad]: gauge
Target[pop3-sslad]: \`/usr/bin/qmailmrtg a /var/log/qmail/pop3-ssl\`
PageTop[pop3-sslad]: <font face=arial size=3><B>FQDN</B> - pop3-ssl (allow/deny)</font><br>
ShortLegend[pop3-sslad]: Pop3-ssl
YLegend[pop3-sslad]: Pop3-ssl
Legend1[pop3-sslad]: Pop3-ssl
LegendI[pop3-sslad]: &nbsp;Allow:
LegendO[pop3-sslad]: &nbsp;Deny:
WithPeak[pop3-sslad]: ymwd


EOF


#-------------------------------------------------------------------
%post
#-------------------------------------------------------------------
# Setup mrtg
cat <<EOF >>%{_tmppath}/setupmrtg
env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
EOF

chmod +x %{_tmppath}/setupmrtg
%{_tmppath}/setupmrtg 2>&1 > /dev/null
rm -f %{_tmppath}/setupmrtg


#-------------------------------------------------------------------
# Install cron-job
#-------------------------------------------------------------------
# Remove old cron-job
grep -v '* * * * root %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > %{crontab}.old
mv -f %{crontab}.old %{crontab}


if ! grep '* * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > /dev/null; then
  echo "" >> %{crontab}
  echo "0-59/5 * * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null" >> %{crontab}
fi


#-------------------------------------------------------------------
%postun
#-------------------------------------------------------------------
# Remove cron-job
if [ "$1" = "0" ]; then
  grep -v '* * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > %{crontab}.new
  mv -f %{crontab}.new %{crontab}
fi


#-------------------------------------------------------------------
%clean
#-------------------------------------------------------------------
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d $RPM_BUILD_DIR/qmailmrtg7-%{pversion} ] && rm -rf $RPM_BUILD_DIR/qmailmrtg7-%{pversion}
[ -f %{_tmppath}/%{name}-%{pversion}-gcc ] && rm -f %{_tmppath}/%{name}-%{pversion}-gcc


#-------------------------------------------------------------------
%files
#-------------------------------------------------------------------
%defattr(-,root,root)
%attr(0755,root,root) %config(noreplace) %{mrtgdir}/qmailmrtg.cfg
%attr(0755,root,root) %{_bindir}/qmailmrtg
%defattr(-,%{apacheuser},%{apachegroup})
%attr(0755,%{apacheuser},%{apachegroup}) %dir  %{basedir}/htdocs/mrtg
%attr(0644,%{apacheuser},%{apachegroup}) %{basedir}/htdocs/mrtg/index.php
%attr(0644,%{apacheuser},%{apachegroup}) %{basedir}/include/*


#-------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------
* Sat Dec 20 2014 Mustafa Ramadhan <mustafa@bigraf.com> 3.4-1.3.8.mr
- cleanup spec based on toaster github (without define like build_cnt_60)

* Sat Jan 12 2013 Mustafa Ramadhan <mustafa@bigraf.com> 3.4-1.3.7.mr
- add build_cnt_60 and build_cnt_6064

* Sun Apr 10 2011 Martin Waschbüsch <martin@waschbuesch.de> 3.4-1.3.7
- Converted PHP tags to full format <? to <?php
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.6
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Changed some commenting in spec file to English for consistency
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.4
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.3.3
- Add CentOS i386 support
- Add CentOS x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.2-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.11
- Add Fedora Core 5 support
* Sat Apr 29 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.10
- Fix qmailmrtg.cfg
* Fri Apr 28 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.9
- Set path variable for distros - Wade Albright <wade@bidnask.com>
- Additional graphs by Guillermo Villasana <gvillasana@exerwebsolutions.com>
* Sat Nov 12 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.8
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.7
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.6
- Add CentOS 4 x86_64 support
* Mon Jul 18 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 4.2-1.2.5
- Upgraded to qmailmrtg 4.2
- Added support for virus scanning
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.4
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 3.4-1.2.3
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Changed Mandrake 9.1,9.2,10.0,10.1 and 10.2 to apache-2x so all spec files has the same requirements.
- Add requirement for mandrake mrtg to Mandrake 9.1,9.2,10.0,10.1 and 10.2
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.2
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.1
- Update spec file
- Add Fedora Core 2 support
* Wed Feb 11 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.11
- Define crontab
* Mon Jan 12 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.10
- Trustix fix - fcrontab dep by Christian Dietrich
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.9
- Add Fedora Core 1 support
* Tue Nov 25 2003 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.8
- Add Trustix 2.0 support
- Fix images to images-toaster
* Fri May 24 2003 Miguel Beccari <miguel.beccari@clikka.com> 03.7-1.0.7
- Fixed mrtg dependency: Red Hat 9 has got its mrtg package
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 03.7-1.0.6
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.5
- Conectiva Linux 7.0 support
- Better managing of apache user (related to distro)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 3.7-1.0.3
- Support for Red Hat 8.0
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sun Oct 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 3.7-0.9.2
- Clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 3.7-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.3.7-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.3.7-2
- Added imap4, imap4-ssl, pop3-ssl statistics.
- Testes crontab jobs: now it REALLY works 100%!!!
* Sun Sep 01 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.3.7-1
- New version: it works now
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3-2
- Deleted Mandrake Release Autodetection (creates problems)
- Fixed RedHat compatibility
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3-1
- First RPM release. It comes with toaster templates, toaster layout,
  toaster dependencies: seems to work.

