#!/usr/bin/env python3
import argparse
import html
import json
import math
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ASSET_RE = re.compile(
    r"^home-assistant-(?P<version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)\.tgz$"
)
API_VERSION = "2022-11-28"
TOP_VERSION_COUNT = 10


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_semver(version):
    core_and_build = version.split("+", 1)[0]
    core, _, prerelease = core_and_build.partition("-")
    major, minor, patch = [int(part) for part in core.split(".")]
    prerelease_key = ()
    if prerelease:
        prerelease_key = tuple(parse_prerelease_part(part) for part in prerelease.split("."))
    return major, minor, patch, 0 if prerelease else 1, prerelease_key


def parse_prerelease_part(part):
    if part.isdigit():
        return 0, int(part)
    return 1, part


def compact_count(count):
    if count < 1000:
        return str(count)
    if count < 1_000_000:
        return f"{count // 1000}k"

    value = math.floor(count / 100_000) / 10
    if value.is_integer():
        return f"{int(value)}M"
    return f"{value:g}M"


def build_stats(releases, generated_at=None):
    versions = []

    for release in releases:
        tag_name = str(release.get("tag_name", ""))
        for asset in release.get("assets") or []:
            asset_name = str(asset.get("name", ""))
            match = ASSET_RE.match(asset_name)
            if not match:
                continue

            versions.append(
                {
                    "version": match.group("version"),
                    "assetName": asset_name,
                    "tagName": tag_name,
                    "downloadCount": int(asset.get("download_count") or 0),
                }
            )

    if not versions:
        raise ValueError("No home-assistant chart archive assets found")

    versions.sort(key=lambda item: parse_semver(item["version"]), reverse=True)
    latest = versions[0]
    top_versions = sorted(versions, key=lambda item: item["downloadCount"], reverse=True)[
        :TOP_VERSION_COUNT
    ]

    return {
        "generatedAt": generated_at or now_utc(),
        "totalDownloads": sum(item["downloadCount"] for item in versions),
        "releaseCount": len(versions),
        "latestVersion": latest["version"],
        "latestVersionDownloads": latest["downloadCount"],
        "versions": versions,
        "topVersions": [
            {
                "version": item["version"],
                "downloadCount": item["downloadCount"],
            }
            for item in top_versions
        ],
    }


def write_outputs(stats, output_dir):
    stats_dir = Path(output_dir) / "stats"
    stats_dir.mkdir(parents=True, exist_ok=True)

    write_json(stats_dir / "downloads.json", stats)
    write_json(stats_dir / "downloads-badge.json", build_badge(stats))
    (stats_dir / "index.html").write_text(build_dashboard(stats), encoding="utf-8")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def build_badge(stats):
    return {
        "schemaVersion": 1,
        "label": "chart downloads",
        "message": compact_count(stats["totalDownloads"]),
        "color": "blue",
    }


def build_dashboard(stats):
    rows = "\n".join(
        build_version_row(version)
        for version in stats["versions"]
    )

    generated_at = html.escape(stats["generatedAt"])
    total_downloads = f"{stats['totalDownloads']:,}"
    latest_version = html.escape(stats["latestVersion"])
    latest_downloads = f"{stats['latestVersionDownloads']:,}"
    release_count = f"{stats['releaseCount']:,}"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Home Assistant Helm Chart Downloads</title>
  <style>
    :root {{
      color-scheme: light dark;
      --accent: #03a9f4;
      --border: #d8dee4;
      --muted: #59636e;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    body {{
      margin: 0;
      background: Canvas;
      color: CanvasText;
    }}
    main {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 2rem;
      font-weight: 650;
    }}
    p {{
      color: var(--muted);
      line-height: 1.5;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 24px 0;
    }}
    .metric {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 16px;
    }}
    .metric strong {{
      display: block;
      font-size: 1.65rem;
      margin-bottom: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
      font-size: 0.95rem;
    }}
    th, td {{
      border-bottom: 1px solid var(--border);
      padding: 10px 8px;
      text-align: left;
    }}
    th {{
      font-weight: 650;
    }}
    td:last-child, th:last-child {{
      text-align: right;
    }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.9em;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Home Assistant Helm Chart Downloads</h1>
    <p>
      These are GitHub release asset downloads, not confirmed installs. A single
      user can download multiple chart versions, and CI jobs, retries, mirrors,
      or cache misses may also increment the count.
    </p>

    <section class="summary" aria-label="Download summary">
      <div class="metric">
        <strong>{total_downloads}</strong>
        <span>chart downloads</span>
      </div>
      <div class="metric">
        <strong>{latest_version}</strong>
        <span>latest chart version</span>
      </div>
      <div class="metric">
        <strong>{latest_downloads}</strong>
        <span>latest version downloads</span>
      </div>
      <div class="metric">
        <strong>{release_count}</strong>
        <span>chart releases counted</span>
      </div>
    </section>

    <p>Last updated: <code>{generated_at}</code></p>

    <h2>Downloads by Version</h2>
    <table>
      <thead>
        <tr>
          <th>Version</th>
          <th>Release tag</th>
          <th>Downloads</th>
        </tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </main>
</body>
</html>
"""


def build_version_row(version):
    return (
        "        <tr>"
        f"<td>{html.escape(version['version'])}</td>"
        f"<td>{html.escape(version['tagName'])}</td>"
        f"<td>{version['downloadCount']:,}</td>"
        "</tr>"
    )


def load_releases_from_file(path):
    with Path(path).open(encoding="utf-8") as release_file:
        return json.load(release_file)


def fetch_releases(repo, token=None):
    releases = []
    url = f"https://api.github.com/repos/{repo}/releases?per_page=100"

    while url:
        request = urllib.request.Request(url, headers=api_headers(token))
        with urllib.request.urlopen(request, timeout=30) as response:
            releases.extend(json.load(response))
            url = next_link(response.headers.get("Link"))

    return releases


def api_headers(token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "home-assistant-helm-chart-download-stats",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def next_link(link_header):
    if not link_header:
        return None

    for part in link_header.split(","):
        pieces = [piece.strip() for piece in part.split(";")]
        if len(pieces) < 2:
            continue
        link = pieces[0]
        rel = next((piece for piece in pieces[1:] if piece == 'rel="next"'), None)
        if rel and link.startswith("<") and link.endswith(">"):
            return link[1:-1]
    return None


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Generate Helm chart download stats")
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--input", help="Path to a GitHub releases JSON fixture")
    source.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"), help="owner/repo")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--generated-at", help="Override generated timestamp")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    if args.input:
        releases = load_releases_from_file(args.input)
    else:
        if not args.repo:
            raise SystemExit("--repo is required when GITHUB_REPOSITORY is not set")
        releases = fetch_releases(args.repo, token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"))

    stats = build_stats(releases, generated_at=args.generated_at)
    write_outputs(stats, args.output)


if __name__ == "__main__":
    main()
