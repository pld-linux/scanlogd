Summary:	Port scanning detection daemon
Summary(pl):	Deamon wykrywaj±cy skanowanie portów
Name:		scanlogd
Version:	2.2.5
Release:	1
License:	BSD
Group:		Networking/Admin
Source0:	http://www.openwall.com/scanlogd/%{name}-%{version}.tar.gz
# Source0-md5:	6b53ad390a51f0835e66b1efa84d710a
# Source0-size:	10809
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.openwall.com/scanlogd/
PreReq:		rc-scripts
BuildRequires:	rpmbuild(macros) >= 1.159
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

%description -l pl
scanlogd s³u¿y do wykrywania skanowania portów TCP. Mo¿e daæ ci znaæ,
¿e kto¶ zamierza przetestowaæ bezpieczeñstwo twojego systemu ;). B±d¼
jednak ¶wiadom, ¿e ten program mo¿e zostaæ ³atwo oszukany przez osobê
z odpowiedni± wiedz±.

%prep
%setup -q
%patch0 -p1

%build
%{__make} linux \
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
if [ -n "`/bin/id -u scanlogd 2>/dev/null`" ]; then
	if [ "`/bin/id -u scanlogd`" != "78" ]; then
		echo "Error: user scanlogd doesn't have uid=78. Correct this before installing scanlogd." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 78 -d /usr/share/empty -s /bin/false -c "scanlogd user" -g nobody scanlogd 1>&2
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
	%userremove scanlogd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/scanlogd
%{_mandir}/man8/*
%attr(754,root,root) /etc/rc.d/init.d/scanlogd
