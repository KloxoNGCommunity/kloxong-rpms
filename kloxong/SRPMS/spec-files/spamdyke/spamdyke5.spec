Summary:	A drop-in connection-time spam filter for qmail.
Name:		spamdyke
Version:	5.0.1
Release:	2.kng%{?dist}
License:	GPL
Group:		Applications/Internet
Packager:	Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org>
URL:		http://www.spamdyke.org/
Source:	http://www.spamdyke.org/releases/%{name}-%{version}-full.tgz
Source1:	spamdyke.cron
Source2:	spamdyke5.conf
Source3:	spamdyke.sql
#Patch1:	spamdyke-4.1.0-mysql.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	mysql-devel, vpopmail-toaster >= 5.4.1

%description
spamdyke is a filter for monitoring and intercepting incoming SMTP connections
to a qmail server. It acts as a transparent middleman, observing the conversation
without interference unless it sees something it should block. Because it can
silently monitor, it can also log mail traffic in several different ways.

%package utils
Group:		Utilities/System
Summary:	These are some additional programs for spamdyke.
Requires:	%{name} = %{version}

%description utils
These are some additional programs for spamdyke.

%prep
%setup
# Not yet
#%patch1 -p1

%build
export LDFLAGS="-L%{_libdir}/mysql"
# Build spamdyke...
cd %{name}
%configure --with-excessive-output
make
# Build utils...
cd ../utils
%configure
make
# Build qrv...
cd ../spamdyke-qrv
%configure --with-excessive-output \
	--with-vpopmail-support \
		VALIAS_PATH=/home/vpopmail/bin/valias \
		VUSERINFO_PATH=/home/vpopmail/bin/vuserinfo
make

%install
install -d $RPM_BUILD_ROOT{%{_bindir},%{_docdir}/%{name}-%{version},%{_sysconfdir}}
install spamdyke/spamdyke $RPM_BUILD_ROOT%{_bindir}
install spamdyke-qrv/spamdyke-qrv $RPM_BUILD_ROOT%{_bindir}
install utils/{dns*[!.c],domain*[!.c]} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/spamdyke.conf
install documentation/{*.txt,*.html} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}


%{__mkdir_p} %{buildroot}/%{_sysconfdir}/cron.daily/
%{__mkdir_p} %{buildroot}/var/qmail/spamdyke
%{__mkdir_p} %{buildroot}/var/qmail/spamdyke/greylist
%{__mkdir_p} %{buildroot}/usr/share/spamdyke/
touch        %{buildroot}/var/qmail/spamdyke/blacklist_senders
touch        %{buildroot}/var/qmail/spamdyke/blacklist_recipients
touch        %{buildroot}/var/qmail/spamdyke/blacklist_keywords
touch        %{buildroot}/var/qmail/spamdyke/blacklist_ip
touch        %{buildroot}/var/qmail/spamdyke/whitelist_rdns
touch        %{buildroot}/var/qmail/spamdyke/whitelist_ip
touch        %{buildroot}/var/qmail/spamdyke/whitelist_senders
%{__install} %{SOURCE1} %{buildroot}/%{_sysconfdir}/cron.daily/spamdyke
%{__install} %{SOURCE3} %{buildroot}/usr/share/spamdyke/spamdyke.sql

%triggerin -- psa-qmail

if [ -f /etc/xinetd.d/smtp_psa ]; then
  SMTP_PSA=/etc/xinetd.d/smtp_psa
else
  SMTP_PSA=/etc/xinetd.d/smtp.psa
fi

if ! grep -q spamdyke $SMTP_PSA ; then
  perl -p -i -e "s[relaylock][relaylock /usr/bin/spamdyke -f /etc/spamdyke.conf]" $SMTP_PSA
fi


%triggerun -- psa-qmail 
if [ -f /etc/xinetd.d/smtp_psa ]; then
  SMTP_PSA=/etc/xinetd.d/smtp_psa
else
  SMTP_PSA=/etc/xinetd.d/smtp.psa
fi

if grep -q spamdyke $SMTP_PSA ; then
 perl -p -i -e "s[/usr/bin/spamdyke -f /etc/spamdyke.conf][]" $SMTP_PSA
fi

