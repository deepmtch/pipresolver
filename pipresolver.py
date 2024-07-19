import argparse
import subprocess
import re
from packaging import version, specifiers
import sys
import concurrent.futures

def debug_print(message):
    print(f"DEBUG: {message}", file=sys.stderr)

def get_versions(pkg):
    debug_print(f"Fetching versions for {pkg}")
    result = subprocess.run(['pip', 'index', 'versions', pkg], capture_output=True, text=True)
    versions = re.findall(r'\d+\.\d+\.\d+', result.stdout)
    versions = sorted(versions, key=version.parse, reverse=True)
    debug_print(f"Found {len(versions)} versions for {pkg}")
    return versions

def check_dependency(pkg, ver, dependency, max_dependency_version):
    debug_print(f"Checking {pkg}=={ver} for {dependency} dependency")
    cmd = ['pip', 'install', f'{pkg}=={ver}', '--dry-run']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    dep_match = re.search(rf'{dependency}([=<>!~]+.*?)(?:\s|$)', result.stdout)
    if not dep_match:
        debug_print(f"{pkg}=={ver} does not depend on {dependency}")
        return None
    
    dep_spec = dep_match.group(1)
    debug_print(f"{pkg}=={ver} depends on {dependency}{dep_spec}")

    spec = specifiers.SpecifierSet(dep_spec)
    max_ver = version.parse(max_dependency_version)
    
    if max_ver in spec:
        debug_print(f"Version {max_dependency_version} is compatible with {dep_spec}")
        return ver
    else:
        debug_print(f"Version {max_dependency_version} is not compatible with {dep_spec}")
        return None

def find_compatible_version(package, dependency, max_dependency_version):
    versions = get_versions(package)
    debug_print(f"Searching for version of {package} with {dependency}<={max_dependency_version}")

    compatible_version = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_version = {executor.submit(check_dependency, package, ver, dependency, max_dependency_version): ver for ver in versions}
        for future in concurrent.futures.as_completed(future_to_version):
            ver = future.result()
            if ver:
                compatible_version = ver
                executor.shutdown(wait=False, cancel_futures=True)
                break

    return compatible_version

def main():
    parser = argparse.ArgumentParser(
        prog='pipresolver',
        description='Find an earlier version of a package that has a dependency version equal to or lower than specified.'
    )
    parser.add_argument('package', help='The package to check')
    parser.add_argument('dependency', help='The dependency to check')
    parser.add_argument('max_version', help='The maximum version of the dependency')
    
    args = parser.parse_args()

    debug_print(f"Starting search for {args.package} with {args.dependency}<={args.max_version}")
    result = find_compatible_version(args.package, args.dependency, args.max_version)
    if result:
        print(f"Compatible version found: {args.package} {result}")
    else:
        print(f"No compatible version found for {args.package}")

if __name__ == '__main__':
    main()
