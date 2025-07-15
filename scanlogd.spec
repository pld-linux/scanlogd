Summary:	Port scanning detection daemon
Summary(pl.UTF-8):	Deamon wykrywający skanowanie portów
Name:		scanlogd
Version:	2.2.6
Release:	1
License:	BSD
Group:		Networking/Admin
Source0:	http://www.openwall.com/scanlogd/%{name}-%{version}.tar.gz
# Source0-md5:	7b8187ea718ebe47f22805b921b909ab
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.openwall.com/scanlogd/
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Provides:	user(scanlogd)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scanlogd is a TCP port scan detection tool. It will hopefully let you
know if some guys are going to make an audit of your system security
;) But be aware that this tool can be easly fooled by person with some
knowledge.

%description -l pl.UTF-8
scanlogd służy do wykrywania skanowania portów TCP. Może dać ci znać,
że ktoś zamierza przetestować bezpieczeństwo twojego systemu ;). Bądź
jednak świadom, że ten program może zostać łatwo oszukany przez osobę
z odpowiednią wiedzą.

%prep
%setup -q
%patch -P0 -p1

%build
%{__make} linux \
	CC="%{__cc}" \
	OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d}

install scanlogd $RPM_BUILD_ROOT%{_sbindir}
install scanlogd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 78 -d /usr/share/empty -s /bin/false -c "scanlogd user" -g nobody scanlogd

%post
/sbin/chkconfig --add scanlogd
if [ -f /var/lock/subsys/scanlogd ]; then
	/etc/rc.d/init.d/scanlogd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/scanlogd start\" to start scanlog daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/scanlogd ]; then
		/etc/rc.d/init.d/scanlogd stop 1>&2
	fi
	/sbin/chkconfig --del scanlogd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove scanlogd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/scanlogd
%{_mandir}/man8/*
%attr(754,root,root) /etc/rc.d/init.d/scanlogd