%post
#if [ $1 = 1 ]; then
#  if [ -f /etc/psa/.psa.shadow ]; then
#    MYSQL="mysql -u admin -p`cat /etc/psa/.psa.shadow` psa "
#  else
#    MYSQL="mysql -u admin -p'' psa "
#  fi

#  $MYSQL  < /usr/share/spamdyke/spamdyke.sql

#  # restart xinetd
#  /sbin/service xinetd restart

#fi

	
%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && %{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config %{_sysconfdir}/spamdyke.conf
# permissions (
%attr(-, qmaild, qmail) %dir /var/qmail/spamdyke
%attr(-, qmaild, qmail) %dir /var/qmail/spamdyke/greylist
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/blacklist_senders
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/blacklist_senders
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/blacklist_recipients
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/blacklist_keywords
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/blacklist_ip
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/whitelist_rdns
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/whitelist_ip
%attr(0644, qmaild, qmail) %config(noreplace) /var/qmail/spamdyke/whitelist_senders
%docdir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*
%{_bindir}/spamdyke
%{_bindir}/spamdyke-qrv
# permissions
/etc/cron.daily/spamdyke
/usr/share/spamdyke/spamdyke.sql


%files utils
%defattr(-,root,root)
%{_bindir}/dns*
%{_bindir}/domain*

%changelog
* Mon Dec 23 2019 John Pierce <john@luckytanuki.com>  5.0.1-2.kng
- Fix warning: File listed twice errors

* Tue Dec 17 2019 Dionysis Kladis <dkstiler@gmail.com> 5.0.1-1.kng
- Adding missing depedency
- Compile on corp for kloxong

* Tue May 19 2015 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.1-1.mr
- update to 5.0.1

* Mon Dec 08 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-7.mr
- disable execute spamdyke database

* Fri Nov 7 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-6.mr
- disable config-mysql in spamdyke.conf

* Tue Nov 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-5.mr
- change %config(noreplace) to %config

* Mon Mar 3 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-4.mr
- add --with-vpopmail-support and --with-excessive-output

* Mon Mar 3 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-3.mr
- include spamdyke-qrv

* Mon Mar 3 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-2.mr
- use spamdyke.conf.example for custom spamdyke.conf

* Thu Feb 27 2014 Mustafa Ramadhan <mustafa@bigraf.com> 5.0.0-1.mr
- update to 5.0.0

* Tue Jul 2 2013 Mustafa Ramadhan <mustafa@bigraf.com> 4.3.1-3.mr
- without mysql request (make less conflict with mysql branch)

* Fri Jan 18 2013 Mustafa Ramadhan <mustafa@bigraf.com> 4.3.1-2.mr
- recompile

* Sun Aug 19 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 4.3.1-2.lx.el5
- Update to 4.3.1

* Tue Dec 13 2011 Danny Terweij <contact@lxcenter.org> - 4.2.0-0
- Update to 4.2.0

* Mon Nov 15 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.1.0-1
- Update to 4.1.0
- Merge in haggybear.de mysql patch 

* Sun Mar 21 2010 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-6
- Added sql patch
- Added sql files and install routine

* Fri Mar 6 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-5
- Permissions updates

* Fri Mar 6 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-4
- Added spamdyke dir, and default configs
- Deprecated reject-ip-in-cc-rdns flag in config

* Mon Mar 2 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-3
- Update to work with Plesk 9

* Wed Feb 11 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-2
- added default spamdyke config for plesk
- added default cleanup cron job for plesk

* Wed Feb 11 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 4.0.10-1
- update to 4.0.10
- import to art-build

* Mon Dec 01 2008 UD <admin@underdark.com.br> 4.0.9-1
- 4.0.9-1

* Fri Nov 21 2008 UD <admin@underdark.com.br> 4.0.8-1
- 4.0.8-1

* Fri Nov 21 2008 UD <admin@underdark.com.br> 4.0.7-1
- 4.0.7-1

* Thu Oct 16 2008 UD <admin@underdark.com.br> 4.0.6-1
- Removed service reload, here's not the right place

* Mon Oct 13 2008 UD <admin@underdark.com.br> 4.0.5-1
- Added excessive flag to configure.
- Added service reload

* Wed Sep 10 2008 UD <admin@underdark.com.br> 4.0.4-1
- 4.0.4-1

* Mon Sep 01 2008 UD <admin@underdark.com.br> 4.0.3-1
- First build on RHEL5.
