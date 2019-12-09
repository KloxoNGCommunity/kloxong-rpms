# $Id$
# Authority: shuff
# Upstream: http://fastcgi.com/fastcgi-developers

%{?el4:%define _without_selinux 1}
%{?el3:%define _without_selinux 1}
%{?rh9:%define _without_selinux 1}
%{?rh7:%define _without_selinux 1}

%define debug_package %{nil}

%define real_name mod_fastcgi

Summary: Apache module that enables FastCGI
Name: mod24u_fastcgi
Version: 2.4.7.1
#Release: 2%{?dist}
Release: 1.kng%{?dist}
License: GPL/Apache License
Group: System Environment/Daemons
URL: http://www.fastcgi.com/

Source0: http://www.fastcgi.com/dist/%{real_name}-%{version}.tar.bz2
#Source1: mod_fastcgi.te
## need for apache 2.4.x
Patch1: mod_fastcgi_byte-compile-against-apache24.patch
Patch2: mod_fastcgi_byte-fix-cast-warning-in-fcgi_config.patch
Patch3: mod_fastcgi_byte-new-packet-type-byte_acc.patch
Patch4: mod_fastcgi_doc-misc-typo-fix.patch

Patch10: mod_fastcgi-2.4.7_processmanagerkill.patch
Patch20: mod_fastcgi-2.4.7-poll.patch

## MR -- combine all above patches
patch1000: mod_fastcgi-2.4.7_all.patch

BuildRoot: %{_tmppath}/%{real_name}-%{version}-%{release}-root

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: httpd-devel >= 2.4
Requires: httpd >= 2.4

#%{!?_without_selinux:BuildRequires: checkpolicy, policycoreutils}

%description
mod_fastcgi is a module for the Apache web server, that enables
FastCGI - a standards based protocol for communicating with
applications that generate dynamic content for web pages.

%prep
%setup -n %{real_name}-%{version}

#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1

#%patch10 -p1
#%patch20 -p1

#%patch1000 -p1

%build
cp Makefile.AP2 Makefile
%{__make} top_dir="%{_libdir}/httpd"

%{__cat} <<EOF >fastcgi.httpd
# WARNING: this is a kludge:
## The User/Group for httpd need to be set before we can load mod_fastcgi,
## but /etc/httpd/conf.d/fastcgi.conf on RHEL gets loaded before
## /etc/httpd/conf/httpd.conf, so we need to set them here :(
## mod_fcgid does not have this bug,
## but it does not handle child PHP processes appropriately per
## http://serverfault.com/questions/303535/a-single-php-fastcgi-process-blocks-all-other-php-requests/305093#305093

User apache
Group apache

LoadModule fastcgi_module modules/mod_fastcgi.so

# dir for IPC socket files
FastCgiIpcDir %{_localstatedir}/run/%{name}

# wrap all fastcgi script calls in suexec
FastCgiWrapper On

# global FastCgiConfig can be overridden by FastCgiServer options in vhost config
FastCgiConfig -idle-timeout 20 -maxClassProcesses 1

# sample PHP config
# see /usr/share/doc/mod_fastcgi-2.4.6 for php-wrapper script
# don't forget to disable mod_php in /etc/httpd/conf.d/php.conf!
#
# to enable privilege separation, add a "SuexecUserGroup" directive
# and chown the php-wrapper script and parent directory accordingly
# see also http://www.brandonturner.net/blog/2009/07/fastcgi_with_php_opcode_cache/
#
#FastCgiServer /var/www/cgi-bin/php-wrapper
#AddHandler php-fastcgi .php
#Action php-fastcgi /cgi-bin/php-wrapper
#AddType application/x-httpd-php .php
#DirectoryIndex index.php
#
#<Location /cgi-bin/php-wrapper>
#    Order Deny,Allow
#    Deny from All
#    Allow from env=REDIRECT_STATUS
#    Options ExecCGI
#    SetHandler fastcgi-script
#</Location>
EOF

%{__cat} <<WRAPPER >php-wrapper
#!/bin/sh

PHPRC="/etc/php.ini"
export PHPRC
PHP_FCGI_CHILDREN=4
export PHP_FCGI_CHILDREN
exec /usr/bin/php-cgi
WRAPPER

%{__chmod} +x php-wrapper

%install
%{__rm} -rf %{buildroot}
%{__make} install top_dir="%{_libdir}/httpd" DESTDIR="%{buildroot}"
%{__install} -Dp -m0644 fastcgi.httpd %{buildroot}%{_sysconfdir}/httpd/conf.d/fastcgi.conf

# make an IPC sockets dir
%{__install} -d -m770 %{buildroot}%{_localstatedir}/run/%{name}

### set up SELinux module if called for (adapted from munin.spec)
%if %{!?_without_selinux:1}
#checkmodule -M -m -o %{name}.mod %{SOURCE1}
#semodule_package -o %{name}.pp -m %{name}.mod
#%{__install} -D -d -m0755 %{buildroot}%{_datadir}/selinux/targeted/
#%{__install} %{name}.pp %{buildroot}%{_datadir}/selinux/targeted/
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if %{!?_without_selinux:1}
#semodule -i %{_datadir}/selinux/targeted/%{name}.pp
%endif

%files
%defattr(-, root, root, 0755)
#%doc CHANGES INSTALL* README docs/ php-wrapper
%doc CHANGES INSTALL*.md README.md docs/ php-wrapper
%config(noreplace) %{_sysconfdir}/httpd/conf.d/fastcgi.conf
%{_libdir}/httpd/modules/mod_fastcgi.so
%dir %attr(770,apache,apache) %{_localstatedir}/run/%{name}
#%attr(0644, root, root) %{_datadir}/selinux/targeted/*

%changelog
* Fri May 10 2019 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.7.1-1.mr
- update to 2.4.7.1

* Sat Feb 12 2016 Mustafa Ramadhan <mustafa@bigraf.com> 2.4.7-5.mr
- compile for Kloxo-MR (based on IUS repo)

* Tue May 12 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.7-4.mr
- add more patches
- remove mod_fastcgi_FD_SETSIZE-bug

* Mon Sep 29 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.7-3.mr
- disable mod_fastcgi_FD_SETSIZE-bug (because not work)
- enable mod_fastcgi_processmanagerkill.patch
- enable mod_fastcgi-2.4.2-poll.patch

* Tue Sep 16 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.7-2.mr
- add patch for process manager kill
- rename patch files name

* Mon Apr 28 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.7-1.mr
- update to 2.4.7 (aka SNAP-0910052141)
- add missing .deps and README files and re-zip with tar.bz2
- need apr-util 1.4.x

* Tue Apr 16 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.6-5.mr
- add patch for FD_SETSIZE bug

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.6-4.mr
- change mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Aug 19 2012 Mustafa Ramadhan (mustafa.ramadhan@lxcenter.org) 2.4.6-3.lx.el5
- Recompile for lxcenter

* Mon May 07 2012 William Horka <whorka@hmdc.harvard.edu> 2.4.6-2
- Add selinux module
- Remove unused log dir and add IPC socket dir
- Add FastCgiWrapper, FastCgiConfig, and FastCgiWrapper to fastcgi.conf
- Set httpd User and Group in fastcgi.conf so mod_fastcgi.so will load

* Fri Aug 26 2011 Philip Durbin <philipdurbin@gmail.com> 2.4.6-1
- Initial release, based on mod_suphp.spec
