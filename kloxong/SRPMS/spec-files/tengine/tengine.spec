%define debug_package %{nil}

%global  _hardened_build     1
%global  nginx_user          nginx
%global  nginx_group         %{nginx_user}
%global  nginx_home          %{_localstatedir}/lib/nginx
%global  nginx_home_tmp      %{nginx_home}/tmp
%global  nginx_confdir       %{_sysconfdir}/nginx
%global  nginx_datadir       %{_datadir}/nginx
%global  nginx_logdir        %{_localstatedir}/log/nginx
%global  nginx_webroot       %{nginx_datadir}/html

# gperftools exist only on selected arches
%ifarch %{ix86} x86_64 ppc ppc64 %{arm}
%global  with_gperftools     1
%endif

# AIO missing on some arches
%ifnarch aarch64
%global  with_aio   1
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:              tengine
Version:           2.2.3
Release:           1.kng%{?dist}

Summary:           A high performance web server and reverse proxy server
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://tengine.taobao.org/

Source0:           http://tengine.taobao.org/download/tengine-%{version}.tar.gz
Source10:          nginx.service
Source11:          nginx.logrotate
Source12:          nginx.conf
Source15:          nginx.init
Source16:          nginx.sysconfig
Source100:         index.html
Source102:         nginx-logo.png
Source103:         404.html
Source104:         50x.html
#Source105:         dso_tool.8

Patch0:            nginx-gcc7-compiler-fix.patch
Patch1:            nginx-glib-salt.patch

# Tengine is drop-in replacement for nginx
Conflicts:         nginx

BuildRequires:     GeoIP-devel
BuildRequires:     gd-devel
%if 0%{?with_gperftools}
BuildRequires:     gperftools-devel
%endif
BuildRequires:     libxslt-devel
BuildRequires:     openssl-devel
BuildRequires:     pcre-devel
BuildRequires:     perl-devel
BuildRequires:     perl(ExtUtils::Embed)
BuildRequires:     zlib-devel
BuildRequires:     luajit-devel

Requires:          nginx-filesystem
Requires:          luajit
Requires:          GeoIP
Requires:          gd
Requires:          openssl
Requires:          pcre
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):     nginx-filesystem
Provides:          webserver

%if 0%{?with_systemd}
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig, initscripts
Requires(postun):  initscripts
%endif

%description
Tengine is a web-server and a reverse proxy server based on Nginx project
supporting many advanced features which can be used as drop-in Nginx
replacement.

%package devel
Group:             Development/Libraries
Summary:           Development interfaces for the Tengine server
Requires:          tengine = %{version}-%{release}

%description devel
The tengine-devel package contains the dso_tool binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Tengine server.

%prep
%setup -q  -n %{name}-%{version}

%if %{?fedora}0 > 150 || %{?rhel}0 > 70
%patch0 -p1
%patch1 -p1
%endif

%build
# tengine does not utilize a standard configure script.  It has its own
# and the standard configure options cause the tengine configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
./configure \
    --prefix=%{nginx_datadir} \
    --includedir="%{_includedir}/nginx" \
    --dso-tool-path="%{_sbindir}" \
    --sbin-path=%{_sbindir}/nginx \
    --conf-path=%{nginx_confdir}/nginx.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --http-uwsgi-temp-path=%{nginx_home_tmp}/uwsgi \
    --http-scgi-temp-path=%{nginx_home_tmp}/scgi \
%if 0%{?with_systemd}
    --pid-path=/run/nginx.pid \
    --lock-path=/run/lock/subsys/nginx \
%else
    --pid-path=%{_localstatedir}/run/nginx.pid \
    --lock-path=%{_localstatedir}/lock/subsys/nginx \
%endif
    --user=%{nginx_user} \
    --group=%{nginx_group} \
%if 0%{?with_aio}
    --with-file-aio \
%endif
    --with-ipv6 \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module \
    --with-http_image_filter_module \
    --with-http_geoip_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_stub_status_module \
    --with-http_perl_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-pcre \
    --with-http_lua_module \
