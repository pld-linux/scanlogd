Summary:	Port scanning detection daemon
Summary(pl):	Deamon wykrywaj±cy skanowanie portów
Name:		scanlogd
Version:	2.2
Release:	1
License:	BSD
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administracyjne
Source0:	http://www.openwall.com/scanlogd/%{name}-%{version}.tar.gz
Source1:	scanlogd.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.openwall.com/scanlogd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scanlogd is a TCP port scan detection tool. It will hopefully let you know
if some guys are going to make an audit of your system security ;) But be aware
that this tool can be easly fooled by person with some knowledge.

%description -l pl
scanlogd s³u¿y do wykrywania skanowania portów TCP. Mo¿e daæ ci znaæ, ¿e kto¶
zamierza przetestowaæ bezpieczeñstwo twojego systemu ;). B±d¼ jednak ¶wiadom,
¿e ten program mo¿e zostaæ ³atwo oszukany przez osobê z odpowiedni± wiedz±.

%prep
%setup  -q
%patch0 -p1

%build

%{__make} linux OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d}

install scanlogd $RPM_BUILD_ROOT%{_sbindir}
install scanlogd.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%pre
if [ -z "`id -u scanlogd 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 78 -d /dev/null -s /bin/false -c "scanlogd user" -g nobody scanlogd 1>&2
fi

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
	/usr/sbin/userdel scanlogd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/scanlogd
%{_mandir}/man8/*
%attr(750,root,root) /etc/rc.d/init.d/scanlogd
