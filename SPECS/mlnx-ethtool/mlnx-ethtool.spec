Name:		 mlnx-ethtool
Version:	 6.9
Release:	 2.2410068
Group:		 Utilities
Summary:	 Settings tool for Ethernet and other network devices
License:	 GPL
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux
URL:		 https://ftp.kernel.org/pub/software/network/ethtool/
Buildroot:	 /var/tmp/%{name}-%{version}-build
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/mlnx-ethtool-6.9.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  libmnl-devel

%description
This utility allows querying and changing settings such as speed,
port, auto-negotiation, PCI locations and checksum offload on many
network devices, especially Ethernet devices.

%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make


%install
make install DESTDIR=${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_sbindir}/ethtool
%{_mandir}/man8/ethtool.8*
%{_datadir}/bash-completion/completions/ethtool
%doc AUTHORS COPYING NEWS README


%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Moving to core from azlinux-ai-ml repo
* Thu Nov 07 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com>
- Initial version Azure Linux
