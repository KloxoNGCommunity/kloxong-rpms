%{!?scl:%global scl httpd24}

%{?scl:%scl_package mod_auth_kerb}

%if 0%{?scl:1}
%{!?_httpd24_apxs:       %{expand: %%global _httpd24_apxs       %%{_sbindir}/apxs}}
%{!?_httpd24_mmn:        %{expand: %%global _httpd24_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd24_confdir:    %{expand: %%global _httpd24_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd24_modconfdir: %{expand: %%global _httpd24_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd24_moddir:    %{expand: %%global _httpd24_moddir    %%{_libdir}/httpd/modules}}
%else
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}
%endif

Summary: Kerberos authentication module for HTTP
Name: %{?scl:%scl_prefix}mod_auth_kerb
Version: 5.4
Release: 30%{?dist}
# src/mod_auth_kerb.c is under 3-clause BSD, ASL 2.0 code is patched in (-s4u2proxy.patch)
# src/mit-internals.h contains MIT-licensed code.
License: BSD and MIT and ASL 2.0
Group: System Environment/Daemons
URL: http://modauthkerb.sourceforge.net/
Source0: http://downloads.sourceforge.net/modauthkerb/mod_auth_kerb-%{version}.tar.gz
Source1: auth_kerb.conf
Source2: LICENSE.ASL
Patch1: mod_auth_kerb-5.4-rcopshack.patch
Patch2: mod_auth_kerb-5.4-fixes.patch
Patch3: mod_auth_kerb-5.4-s4u2proxy.patch
Patch4: mod_auth_kerb-5.4-httpd24.patch
Patch5: mod_auth_kerb-5.4-delegation.patch
Patch6: mod_auth_kerb-5.4-cachedir.patch
Patch7: mod_auth_kerb-5.4-longuser.patch
Patch8: mod_auth_kerb-5.4-handle-continue.patch
BuildRequires: %{?scl:%scl_prefix}httpd-devel, krb5-devel
%if 0%{?scl:1}
Requires: %{?scl:%scl_prefix}httpd-mmn = %{_httpd24_mmn}
%else
Requires: httpd-mmn = %{_httpd_mmn}
%endif
Requires(pre): %{?scl:%scl_prefix}httpd
%{?scl:Requires:%scl_runtime}

# Suppres auto-provides for module DSO
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
mod_auth_kerb is module for the Apache HTTP Server designed to
provide Kerberos authentication over HTTP.  The module supports the
Negotiate authentication method, which performs full Kerberos
authentication based on ticket exchanges.

%prep
%setup -q -n mod_auth_kerb-%{version}
%patch1 -p1 -b .rcopshack
%patch2 -p1 -b .fixes
%patch3 -p1 -b .s4u2proxy
%patch4 -p1 -b .httpd24
%patch5 -p1 -b .delegation
%patch6 -p1 -b .cachedir
%patch7 -p1 -b .longuser
%patch8 -p1 -b .handlecontinue

%build
%if 0%{?scl:1}
export APXS=%{_httpd24_apxs}
%configure --without-krb4 --with-krb5=%{_root_prefix}
%else
export APXS=%{_httpd_apxs}
%configure --without-krb4 --with-krb5=%{_prefix}
%endif

make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?scl:1}
install -Dm 755 src/.libs/mod_auth_kerb.so \
        $RPM_BUILD_ROOT%{_httpd24_moddir}/mod_auth_kerb.so
%else
install -Dm 755 src/.libs/mod_auth_kerb.so \
        $RPM_BUILD_ROOT%{_httpd_moddir}/mod_auth_kerb.so
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?scl:1}
# httpd >= 2.4.x
sed -n /^LoadModule/p %{SOURCE1} > 10-auth_kerb.conf
sed '/LoadModule/d;/Location /,/Location>/s,^#,,' %{SOURCE1} > example.conf
%if 0%{?scl:1}
install -Dp -m 0644 10-auth_kerb.conf $RPM_BUILD_ROOT%{_httpd24_modconfdir}/10-auth_kerb.conf
%else
install -Dp -m 0644 10-auth_kerb.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-auth_kerb.conf
%endif
%else
# httpd <= 2.2.x
%if 0%{?scl:1}
install -Dp -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/auth_kerb.conf
%else
install -Dp -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd24_confdir}/auth_kerb.conf
%endif
%endif

%if 0%{?scl:0}
# Credentials cache
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
echo 'd %{_localstatedir}/run/httpd/krbcache 700 apache apache' \
     > $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd-krbcache.conf
%endif

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/run/httpd/krbcache

# Copy the license files here so we can include them in %doc
cp -p %{SOURCE2} .

