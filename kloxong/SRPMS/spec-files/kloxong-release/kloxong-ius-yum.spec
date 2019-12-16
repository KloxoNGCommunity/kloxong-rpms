%define repohost repo.kloxong.org
%define mirrorhost raw.githubusercontent.com/KloxoNGCommunity/KloxoNG-rpms/dev/kloxong/mirror
Summary: KloxoNG ius yum
Name: kloxong-ius-yum
Version: 0.1.1
Release: 1
License: AGPLV3
Group: System Environment/Base
URL: http://kloxong.org/

BuildArch: noarch
Packager: John Parnell Pierce <john@luckytanuki.com>
Vendor: Kloxo Next Generation Repository, http://%{repohost}/
#BuildRequires: redhat-rpm-config


%description
Provides yum file for ius for 24u install

%prep

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/yum.repos.d/

cat > %{buildroot}/%{_sysconfdir}/yum.repos.d/kloxongius.repo << _EOF_

[kloxong-ius]
name=KloxoNG - IUS Community Packages for EL \$releasever
baseurl=https://repo.ius.io/\$releasever/\$basearch
enabled=1
gpgcheck=0
exclude=mysql51* mysql56*

[kloxong-ius-archive]
name=KloxoNG - IUS Community Packages for EL \$releasever (archive)
baseurl=https://repo.ius.io/archive/\$releasever/\$basearch
enabled=1
gpgcheck=0
exclude=mysql51* mysql56*

[kloxong-ius-testing]
name=KloxoNG - IUS Community Packages for EL \$releasever (testing)
baseurl=https://repo.ius.io/testing/\$releasever/\$basearch
enabled=0
gpgcheck=0
exclude=mysql51* mysql56*



_EOF_


%{__cp} -f %{buildroot}/%{_sysconfdir}/yum.repos.d/kloxongius.repo %{_sysconfdir}/yum.repos.d/kloxongius.repo

%clean

%post

%files
%defattr(-, root, root, 0755)
%dir %{_sysconfdir}/yum.repos.d/
%config %{_sysconfdir}/yum.repos.d/kloxongius.repo

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- rebrand to Kloxo Next Generation
- change product name to kloxong
- add obsolete for kloxomr 
- change MRatWork to kloxong

* Mon Dec 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 0.0.1-1
- first release
