
# TODO: rename spec to ipw2100.spec

# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
#
Summary:	Intel(R) PRO/Wireless 2100 Driver for Linux
Summary(pl):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2100
Name:		ipw2100
Version:	0.46_3
Release:	0.1
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2100/%{name}-%{version}.tgz
Source1:	http://hostap.epitest.fi/releases/hostap-driver-0.1.3.tar.gz
URL:		http://ipw2100.sourceforge.net/
Patch0:		%{name}_0.46_3-2.4.patch
Patch1:		%{name}-use-ieee802_11.h.patch
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-headers}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2100 Network Connection mini PCI adapter.

%description -l pl
Ten projekt zosta³ stworzony przez Intela, aby umo¿liwiæ obs³ugê kart
mini PCI Intel PRO/Wireless 2100 Network Connection.

%package -n kernel-net-ipw2100
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2100
Summary(pl):	Modu³ j±dra Linuksa dla kart Intel(R) PRO/Wireless 2100
Group:		Base/Kernel
PreReq:		kernel-net-hostap = 0.1.3
Requires:	ipw2100-firmware >= 1.1

%description -n kernel-net-ipw2100
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2100.

%description -n kernel-net-ipw2100 -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa dla kart Intel(R)
PRO/Wireless 2100.

%package -n kernel-smp-net-ipw2100
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 2100
Summary(pl):	Modu³ j±dra Linuksa SMP dla kart Intel(R) PRO/Wireless 2100
Group:		Base/Kernel
PreReq:		kernel-net-hostap = 0.1.3
Requires:	ipw2100-firmware >= 1.1

%description -n kernel-smp-net-ipw2100
This package contains Linux SMP kernel drivers for the Intel(R)
PRO/Wireless 2100.

%description -n kernel-smp-net-ipw2100 -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa SMP dla kart Intel(R)
PRO/Wireless 2100.

%prep
%setup -q -a1
%patch0 -p0
%patch1 -p1
perl -pi -e's,# CONFIG_IPW2100_LEGACY_FW_LOAD=y,CONFIG_IPW2100_LEGACY_FW_LOAD=y,' Makefile
perl -pi -e's,/sbin/depmod,:,g' Makefile

%build
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER


%if %{with kernel}
%{__make} \
	 KSRC=%{_kernelsrcdir}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install ipwinfo $RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2100
%{__make} install \
	KSRC=%{_kernelsrcdir} \
	KMISC=$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2100
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
%doc README* LICENSE ISSUES
%attr(755,root,root) %{_sbindir}/ipwinfo
%endif

%if %{with kernel}
%files -n kernel-net-ipw2100
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/ipw2100/*

#%files -n kernel-smp-net-ipw2100
#%defattr(644,root,root,755)
#/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/ipw2100/*
%endif
