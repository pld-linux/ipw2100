#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Intel(R) PRO/Wireless 2100 Driver for Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2100
Name:		ipw2100
Version:	1.2.1
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2100/%{name}-%{version}.tgz
# Source0-md5:	9db50b836c63dc3a7e56653d2009717a
Patch0:		%{name}-firmware_path.patch
URL:		http://ipw2100.sourceforge.net/
BuildRequires:	ieee80211-devel
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	sed >= 4.0
%endif
BuildConflicts:	kernel-module-build < 2.6.0
Requires:	ipw2100-firmware = 1.3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2100 Network Connection mini PCI adapter.

%description -l pl.UTF-8
Ten projekt został stworzony przez Intela, aby umożliwić obsługę kart
mini PCI Intel PRO/Wireless 2100 Network Connection.

%package -n kernel-net-ipw2100
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2100
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart Intel(R) PRO/Wireless 2100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2100-firmware = 1.3
#Requires:	kernel-net-hostap >= 0.1.3
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-ipw2100
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2100.

%description -n kernel-net-ipw2100 -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart Intel(R)
PRO/Wireless 2100.

%package -n kernel-smp-net-ipw2100
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 2100
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP dla kart Intel(R) PRO/Wireless 2100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2100-firmware = 1.3
#Requires:	kernel-net-hostap >= 0.1.3
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-ipw2100
This package contains Linux SMP kernel drivers for the Intel(R)
PRO/Wireless 2100.

%description -n kernel-smp-net-ipw2100 -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa SMP dla kart Intel(R)
PRO/Wireless 2100.

%prep
%setup -q
##%patch0 -p1
sed -i 's:CONFIG_IPW2100_DEBUG=y::' Makefile

%build
%if %{with kernel}
# kernel module(s)
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	export IEEE80211_INC=%{_kernelsrcdir}/include
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv *.ko built/$cfg
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install ipwinfo $RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with kernel}
cd built
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
%if %{with smp} && %{with dist_kernel}
install smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-ipw2100
%depmod %{_kernel_ver}

%postun	-n kernel-net-ipw2100
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-ipw2100
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-net-ipw2100
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README* LICENSE
%attr(755,root,root) %{_sbindir}/ipwinfo
%endif

%if %{with kernel}
%files -n kernel-net-ipw2100
%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ieee80211*.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2100.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-ipw2100
%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ieee80211*.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ipw2100.ko*
%endif
%endif
