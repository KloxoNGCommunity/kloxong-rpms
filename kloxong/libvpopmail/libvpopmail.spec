%define debug_package %{nil}
%define vdir          /home/vpopmail

Name:		libvpopmail
Summary:	Vpopmail libraries for QMail Toaster
Version:	5.4.33
Release:	1.kng%{?dist}
License:	GPL
Group:		Networking/Other
URL:		http://www.inter7.com/%{name}

Source0:	http://downloads.sourceforge.net/project/vpopmail/vpopmail-stable/5.4.33/vpopmail-%{version}.tar.gz
#Source1:	vpopmail.mysql
#Source2:	vpopmail-secure-create-mysql
Patch0:	vpopmail-toaster-5.4.33.patch
Patch1:	vpopmail-build-no-root-5.4.33.patch
Patch2:	vpopmail-build-no-qmail-5.4.33.patch
Patch3:	libvpopmail-build-devel-5.4.33.patch

BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%description
Headers and libs for building packages which use vpopmail.

#-------------------------------------------------------------------------------
%package -n %{name}-devel
#-------------------------------------------------------------------------------

Summary:		vpopmail development headers and libs
Group:			System/Servers
Provides:		%{name}-static
#Obsoletes:		vpopmail-toaster
Obsoletes:		vpopmail-toaster-doc
Conflicts:      	set-toaster, checkpassword
BuildRequires:	automake
BuildRequires:	mysql-devel >= 5.0.22
#Requires:		mysql >= 5.0.22

%description -n %{name}-devel
Headers and libs for building packages which use vpopmail.

vpopmail has been patched as follows:
etc/     is in /etc/libvpopmail (only devel related files)
include/ is in /usr/include/libvpopmail
lib/     is in /usr/lib/libvpopmail
 
           libvpopmail 5.4.33
            Current settings
---------------------------------------

vpopmail directory = /home/vpopmail
               uid = 89
               gid = 89
     roaming users = OFF --disable-roaming-users   (default)
 password learning = OFF --disable-learn-passwords (default)
     md5 passwords = ON  --enable-md5-passwords    (default)
      file locking = ON  --enable-file-locking     (default)
vdelivermail fsync = OFF --disable-file-sync       (default)
     make seekable = ON  --enable-make-seekable    (default)
      clear passwd = ON  --enable-clear-passwd     (default)
 user dir hashing  = OFF --disable-users-big-dir
address extensions = ON  --enable-qmail-ext
          ip alias = OFF --disable-ip-alias-domains (default)
       auth module = mysql --enable-auth-module=mysql
 mysql replication = OFF --disable-mysql-replication (default)
       sql logging = OFF --disable-sql-logging       (default)
      mysql limits = OFF --disable-mysql-limits      (default)
      MySQL valias = ON  --enable-valias
          auth inc = -I/usr/include/mysql
          auth lib = -L/usr/lib64/mysql  -lmysqlclient -lz -lm
  system passwords = OFF --disable-passwd (default)
        pop syslog = log success and errors including passwords
                         --enable-logging=v
      auth logging = ON  --enable-auth-logging (default)
one domain per SQL table = --disable-many-domains

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------
%setup -q -n vpopmail-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
# We are using the devel patch here and configure properly
# Beware if This is enabled we need to do the same on libvpopmail and set proper paths on qmail-toaster
%patch3 -p1

#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------
autoreconf
%{__automake}
%{__autoconf}
./configure --prefix=%{vdir} \
	--enable-vpopuser=vpopmail \
	--enable-vpopgroup=vchkpw \
       --enable-libdir=%{_libdir}/mysql \
	--disable-roaming-users \
	--enable-tcprules-prog=/usr/bin/tcprules \
	--enable-tcpserver-file=/etc/tcprules.d/tcp.smtp \
	--enable-make-seekable \
	--enable-clear-passwd \
	--disable-users-big-dir \
	--enable-qmail-ext \
	--disable-ip-alias-domains \
	--enable-auth-module=mysql \
	--disable-passwd \
	--enable-logging=v \
	--enable-log-name=vpopmail \
	--disable-mysql-limits \
	--enable-valias \
	--enable-many-domains \
	--enable-non-root-build

# this is a hack. I don't know why cdb isn't being built with libvpopmail.a.
# cdb is from DJB, and should probably be removed at some point. Either that
# or it should be properly packaged as a library.
pushd cdb
  make
popd

make libvpopmail.a

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name} \
             %{buildroot}%{_includedir}/%{name} \
             %{buildroot}%{_libdir}/%{name} \
             %{buildroot}%{vdir}/etc \
             %{buildroot}%{vdir}/include \
             %{buildroot}%{vdir}/lib \
             %{buildroot}%{vdir}/doc

make DESTDIR=%{buildroot} install-data-local

# disabling the devel patch we dont need this library handling if we dont use development
# shubes 11/18/2013 - This is a hack.
# TODO: Need to get proper object library handling implemented
%ifarch x86_64
  sed -i 's|/usr/lib/|/usr/lib64/|' %{buildroot}%{_sysconfdir}/%{name}/lib_deps
 %endif

%{__cp} %{buildroot}%{vdir}/include/*  %{buildroot}%{_includedir}/%{name}/.
%{__cp} %{buildroot}%{vdir}/lib/*      %{buildroot}%{_libdir}/%{name}/.
#Cleaning up
%{__rm} -rf %{buildroot}%{vdir}


#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
%{__rm} -rf %{buildroot}

#-------------------------------------------------------------------------------
%files -n %{name}-devel
#-------------------------------------------------------------------------------
%defattr (-,vpopmail,vchkpw)
%attr(0755,vpopmail,vchkpw) %dir %{_sysconfdir}/%{name}
%attr(0755,vpopmail,vchkpw) %dir %{_includedir}/%{name}
%attr(0755,vpopmail,vchkpw) %dir %{_libdir}/%{name}
# this is not needed as well if we disable the development patch
%attr(0644,vpopmail,vchkpw)      %{_sysconfdir}/%{name}/*_deps

# this is for ouc case speficic but we will see if we need them
#%attr(0755,vpopmail,vchkpw) %dir %{vdir}
#%attr(0755,vpopmail,vchkpw) %dir %{vdir}/bin
#%attr(0755,vpopmail,vchkpw) %dir %{vdir}/etc
#%attr(0755,vpopmail,vchkpw) %dir %{vdir}/include
#%attr(0755,vpopmail,vchkpw) %dir %{vdir}/lib

%attr(0644,vpopmail,vchkpw)      %{_includedir}/%{name}/*
%attr(0644,vpopmail,vchkpw)      %{_libdir}/%{name}/*

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Tue Dec 17 2019 Dionysis Kladis <dkstiler@gmail.com> - 5.4.33-1.1.kng
- Compile for KloxoNG (need by dovecot-toaster compile)
- Moving seting permissions directives from  install section to files
- Enabling devel patch for libvpopmail and preparing the rest packages as well 

* Fri Jun 17 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 5.4.33-1
- Compile for Kloxo-MR (need by dovecot-toaster compile)
- set as 'enable-many-domains' instead 'disable-many-domains'
- Disable Obsolete for qmail-toaster

* Sat Dec 14 2013 Eric Shubert <eric@datamatters.us> 5.4.33-0.qt
- Created initial libvpopmail-devel package 
