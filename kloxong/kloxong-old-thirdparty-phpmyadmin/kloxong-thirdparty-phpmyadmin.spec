%define kloxo /usr/local/lxlabs/kloxo/httpdocs/thirdparty
%define productname kloxo-thirdparty
%define packagename phpMyAdmin
%define packagename2 phpmyadmin

Name: %{productname}-%{packagename2}
Version: 4.0.10.20
Release: 1.kng%{?dist}
Summary: Web based MySQL browser written in php

Group: Applications/Internet
License: GPLv2+
URL: http://www.phpmyadmin.net/
Source0: http://downloads.sourceforge.net/sourceforge/phpmyadmin/%{packagename}-%{version}-all-languages.tar.gz

#Source10: http://downloads.sourceforge.net/sourceforge/phpmyadmin/arctic_ocean-3.3.zip
#Source11: http://downloads.sourceforge.net/sourceforge/phpmyadmin/smooth_yellow-3.3.zip
#Source12: http://downloads.sourceforge.net/sourceforge/phpmyadmin/graphite-1.0.zip
#Source13: http://downloads.sourceforge.net/sourceforge/phpmyadmin/toba-0.2.zip
#Source14: http://downloads.sourceforge.net/sourceforge/phpmyadmin/paradice-3.4.zip
#Source15: http://downloads.sourceforge.net/sourceforge/phpmyadmin/darkblue_orange-2.11.zip
#Source16: http://downloads.sourceforge.net/sourceforge/phpmyadmin/blueorange-1.0b.zip
#Source17: http://downloads.sourceforge.net/sourceforge/phpmyadmin/cleanstrap-1.0.zip
#Source18: http://downloads.sourceforge.net/sourceforge/phpmyadmin/metro-2.0.zip

BuildRoot: %{_tmppath}/%{packagename}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: unzip

#Requires: webserver 
#Requires: php-mysql >= 5.2.0
#Requires: php-mbstring >= 5.2.0
#Requires: php-gd >= 5.2.0
#Requires: php-mcrypt >= 5.2.0
Provides: phpmyadmin = %{version}-%{release}

Obsoletes: kloxomr-thirdparty-phpmyadmin

%description
phpMyAdmin is a tool written in PHP intended to handle the administration of
MySQL over the Web. Currently it can create and drop databases,
create/drop/alter tables, delete/edit/add fields, execute any SQL statement,
manage keys on fields, manage privileges,export data into various formats and
is available in 50 languages


%prep
%setup -qn phpMyAdmin-%{version}-all-languages

# Minimal configuration file
sed -e "/'extension'/s@'mysql'@'mysqli'@"  \
    -e "/'blowfish_secret'/s@''@'MUSTBECHANGEDONINSTALL'@"  \
    config.sample.inc.php >CONFIG

# to avoid rpmlint warnings
find . -name \*.php -exec chmod -x {} \;

#for archive in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} \
#        %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18}
#do
#    %{__unzip} -q $archive -d themes
#done


%build
# Nothing to do


