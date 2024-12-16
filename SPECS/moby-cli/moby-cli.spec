%define commit_hash 293681613032e6d1a39cc88115847d3984195c24
%define OUR_GOPATH  %{_topdir}/.gopath
Summary:        The open-source application container engine client.
Name:           moby-cli
Version:        24.0.9
<<<<<<< HEAD
Release:        4%{?dist}
=======
Release:        6%{?dist}
>>>>>>> 8ba100af4 (Patch CVE-2024-24786 in moby-cli (#11320))
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Tools/Container
URL:            https://github.com/docker/cli
Source0:        https://github.com/docker/cli/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-govendor-v1.tar.gz
Patch0:         disable_manpage_vendor.patch
Patch1:         CVE-2023-45288.patch
<<<<<<< HEAD
=======
Patch2:         CVE-2024-36623.patch
Patch3:         CVE-2024-24786.patch
>>>>>>> 8ba100af4 (Patch CVE-2024-24786 in moby-cli (#11320))
BuildRequires:  git
BuildRequires:  go-md2man
BuildRequires:  golang
BuildRequires:  make
Requires:       /bin/sh
Requires:       tar
Requires:       xz

%description
%{summary}

%prep
%autosetup -p1 -n cli-%{version}
%setup -q -n cli-%{version} -T -D -a 1

mkdir -p %{OUR_GOPATH}/src/github.com/docker
ln -sfT %{_builddir}/cli-%{version} %{OUR_GOPATH}/src/github.com/docker/cli

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=off
export DISABLE_WARN_OUTSIDE_CONTAINER=1
export GO111MODULE=off
export GOGC=off
export CGO_ENABLED=1

make \
    LDFLAGS='' \
    VERSION=%{version} \
    GITCOMMIT=%{commit_hash} \
    dynbinary

# Generating man pages.
mkdir -p ./github.com/docker
ln -sfT %{_builddir}/cli-%{version} ./github.com/docker/cli
make manpages

%install
mkdir -p %{buildroot}/%{_bindir}
install -p -m 755 build/docker %{buildroot}%{_bindir}/docker

install -dp %{buildroot}%{_mandir}/man{1,5,8}
install -p -m 644 man/man1/*.1 %{buildroot}%{_mandir}/man1
install -p -m 644 man/man5/*.5 %{buildroot}%{_mandir}/man5
install -p -m 644 man/man8/*.8 %{buildroot}%{_mandir}/man8

install -d %{buildroot}%{_datadir}/bash-completion/completions
install -d %{buildroot}%{_datadir}/zsh/vendor-completions
install -d %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/docker
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/vendor-completions/_docker
install -p -m 644 contrib/completion/fish/docker.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/docker.fish

%files
%license NOTICE LICENSE
%{_bindir}/docker
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_datadir}/bash-completion/completions/docker
%{_datadir}/zsh/vendor-completions/_docker
%{_datadir}/fish/vendor_completions.d/docker.fish

%changelog
<<<<<<< HEAD
=======
* Fri Dec 13 2024 Suresh Thelkar <sthelkar@microsoft.com> - 24.0.9-6
- Patch CVE-2024-24786

* Tue Dec 10 2024 Sudipta Pandit <sudpandit@microsoft.com> - 24.0.9-5
- Add patch for CVE-2024-36623

>>>>>>> 8ba100af4 (Patch CVE-2024-24786 in moby-cli (#11320))
* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.0.9-4
- Bump release to rebuild with go 1.22.7

* Thu Aug 22 2024 Sumedh Sharma <sumsharma@microsoft.com> - 24.0.9-3
- Add patch to resolve CVE-2023-45288

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.0.9-2
- Bump release to rebuild with go 1.21.11

* Mon Mar 25 2024 Muhammad Falak <mwani@microsoft.com> - 24.0.9-1
- Bump version to 24.X
- Drop un-needed patches
- Add vendor tarball for new deps in make manpages

* Thu Feb 08 2024 Muhammad Falak <mwani@microsoft.com> - 20.10.27-5
- Bump release to rebuild with go 1.21.6

* Mon Feb 05 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.27-4
- Patch CVE-2021-44716

* Fri Feb 02 2024 Tobias Brick <tobiasb@microsoft.com> - 20.10.27-3
- Patch CVE-2022-21698

* Tue Jan 9 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 20.10.27-2
- Patch CVE-2023-48795

* Fri Dec 15 2023 Rohit Rawat <rohitrawat@microsoft.com> - 20.10.27-1
- Bump version to to match with moby-engine

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.25-3
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 20.10.25-2
- Bump release to rebuild with updated version of Go.

* Thu Aug 17 2023 Muhammad Falak <mwani@microsoft.com> - 20.10.25-1
- Bump version to 20.10.25

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-2
- Bump release to rebuild with go 1.19.10

* Fri Apr 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-1
- Auto-upgrade to 20.10.24 - none

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.12-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.12-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.12-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.12-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.12-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 20.10.12-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 20.10.12-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 20.10.12-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 20.10.12-2
- Bump release to rebuild with golang 1.18.3

* Thu Feb 3 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.12-1
- Update to version 20.10.12
- Use code from upstream instead of Azure fork.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 19.03.15+azure-2
- Increment release to force republishing using golang 1.15.13.

* Thu Apr 15 2021 Andrew Phelps <anphel@microsoft.com> 19.03.15+azure-1
- Update to version 19.03.15+azure
- Rename 'md2man' to 'go-md2man' in md2man-all.sh

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-2
- Increment release to force republishing using golang 1.15.

* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-1
- Update to version 19.03.11+azure

* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 3.0.12~rc.1+azure-5
- Remove reliance on existing GOPATH environment variable.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.0.12~rc.1+azure-4
- Added %%license line automatically

* Tue May 05 2020 Eric Li <eli@microsoft.com> 3.0.12~rc.1+azure-3
- Add #Source0:, update URL:, and license verified

* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.12~rc.1+azure-2
- Renaming go to golang

* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 3.0.12~rc.1+azure-1
- Initial CBL-Mariner import from Azure.

* Mon Jan 27 2020 Brian Goffs <brgoff@microsoft.com>
- Use dynamic linking and issue build commands from rpm spec

* Tue Aug 7 2018 Robledo Pontes <rafilho@microsoft.com>
- Adding to moby build tools.

* Mon Mar 12 2018 Xing Wu <xingwu@microsoft.com>
- First draft
