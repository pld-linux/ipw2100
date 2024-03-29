#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
%define         _mod_suffix     current
Summary:	Intel(R) PRO/Wireless 2100 Driver for Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 2100
Name:		ipw2100
Version:	1.2.2
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw2100/%{name}-%{version}.tgz
# Source0-md5:	ce77c41f2718aa8d70579351b475cd80
Patch0:		%{name}-firmware_path.patch
Patch1:		%{name}-2.6.24.patch
URL:		http://ipw2100.sourceforge.net/
BuildRequires:	ieee80211-devel
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	sed >= 4.0
%endif
BuildConflicts:	kernel-module-build < 2.6.20.2
Requires:	ipw2100-firmware = 1.3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2100 Network Connection mini PCI adapter.

%description -l pl.UTF-8
Ten projekt został stworzony przez Intela, aby umożliwić obsługę kart
mini PCI Intel PRO/Wireless 2100 Network Connection.

%package -n kernel%{_alt_kernel}-net-ipw2100
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 2100
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart Intel(R) PRO/Wireless 2100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	hotplug
Requires:	ipw2100-firmware = 1.3
#Requires:	kernel-net-hostap >= 0.1.3
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-net-ipw2100
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 2100.

%description -n kernel%{_alt_kernel}-net-ipw2100 -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart Intel(R)
PRO/Wireless 2100.

%prep
%setup -q
##%patch0 -p1
%patch1 -p1
sed -i 's:CONFIG_IPW2100_DEBUG=y::' Makefile

%build
%if %{with kernel}
# kernel module(s)
%build_kernel_modules -m ipw2100
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install ipwinfo $RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with kernel}
%install_kernel_modules -s %{_mod_suffix} -n %{name} -m ipw2100 -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-ipw2100
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-ipw2100
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README* LICENSE
%attr(755,root,root) %{_sbindir}/ipwinfo
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-net-ipw2100
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ipw2100-%{_mod_suffix}.ko*
%endif