%install
rm -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{kloxo}/%{packagename}
%{__cp} -ad ./* %{buildroot}/%{kloxo}/%{packagename}
%{__cp} CONFIG %{buildroot}/%{kloxo}/%{packagename}/config.inc.php

%{__rm} -rf %{buildroot}/%{kloxo}/%{packagename}/setup
%{__rm} -rf %{buildroot}/%{kloxo}/%{packagename}/contrib



%clean
rm -rf %{buildroot}

%post
# generate a secret key for this install
sed -i -e "/'blowfish_secret'/s/MUSTBECHANGEDONINSTALL/$RANDOM$RANDOM$RANDOM$RANDOM/" \
    %{kloxo}/%{packagename}/config.inc.php
rm -rf %{kloxo}/%{packagename}/config.inc.php.*

%files
%defattr(-,lxlabs,lxlabs,-)
%{kloxo}/%{packagename}
%dir %{kloxo}/%{packagename}
#%config(noreplace) %{kloxo}/%{packagename}/config.inc.php


%changelog
* Wed Jun 19 2024 John Parnell Pierce <john@luckytanuki.com> - 1.3.2-4.kng
- Change product name back to Kloxo

* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.20-1.mr
- update to 4.0.10.20

* Thu May 14 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.10-1.mr
- update to 4.0.10.10

* Mon Mar 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.9-2.mr
- not use %config for security reason
- remove config.inc.php.*

* Mon Mar 09 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.9-1.mr
- update

* Sun Jan 10 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.8-1.mr
- update

* Wed Dec 03 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.6-1.mr
- update

* Fri Oct 09 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10.4-2.mr
- update

* Tue Feb 4 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.10-1.mr
- update to 4.0.10 (still stay in 4.0.x because php 5.2 issue)

* Fri Nov 8 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.9-1.mr
- update to 4.0.9

* Tue Sep 23 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.7-1.mr
- update to 4.0.6

* Tue Sep 10 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.6-1.mr
- update to 4.0.6

* Wed Aug 14 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.5-1.mr
- update to 4.0.5

* Sun Jun 30 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.4.1-1.mr
- update to 4.0.4.1

* Tue Jun 11 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.3-1.mr
- update to 4.0.3

* Sun May 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.2-1.mr
- update to 4.0.2

* Sun May 5 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 4.0.0-1.mr
- update to 4.0.0 but remove themes addons because not compatible

* Fri Apr 26 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5.8.1-1.mr
- update to 3.5.8.1-1

* Sun Apr 21 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5.8-1.mr
- update to 3.5.8-1, update darkblue_orange and add metro theme

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5.7-1.mr
- rename rpm and update

* Tue Jan 29 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5.6-1.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.5.5-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Jan 6 2013 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.5.5-2.lx
- update to 3.5.3

* Mon Nov 26 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.5.4-2.lx
- update to 3.5.4

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.5.3-2.lx
- update to 3.5.3

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.5.2.2-1.lx
- update to 3.5.2.2

* Fri Feb 17 2012 Danny Terweij <contact@lxcenter.org> 3.4.10-1
- SPEC changed for Kloxo (Paths)

* Tue Feb 14 2012 Remi Collet <rpms@famillecollet.com> 3.4.10-1
- Upstream released 3.4.10 (bugfix)

* Wed Dec 21 2011 Remi Collet <rpms@famillecollet.com> 3.4.9-1
- Upstream released 3.4.9 (bugfix and minor security)
  Fix PMASA-2011-19 and PMASA-2011-20

* Thu Dec 01 2011 Remi Collet <rpms@famillecollet.com> 3.4.8-1
- Upstream released 3.4.8 (security)
  Fix PMASA-2011-18
- remove patch merged upstream

* Sun Nov 13 2011 Remi Collet <rpms@famillecollet.com> 3.4.7.1-2
- add patch to avoid notice with php 5.4

* Sat Nov 12 2011 Remi Collet <rpms@famillecollet.com> 3.4.7.1-1
- Upstream released 3.4.7.1 (security)
  Fix PMASA-2011-17

* Sun Oct 23 2011 Remi Collet <rpms@famillecollet.com> 3.4.7-1
- Upstream released 3.4.7 (bugfix)
- add Paradice 3.4 theme

* Sun Oct 16 2011 Remi Collet <rpms@famillecollet.com> 3.4.6-1
- Upstream released 3.4.6 (security)
  Fix PMASA-2011-15 and PMASA-2011-16

* Wed Sep 14 2011 Remi Collet <rpms@famillecollet.com> 3.4.5-1
- Upstream released 3.4.5 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-14.php

* Wed Aug 24 2011 Remi Collet <rpms@famillecollet.com> 3.4.4-1
- Upstream released 3.4.4 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-13.php

* Sat Jul 23 2011 Remi Collet <rpms@famillecollet.com> 3.4.3.2-1
- Upstream released 3.4.3.2 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-12.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-9.php

* Sun Jul  3 2011 Remi Collet <rpms@famillecollet.com> 3.4.3.1-1
- Upstream released 3.4.3.1 (security)
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-8.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-5.php

* Mon Jun 27 2011 Remi Collet <rpms@famillecollet.com> 3.4.3-1
- Upstream released 3.4.3

* Fri Jun 10 2011 Remi Collet <rpms@famillecollet.com> 3.4.2-1
- Upstream released 3.4.2

* Thu May 26 2011 Remi Collet <rpms@famillecollet.com> 3.4.1-1
- Upstream released 3.4.1
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-3.php
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-4.php

* Wed May 11 2011 Remi Collet <rpms@famillecollet.com> 3.4.0-1
- Upstream released 3.4.0
- remove 3.3 themes and add 3.4 ones

* Sat Mar 19 2011 Remi Collet <rpms@famillecollet.com> 3.3.10-1
- Upstream released 3.3.10

* Fri Feb 11 2011 Remi Collet <rpms@famillecollet.com> 3.3.9.2-1
- Upstream released 3.3.9.2
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-2.php

* Tue Feb 08 2011 Remi Collet <rpms@famillecollet.com> 3.3.9.1-1
- Upstream released 3.3.9.1
  http://www.phpmyadmin.net/home_page/security/PMASA-2011-1.php

* Sat Feb 05 2011 Remi Collet <rpms@famillecollet.com> 3.3.9-2
- upstream patches for CVE-2010-4480 and CVE-2010-4481

* Mon Jan 03 2011 Remi Collet <rpms@famillecollet.com> 3.3.9-1
- Upstream released 3.3.9
- update pmamhomme to 1.0b
- don't requires php (to allow nginx or lighttpd instead of apache)

* Mon Oct 25 2010 Remi Collet <rpms@famillecollet.com> 3.3.8.1-1
- Upstream released 3.3.8.1
- add pmamhomme 1.0 theme

* Mon Oct 25 2010 Remi Collet <rpms@famillecollet.com> 3.3.8-1
- Upstream released 3.3.8

* Tue Sep 07 2010 Remi Collet <rpms@famillecollet.com> 3.3.7-1
- Upstream released 3.3.7

* Sun Aug 29 2010 Remi Collet <rpms@famillecollet.com> 3.3.6-1
- Upstream released 3.3.6

* Fri Aug 20 2010 Remi Collet <rpms@famillecollet.com> 3.3.5.1-1
- Upstream released 3.3.5.1

* Mon Jul 26 2010 Remi Collet <rpms@famillecollet.com> 3.3.5-1
- Upstream released 3.3.5

* Tue Jun 29 2010 Remi Collet <rpms@famillecollet.com> 3.3.4-1
- Upstream released 3.3.4
- add Paradice 3.0b theme

* Mon May 10 2010 Remi Collet <rpms@famillecollet.com> 3.3.3-1.###.remi
- Upstream released 3.3.3
- clean old changelog entry (version < 3.0.0)

* Thu Mar 18 2010 Remi Collet <rpms@famillecollet.com> 3.3.1-1.###.remi
- Upstream released 3.3.1

* Mon Mar 08 2010 Remi Collet <rpms@famillecollet.com> 3.3.0-1.###.remi
- Upstream released 3.3.0
- remove obsolete 3.2 themes (clearview3, crimson_gray, grid, hillside, paradice)
- add new 3.3 themes (smooth_yellow, arctic_ocean)
- add some required extensions (gd, mcrypt)
- add upload, save, config dir in /var/lib/phpMyAdmin
- use vendor_config.php
- swicth to mysqli

* Sun Jan 10 2010 Remi Collet <rpms@famillecollet.com> 3.2.5-1.###.remi
- Upstream released 3.2.5 (bug fixes)
- build for EOL fedora and EL

* Wed Dec 02 2009 Remi Collet <rpms@famillecollet.com> 3.2.4-1.###.remi
- Upstream released 3.2.4 (bug fixes)
- build for EOL fedora and EL

* Fri Oct 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.3-1.###.remi
- Upstream released 3.2.3 (bug fixes)
- build for EOL fedora and EL

* Tue Oct 13 2009 Remi Collet <rpms@famillecollet.com> 3.2.2.1-1.###.remi
- Upstream released 3.2.2.1 (security fix)
- build for EOL fedora and EL

* Sun Sep 13 2009 Remi Collet <rpms@famillecollet.com> 3.2.2-1.###.remi
- Upstream released 3.2.2 (bug fixes)
- build for EOL fedora and EL

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.1-1.###.remi
- Upstream released 3.2.1 (bug fixes and a new language: Uzbek)
- build for EOL fedora and EL

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> 3.2.0.1-1.###.remi
- Upstream released 3.2.0.1 (security release)
- build for EOL fedora and EL

* Mon Jun 15 2009 Remi Collet <rpms@famillecollet.com> 3.2.0-1.###.remi
- Upstream released 3.2.0
- build for EOL fedora and EL
- add theme clearview3-3.1.zip
- add theme crimson_gray-3.1-3.2.zip
- add theme grid-2.11d.zip
- add theme hillside-3.0.zip
- add theme paradice-3.0a.zip

* Fri May 15 2009 Remi Collet <rpms@famillecollet.com> 3.1.5-1.###.remi
- Upstream released 3.1.5
- build for EOL fedora and EL

* Sat Apr 25 2009 Remi Collet <rpms@famillecollet.com> 3.1.4-1.###.remi
- Upstream released 3.1.4
- build for EOL fedora and EL

* Tue Apr 14 2009 Remi Collet <rpms@famillecollet.com> 3.1.3.2-1.###.remi
- Upstream released 3.1.3.1
- build for EOL fedora and EL

* Wed Mar 25 2009 Remi Collet <rpms@famillecollet.com> 3.1.3.1-1.###.remi
- build for EOL fedora and EL

* Wed Mar 25 2009 Robert Scheck <robert@fedoraproject.org> 3.1.3.1-1
- Upstream released 3.1.3.1 (#492066)

* Sun Mar 01 2009 Remi Collet <rpms@famillecollet.com> 3.1.3-1.###.remi
- Upstream released 3.1.3
- build for EOL fedora and EL

* Tue Jan 20 2009 Remi Collet <rpms@famillecollet.com> 3.1.2-1.###.remi
- rebuild for EOL fedora and EL

* Tue Jan 20 2009 Robert Scheck <robert@fedoraproject.org> 3.1.2-1
- Upstream released 3.1.2

* Fri Dec 12 2008 Remi Collet <rpms@famillecollet.com> 3.1.1-1.###.remi
- rebuild for EOL fedora and EL

* Thu Dec 11 2008 Robert Scheck <robert@fedoraproject.org> 3.1.1-1
- Upstream released 3.1.1 (#475954)

* Sat Nov 29 2008 Remi Collet <rpms@famillecollet.com> 3.1.0-1.###.remi
- rebuild for EOL fedora and EL

* Sat Nov 29 2008 Robert Scheck <robert@fedoraproject.org> 3.1.0-1
- Upstream released 3.1.0
- Replaced LocationMatch with Directory directive (#469451)

* Fri Oct 31 2008 Remi Collet <rpms@famillecollet.com> 3.0.1.1-1.###.remi
- rebuild for EOL fedora and EL

* Thu Oct 30 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1.1-1
- Upstream released 3.0.1.1 (#468974)

* Thu Oct 23 2008 Remi Collet <rpms@famillecollet.com> 3.0.1-1.###.remi
- rebuild for EOL fedora 

* Wed Oct 22 2008 Robert Scheck <robert@fedoraproject.org> 3.0.1-1
- Upstream released 3.0.1

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-1
- Upstream released 3.0.0

* Sun Oct 12 2008 Remi Collet <rpms@famillecollet.com> 3.0.0-1.fc#.remi
- update to 3.0.0 
- update requires for php 5.2.0

