%global php php52
%global php_basever 5.2
%global _php5_mod_dir %{_libdir}/php/modules

Summary:        PHP Zend Optimizer
Name:           %{php}-zend-optimizer
Version:        3.3.9
#Release:        2.art
Release:        5%{?dist}
Epoch:		1
URL:            http://www.zend.com/en/products/guard/downloads
Packager:	Scott R. Shinn <scott@atomicrocketturtle.com>
Source0:        ZendOptimizer-%{version}-linux-glibc23-i386.tar.gz
Source1:	ZendOptimizer-%{version}-linux-glibc23-x86_64.tar.gz
License:        Commercial
Group:          Development/Languages
BuildRoot:      %{_tmppath}/%{name}-root
#Requires: 	php52 php52-devel

%description
PHP Zend Optimizer


%prep

%ifarch i386 i586 i686
%setup -T -b 0 -n ZendOptimizer-%{version}-linux-glibc23-i386
%endif

%ifarch x86_64
%setup -T -b 1 -n ZendOptimizer-%{version}-linux-glibc23-x86_64
%endif

%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} -m 755 %{buildroot}/%{_libdir}/php/zend/

%{__install} -m 644 LICENSE %{buildroot}/%{_libdir}/php/zend/
%{__install} -m 644 EULA-ZendOptimizer %{buildroot}/%{_libdir}/php/zend/
%{__install} -m 644 README-ZendOptimizer  %{buildroot}/%{_libdir}/php/zend/

%{__install} -m 755 data/4_3_x_comp/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-4.3.so
#%{__install} -m 755 data/4_3_x_comp/TS/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-4.3-TS.so

%{__install} -m 755 data/4_4_x_comp/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-4.4.so
#%{__install} -m 755 data/4_4_x_comp/TS/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-4.4-TS.so

%{__install} -m 755 data/5_0_x_comp/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.0.so
#%{__install} -m 755 data/5_0_x_comp/TS/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.0-TS.so

%{__install} -m 755 data/5_1_x_comp/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.1.so
#%{__install} -m 755 data/5_1_x_comp/TS/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.1-TS.so

%{__install} -m 755 data/5_2_x_comp/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.2.so
#%{__install} -m 755 data/5_2_x_comp/TS/ZendOptimizer.so %{buildroot}/%{_libdir}/php/zend/ZendOptimizer-5.2-TS.so



%pre
# remove ioncube loader from config
sed -i -e '/^zend_extension.*[Zz]end[Oo]ptimizer.*/d' /etc/php.ini
sed -i -e '/^zend_extension.*[Zz]end.*[Oo]ptimizer.*/d' /etc/php.ini
sed -i -e '/^zend_extension.*[Zz]end[Ee]xtension.*/d' /etc/php.ini
sed -i -e '/^zend_optimizer.*version/d' /etc/php.ini

%triggerin -- php 

if [ -f /usr/bin/php ]; then
  PHP="/usr/bin/php -q"
  PHP_VER=`echo "<?php echo phpversion(); ?>" | $PHP 2>/dev/null|cut -c1-3`
  #echo "PHP version is: $PHP_VER"   
  if [ "$PHP_VER" == "" ]; then
    PHP_VER="5.2"
  fi

  ARCH=`uname -m`
  PHP_EXT=/etc/php.d

#  if [ "$ARCH" == "x86_64" ]; then
#    echo "zend_extension=/usr/lib64/php/zend/ZendOptimizer-$PHP_VER.so" > $PHP_EXT/zendoptimizer.ini
#  else
#    echo "zend_extension=/usr/lib/php/zend/ZendOptimizer-$PHP_VER.so" > $PHP_EXT/zendoptimizer.ini
#  fi

%{__cat} >> %{buildroot}/etc/php.d/zendoptimizer.ini <<EOF
zend_extension=%{_php5_mod_dir}/ZendOptimizer-$PHP_VER.so
EOF

fi

# No, you don't really need an executible stack.
if [ -x /usr/bin/execstack ]; then
  /usr/bin/execstack -c  /usr/lib*/php/zend/ZendOptimizer*so >/dev/null 2>&1
fi


%postun 
# only if deinstall
[ 0$1 -le 0 ] || exit 0

# remove config file
if [ -f /etc/php.d/zend.ini ]; then
  rm -f /etc/php.d/zend.ini
fi



%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/php/zend/



%changelog
* Thu Apr 10 2014 Mustafa Ramadhan <mustafa@bigraf.com> - 3.3.9-5.mr
- remove requires to php and php-devel

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 3.3.9-4.mr
- change mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sun Aug 19 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 3.3.9-3.lx.el5
- Recompile for lxcenter

* Thu Jul 29 2010 Support <support@atomicorp.com> - 3.3.9-2
- Remove short tags in triggers

* Sat Oct 10 2009 Scott R. Shinn <scott@atomicrocketturtle.com> - 3.3.9-1
- Update to 3.3.9

* Mon Dec 15 2008 Scott R. Shinn <scott@atomicrocketturtle.com> - 3.3.3-2
- Fix for php trigger, only run if php exists. 

* Wed Jun 11 2008 Scott R. Shinn <scott@atomicrocketturtle.com> 3.3.3-1
- update to 3.3.3

* Wed Aug 29 2007 Scott R. Shinn <scott@atomicrocketturtle.com> 3.3.0-1
- initial build
