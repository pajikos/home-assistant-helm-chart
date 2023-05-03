import yaml
import sys
from pathlib import Path

def increment_semver(version, version_part):
    major, minor, patch = map(int, version.split("."))

    if version_part == "major":
        major += 1
        minor, patch = 0, 0
    elif version_part == "minor":
        minor += 1
        patch = 0
    elif version_part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid version part: {version_part}")

    return f"{major}.{minor}.{patch}"

def update_version_in_yaml(file_path, version_part):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    current_version = data["version"]
    new_version = increment_semver(current_version, version_part)
    data["version"] = new_version

    with open(file_path, "w") as file:
        yaml.safe_dump(data, file)

    print(f"Updated SemVer from {current_version} to {new_version}")

if __name__ == "__main__":
    version_part = sys.argv[1] if len(sys.argv) > 1 else "patch"
    config_file_path = Path("charts/home-asistant/Chart.yaml")
    update_version_in_yaml(config_file_path, version_part)
