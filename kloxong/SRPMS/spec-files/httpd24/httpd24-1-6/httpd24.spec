%{!?scl:%global scl httpd24}
%if 0%{?scl_package:1}
%scl_package %scl
%else
%global scl_name %{scl}
%endif

%define use_system_apr 0

Summary:       Package that installs %scl
Name:          %scl_name
Version:       1
Release:       6%{?dist}
License:       GPLv2+

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
# Temporary work-around
BuildRequires: iso-codes

%if ! %{use_system_apr}
Requires: %{scl_prefix}apr
Requires: %{scl_prefix}apr-util
%endif
Requires: %{scl_prefix}httpd

%description
This is the main package for %scl Software Collection.

%package runtime
Summary:   Package that handles %scl Software Collection.
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:   Package shipping basic build configuration
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

# Not required for now
#export LIBRARY_PATH=%{_libdir}\${LIBRARY_PATH:+:\${LIBRARY_PATH}}
#export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

%install
mkdir -p %{buildroot}%{_scl_scripts}/root
install -m 644 enable  %{buildroot}%{_scl_scripts}/enable

%scl_install

%post runtime
# Simple copy of context from system root to DSC root.
# In case new version needs some additional rules or context definition,
# it needs to be solved.
# Unfortunately, semanage does not have -e option in RHEL-5, so we have to
# have its own policy for collection
%if 0%{?rhel} >= 6
    semanage fcontext -a -e / %{_scl_root} >/dev/null 2>&1 || :
    restorecon -R %{_scl_root} >/dev/null 2>&1 || :
%endif

%files

%files runtime
%defattr(-,root,root)
%scl_files

%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%changelog
* Fri Sep 20 2013 Jan Kaluza <jkaluza@redhat.com> - 1.6
- add prep section and cleanup spec file

* Fri Jul 26 2013 Jan Kaluza <jkaluza@redhat.com> - 1-5
- do not build httpd24 as noarch, fix export PATH

* Fri Jul 26 2013 Jan Kaluza <jkaluza@redhat.com> - 1-4
- add PKG_CONFIG_PATH to "enable" script

* Fri Apr 19 2013 Jan Kaluza <jkaluza@redhat.com> - 1-3
- handle selinux and manpath
- build with apr and apr-util from collection

* Tue Oct 02 2012 Jan Kaluza <jkaluza@redhat.com> - 1-2
- updated specfile according to latest guidelines
- require iso-codes

* Wed May 16 2012 Jan Kaluza <jkaluza@redhat.com> - 1-1
- initial packaging
