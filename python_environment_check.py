import sys
from packaging.version import Version


# -------------------------------
# Python version check
# -------------------------------
if Version(sys.version.split()[0]) < Version("3.8"):
    print(
        "[FAIL] We recommend Python 3.8 or newer but"
        " found version %s" % (sys.version)
    )
else:
    print("[OK] Your Python version is %s" % (sys.version))


# -------------------------------
# Package version helpers
# -------------------------------
def get_packages(pkgs):
    versions = []
    for p in pkgs:
        try:
            imported = __import__(p)
            try:
                versions.append(imported.__version__)
            except AttributeError:
                try:
                    versions.append(imported.version)
                except AttributeError:
                    try:
                        versions.append(imported.version_info)
                    except AttributeError:
                        versions.append("0.0")
        except ImportError:
            print(f"[FAIL]: {p} is not installed and/or cannot be imported.")
            versions.append("N/A")
    return versions


def check_packages(d):
    versions = get_packages(d.keys())

    for (pkg_name, suggested_ver), actual_ver in zip(d.items(), versions):
        if actual_ver == "N/A":
            continue

        actual_ver = Version(str(actual_ver))
        suggested_ver = Version(str(suggested_ver))

        # Preserve the original matplotlib 3.8 special case
        if pkg_name == "matplotlib" and actual_ver == Version("3.8"):
            print(
                f"[FAIL] {pkg_name} {actual_ver}, "
                f"please upgrade to {suggested_ver} >= matplotlib > 3.8"
            )
        elif actual_ver < suggested_ver:
            print(
                f"[FAIL] {pkg_name} {actual_ver}, "
                f"please upgrade to >= {suggested_ver}"
            )
        else:
            print(f"[OK] {pkg_name} {actual_ver}")


# -------------------------------
# Script entry point
# -------------------------------
if __name__ == "__main__":
    d = {
        "numpy": "1.21.2",
        "scipy": "1.7.0",
        "matplotlib": "3.4.3",
        "sklearn": "1.0",
        "pandas": "1.3.2",
    }
    check_packages(d)