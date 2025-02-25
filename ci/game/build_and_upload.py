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
    packages = ['mathlib', 'ai', 'graphics', 'engine', 'game', 'mapviewer']
    reference = "proj/stable"

    for package in packages:
        package_dir = base_dir / package
        if not package_dir.exists():
            print(f"Warning: Directory {package_dir} not found, skipping...")
            continue

        conanfile_path = package_dir / "conanfile.py"
        if not conanfile_path.exists():
            print(f"Warning: conanfile.py not found in {package_dir}, skipping...")
            continue

        version = get_version_from_conanfile(conanfile_path)
        if not version:
            print(f"Warning: Could not find version in {conanfile_path}, skipping...")
            continue

        print(f"\nProcessing {package}...")

        # Change to package directory
        os.chdir(package_dir)
        # Install dependencies
        install_cmd = "conan install . -r conan-local"
        print(f"Running: {install_cmd}")
        if os.system(install_cmd) != 0:
            print(f"Error installing dependencies for {package}")
            continue

        # Build the package
        build_cmd = "conan build ."
        print(f"Running: {build_cmd}")
        if os.system(build_cmd) != 0:
            print(f"Error building package {package}")
            continue

        # Create the package
        create_cmd = f"conan create . {reference} -r conan-local -pr custom_and_env"
        print(f"Running: {create_cmd}")
        if os.system(create_cmd) != 0:
            print(f"Error creating package {package}")
            continue

        # Upload the package
        upload_cmd = f"conan upload {package}/{version}@{reference} -r conan-local --all"
        print(f"Running: {upload_cmd}")
        if os.system(upload_cmd) != 0:
            print(f"Error uploading package {package}")

        # Clean local cache before uploading
        clean_cmd = "rm -rf ~/.conan/data"
        print(f"Running: {clean_cmd}")
        if os.system(clean_cmd) != 0:
            print("Error cleaning local cache")
            continue

        # Add a small delay between packages
        time.sleep(1)

if __name__ == "__main__":
    build_and_upload_packages()
