%define debug_package %{nil}
%global real_name httpd

%{?scl:%scl_package httpd24}

%define use_systemd 0
%define use_system_apr 0

# If we are using system APR and building as collection, we have to set
# apr prefix to _root_prefix
%if %{use_system_apr} && %{?scl:1}0
%define apr_prefix %_root_prefix
%else
%define apr_prefix %_prefix
%endif

%if %{?scl}0
%define _localstatedir %{_scl_root}/var
%define httpd_service %{scl_prefix}httpd.service
%define htcacheclean_service %{scl_prefix}htcacheclean.service
%define httpd_logrotate %{scl_prefix}httpd
%define httpd_init %{scl_prefix}httpd
%define htcacheclean_init %{scl_prefix}htcacheclean
%define httpd_logdir %{_root_localstatedir}/log/httpd24
%else
%define httpd_service httpd.service
%define htcacheclean_service htcacheclean.service
%define httpd_logrotate httpd
%define httpd_init httpd
%define htcacheclean_init htcacheclean
%define httpd_logdir %{_localstatedir}/log/httpd
%endif

%define contentdir %{_datadir}/httpd
%define docroot %{?scl:%_scl_root}/var/www
%define suexec_caller apache
%define mmn 20120211
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%define vstring Red Hat

# Drop automatic provides for module DSOs
%{?filter_setup:
%filter_provides_in %{_libdir}/httpd/modules/.*\.so$
%filter_setup
}

Summary: Apache HTTP Server
Name: %{?scl:%scl_prefix}%{real_name}
Version: 2.4.18
Release: 1%{?dist}
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/%{real_name}-%{version}.tar.bz2
Source1: index.html
Source3: httpd.logrotate
Source4: httpd.init
Source5: httpd.sysconf
Source6: httpd-ssl-pass-dialog
Source7: httpd.tmpfiles
Source8: httpd.service
Source10: %{real_name}.conf
Source11: 00-base.conf
Source12: 00-mpm.conf
Source13: 00-lua.conf
Source14: 01-cgi.conf
Source15: 00-dav.conf
Source16: 00-proxy.conf
Source17: 00-ssl.conf
Source18: 01-ldap.conf
Source19: 00-proxyhtml.conf
Source20: userdir.conf
Source21: ssl.conf
Source22: welcome.conf
Source23: manual.conf
Source25: 01-session.conf
Source26: action-graceful.sh
Source27: action-configtest.sh
Source28: 00-optional.conf
# Documentation
Source30: README.confd
Source40: htcacheclean.service
Source41: htcacheclean.sysconf
Source42: htcacheclean.init
# build/scripts patches
Patch1: httpd-2.4.1-apctl.patch
Patch2: httpd-2.4.3-apxs.patch
Patch3: httpd-2.4.1-deplibs.patch
Patch5: httpd-2.4.3-layout.patch
# Features/functional changes
Patch21: httpd-2.4.6-full-release.patch
Patch23: httpd-2.4.4-export.patch
Patch24: httpd-2.4.1-corelimit.patch
Patch25: httpd-2.4.1-selinux.patch
Patch26: httpd-2.4.4-r1337344+.patch
Patch27: httpd-2.4.2-icons.patch
Patch29: httpd-2.4.10-mod_systemd.patch
Patch30: httpd-2.4.4-cachehardmax.patch
Patch31: httpd-2.4.18-sslmultiproxy.patch
Patch34: httpd-2.4.9-socket-activation.patch

