%kmdl ipw2100

Summary:	Intel® PRO/Wireless 2100 Driver for Linux.
Name:		ipw2100
Version:	0.46_3
Release:	0.1
License:        GPL v2
Group:          Base/Kernel
URL:		http://ipw2100.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/ipw2100/%{name}-%{version}.tgz
Source1:	http://hostap.epitest.fi/releases/hostap-driver-0.1.3.tar.gz
Patch0:		%{name}_0.46_3-2.4.patch
Patch1:		%{name}-use-ieee802_11.h.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%kmdl_parentdependencies

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 2100 Network Connection mini PCI adapter.

%package -n %kmdl_name
%kmdl_dependencies
Summary:	Kernel module for the Intel® PRO/Wireless 2100.
Group:          Base/Kernel
PreReq:		%{kmdl_nameof hostap} = 0.1.3
Requires:	ipw2100-firmware >= 1.1

%description -n %kmdl_name
This package contains kernel drivers for the Intel® PRO/Wireless 2100.

%kmdl_desc

%prep
%setup -q -a1
%patch0 -p0
%patch1 -p1
perl -pi -e's,# CONFIG_IPW2100_LEGACY_FW_LOAD=y,CONFIG_IPW2100_LEGACY_FW_LOAD=y,' Makefile
perl -pi -e's,/sbin/depmod,:,g' Makefile

%build

%if %{kmdl_userland}
%else

%kmdl_config
make KSRC=%{kmdl_kernelsrcdir}

%endif

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}

%if %{kmdl_userland}
install -d %{buildroot}%{_sbindir}
install -p ipwinfo %{buildroot}%{_sbindir}/
%else

mkdir -p %{buildroot}%{kmdl_moduledir}/drivers/net/wireless/ipw2100
make KSRC=%{kmdl_kernelsrcdir} KMISC=%{buildroot}%{kmdl_moduledir}/drivers/net/wireless/ipw2100 install

%endif


%clean
rm -rf %{buildroot}

%post -n %kmdl_name
%kmdl_install

%postun -n %kmdl_name
%kmdl_remove

%if %{kmdl_userland}

%files
%defattr(644,root,root,755)
%doc README* LICENSE ISSUES
%attr(755,root,root) %{_sbindir}/

%else

%files -n %kmdl_name
%defattr(644,root,root,755)
%{kmdl_moduledir}/drivers/net/wireless/ipw2100/*

%endif
