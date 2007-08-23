Summary:	CAPI 2.0 Interface to Hylafax
Name:		capi4hylafax
Version:	01.02.03
Release:	%mkrel 3
License:	GPL
Group:		Communications
URL:		http://capi4linux.thepenguin.de/
# http://mungo.homelinux.org/
# ftp://ftp.avm.de/tools/capi4hylafax.linux/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		capi4hylafax-01.02.03-mdk.diff
Patch1:		capi4hylafax-01.02.03-x86_64.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
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
libtoolize --copy --force && aclocal-1.7 && autoconf && automake-1.7

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


