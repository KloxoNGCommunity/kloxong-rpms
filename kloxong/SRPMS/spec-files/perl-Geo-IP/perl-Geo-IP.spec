%{!?perl_vendorlib:  %define perl_vendorlib  %(eval "`%{__perl} -V:installvendorlib`" ; echo $installvendorlib)}
%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}
%{!?perl_version:    %define perl_version    %(eval "`%{__perl} -V:version`"          ; echo $version)}

%define modn   Geo-IP
%define modv   1.45
%define modp   %(echo %{modn} | cut -d'-' -f1)


Summary:       A Perl module to look up location and network information
Name:          perl-%{modn}
Version:       %{modv}
Release:       1%{?dist}%{?pext}
License:       GPL+ or Artistic
Group:         Development/Libraries
Source0:       http://search.cpan.org/CPAN/authors/id/M/MA/MAXMIND/%{modn}-%{modv}.tar.gz
URL:           http://search.cpan.org/dist/%{modn}/
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:        MaxMind, Inc.
Requires:      perl(:MODULE_COMPAT_%{perl_version})
BuildRequires: perl >= 5.6
BuildRequires: perl(Config)
BuildRequires: perl(Cwd)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Encode)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(FileHandle)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Spec)
BuildRequires: perl(Socket)
BuildRequires: perl(Socket6)
BuildRequires: perl(Test)
BuildRequires: perl(Test::More)
BuildRequires: GeoIP-devel >= 1.5.0


%description
Geo::IP is a Perl module to look up location and network information by IP
address using the MaxMind GeoIP Legacy binary databases. It can be used to
automatically select the geographically closest mirror, or to analyze web
server logs to determine the countries of visitors.


%prep
%setup -q -n %{modn}-%{modv}


%build
%{__perl} \
	Makefile.PL          \
	INSTALLDIRS="vendor" \
	OPTIMIZE="${RPM_OPT_FLAGS}"

%{__make} %{?_smp_mflags}


%check
%{__make} test


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_prefix}

%{__make} \
	PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} \
	pure_install

find ${RPM_BUILD_ROOT} -type f -name ".packlist"       -exec %{__rm} -f {} \;
find ${RPM_BUILD_ROOT} -type f -name "*.bs" -a -size 0 -exec %{__rm} -f {} \;
find ${RPM_BUILD_ROOT} -depth  -empty -type d          -exec rmdir      {} \;

%{__chmod} -R u+w ${RPM_BUILD_ROOT}/*


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc Changes INSTALL LICENSE README
%{perl_vendorarch}/auto/%{modp}
%{perl_vendorarch}/%{modp}
%{_mandir}/man3/*.3*


%changelog
* Sat Jan 10 2015 Peter Pramberger <peterpramb@member.fsf.org> - 1.45-1
- Initial build
