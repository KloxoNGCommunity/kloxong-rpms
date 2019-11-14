%define kloxo /home/kloxo/httpd
%define productname kloxong-stats
%define packagename awstats

Name: %{productname}-%{packagename}
Summary: AWStats logfile analyzer
Version: 7.7
Release: 1.kng%{?dist}
License: GPL
URL: http://awstats.sourceforge.net/
Group: Applications/Internet
Source0: http://prdownloads.sourceforge.net/awstats/%{packagename}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
#Requires: webserver, php >= 5.2.17, php-mbstring
Provides: awstats
Obsoletes: kloxo-awstats, kloxomr-stats-awstats

%description
AWStats is a free powerful and featureful tool that generates advanced 
web, streaming, ftp or mail server statistics, graphically. This log 
analyzer works as a CGI or from command line and shows you all possible 
information your log contains, in few graphical web pages. It uses a 
partial information file to be able to process large log files, often 
and quickly. It can analyze log files from all major server tools like 
Apache log files (NCSA combined/XLF/ELF log format or common/CLF log 
format), WebStar, IIS (W3C log format) and a lot of other web, proxy, 
wap, streaming servers, mail servers and some ftp servers.

AWStats is a free software distributed under the GNU General Public 
License. You can have a look at this license chart to know what you 
can/can't do.

As AWStats works from the command line but also as a CGI, it can work 
with all web hosting providers which allow Perl, CGI and log access.

%prep
%setup -q -n %{packagename}-%{version}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p -m0755 $RPM_BUILD_ROOT%{kloxo}/%{packagename}
%{__cp} -rp * $RPM_BUILD_ROOT%{kloxo}/%{packagename}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(755,apache,apache,755)
%doc docs/*
%{kloxo}/%{packagename}

%changelog
* Mon Jan 29 2018 John Parnell Pierce <john@luckytanuki.com> 
- change product name to kloxong
- add obsolete for kloxomr 

* Sun May 01 2017 Mustafa Ramadhan <mustafa@bigraf.com> - 7.6-1.mr
- update to 7.6

* Thu Sep 22 2016 Mustafa Ramadhan <mustafa@bigraf.com> - 7.5-1.mr
- update to 7.5

* Fri Apr 19 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 7.1-4.mr
- change to apache:apache from lxlabs:lxlabs and 755 for files

* Sun Feb 17 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 7.1-3.mr
- rename rpm

* Tue Jan 22 2013 Mustafa Ramadhan <mustafa@bigraf.com> - 7.1-3.mr
- change email from mustafa.ramadhan@lxcenter.org to mustafa@bigraf.com

* Sat Dec 15 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 7.1-2.lx
- update to new version

* Sun Sep 23 2012 Mustafa Ramadhan <mustafa.ramadhan@lxcenter.org> - 7.0-2.lx
- update to new version

* Sun Mar 11 2012 Danny Terweij <contact@lxcenter.org> - 7.0-1
- Initial start of this SPEC
