# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
%define soversion 1.1

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: compat-openssl11
Version: 1.1.1k
Release: 4%{?dist}
Epoch: 1
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: openssl-%{version}-hobbled.tar.xz

Source2: Makefile.certificate
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source12: ec_curve.c
Source13: ectest.c
# Build changes
Patch1: openssl-1.1.1-build.patch
Patch2: openssl-1.1.1-defaults.patch
Patch3: openssl-1.1.1-no-html.patch
Patch4: openssl-1.1.1-man-rename.patch

# Functionality changes
Patch31: openssl-1.1.1-conf-paths.patch
Patch32: openssl-1.1.1-version-add-engines.patch
Patch33: openssl-1.1.1-apps-dgst.patch
Patch36: openssl-1.1.1-no-brainpool.patch
Patch37: openssl-1.1.1-ec-curves.patch
Patch38: openssl-1.1.1-no-weak-verify.patch
Patch40: openssl-1.1.1-disable-ssl3.patch
Patch41: openssl-1.1.1-system-cipherlist.patch
Patch42: openssl-1.1.1-fips.patch
Patch45: openssl-1.1.1-weak-ciphers.patch
Patch46: openssl-1.1.1-seclevel.patch
Patch47: openssl-1.1.1-ts-sha256-default.patch
Patch48: openssl-1.1.1-fips-post-rand.patch
Patch49: openssl-1.1.1-evp-kdf.patch
Patch50: openssl-1.1.1-ssh-kdf.patch
Patch51: openssl-1.1.1-intel-cet.patch
Patch60: openssl-1.1.1-krb5-kdf.patch
Patch61: openssl-1.1.1-edk2-build.patch
Patch62: openssl-1.1.1-fips-curves.patch
Patch65: openssl-1.1.1-fips-drbg-selftest.patch
Patch66: openssl-1.1.1-fips-dh.patch
Patch67: openssl-1.1.1-kdf-selftest.patch
Patch69: openssl-1.1.1-alpn-cb.patch
Patch70: openssl-1.1.1-rewire-fips-drbg.patch
Patch71: openssl-1.1.1-new-config-file.patch
# This modifies code that was patched before, but removing all FIPS patches
# comes with a much greater risk of introducing regressions.
Patch72: openssl-1.1.1-disable-fips.patch

# Backported fixes including security fixes
Patch52: openssl-1.1.1-s390x-update.patch
Patch53: openssl-1.1.1-fips-crng-test.patch
Patch55: openssl-1.1.1-arm-update.patch
Patch56: openssl-1.1.1-s390x-ecc.patch
Patch73: openssl-1.1.1-cve-2022-0778.patch

License: OpenSSL and ASL 2.0
URL: http://www.openssl.org/
BuildRequires: make
BuildRequires: gcc
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/sbin/sysctl
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy)
Requires: coreutils, crypto-policies
Conflicts: openssl < 1:3.0, openssl-libs < 1:3.0

%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
from the 1.1.1 version and is provided for compatibility with previous
releases.

%prep
%setup -q -n openssl-%{version}

# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.


cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/

%patch1 -p1 -b .build   %{?_rawbuild}
%patch2 -p1 -b .defaults
%patch3 -p1 -b .no-html  %{?_rawbuild}
%patch4 -p1 -b .man-rename

%patch31 -p1 -b .conf-paths
%patch32 -p1 -b .version-add-engines
%patch33 -p1 -b .dgst
%patch36 -p1 -b .no-brainpool
%patch37 -p1 -b .curves
%patch38 -p1 -b .no-weak-verify
%patch40 -p1 -b .disable-ssl3
%patch41 -p1 -b .system-cipherlist
%patch42 -p1 -b .fips
%patch45 -p1 -b .weak-ciphers
%patch46 -p1 -b .seclevel
%patch47 -p1 -b .ts-sha256-default
%patch48 -p1 -b .fips-post-rand
%patch49 -p1 -b .evp-kdf
%patch50 -p1 -b .ssh-kdf
%patch51 -p1 -b .intel-cet
%patch52 -p1 -b .s390x-update
%patch53 -p1 -b .crng-test
%patch55 -p1 -b .arm-update
%patch56 -p1 -b .s390x-ecc
%patch60 -p1 -b .krb5-kdf
%patch61 -p1 -b .edk2-build
%patch62 -p1 -b .fips-curves
%patch65 -p1 -b .drbg-selftest
%patch66 -p1 -b .fips-dh
%patch67 -p1 -b .kdf-selftest
%patch69 -p1 -b .alpn-cb
%patch70 -p1 -b .rewire-fips-drbg
%patch71 -p1 -b .conf-new
%patch72 -p1 -b .disable-fips
%patch73 -p1 -b .cve-2022-0778

cp apps/openssl.cnf apps/openssl11.cnf

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux-generic64
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	--system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
	zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
	enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
	enable-weak-ssl-ciphers \
	no-mdc2 no-ec2m no-sm2 no-sm4 \
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

cp apps/openssl.cnf apps/openssl11.cnf

# Hack - either enable SCTP AUTH chunks in kernel or disable sctp for check
(sysctl net.sctp.addip_enable=1 && sysctl net.sctp.auth_enable=1) || \
(echo 'Failed to enable SCTP AUTH chunks, disabling SCTP for tests...' &&
 sed '/"zlib-dynamic" => "default",/a\ \ "sctp" => "default",' configdata.pm > configdata.pm.new && \
 touch -r configdata.pm configdata.pm.new && \
 mv -f configdata.pm.new configdata.pm)

# We must revert patch31 before tests otherwise they will fail
patch -p1 -R < %{PATCH31}

OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
make test

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
%make_install
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Delete static library
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a || :

# Delete non-devel man pages in the compat package
rm -rf $RPM_BUILD_ROOT%{_mandir}/man[157]*

# Delete configuration files
rm -rf  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/*

# Remove binaries
rm -rf $RPM_BUILD_ROOT/%{_bindir}

# Remove useless capi engine
rm -f $RPM_BUILD_ROOT/%{_libdir}/engines-1.1/capi.so

# Delete devel files
rm -rf $RPM_BUILD_ROOT%{_includedir}/openssl
rm -rf $RPM_BUILD_ROOT%{_mandir}/man3*
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig

# Install compat config file
install -m 644 apps/openssl11.cnf $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl11.cnf

%files
%license LICENSE
%doc FAQ NEWS README
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%config(noreplace) %{_sysconfdir}/pki/tls/openssl11.cnf

%dir %{_sysconfdir}/pki/tls
%attr(0644,root,root) %{_sysconfdir}/pki/tls/openssl11.cnf

%ldconfig_scriptlets

%changelog
* Mon May 30 2022 Clemens Lang <cllang@redhat.com> - 1:1.1.1k-4
- Fixes CVE-2022-0778 openssl: Infinite loop in BN_mod_sqrt() reachable when parsing certificates
  Resolves: rhbz#2063148
- Disable FIPS mode; it does not work and will not be certified
  Resolves: rhbz#2013669

* Tue Oct 05 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-3
- updates OPENSSL_CONF to openssl11.cnf.
- Related: rhbz#1947584, rhbz#2003123

* Mon Aug 16 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-2
- Remove support for building FIPS mode binaries for the
  compat libraries
- Ships openssl11.cnf as the configuration file.
- Resolves: rhbz#1993795
- Related: rhbz#1947584

* Thu Apr 08 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-1
- Repackage old openssl 1.1.1k package into compat-openssl11
  Resolves: bz#1947584
