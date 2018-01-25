%global php php53u
%global php_basever 5.3
%global _php5_mod_dir %{_libdir}/php/modules

Summary:        PHP Zend Guard
Name:           %{php}-zend-guard
Version:        5.5.0
#Release:        3.art
Release:        5%{?dist}
URL:            http://www.zend.com/en/products/guard/downloads
Packager:	Scott R. Shinn <scott@atomicrocketturtle.com>
Source0:        ZendGuardLoader-php-5.3-linux-glibc23-i386.tar.gz
Source1:	ZendGuardLoader-php-5.3-linux-glibc23-x86_64.tar.gz
License:        Commercial
Group:          Development/Languages
BuildRoot:      %{_tmppath}/%{name}-root
Requires: 	php php-devel

%description
Zend Guard is the industry leading solution for PHP IP protection.

Zend Guard provides independent software vendors and IT managers with the ability to safely distribute and manage the distribution of their PHP applications while protecting their source code.

Zend Optimizer is a free application that runs the files encoded using Zend Guard and enhances the overall performance of your PHP applications. 

%prep

%ifarch i386 i586 i686
%setup -T -b 0 -n ZendGuardLoader-php-5.3-linux-glibc23-i386
%endif

%ifarch x86_64
%setup -T -b 1 -n ZendGuardLoader-php-5.3-linux-glibc23-x86_64
%endif

%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} -m 755 %{buildroot}/etc/php.d/
%{__mkdir_p} -m 755 %{buildroot}/%{_libdir}/php/modules/

%{__install} -m 755 php-5.3.x/ZendGuardLoader.so %{buildroot}/%{_libdir}/php/modules/ZendGuardLoader.so

%triggerin -- php

ARCH=$(uname -m)
#if [ "$ARCH" == "x86_64" ]; then
#  echo "zend_extension=/usr/lib64/php/modules/ZendGuardLoader.so" > /etc/php.d/zendguard.ini
#else
#  echo "zend_extension=/usr/lib/php/modules/ZendGuardLoader.so" > /etc/php.d/zendguard.ini
#fi

%{__cat} >> %{buildroot}/etc/php.d/zendguard.ini <<EOF
zend_extension=%{_php5_mod_dir}/ZendGuardLoader.so
EOF

%post
# No, you don't really need an executable stack.
if [ -x /usr/bin/execstack ]; then
  /usr/bin/execstack -c  /usr/lib*/php/modules/ZendGuardLoader.so >/dev/null 2>&1
fi


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/php/modules/ZendGuardLoader.so



%changelog
* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 5.5.0-5.mr
- change mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Aug 19 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 5.5.0-4.lx.el5
- Recompile for lxcenter

* Tue Apr 26 2011 Support <support@atomicorp.com> - 5.5.0-1
- Initial release