%files
%doc README LICENSE LICENSE.ASL
%if 0%{?scl:1}
%config(noreplace) %{_httpd24_modconfdir}/*.conf
%{_httpd24_moddir}/*.so
%else
%config(noreplace) %{_httpd_modconfdir}/*.conf
%{_httpd_moddir}/*.so
%{_prefix}/lib/tmpfiles.d/httpd24-krbcache.conf
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%doc example.conf
%endif

%attr(0700,apache,apache) %dir %{_localstatedir}/run/httpd/krbcache

%changelog
* Wed Jan 28 2015 Jan Kaluza <jkaluza@redhat.com> - 5.4-30
- rebuild for rhscl-2.0

* Thu Jan 30 2014 Jan Kaluza <jkaluza@redhat.com> - 5.4-29
- fix krbcache directory and apply handle-continue patch (#1059562)

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com> - 5.4-26.2
- fix httpd-mmn dependency

* Tue Oct 29 2013 Jan Kaluza <jkaluza@redhat.com> - 5.4-25
- support for software collections

* Tue Jun 04 2013 Jan Kaluza <jkaluza@redhat.com> - 5.4-24
- don't truncate translated names with KrbLocalUserMapping

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Joe Orton <jorton@redhat.com> - 5.4-22
- clarify licensing; clean up spec file

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 5.4-21
- fix httpd_mmn stderr filter (thanks rcollet)

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 5.4-20
- hide stderr if finding httpd_mmn 
- package LICENSE
- filter DSO auto provides

* Wed Aug  8 2012 Joe Orton <jorton@redhat.com> - 5.4-19
- add Requires(pre) for httpd to ensure apache uid exists at install time

* Wed Aug  8 2012 Joe Orton <jorton@redhat.com> - 5.4-18
- move ccache to /run/httpd/ccache

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Joe Orton <jorton@redhat.com> - 5.4-16
- hard-code use of /run/user/apache for cache dir
- package /run/user/apache
- move tmpfiles drop-in to /usr/lib

* Wed Jun 13 2012 Joe Orton <jorton@redhat.com> - 5.4-15
- fix segfault in cache dir fix (#796430)

* Fri May 11 2012 Joe Orton <jorton@redhat.com> - 5.4-14
- add tmpfile drop-in for cred cache (#796430)
- really apply delegation fix

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 5.4-13
- add delegation fix (Ben Kahn, mgbowman, #687975)

* Tue Mar 27 2012 Joe Orton <jorton@redhat.com> - 5.4-12
- rebuild for httpd 2.4

* Fri Mar  9 2012 Joe Orton <jorton@redhat.com> - 5.4-11
- adapt for 2.4 API

* Thu Mar  1 2012 Rob Crittenden <rcritten@redhat.com> - 5.4-10
- Updated s4u2proxy patch to add missing braces around conditional.

* Tue Jan 31 2012 Rob Crittenden <rcritten@redhat.com> - 5.4-9
- Add support for Constrained Delegation/s4u2proxy (#767740)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Joe Orton <jorton@redhat.com> - 5.4-6
- fix build (thanks to Mike Bonnet, #599754)

* Fri Aug 07 2009 Parag <paragn@fedoraproject.org> 5.4-5
- Spec cleanup as suggested in review bug #226150

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Joe Orton <jorton@redhat.com> 5.4-2
- update to 5.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.3-7
- Autorebuild for GCC 4.3

* Tue Sep 25 2007 Joe Orton <jorton@redhat.com> 5.3-6
- fix configure invocation (#301181)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 5.3-5
- rebuild for fixed 32-bit APR

* Thu Aug 30 2007 Joe Orton <jorton@redhat.com> 5.3-4
- clarify License tag

* Wed Nov 29 2006 Joe Orton <jorton@redhat.com> 5.3-3
- fix r->user caching (Enrico Scholz, #214207)
- update to 5.3 (CVE-2006-5989, #215443)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 5.1-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Joe Orton <jorton@redhat.com> 5.1-2
- update to 5.1

* Thu Aug  3 2006 Joe Orton <jorton@redhat.com> 5.0-10
- fix segfault at startup (#201145)

* Thu Jul 20 2006 Joe Orton <jorton@redhat.com> 5.0-9
- add Russ Allbery's fix for disabling replay cache with krb15

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.0-8.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.0-8.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.0-8.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 5.0-8
- rebuild for httpd 2.2

* Wed Sep 21 2005 Joe Orton <jorton@redhat.com> 5.0-7
- fix build without /usr/sbin in $PATH (Roozbeh Pournader, #168212)

* Tue May 10 2005 Joe Orton <jorton@redhat.com> 5.0-6
- update to 5.0rc6
- don't force CC=gcc4

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 5.0-3
- fix build with GCC 4
- only add "auth_kerb_module" symbol to dynamic symbol table

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  8 2004 Joe Orton <jorton@redhat.com> 5.0-0.rc4.5
- remove static globals
- add SSLRequireSSL

* Mon Mar 29 2004 Joe Orton <jorton@redhat.com> 5.0-0.rc4.3
- support mutual authentication (Nalin Dahyabhai)
- once authentication returns COMPLETE, cache name for the duration
  of the connection

* Thu Mar 25 2004 Joe Orton <jorton@redhat.com> 5.0-0.rc4.2
- add example config file

* Wed Mar 24 2004 Joe Orton <jorton@redhat.com> 5.0-0.rc4.1
- update to mod_auth_kerb.c from HEAD to get workaround for
  "Request is a replay" errors

* Tue Mar 23 2004 Joe Orton <jorton@redhat.com> 
- Initial build.
