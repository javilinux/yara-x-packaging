#!/usr/bin/env bash
# Deterministically generate the clean vendor tarball for yara-x on Fedora.
# Removes prebuilt foreign binary blobs (.dll/.lib/.a/.exe/.wasm) prohibited by
# Fedora Packaging Guidelines while preserving Cargo.lock integrity.
set -euo pipefail

VERSION="${1:-1.23.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_TARBALL="${SCRIPT_DIR}/yara-x-${VERSION}.tar.gz"
PATCH_FILE="${SCRIPT_DIR}/yara-x-fix-metadata.patch"
OUT_TARBALL="${SCRIPT_DIR}/yara-x-${VERSION}-vendor.tar.xz"

if [ ! -f "${SRC_TARBALL}" ]; then
    echo "Downloading upstream tarball yara-x-${VERSION}.tar.gz..."
    curl -fL "https://github.com/VirusTotal/yara-x/archive/v${VERSION}/yara-x-${VERSION}.tar.gz" \
        -o "${SRC_TARBALL}"
fi

WORKDIR="$(mktemp -d)"
trap 'rm -rf "${WORKDIR}"' EXIT

tar -xzf "${SRC_TARBALL}" -C "${WORKDIR}"
pushd "${WORKDIR}/yara-x-${VERSION}" >/dev/null

patch -p1 < "${PATCH_FILE}"
cargo vendor --versioned-dirs vendor >/dev/null

# Strip prebuilt Windows/WASI binary archives and DLLs from vendored crates
# (e.g. winapi-*-pc-windows-gnu, windows_*, vcpkg test-data, wit-bindgen)
find vendor -type f \( \
    -name '*.a' -o \
    -name '*.lib' -o \
    -name '*.dll' -o \
    -name '*.exe' -o \
    -name '*.dylib' -o \
    -name '*.so' -o \
    -name '*.wasm' \
\) -delete

# Update cargo checksum manifests keeping "package" hash and remaining source checksums intact
python3 - << 'PYEOF'
import json, pathlib
for p in pathlib.Path("vendor").rglob(".cargo-checksum.json"):
    d = json.loads(p.read_text())
    d["files"] = {k: v for k, v in d.get("files", {}).items() if (p.parent / k).exists()}
    p.write_text(json.dumps(d, separators=(",", ":")))
PYEOF

XZ_OPT="-T0 -6" tar --sort=name --mtime="@0" --owner=0 --group=0 --numeric-owner \
    -cJf "${OUT_TARBALL}" vendor/

popd >/dev/null
echo "Created clean vendor tarball: ${OUT_TARBALL}"