%if %{?fedora}0 > 150 || %{?rhel}0 > 70
    --with-luajit-inc="%{_includedir}/luajit-2.1" \
%else
    --with-luajit-inc="%{_includedir}/luajit-2.0" \
%endif  
    --with-luajit-lib="%{_libdir}" \
%if 0%{?with_gperftools}
    --with-google_perftools_module \
%endif
    --with-debug \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --with-ld-opt="$RPM_LD_FLAGS -Wl,-E" # so the perl module finds its symbols

make %{?_smp_mflags}


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;
%if 0%{?with_systemd}
install -p -D -m 0644 %{SOURCE10} \
    %{buildroot}%{_unitdir}/nginx.service
%else
install -p -D -m 0755 %{SOURCE15} \
    %{buildroot}%{_initrddir}/nginx
install -p -D -m 0644 %{SOURCE16} \
    %{buildroot}%{_sysconfdir}/sysconfig/nginx
%endif

install -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/default.d
install -p -d -m 0700 %{buildroot}%{nginx_home}
install -p -d -m 0700 %{buildroot}%{nginx_home_tmp}
install -p -d -m 0700 %{buildroot}%{nginx_logdir}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}

install -p -m 0644 %{SOURCE12} \
    %{buildroot}%{nginx_confdir}
install -p -m 0644 %{SOURCE100} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE102} \
    %{buildroot}%{nginx_webroot}
install -p -m 0644 %{SOURCE103} %{SOURCE104} \
    %{buildroot}%{nginx_webroot}
install -p -D -m 0644 %{_builddir}/tengine-%{version}/man/nginx.8 \
    %{buildroot}%{_mandir}/man8/nginx.8
#install -p -D -m 0644 %{SOURCE105} \
#    %{buildroot}%{_mandir}/man8/dso_tool.8
ln -s %{_mandir}/man8/nginx.8 %{buildroot}%{_mandir}/man8/tengine.8

chmod +x %{buildroot}%{_sbindir}/dso_tool
# Make sure these directories are not world readable, because otherwise,
# unprivileged users could read documents served by tengine and also
# read tengine logs.
chmod 700 %{buildroot}%{nginx_home}
chmod 700 %{buildroot}%{nginx_home_tmp}
chmod 700 %{buildroot}%{nginx_logdir}

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if 0%{?with_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_group} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_group} %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if 0%{?with_systemd}
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi

%postun
%if 0%{?with_systemd}
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%files
%doc LICENSE CHANGES README
%{nginx_datadir}/html/*
%{_sbindir}/nginx
%{_mandir}/man3/nginx.3pm*
%{_mandir}/man8/nginx.8*
%{_mandir}/man8/tengine.8*
%if 0%{?with_systemd}
%{_unitdir}/nginx.service
%else
%{_initrddir}/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%endif
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/nginx.conf
%config(noreplace) %{nginx_confdir}/nginx.conf.default
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/browsers
%config(noreplace) %{nginx_confdir}/module_stubs
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%dir %{perl_vendorarch}/auto/nginx
%{perl_vendorarch}/nginx.pm
%{perl_vendorarch}/auto/nginx/nginx.so
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}

%files devel
%{_includedir}/nginx
%{_sbindir}/dso_tool
#%{_mandir}/man8/dso_tool.8*

%changelog
* Fri Sep 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.1.2-1
- update to 2.1.2

* Fri Sep 04 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.1.1-1
- update to 2.1.1

* Sat May 16 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.1.0-3
- fix scripts pre/post/preun/postun (taken from nginx)

* Tue Apr 21 2015 Mustafa Ramadhan <mustafa@bigraf.com> - 2.1.0-2
- update to 2.1.0
- compile for Kloxo-MR
- add missing tengine.init
- use nginx.init/nginx.service instead tengine.init/tengine.service
- fix init register

* Tue Oct 21 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.3-2
- add dso_tool and tengine man-pages
- fix the "Powered by" message in 404 and 503 error pages
- change mode of tengine directories in install section

* Mon Oct 06 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.3-1
- initial packaging