# Bug fixes
Patch55: httpd-2.4.4-malformed-host.patch
Patch56: httpd-2.4.4-mod_unique_id.patch
Patch60: httpd-2.4.6-r1556473.patch
Patch62: httpd-2.4.6-apachectl-status.patch
Patch63: httpd-2.4.6-ab-overflow.patch
Patch64: httpd-2.4.6-sigint.patch
License: ASL 2.0
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{real_name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, pkgconfig, findutils, xmlto
BuildRequires: zlib-devel, libselinux-devel, lua-devel
%if %{use_system_apr}
BuildRequires: apr-devel >= 1.4.0, apr-util-devel >= 1.2.0
%else
BuildRequires: %{?scl:%scl_prefix}apr-devel >= 1.4.0, %{?scl:%scl_prefix}apr-util-devel >= 1.2.0
%endif
BuildRequires: pcre-devel >= 5.0
Requires: /etc/mime.types, system-logos >= 7.92.1-1
Provides: %{?scl:%scl_prefix}mod_dav = %{version}-%{release}, %{?scl:%scl_prefix}httpd-suexec = %{version}-%{release}
Provides: %{?scl:%scl_prefix}httpd-mmn = %{mmn}, %{?scl:%scl_prefix}httpd-mmn = %{mmnisa}
Requires: %{?scl:%scl_prefix}httpd-tools = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
%if %{use_systemd}
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
%else
Requires(post): chkconfig
%endif
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python
%{?scl:Requires:%scl_runtime}

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
%if %{use_system_apr}
Requires: apr-devel, apr-util-devel
%else
Requires: %{?scl:%scl_prefix}apr-devel, %{?scl:%scl_prefix}apr-util-devel
%endif
Requires: pkgconfig
Requires: %{?scl:%scl_prefix}httpd = %{version}-%{release}
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server
Requires: %{?scl:%scl_prefix}httpd = %{version}-%{release}
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python
BuildArch: noarch

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.2/.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python

%description tools
The httpd-tools package contains tools which can be used with 
the Apache HTTP Server.

%package -n %{?scl:%scl_prefix}mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(post): openssl, /bin/cat
Requires(pre): %{?scl:%scl_prefix}httpd
Requires: %{?scl:%scl_prefix}httpd = 0:%{version}-%{release}, %{?scl:%scl_prefix}httpd-mmn = %{mmnisa}
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python

%description -n %{?scl:%scl_prefix}mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n %{?scl:%scl_prefix}mod_proxy_html
Group: System Environment/Daemons
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: %{?scl:%scl_prefix}httpd = 0:%{version}-%{release}, %{?scl:%scl_prefix}httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python
Epoch: 1

%description -n %{?scl:%scl_prefix}mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n %{?scl:%scl_prefix}mod_ldap
Group: System Environment/Daemons
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: %{?scl:%scl_prefix}httpd = 0:%{version}-%{release}, %{?scl:%scl_prefix}httpd-mmn = %{mmnisa}
%if %{use_system_apr}
Requires: apr-util-ldap
%else
Requires: %{?scl:%scl_prefix}apr-util-ldap
%endif
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python

%description -n %{?scl:%scl_prefix}mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n %{?scl:%scl_prefix}mod_session
Group: System Environment/Daemons
Summary: Session interface for the Apache HTTP Server
Requires: %{?scl:%scl_prefix}httpd = 0:%{version}-%{release}, %{?scl:%scl_prefix}httpd-mmn = %{mmnisa}
Requires(post):    policycoreutils
Requires(post):    policycoreutils-python

%description -n %{?scl:%scl_prefix}mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%prep
%if %{?scl}0
export LD_LIBRARY_PATH=%{_libdir}:$LD_LIBRARY_PATH
%endif
%setup -q -n %{real_name}-%{version}
%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs
%patch5 -p1 -b .layout

%patch21 -p1 -b .fullrelease
%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .r1337344+
%patch27 -p1 -b .icons
%if %{use_systemd}
%patch29 -p1 -b .systemd
%endif
%patch30 -p1 -b .cachehardmax
%patch31 -p1 -b .sslmultiproxy
%if %{use_systemd}
%patch34 -p1 -b .socketactivation
%endif

%patch55 -p1 -b .malformedhost
%patch56 -p1 -b .uniqueid
%patch60 -p1 -b .r1556473
%patch62 -p1 -b .apachectlstatus
%patch63 -p1 -b .aboverflow
%patch64 -p1 -b .sigint

# Patch in the vendor string and the release string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h
sed -i 's/@RELEASE@/%{release}/' server/core.c

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn}, MMN-ISA %{mmnisa} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

# Build the daemon
./configure \
 	--prefix=%{_sysconfdir}/httpd \
 	--exec-prefix=%{_prefix} \
 	--bindir=%{_bindir} \
 	--sbindir=%{_sbindir} \
 	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
        --enable-layout=Fedora \
        --with-installbuilddir=%{_libdir}/httpd/build \
        --enable-mpms-shared=all \
        --with-apr=%{apr_prefix} --with-apr-util=%{apr_prefix} \
	--enable-suexec --with-suexec \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{docroot} \
	--with-suexec-logfile=%{_root_localstatedir}/log/httpd/suexec.log \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=500 --with-suexec-gidmin=100 \
        --enable-pie \
        --with-pcre \
        --enable-mods-shared=all \
	--enable-ssl --with-ssl --disable-distcache \
	--enable-proxy \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi \
        --enable-authn-anon --enable-authn-alias \
        --disable-imagemap  \
	--localstatedir=%{_localstatedir}
	$*
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%if %{use_systemd}
# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 $RPM_SOURCE_DIR/httpd.service \
         $RPM_BUILD_ROOT%{_unitdir}/%{httpd_service}
