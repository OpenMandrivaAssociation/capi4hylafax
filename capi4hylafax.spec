Summary:	CAPI 2.0 Interface to Hylafax
Name:		capi4hylafax
Version:	01.02.03
Release:	10
License:	GPL
Group:		Communications
URL:		https://capi4linux.thepenguin.de/
# http://mungo.homelinux.org/
# ftp://ftp.avm.de/tools/capi4hylafax.linux/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		capi4hylafax-01.02.03-mdk.diff
Patch1:		capi4hylafax-01.02.03-x86_64.diff
Patch2:		capi4hylafax-01.02.03-fix-str-fmt.patch
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	coreutils
BuildRequires:	isdn4k-utils-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
#Requires:	hylafax-server >= 4.1.5
Buildroot:	%{_tmppath}/%{name}-%{version}

%description
CAPI4HylaFAX provides the programs to make Hylafax compatibel to
the CAPI 2.0 interface used by AVM ISDN cards.

%prep

%setup -q
%patch0 -p1 -b .mdk
%patch1 -p0 -b .x86_64
%patch2 -p0 -b .str

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# fix dir perms
find . -type d | xargs chmod 755
    
# fix file perms
find . -type f | xargs chmod 644

%build
export WANT_AUTOCONF_2_5=1

%ifarch x86_64
export CXXFLAGS="%{optflags} -DC_PLATFORM_64"
%else
export CXXFLAGS="%{optflags}"
%endif

rm -f configure
libtoolize --copy --force && aclocal && autoconf && automake

%configure2_5x \
    --with-hylafax-spooldir=/var/spool/fax

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

install -d %{buildroot}/var/spool/fax/etc
install -d %{buildroot}%{_bindir}

install -m0644 config.faxCAPI %{buildroot}/var/spool/fax/etc/
install -m755 src/scripts/setupconffile %{buildroot}%{_bindir}/capi4hylafax-faxaddmodem

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog *.html config.faxCAPI fritz_pic.tif sample_*
%attr(0755,uucp,uucp) %dir /var/spool/fax/etc
%attr(0644,root,root) %config(noreplace) /var/spool/fax/etc/config.faxCAPI
%attr(0755,root,root) %{_bindir}/capi4hylafax-faxaddmodem
%attr(0755,root,root) %{_bindir}/c2faxrecv
%attr(0755,root,root) %{_bindir}/c2faxsend




%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 01.02.03-9mdv2011.0
+ Revision: 627769
- don't force the usage of automake1.7

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 01.02.03-8mdv2011.0
+ Revision: 616939
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 01.02.03-7mdv2010.0
+ Revision: 436940
- rebuild

* Sat Jan 24 2009 Funda Wang <fwang@mandriva.org> 01.02.03-6mdv2009.1
+ Revision: 333164
- fix str fmt

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 01.02.03-6mdv2009.0
+ Revision: 240485
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 01.02.03-4mdv2008.0
+ Revision: 69928
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago


* Fri Mar 02 2007 Oden Eriksson <oeriksson@mandriva.com> 01.02.03-3mdv2007.0
+ Revision: 131175
- Import capi4hylafax

* Fri Feb 03 2006 Oden Eriksson <oeriksson@mandriva.com> 01.02.03-3mdk
- rebuild

* Sat Jan 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 01.02.03-2mdk
- added P1 (amd64 fixes, debian)

* Tue Sep 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 01.02.03-1mdk
- initial mandrake package
- used parts from the spec file by Herbert U. Hübner
- added P0

