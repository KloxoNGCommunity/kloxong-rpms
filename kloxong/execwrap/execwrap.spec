Name:           execwrap
Version:        0.5
Release:        1.kng%{?dist}
#
License:        BSD
Group:          Productivity/Networking/Web/Utilities
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#
Url:            http://cyanite.org/execwrap/
Source:         http://cyanite.org/execwrap/execwrap-%{version}.tar.gz
#
Summary:        a super-user exec wrapper for the lighttpd web-server
%description
ExecWrap is a super-user exec wrapper for the lighttpd web-server, but it can
be used in any environment as long as arguments can be passed from the server
to its children via the environment.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fstack-protector"
gcc $CFLAGS -o execwrap execwrap.c

%install
install -D -m 0755 execwrap %{buildroot}%{_sbindir}/execwrap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/execwrap

%changelog
* Sun Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> 0.5-1
- first compile for Kloxo-MR
