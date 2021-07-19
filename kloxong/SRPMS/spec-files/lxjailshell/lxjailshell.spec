%define defaultbuildroot /
AutoProv: no
%undefine __find_provides
AutoReq: no
%undefine __find_requires
# Do not try autogenerate prereq/conflicts/obsoletes and check files
%undefine __check_files
%undefine __find_prereq
%undefine __find_conflicts
%undefine __find_obsoletes
# Be sure buildpolicy set to do nothing
%define __spec_install_post %{nil}
# Something that need for rpm-4.1
%define _missing_doc_files_terminate_build 0
#dummy
#dummy

BuildArch:     x86_64
Name:          lxjailshell
Version:       3.2
Release:       34
License:       GPL 
Group:         Shell
Summary:       A shell to jail a user to his home directory


URL:           https://kloxong.org

Packager:      KloxoNG

Source0:       lxjailshell.bin

Provides:      lxjailshell = 3.2-34
Requires:      /bin/sh  
Requires:      /bin/sh  
Requires:      libc.so.6()(64bit)  
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)  
Requires:      libc.so.6(GLIBC_2.3)(64bit)  
Requires:      libc.so.6(GLIBC_2.3.4)(64bit)  
Requires:      libc.so.6(GLIBC_2.4)(64bit)  
Requires:      libdl.so.2()(64bit)  
Requires:      libdl.so.2(GLIBC_2.2.5)(64bit)  
Requires:      pcre >= 3.1
#Requires:      rpmlib(CompressedFileNames) <= 3.0.4-1
#Requires:      rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires:      rtld(GNU_HASH)  
Requires:      zlib  
#suggest
#enhance
%description
Jailshell is meant to restrict a user to his home directory.

%install
install -d $RPM_BUILD_ROOT/usr
install -d $RPM_BUILD_ROOT/usr/bin
install -m755 %{SOURCE0} $RPM_BUILD_ROOT/usr/bin/lxjailshell

%files
%attr(0755, root, root) "/usr/bin/lxjailshell"
%post -p /bin/sh
## read http://www.fedora.us/docs/spec.html next time :)
%preun -p /bin/sh
%changelog
* Sun Jul 18 2021 22:41 John Pierce <john@luckytanuki.com>  3.2-34
- repackage lxjailshell for copr build

* Thu Sep 30 2004 12:41 <jan@kneschke.de> 1.3.1
- upgraded to 1.3.1

* Tue Jun 29 2004 17:26 <jan@kneschke.de> 1.2.3
- rpmlint'ed the package
- added URL
- added (noreplace) to start-script
- change group to Networking/Daemon (like apache)

* Sun Feb 23 2003 15:04 <jan@kneschke.de>
- initial version

