# pylint: disable=C0114,C0116
import os
import re
import time
from pathlib import Path

def get_version_from_conanfile(conanfile_path):
    with open(conanfile_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for version = "X.Y" pattern
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return None

def build_and_upload_packages():
    # Get the current directory
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))

    # List of package directories to process
    # Order matters due to dependencies
    packages = ['ai', 'graphics', 'engine', 'game', 'mapviewer']
    user = "proj"
    channel = "stable"
    reference = f"{user}/{channel}"

    process_package('mathlib', base_dir, user, channel, reference, "1.0")
    process_package('mathlib', base_dir, user, channel, reference, "2.0")
    time.sleep(1)

    for package in packages:
        process_package(package, base_dir, user, channel, reference)
        time.sleep(1)


def process_package(package, base_dir, user, channel, reference, version=None):
    package_dir = base_dir / package
    if not package_dir.exists():
        print(f"Warning: Directory {package_dir} not found, skipping...")

    if version:
        version_option = f"--version {version}"
    else:
        version_option = ""

        conanfile_path = package_dir / "conanfile.py"
        if not conanfile_path.exists():
            print(f"Warning: conanfile.py not found in {package_dir}, skipping...")
        version = get_version_from_conanfile(conanfile_path)

    if not version:
        print(f"Warning: Could not find version in {conanfile_path}, skipping...")

    print(f"\nProcessing {package}...")

    # Change to package directory
    os.chdir(package_dir)

    # Create the package
    create_cmd = f"conan create . --user {user} --channel {channel} {version_option} -r conan-local"
    print(f"Running: {create_cmd}")
    if os.system(create_cmd) != 0:
        print(f"Error creating package {package}")


    # Upload the package
    upload_cmd = f"conan upload {package}/{version}@{reference} -r conan-local"
    print(f"Running: {upload_cmd}")
    if os.system(upload_cmd) != 0:
        print(f"Error uploading package {package}")
        return False

    # Clean local cache before uploading
    clean_cmd = "conan remove -c '*/*@proj/stable'"
    print(f"Running: {clean_cmd}")
    if os.system(clean_cmd) != 0:
        print("Error cleaning local cache")
        return False

    return True

if __name__ == "__main__":
    build_and_upload_packages()
