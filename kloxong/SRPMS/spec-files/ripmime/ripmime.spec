Name:           ripmime
Version:        1.4.0.9
Release:        2.kng%{?dist}
Summary:        Extract attachments out of a MIME encoded email packages

Group:          Applications/Internet
License:        BSD
URL:            http://www.pldaniels.com/ripmime/
Source0:        http://www.pldaniels.com/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
ripMIME extract attachments out of a MIME encoded email packages.

%prep
%setup -q

%build
make CFLAGS="%{optflags}" %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT

install -Dp -m 0755 $RPM_BUILD_DIR/%{name}-%{version}/%{name} %{buildroot}%{_bindir}/%{name}
install -Dp -m 0644 $RPM_BUILD_DIR/%{name}-%{version}/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/*
%doc CHANGELOG CONTRIBUTORS INSTALL LICENSE TODO README

%changelog

* Fri Jan 23 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.4.0.9-2
- Include CFLAGS in build process

* Fri Dec 26 2008 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.4.0.9-1
- Initial RPM release