install -p -m 644 $RPM_SOURCE_DIR/htcacheclean.service \
        $RPM_BUILD_ROOT%{_unitdir}/%{htcacheclean_service}

# Change the httpd.service paths
sed -i 's|\$sbindir|%{_sbindir}|' \
    $RPM_BUILD_ROOT/lib/systemd/system/%{httpd_service}
sed -i 's|\$sysconfdir|%{_sysconfdir}|' \
    $RPM_BUILD_ROOT/lib/systemd/system/%{httpd_service}
sed -i 's|\$localstatedir|%{_localstatedir}|' \
    $RPM_BUILD_ROOT/lib/systemd/system/%{httpd_service}

# Change the htcacheclean.service paths
sed -i 's|\$sbindir|%{_sbindir}|' \
    $RPM_BUILD_ROOT%{_unitdir}/%{htcacheclean_service}
sed -i 's|\$sysconfdir|%{_sysconfdir}|' \
    $RPM_BUILD_ROOT%{_unitdir}/%{htcacheclean_service}
sed -i 's|\$localstatedir|%{_localstatedir}|' \
    $RPM_BUILD_ROOT%{_unitdir}/%{htcacheclean_service}
sed -i 's|\$httpd_service|%{httpd_service}|' \
    $RPM_BUILD_ROOT%{_unitdir}/%{htcacheclean_service}
%else
# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 $RPM_SOURCE_DIR/httpd.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{httpd_init}
install -m755 $RPM_SOURCE_DIR/htcacheclean.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/%{htcacheclean_init}

# Change the httpd.init paths
sed -i 's|\$sbindir|%{_sbindir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{httpd_init}
sed -i 's|\$sysconfdir|%{_sysconfdir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{httpd_init}
sed -i 's|\$localstatedir|%{_localstatedir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{httpd_init}
sed -i 's|\$sclscripts|%{?_scl_scripts}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{httpd_init}

# Change the htcacheclean.init paths
sed -i 's|\$sbindir|%{_sbindir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{htcacheclean_init}
sed -i 's|\$sysconfdir|%{_sysconfdir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{htcacheclean_init}
sed -i 's|\$localstatedir|%{_localstatedir}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{htcacheclean_init}
sed -i 's|\$sclscripts|%{?_scl_scripts}|' \
    $RPM_BUILD_ROOT/etc/rc.d/init.d/%{htcacheclean_init}
%endif

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d \
      $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
for f in 00-base.conf 00-mpm.conf 00-lua.conf 01-cgi.conf 00-dav.conf \
         00-proxy.conf 00-ssl.conf 01-ldap.conf 00-proxyhtml.conf \
         01-ldap.conf 01-session.conf 00-optional.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

for f in welcome.conf ssl.conf manual.conf userdir.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
	sed -i 's|\$localstatedir|%{_localstatedir}|' \
		$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
	sed -i 's|\$libexecdir|%{_libexecdir}|' \
		$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
	sed -i 's|\$datadir|%{_datadir}|' \
		$RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

# Split-out extra config shipped as default in conf.d:
for f in autoindex; do
  mv docs/conf/extra/httpd-${f}.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/${f}.conf
done

# Extra config trimmed:
rm -v docs/conf/extra/httpd-{ssl,userdir}.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf
sed -i 's|\$sysconfdir|%{_sysconfdir}|' \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf
sed -i 's|\$localstatedir|%{_localstatedir}|' \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf


mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
for s in httpd htcacheclean; do
  install -m 644 -p $RPM_SOURCE_DIR/${s}.sysconf \
                    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/${s}
  sed -i 's|\$localstatedir|%{_localstatedir}|' \
      $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/${s}
done

# tmpfiles.d configuration
%if 0%{?fedora} > 16
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d 
install -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
   $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/httpd.conf
%endif

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dav \
         $RPM_BUILD_ROOT%{_localstatedir}/run/httpd/htcacheclean

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/ssl

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn

