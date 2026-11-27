%bcond check 1

Name:           yara-x
Version:        1.25.0
Release:        %autorelease
Summary:        Malware identification and classification tool

SourceLicense:  BSD-3-Clause
# Output of %%{cargo_license_summary}:
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Unicode-3.0
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR MIT OR Apache-2.0
# BSD-3-Clause
# CC0-1.0 OR MIT-0 OR Apache-2.0
# MIT
# MIT OR Apache-2.0
# MIT OR Apache-2.0 OR BSD-1-Clause
# MIT OR Apache-2.0 OR LGPL-2.1-or-later
# MIT OR Zlib OR Apache-2.0
# Unlicense OR MIT
# Zlib
# Zlib OR Apache-2.0 OR MIT
License:        %{shrink:
    BSD-3-Clause AND
    Apache-2.0 AND
    Apache-2.0 WITH LLVM-exception AND
    MIT AND
    Unicode-3.0 AND
    Zlib AND
    (0BSD OR MIT OR Apache-2.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (BSD-2-Clause OR MIT OR Apache-2.0) AND
    (CC0-1.0 OR MIT-0 OR Apache-2.0) AND
    (MIT OR Apache-2.0 OR BSD-1-Clause) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    (MIT OR Zlib OR Apache-2.0) AND
    (Unlicense OR MIT)
}
# LICENSE.dependencies contains a full license breakdown

URL:            https://virustotal.github.io/yara-x/
Source0:        https://github.com/VirusTotal/yara-x/archive/v%{version}/%{name}-%{version}.tar.gz
# Bundled Rust crates are currently required because several core dependencies
# are not yet packaged in Fedora Rawhide (most notably wasmtime 48 + Cranelift
# workspace ~90 crates, walrus 0.28, ascii_tree, ihex, intaglio, md2, tinyzip,
# simd_cesu8) or require newer versions (rsa 0.10).
#
# To reproducibly generate %%{name}-%%{version}-vendor.tar.xz from Source0
# (stripping prebuilt foreign Windows/WASI binary blobs), run:
#   ./create-vendor-tarball.sh %%{version}
Source1:        %{name}-%{version}-vendor.tar.xz
Source2:        create-vendor-tarball.sh

# Restrict workspace members to crates needed for the yr CLI (excluding Python,
# JS/WASM, C-API, and LSP subprojects), drop disabled magic-module and criterion
# benchmarks, and remove foreign target-only dependencies.
Patch0:         yara-x-fix-metadata.patch

# Wasmtime's Cranelift JIT backend only supports 64-bit x86_64, aarch64, s390x, and riscv64
ExclusiveArch:  x86_64 aarch64 s390x riscv64

BuildRequires:  cargo-rpm-macros >= 25

%description
YARA-X is the Rust-based rewrite of the well-known YARA pattern-matching tool
aimed at helping malware researchers identify and classify malware samples.
With YARA-X you can create descriptions of malware families based on textual
or binary patterns contained in samples. Each description consists of a set of
strings and a Boolean expression which determines its logic.

This package provides the yr(1) command-line interface, shell completions, and
manual pages.

%prep
%autosetup -p1 -a1
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

mkdir -p completions
./target/rpm/yr completion bash > completions/yr.bash
./target/rpm/yr completion fish > completions/yr.fish
./target/rpm/yr completion zsh  > completions/_yr

%install
install -Dpm 0755 target/rpm/yr -t %{buildroot}%{_bindir}
install -Dpm 0644 cli/man/*.1 -t %{buildroot}%{_mandir}/man1
install -Dpm 0644 completions/yr.bash %{buildroot}%{bash_completions_dir}/yr
install -Dpm 0644 completions/yr.fish %{buildroot}%{fish_completions_dir}/yr.fish
install -Dpm 0644 completions/_yr %{buildroot}%{zsh_completions_dir}/_yr

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/yr
%{_mandir}/man1/yr*.1*
%{bash_completions_dir}/yr
%{fish_completions_dir}/yr.fish
%{zsh_completions_dir}/_yr

%changelog
%autochangelog
