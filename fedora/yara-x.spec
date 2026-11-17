Name:           yara-x
Version:        1.23.0
Release:        1%{?dist}
Summary:        A malware identification and classification tool
License:        BSD-3-Clause
URL:            https://virustotal.github.io/yara-x/
Source:         %{name}-%{version}.tar.xz
Source1:        vendor.tar.zst
Source2:        yr.1

BuildRequires:  cargo
BuildRequires:  rust >= 1.78.0
BuildRequires:  zstd

%description
YARA-X is the Rust-based rewrite of the well-known YARA tool aimed at
helping malware researchers identify and classify malware samples.
With YARA-X you can create descriptions of malware families based on
textual or binary patterns contained in samples. Each description
consists of a set of strings and a Boolean expression which determines
its logic.

This package provides the yr(1) CLI tool, bash completion, and manual page.

%prep
%autosetup -p 1 -a 1

%build
RUSTFLAGS="-C debuginfo=2 -C strip=none" cargo build %{?_smp_mflags} --release --offline

%install
install -Dm 0755 target/release/yr %{buildroot}%{_bindir}/yr
install -D -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/yr.1

# create and install bash-completion
install -d %{buildroot}%{_datadir}/bash-completion/completions/
./target/release/yr completion bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%check
cargo test %{?_smp_mflags} --offline --no-fail-fast

%files
%license LICENSE
%doc README.md
%{_bindir}/yr
%{_datadir}/bash-completion/completions/%{name}
%{_mandir}/man1/yr.1*

%changelog
* Tue Nov 17 2026 Javier Ramirez <javilinux@gmail.com> - 1.23.0-1
- Initial Fedora package review request