# When building as SCL, use different prefix for macros
%if %{?scl}0
mkdir -p $RPM_BUILD_ROOT%{_root_sysconfdir}/rpm/
cat > $RPM_BUILD_ROOT%{_root_sysconfdir}/rpm/macros.httpd24 <<EOF
%%_httpd24_mmn %{mmnisa}
%%_httpd24_apxs %{_bindir}/apxs
%%_httpd24_modconfdir %{_sysconfdir}/httpd/conf.modules.d
%%_httpd24_confdir %{_sysconfdir}/httpd/conf.d
%%_httpd24_contentdir %{contentdir}
%%_httpd24_moddir %{_libdir}/httpd/modules
EOF
%else
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_bindir}/apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
EOF
%endif

# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{contentdir}/noindex/index.html
rm -rf %{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s /usr/share/pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# symlinks for /etc/httpd
ln -s %{httpd_logdir} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/logs
ln -s %{_localstatedir}/run/httpd $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/run
ln -s %{_libdir}/httpd/modules $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/modules

# install http-ssl-pass-dialog
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}
install -m755 $RPM_SOURCE_DIR/httpd-ssl-pass-dialog \
	$RPM_BUILD_ROOT/%{_libexecdir}/httpd-ssl-pass-dialog

%if %{use_systemd}
# Install action scripts
mkdir -p $RPM_BUILD_ROOT/%{_root_libexecdir}/initscripts/legacy-actions/%{?scl:%scl_prefix}httpd
for f in graceful configtest; do
	install -p -m 755 $RPM_SOURCE_DIR/action-${f}.sh \
			$RPM_BUILD_ROOT/%{_root_libexecdir}/initscripts/legacy-actions/%{?scl:%scl_prefix}httpd/${f}
	sed -i 's|\$sbindir|%{_sbindir}|' \
		$RPM_BUILD_ROOT/%{_root_libexecdir}/initscripts/legacy-actions/%{?scl:%scl_prefix}httpd/${f}
done
%endif

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/%{httpd_logrotate}

# Change the httpd logrotate script paths
sed -i 's|\$httpd_service|%{name}|' \
    $RPM_BUILD_ROOT/etc/logrotate.d/%{httpd_logrotate}
sed -i 's|\$logdir|%{httpd_logdir}|' \
    $RPM_BUILD_ROOT/etc/logrotate.d/%{httpd_logrotate}

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|%{httpd_logdir}/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|%{httpd_logdir}/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|%{_localstatedir}/run/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,dbmmanage,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf/{original,extra}

# Make suexec a+rw so it can be stripped.  %%files lists real permissions
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/suexec

%pre
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%post
restorecon -R %{_scl_root} >/dev/null 2>&1 || :
%if %{use_systemd}
%systemd_post %{httpd_service} %{htcacheclean_service}
fi
%else
# Register the httpd service
/sbin/chkconfig --add %{?scl:%scl_prefix}httpd
/sbin/chkconfig --add %{?scl:%scl_prefix}htcacheclean
%endif

semanage fcontext -a -e /var/log/httpd %{httpd_logdir} >/dev/null 2>&1 || :
restorecon -R %{httpd_logdir} >/dev/null 2>&1 || :

semanage fcontext -a -e /etc/rc.d/init.d/httpd /etc/rc.d/init.d/httpd24-httpd >/dev/null 2>&1 || :
restorecon -R /etc/rc.d/init.d/httpd24-httpd >/dev/null 2>&1 || :

semanage fcontext -a -e /etc/rc.d/init.d/htcacheclean /etc/rc.d/init.d/httpd24-htcacheclean >/dev/null 2>&1 || :
restorecon -R /etc/rc.d/init.d/httpd24-httpd >/dev/null 2>&1 || :

%preun
%if %{use_systemd}
%systemd_preun %{httpd_service} %{htcacheclean_service}
%else
if [ $1 = 0 ]; then
	/sbin/service %{?scl:%scl_prefix}httpd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del %{?scl:%scl_prefix}httpd || :
	/sbin/service %{?scl:%scl_prefix}htcacheclean stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del %{?scl:%scl_prefix}htcacheclean || :
fi
%endif

