# yara-x-packaging

Multi-distribution packaging files and reproducible build environments for **VirusTotal [yara-x](https://github.com/VirusTotal/yara-x)** (`v1.23.0`).

Maintained by **Javier Ramírez** ([@javilinux](https://github.com/javilinux)).

---

## 📦 Distribution Status

| Distribution | Tracker / Request | Repository / Target | Status |
| :--- | :--- | :--- | :--- |
| **Fedora** | [RHBZ#2574288](https://bugzilla.redhat.com/show_bug.cgi?id=2574288) | Fedora Copr: `javilinux/yara-x` | Review Request (Package Review) |
| **openSUSE** | [SR#1397968](https://build.opensuse.org/request/show/1397968) | `openSUSE:Factory` / `security:forensics` | **Approved by openSUSE Review Team** (Staging) |
| **Debian** | [Bug#1154199 (ITP)](https://bugs.debian.org/1154199) | [Salsa DEP-14](https://salsa.debian.org/javilinux/yara-x) | Debian Security Tools Packaging Team |

---

## 🗂️ Repository Structure

- `fedora/`: Clean Fedora Rawhide `.spec` file conforming to Fedora Packaging Guidelines and `yr.1` man page.
- `opensuse/`: openSUSE Factory spec file, changes log, and OBS source service.
- `debian/`: Standard `debian/` packaging tree (control, rules, changelog, copyright).
- `containers/`: `Containerfile.fedora` for building Fedora packages reproducibly on any system (local, Oracle Cloud, GCP).

---

## 🚀 How to Reproduce / Build (Fedora)

### Using Podman / Docker

```bash
# 1. Build the builder container image
podman build -t fedora-yara-builder -f containers/Containerfile.fedora .

# 2. Download upstream tarball and vendor crates into a local workdir
mkdir -p build-dir && cd build-dir
cp ../fedora/* .
# Download yara-x-1.23.0.tar.xz and vendor.tar.zst here

# 3. Build SRPM and RPM inside container
podman run --rm -v $(pwd):/work:Z fedora-yara-builder bash -c "
  rpmbuild -ba /work/yara-x.spec --define '_sourcedir /work' --define '_rpmdir /work' --define '_srcrpmdir /work'
"
```