%postun
%if %{use_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
/sbin/service %{?scl:%scl_prefix}httpd condrestart >/dev/null 2>&1 || :
%endif

%posttrans
%if %{use_systemd}
test -f %{_sysconfdir}/sysconfig/httpd-disable-posttrans || \
  /bin/systemctl try-restart %{httpd_service} %{htcacheclean_service} >/dev/null 2>&1 || :
%else
test -f %{_sysconfdir}/sysconfig/httpd-disable-posttrans || \
  /sbin/service %{?scl:%scl_prefix}httpd condrestart >/dev/null 2>&1 || :
test -f %{_sysconfdir}/sysconfig/httpd-disable-posttrans || \
  /sbin/service %{?scl:%scl_prefix}htcacheclean condrestart >/dev/null 2>&1 || :
%endif

%define sslcert %{_root_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_root_sysconfdir}/pki/tls/private/localhost.key

%post -n %{?scl:%scl_prefix}mod_ssl
restorecon -R %{_scl_root} >/dev/null 2>&1 || :
umask 077

if [ -f %{sslkey} -o -f %{sslcert} ]; then
   exit 0
fi

%{_root_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > %{sslkey} 2> /dev/null

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

cat << EOF | %{_root_bindir}/openssl req -new -key %{sslkey} \
         -x509 -sha256 -days 365 -set_serial $RANDOM -extensions v3_req \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF

%post tools
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%post manual
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%post -n %{?scl:%scl_prefix}mod_proxy_html
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%post -n %{?scl:%scl_prefix}mod_ldap
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%post -n %{?scl:%scl_prefix}mod_session
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%post devel
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) /etc/logrotate.d/%{httpd_logrotate}

%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.d/ssl.conf
%exclude %{_sysconfdir}/httpd/conf.d/manual.conf

%dir %{_sysconfdir}/httpd/conf.modules.d
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%config(noreplace) %{_sysconfdir}/sysconfig/httpd
%config(noreplace) %{_sysconfdir}/sysconfig/htcacheclean
%if 0%{?fedora} > 16
%config %{_sysconfdir}/tmpfiles.d/httpd.conf
%endif

%if %{use_systemd}
%dir %{_root_libexecdir}/initscripts/legacy-actions/%{?scl:%scl_prefix}httpd
%{_root_libexecdir}/initscripts/legacy-actions/%{?scl:%scl_prefix}httpd/*
%endif

%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%exclude %{_libdir}/httpd/modules/mod_session*.so

%dir %{contentdir}
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html

%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html

%attr(0710,root,apache) %dir %{_localstatedir}/run/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/run/httpd/htcacheclean
%attr(0700,root,root) %dir %{httpd_logdir}
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy

%{_mandir}/man8/*

%if %{use_systemd}
/lib/systemd/system/*.service
%else
/etc/rc.d/init.d/%{httpd_init}
/etc/rc.d/init.d/%{htcacheclean_init}
%endif

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files manual
%defattr(-,root,root)
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n %{?scl:%scl_prefix}mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_libexecdir}/httpd-ssl-pass-dialog

%files -n %{?scl:%scl_prefix}mod_proxy_html
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n %{?scl:%scl_prefix}mod_ldap
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n %{?scl:%scl_prefix}mod_session
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%if %{?scl}0
%{_root_sysconfdir}/rpm/macros.httpd24
%else
%{_sysconfdir}/rpm/macros.httpd
%endif

%changelog
* Fri Jan 15 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.18-1
- update to 2.4.18

* Thu Jul 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.4.16-1
- compile for Kloxo-MR
- disable debug
- scl as httpd24

* Thu Mar 05 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-4
- remove old sslsninotreq patch (#1199040)

* Thu Feb 26 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-3
- fix wrong path to document root in httpd.conf (#1196559)

* Mon Feb 02 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-2
- rebuild against new APR/APR-util (#1187646)

* Wed Jan 28 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-1
- update to version 2.4.12
- fix possible crash in SIGINT handling (#1184034)
- fix return value of httpd init script when lockfile exists, but
  httpd is not running (#1184441)

* Thu Jan 08 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-2
- enable mod_request by default for mod_auth_form
- move disabled-by-default modules from 00-base.conf to 00-optional.conf

* Fri Jan 02 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-1
- update to 2.4.10
- fix return value of htcacheclean init script when lockfile exists, but
  htcacheclean is not running (#1092067)
- use proper SELinux context for initscripts (#1093039)
- remove mod_proxy_html obsolete (#1174790)
- remove dbmmanage from httpd-tools (#1151375)
- add slash before root_libexecdir macro (#1149076)
- ab: fix integer overflow when printing stats with lot of requests (#1091650)
- mod_ssl: use 2048-bit RSA key with SHA-256 signature in dummy certificate (#1079925)

* Tue Nov 25 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-22
- Remove mod_proxy_fcgi fix for heap-based buffer overflow,
  httpd-2.4.6 is not affected (CVE-2014-3583)

* Tue Nov 25 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-21
- mod_proxy_wstunnel: Fix the use of SSL with the "wss:" scheme (#1141950)

* Mon Nov 24 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-20
- core: fix bypassing of mod_headers rules via chunked requests (CVE-2013-5704)
- mod_cache: fix NULL pointer dereference on empty Content-Type (CVE-2014-3581)
- mod_proxy_fcgi: fix heap-based buffer overflow (CVE-2014-3583)

* Fri Jul 18 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-19
- mod_cgid: add security fix for CVE-2014-0231
- mod_proxy: add security fix for CVE-2014-0117
- mod_deflate: add security fix for CVE-2014-0118
- mod_status: add security fix for CVE-2014-0226
- mod_cache: add secutiry fix for CVE-2013-4352

* Tue Mar 25 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-16
- apachectl status: return exit code 3 when httpd is not running (#1077334)

* Thu Mar 20 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-15
- mod_dav: add security fix for CVE-2013-6438 (#1077885)
- mod_log_config: add security fix for CVE-2014-0098 (#1077885)

* Wed Feb 05 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-14
- add htcacheclean init script (#1061009)
- mod_dav: fix locktoken handling (#1061010)
- mod_ssl: sanity-check use of "SSLCompression" (#1061011)
- mod_ssl: allow SSLEngine to override Listen-based default (#1061016)

* Wed Feb 05 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-13
- don't run posttrans restart if httpd-disable-posttrans exists (#1047097)

* Wed Jan 15 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-12
- call restorecon in post script (#1052933)

* Thu Jan  9 2014 Joe Orton <jorton@redhat.com> - 2.4.6-11
- mod_ssl: enable support at run-time for TLSv1.x with newer OpenSSL (#1035371)

* Tue Jan 07 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-10
- don't run posttrans restart if httpd-disable-posttrans exists (#1047097)
- mod_proxy: fix crash in brigade cleanup under high load (#1040448)
- remove "webserver" from provides (#1042877)

* Wed Nov 27 2013 Joe Orton <jorton@redhat.com> - 2.4.6-9
- rebuild

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com> - 2.4.6-7
- mod_ssl post script fixes
- use system /var/log for logging

* Tue Nov 12 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-6
- enable collections from service-environment file in init script

* Wed Sep 25 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-5
- do not use capabilities in RHEL6

* Mon Sep 23 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-4
- fix logrotate postrotate script

* Wed Sep 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-3
- rebuild for new APR/APR-util

* Tue Aug 13 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-2
- update to 2.4.6
- revert fix for dumping vhosts twice

* Mon Jul 29 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-7
- use expanded directory variables in macros, remove '-' from mmnisa

* Mon Jul 29 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- when building as SCL, use _httpd24_ prefix for macros

* Thu Jul 11 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-12
- mod_unique_id: replace use of hostname + pid with PRNG output (#976666)
- apxs: mention -p option in manpage

* Tue Jul  2 2013 Joe Orton <jorton@redhat.com> - 2.4.4-11
- add patch for aarch64 (Dennis Gilmore, #925558)

* Mon Jul  1 2013 Joe Orton <jorton@redhat.com> - 2.4.4-10
- remove duplicate apxs man page from httpd-tools

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.4.4-9
- remove zombie dbmmanage script

* Fri May 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-8
- return 400 Bad Request on malformed Host header

* Mon May 20 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- htpasswd/htdbm: fix hash generation bug (#956344)
- do not dump vhosts twice in httpd -S output (#928761)
- mod_cache: fix potential crash caused by uninitialized variable (#954109)

* Thu Apr 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-5
- execute systemctl reload as result of apachectl graceful
- mod_ssl: ignore SNI hints unless required by config
- mod_cache: forward-port CacheMaxExpire "hard" option
- mod_ssl: fall back on another module's proxy hook if mod_ssl proxy
  is not configured.

* Tue Apr 16 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-4
- fix service file to not send SIGTERM after ExecStop (#906321, #912288)

* Tue Mar 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-3
- protect MIMEMagicFile with IfModule (#893949)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-2
- really package mod_auth_form in mod_session (#915438)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-1
- update to 2.4.4
- fix duplicate ownership of mod_session config (#914901)

* Fri Feb 22 2013 Joe Orton <jorton@redhat.com> - 2.4.3-17
- add mod_session subpackage, move mod_auth_form there (#894500)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 2.4.3-15
- add systemd service for htcacheclean

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-14
- drop patch for r1344712

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-13
- filter mod_*.so auto-provides (thanks to rcollet)
- pull in syslog logging fix from upstream (r1344712)

* Fri Oct 26 2012 Joe Orton <jorton@redhat.com> - 2.4.3-12
- rebuild to pick up new apr-util-ldap

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 2.4.3-11
- rebuild

* Wed Oct  3 2012 Joe Orton <jorton@redhat.com> - 2.4.3-10
- pull upstream patch r1392850 in addition to r1387633

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9.1
- restore "ServerTokens Full-Release" support (#811714)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9
- define PLATFORM in os.h using vendor string

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-8
- use systemd script unconditionally (#850149)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-7
- use systemd scriptlets if available (#850149)
- don't run posttrans restart if /etc/sysconfig/httpd-disable-posttrans exists

* Mon Oct 01 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-6
- use systemctl from apachectl (#842736)

* Wed Sep 19 2012 Joe Orton <jorton@redhat.com> - 2.4.3-5
- fix some error log spam with graceful-stop (r1387633)
- minor mod_systemd tweaks

* Thu Sep 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-4
- use IncludeOptional for conf.d/*.conf inclusion

* Fri Sep 07 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-3
- adding mod_systemd to integrate with systemd better

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-2
- mod_ssl: add check for proxy keypair match (upstream r1374214)

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-1
- update to 2.4.3 (#849883)
- own the docroot (#848121)

* Mon Aug  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-23
- add mod_proxy fixes from upstream (r1366693, r1365604)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-21
- drop explicit version requirement on initscripts

* Thu Jul  5 2012 Joe Orton <jorton@redhat.com> - 2.4.2-20
- mod_ext_filter: fix error_log warnings

* Mon Jul  2 2012 Joe Orton <jorton@redhat.com> - 2.4.2-19
- support "configtest" and "graceful" as initscripts "legacy actions"

* Fri Jun  8 2012 Joe Orton <jorton@redhat.com> - 2.4.2-18
- avoid use of "core" GIF for a "core" directory (#168776)
- drop use of "syslog.target" in systemd unit file

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-17
- use _unitdir for systemd unit file
- use /run in unit file, ssl.conf

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-16
- mod_ssl: fix NPN patch merge

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-15
- move tmpfiles.d fragment into /usr/lib per new guidelines
- package /run/httpd not /var/run/httpd
- set runtimedir to /run/httpd likewise

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-14
- fix htdbm/htpasswd crash on crypt() failure (#818684)

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-13
- pull fix for NPN patch from upstream (r1345599)

* Thu May 31 2012 Joe Orton <jorton@redhat.com> - 2.4.2-12
- update suexec patch to use LOG_AUTHPRIV facility

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-11
- really fix autoindex.conf (thanks to remi@)

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-10
- fix autoindex.conf to allow symlink to poweredby.png

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-9
- suexec: use upstream version of patch for capability bit support

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-8
- suexec: use syslog rather than suexec.log, drop dac_override capability

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-7
- mod_ssl: add TLS NPN support (r1332643, #809599)

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-6
- add BR on APR >= 1.4.0

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-5
- use systemctl from logrotate (#221073)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-4
- pull from upstream:
  * use TLS close_notify alert for dummy_connection (r1326980+)
  * cleanup symbol exports (r1327036+)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3.2
- rebuild

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3
- really fix restart

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-2
- tweak default ssl.conf
- fix restart handling (#814645)
- use graceful restart by default

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.2-1
- update to 2.4.2

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-6
- fix macros

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-5
- add _httpd_moddir to macros

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-4
- fix symlink for poweredby.png
- fix manual.conf

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-3
- add mod_proxy_html subpackage (w/mod_proxy_html + mod_xml2enc)
- move mod_ldap, mod_authnz_ldap to mod_ldap subpackage

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-2
- clean docroot better
- ship proxy, ssl directories within /var/cache/httpd
- default config:
 * unrestricted access to (only) /var/www
 * remove (commented) Mutex, MaxRanges, ScriptSock
 * split autoindex config to conf.d/autoindex.conf
- ship additional example configs in docdir

* Tue Mar  6 2012 Joe Orton <jorton@redhat.com> - 2.4.1-1
- update to 2.4.1
- adopt upstream default httpd.conf (almost verbatim)
- split all LoadModules to conf.modules.d/*.conf
- include conf.d/*.conf at end of httpd.conf
- trim %%changelog

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-2
- fix build against PCRE 8.30

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-1
- update to 2.2.22

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.2.21-8
- Rebuild against PCRE 8.30

* Mon Jan 23 2012 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-7
- fix #783629 - start httpd after named

* Mon Jan 16 2012 Joe Orton <jorton@redhat.com> - 2.2.21-6
- complete conversion to systemd, drop init script (#770311)
- fix comments in /etc/sysconfig/httpd (#771024)
- enable PrivateTmp in service file (#781440)
- set LANG=C in /etc/sysconfig/httpd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-4
- fix #751591 - start httpd after remote-fs

* Mon Oct 24 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-3
- allow change state of BalancerMember in mod_proxy_balancer web interface

* Thu Sep 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.2.21-2
- Make mmn available as %%{_httpd_mmn}.
- Add .svgz to AddEncoding x-gzip example in httpd.conf.

* Tue Sep 13 2011 Joe Orton <jorton@redhat.com> - 2.2.21-1
- update to 2.2.21

* Mon Sep  5 2011 Joe Orton <jorton@redhat.com> - 2.2.20-1
- update to 2.2.20
- fix MPM stub man page generation

* Wed Aug 10 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-5
- fix #707917 - add httpd-ssl-pass-dialog to ask for SSL password using systemd

* Fri Jul 22 2011 Iain Arnell <iarnell@gmail.com> 1:2.2.19-4
- rebuild while rpm-4.9.1 is untagged to remove trailing slash in provided
  directory names

* Wed Jul 20 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-3
- fix #716621 - suexec now works without setuid bit

* Thu Jul 14 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-2
- fix #689091 - backported patch from 2.3 branch to support IPv6 in logresolve

* Fri Jul  1 2011 Joe Orton <jorton@redhat.com> - 2.2.19-1
- update to 2.2.19
- enable dbd, authn_dbd in default config

* Thu Apr 14 2011 Joe Orton <jorton@redhat.com> - 2.2.17-13
- fix path expansion in service files

* Tue Apr 12 2011 Joe Orton <jorton@redhat.com> - 2.2.17-12
- add systemd service files (#684175, thanks to Jóhann B. Guðmundsson)

* Wed Mar 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-11
- minor updates to httpd.conf
- drop old patches

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 2.2.17-10
- rebuild

* Wed Feb 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-9
- use arch-specific mmn

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Joe Orton <jorton@redhat.com> - 2.2.17-7
- generate dummy mod_ssl cert with CA:FALSE constraint (#667841)
- add man page stubs for httpd.event, httpd.worker
- drop distcache support
- add STOP_TIMEOUT support to init script

* Sat Jan  8 2011 Joe Orton <jorton@redhat.com> - 2.2.17-6
- update default SSLCipherSuite per upstream trunk

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-5
- fix requires (#667397)

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-4
- de-ghost /var/run/httpd

* Tue Jan  4 2011 Joe Orton <jorton@redhat.com> - 2.2.17-3
- add tmpfiles.d configuration, ghost /var/run/httpd (#656600)

* Sat Nov 20 2010 Joe Orton <jorton@redhat.com> - 2.2.17-2
- drop setuid bit, use capabilities for suexec binary

* Wed Oct 27 2010 Joe Orton <jorton@redhat.com> - 2.2.17-1
- update to 2.2.17

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 2.2.16-2
- link everything using -z relro and -z now

* Mon Jul 26 2010 Joe Orton <jorton@redhat.com> - 2.2.16-1
- update to 2.2.16

* Fri Jul  9 2010 Joe Orton <jorton@redhat.com> - 2.2.15-3
- default config tweaks:
 * harden httpd.conf w.r.t. .htaccess restriction (#591293)
 * load mod_substitute, mod_version by default
 * drop proxy_ajp.conf, load mod_proxy_ajp in httpd.conf
 * add commented list of shipped-but-unloaded modules
 * bump up worker defaults a little
 * drop KeepAliveTimeout to 5 secs per upstream
- fix LSB compliance in init script (#522074)
- bundle NOTICE in -tools
- use init script in logrotate postrotate to pick up PIDFILE
- drop some old Obsoletes/Conflicts

* Sun Apr 04 2010 Robert Scheck <robert@fedoraproject.org> - 2.2.15-1
- update to 2.2.15 (#572404, #579311)

