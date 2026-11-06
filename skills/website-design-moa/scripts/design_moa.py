#!/usr/bin/env python3
"""Deterministic, fail-closed contracts for the website design MOA.

The script deliberately does not execute project code.  It inventories a web
repository, normalizes untrusted agent JSON, and stores a complete run outside
the repository.  Project commands are represented as argv arrays only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = 1
MAX_SCAN_FILES = 30_000
MAX_ITEMS = 100
MAX_INPUT_BYTES = 2 * 1024 * 1024
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SPECIALIST_ROLES = ("ux", "visual", "conversion")
ALL_ROLES = (*SPECIALIST_ROLES, "director")

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}
WEB_SOURCE_EXTENSIONS = {
    ".astro",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".mdx",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
}
STYLE_EXTENSIONS = {".css", ".less", ".pcss", ".sass", ".scss", ".styl"}
ASSET_EXTENSIONS = {
    ".avif",
    ".eot",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".otf",
    ".png",
    ".svg",
    ".ttf",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
}


class DesignMoaError(ValueError):
    """Raised when a deterministic design-MOA contract is violated."""


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _absolute_lexical(path: str | Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _assert_no_symlink_components(path: str | Path, *, allow_missing: bool) -> Path:
    """Reject symlinks in every existing path component.

    Canonicalizing first is insufficient for write targets because a symlink
    could silently move an apparently external artifact path into the project.
    """

    candidate = _absolute_lexical(path)
    current = Path(candidate.anchor)
    remaining_parts = candidate.parts[1:]
    for index, part in enumerate(remaining_parts):
        current = current / part
        if not os.path.lexists(current):
            if allow_missing:
                continue
            raise DesignMoaError(f"path does not exist: {current}")
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            # macOS exposes root-owned compatibility links such as
            # /var -> /private/var and /tmp -> /private/tmp. Canonicalize only
            # that trusted first component; user-controlled links deeper in a
            # path remain forbidden.
            if current.parent == Path(candidate.anchor) and info.st_uid == 0:
                trusted_target = current.resolve(strict=True)
                rewritten = trusted_target.joinpath(*remaining_parts[index + 1 :])
                return _assert_no_symlink_components(rewritten, allow_missing=allow_missing)
            raise DesignMoaError(f"symlink path component is not allowed: {current}")
    return candidate


def _secure_makedirs(path: Path) -> None:
    candidate = _assert_no_symlink_components(path, allow_missing=True)
    candidate.mkdir(mode=0o700, parents=True, exist_ok=True)
    _assert_no_symlink_components(candidate, allow_missing=False)
    if not candidate.is_dir():
        raise DesignMoaError(f"not a directory: {candidate}")


def _read_regular(path: str | Path, *, max_bytes: int = MAX_INPUT_BYTES) -> bytes:
    candidate = _assert_no_symlink_components(path, allow_missing=False)
    info = candidate.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise DesignMoaError(f"input must be a regular file: {candidate}")
    if info.st_size > max_bytes:
        raise DesignMoaError(f"input exceeds {max_bytes} bytes: {candidate}")
    return candidate.read_bytes()


def _atomic_write(path: str | Path, content: bytes) -> Path:
    target = _absolute_lexical(path)
    _secure_makedirs(target.parent)
    _assert_no_symlink_components(target.parent, allow_missing=False)
    if os.path.lexists(target) and stat.S_ISLNK(target.lstat().st_mode):
        raise DesignMoaError(f"refusing to replace symlink: {target}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        temporary.unlink(missing_ok=True)
        raise
    return target


def _run(argv: Sequence[str], *, timeout: int = 20) -> subprocess.CompletedProcess[str]:
    try:
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "GIT_OPTIONAL_LOCKS": "0",
            "LANG": "C",
            "LC_ALL": "C",
        }
        return subprocess.run(
            list(argv),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=environment,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(list(argv), 127, "", str(error))


def _git_root(path: Path) -> Path | None:
    result = _run(["git", "-C", str(path), "rev-parse", "--show-toplevel"])
    if result.returncode != 0 or not result.stdout.strip():
        return None
    root = Path(result.stdout.strip()).resolve()
    return root if root.is_dir() else None


def _git_head(root: Path) -> str | None:
    result = _run(["git", "-C", str(root), "rev-parse", "HEAD"])
    return result.stdout.strip() if result.returncode == 0 else None


def _git_dirty_paths(root: Path) -> list[str]:
    result = _run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"]
    )
    if result.returncode != 0:
        return []
    values: set[str] = set()
    for line in result.stdout.splitlines():
        value = line[3:] if len(line) >= 4 else line
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        values.add(value.strip().strip('"'))
    return sorted(values)


def _walk_project(root: Path) -> tuple[list[Path], dict[str, Any]]:
    files: list[Path] = []
    skipped_symlinks: list[str] = []
    limit_reached = False
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        safe_dirs: list[str] = []
        for name in sorted(dirnames):
            candidate = base / name
            if name in SKIP_DIRS:
                continue
            try:
                if candidate.is_symlink():
                    skipped_symlinks.append(candidate.relative_to(root).as_posix())
                    continue
            except OSError:
                continue
            safe_dirs.append(name)
        dirnames[:] = safe_dirs
        for name in sorted(filenames):
            candidate = base / name
            try:
                info = candidate.lstat()
            except OSError:
                continue
            if stat.S_ISLNK(info.st_mode):
                skipped_symlinks.append(candidate.relative_to(root).as_posix())
                continue
            if not stat.S_ISREG(info.st_mode):
                continue
            files.append(candidate)
            if len(files) >= MAX_SCAN_FILES:
                limit_reached = True
                dirnames[:] = []
                break
        if limit_reached:
            break
    return files, {
        "files_scanned": len(files),
        "file_limit_reached": limit_reached,
        "skipped_symlinks": _collection(skipped_symlinks),
    }


def _stable_items(items: Iterable[Any]) -> list[Any]:
    keyed: dict[str, Any] = {}
    for item in items:
        keyed[_json_text(item) if not isinstance(item, str) else item] = item
    return [keyed[key] for key in sorted(keyed)]


def _collection(items: Iterable[Any], *, limit: int = MAX_ITEMS) -> dict[str, Any]:
    values = _stable_items(items)
    return {
        "items": values[:limit],
        "total": len(values),
        "truncated": len(values) > limit,
    }


def _relative(root: Path, path: Path) -> str:
    value = path.relative_to(root).as_posix()
    return value or "."


def _load_package_manifests(root: Path, files: list[Path]) -> list[tuple[Path, dict[str, Any]]]:
    manifests: list[tuple[Path, dict[str, Any]]] = []
    for path in files:
        if path.name != "package.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            manifests.append((path, payload))
        if len(manifests) >= MAX_ITEMS:
            break
    return manifests


def _frameworks(
    root: Path, files: list[Path], manifests: list[tuple[Path, dict[str, Any]]]
) -> dict[str, Any]:
    found: list[dict[str, str]] = []
    dependency_map = {
        "next": "Next.js",
        "nuxt": "Nuxt",
        "@sveltejs/kit": "SvelteKit",
        "astro": "Astro",
        "@remix-run/react": "Remix",
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "vite": "Vite",
        "gatsby": "Gatsby",
    }
    for path, payload in manifests:
        dependencies: dict[str, Any] = {}
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            value = payload.get(key)
            if isinstance(value, dict):
                dependencies.update(value)
        for package, name in dependency_map.items():
            if package in dependencies:
                found.append({"name": name, "evidence": _relative(root, path)})

    config_map = {
        "next.config.js": "Next.js",
        "next.config.mjs": "Next.js",
        "next.config.ts": "Next.js",
        "nuxt.config.js": "Nuxt",
        "nuxt.config.ts": "Nuxt",
        "astro.config.mjs": "Astro",
        "astro.config.ts": "Astro",
        "svelte.config.js": "SvelteKit",
        "gatsby-config.js": "Gatsby",
        "vite.config.js": "Vite",
        "vite.config.ts": "Vite",
    }
    for path in files:
        if path.name in config_map:
            found.append({"name": config_map[path.name], "evidence": _relative(root, path)})
    if not found and any(path.suffix.lower() in {".html", ".htm"} for path in files):
        html = next(path for path in files if path.suffix.lower() in {".html", ".htm"})
        found.append({"name": "Static HTML", "evidence": _relative(root, html)})
    return _collection(found)


def _package_managers(
    root: Path, files: list[Path], manifests: list[tuple[Path, dict[str, Any]]]
) -> dict[str, Any]:
    lock_map = {
        "package-lock.json": "npm",
        "npm-shrinkwrap.json": "npm",
        "pnpm-lock.yaml": "pnpm",
        "yarn.lock": "yarn",
        "bun.lock": "bun",
        "bun.lockb": "bun",
    }
    found: list[dict[str, str]] = []
    for path in files:
        manager = lock_map.get(path.name)
        if manager:
            found.append({"name": manager, "evidence": _relative(root, path)})
    for path, payload in manifests:
        declared = payload.get("packageManager")
        if isinstance(declared, str) and declared.strip():
            found.append(
                {
                    "name": declared.split("@", 1)[0],
                    "evidence": f"{_relative(root, path)}#packageManager",
                }
            )
    if manifests and not found:
        found.append({"name": "npm", "evidence": _relative(root, manifests[0][0])})
    return _collection(found)


def _is_route(relative: Path) -> bool:
    parts = relative.parts
    lowered = [part.lower() for part in parts]
    name = relative.name.lower()
    if relative.suffix.lower() in {".html", ".htm"}:
        return True
    if name.startswith(("page.", "+page.", "route.", "+server.")):
        return True
    if "pages" in lowered and relative.suffix.lower() in WEB_SOURCE_EXTENSIONS:
        return True
    if "routes" in lowered and relative.suffix.lower() in WEB_SOURCE_EXTENSIONS:
        return True
    if "router" in lowered or name.startswith("router.") or name.startswith("routes."):
        return relative.suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".vue"}
    return False


def _routes(root: Path, files: list[Path]) -> dict[str, Any]:
    return _collection(
        _relative(root, path)
        for path in files
        if path.suffix.lower() in WEB_SOURCE_EXTENSIONS and _is_route(path.relative_to(root))
    )


def _components(root: Path, files: list[Path]) -> dict[str, Any]:
    found = []
    for path in files:
        relative = path.relative_to(root)
        if path.suffix.lower() not in WEB_SOURCE_EXTENSIONS:
            continue
        if any(part.lower() in {"component", "components", "ui"} for part in relative.parts[:-1]):
            found.append(relative.as_posix())
    return _collection(found)


def _styles_and_tokens(root: Path, files: list[Path]) -> dict[str, Any]:
    found = []
    token_names = {"theme", "themes", "token", "tokens", "variables"}
    for path in files:
        relative = path.relative_to(root)
        stem = path.stem.lower()
        name = path.name.lower()
        if path.suffix.lower() in STYLE_EXTENSIONS:
            found.append(relative.as_posix())
        elif any(token in stem for token in token_names) and path.suffix.lower() in {
            ".js",
            ".json",
            ".ts",
            ".yaml",
            ".yml",
        }:
            found.append(relative.as_posix())
        elif name.startswith(("tailwind.config.", "postcss.config.")):
            found.append(relative.as_posix())
    return _collection(found)


def _assets(root: Path, files: list[Path]) -> dict[str, Any]:
    found = []
    asset_dirs = {"asset", "assets", "font", "fonts", "icon", "icons", "image", "images", "public", "static"}
    for path in files:
        relative = path.relative_to(root)
        if path.suffix.lower() in ASSET_EXTENSIONS and any(
            part.lower() in asset_dirs for part in relative.parts[:-1]
        ):
            found.append(relative.as_posix())
    return _collection(found)


def _manager_for_manifest(path: Path, payload: dict[str, Any]) -> str:
    declared = payload.get("packageManager")
    if isinstance(declared, str) and declared:
        candidate = declared.split("@", 1)[0]
        if candidate in {"npm", "pnpm", "yarn", "bun"}:
            return candidate
    directory = path.parent
    if (directory / "pnpm-lock.yaml").is_file():
        return "pnpm"
    if (directory / "yarn.lock").is_file():
        return "yarn"
    if (directory / "bun.lock").is_file() or (directory / "bun.lockb").is_file():
        return "bun"
    return "npm"


def _commands(
    root: Path, manifests: list[tuple[Path, dict[str, Any]]]
) -> dict[str, Any]:
    found: list[dict[str, Any]] = []
    for path, payload in manifests:
        scripts = payload.get("scripts")
        if not isinstance(scripts, dict):
            continue
        manager = _manager_for_manifest(path, payload)
        cwd = _relative(root, path.parent)
        for name in sorted(scripts):
            if not (name == "test" or name.startswith("test:") or name == "build" or name.startswith("build:")):
                continue
            if manager == "yarn":
                argv = ["yarn", name]
            else:
                argv = [manager, "run", name]
            found.append(
                {
                    "argv": argv,
                    "cwd": cwd,
                    "declared_by": _relative(root, path),
                    "kind": "test" if name.startswith("test") else "build",
                }
            )
    return _collection(found)


def _agents_files(root: Path, files: list[Path]) -> dict[str, Any]:
    found: dict[str, dict[str, Any]] = {}

    def add(path: Path, kind: str, scope: str) -> None:
        try:
            canonical = _assert_no_symlink_components(path, allow_missing=False)
            info = canonical.lstat()
            if not stat.S_ISREG(info.st_mode):
                return
            found[str(canonical)] = {
                "path": str(canonical),
                "kind": kind,
                "scope": scope,
                "sha256": _sha256_file(canonical),
            }
        except (OSError, DesignMoaError):
            return

    global_agents = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "AGENTS.md"
    if global_agents.is_file():
        add(global_agents, "global", "*")

    ancestors = list(root.parents)
    for directory in reversed(ancestors):
        candidate = directory / "AGENTS.md"
        if candidate.is_file():
            add(candidate, "ancestor", str(root))

    for path in files:
        if path.name != "AGENTS.md":
            continue
        relative_parent = path.parent.relative_to(root).as_posix() or "."
        add(path, "repository" if path.parent == root else "nested", relative_parent)
    return _collection(found.values())


def build_preflight(repo: str | Path) -> dict[str, Any]:
    requested = Path(repo).expanduser().resolve()
    if not requested.is_dir():
        raise DesignMoaError(f"repository path is not a directory: {requested}")
    git_root = _git_root(requested)
    root = git_root or requested
    files, scan = _walk_project(root)
    manifests = _load_package_manifests(root, files)
    dirty_paths = _git_dirty_paths(root) if git_root else []
    dirty_collection = _collection(dirty_paths)
    sections = {
        "frameworks": _frameworks(root, files, manifests),
        "package_managers": _package_managers(root, files, manifests),
        "routes_and_pages": _routes(root, files),
        "components": _components(root, files),
        "styles_and_tokens": _styles_and_tokens(root, files),
        "assets": _assets(root, files),
        "commands": _commands(root, manifests),
    }
    instructions = _agents_files(root, files)
    partial = bool(
        scan["file_limit_reached"]
        or scan["skipped_symlinks"]["total"]
        or dirty_collection["truncated"]
        or instructions["truncated"]
        or any(section["truncated"] for section in sections.values())
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "website-design-preflight",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository": {
            "requested_path": str(requested),
            "root": str(root),
            "is_git": git_root is not None,
            "git_root": str(git_root) if git_root else None,
            "head": _git_head(root) if git_root else None,
            "dirty": bool(dirty_paths) if git_root else None,
            "dirty_paths": dirty_collection,
        },
        "instructions": instructions,
        "inventory": sections,
        "scan": scan,
        "limits": {"max_files": MAX_SCAN_FILES, "max_items_per_list": MAX_ITEMS},
        "coverage": "PARTIAL" if partial else "COMPLETE",
    }


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and all(
        _nonempty_string(item) for item in value
    )


def _inconclusive(role: str, errors: list[str], source: Any = None) -> dict[str, Any]:
    """Return a valid role contract that cannot be mistaken for approval."""

    reasons = [item for item in errors if _nonempty_string(item)] or [
        "agent result is inconclusive"
    ]
    if role in SPECIALIST_ROLES:
        return {
            "specialist": role,
            "status": "INCONCLUSIVE",
            "summary": reasons[0],
            "strengths": [],
            "findings": [],
            "coverage": {"inspected": [], "not_inspected": []},
            "gaps": reasons,
        }
    return {
        "director": "site-design-director",
        "status": "INCONCLUSIVE",
        "summary": reasons[0],
        "input_integrity": {
            "ux": "invalid",
            "visual": "invalid",
            "conversion": "invalid",
        },
        "design_spec": {
            "intent": "",
            "principles": [],
            "priorities": [],
            "system": {
                "information_architecture": [],
                "journeys_and_interactions": [],
                "responsive_behavior": [],
                "art_direction": [],
                "typography_color_grid": [],
                "component_language": [],
                "content_cta_trust": [],
                "accessibility_performance": [],
            },
        },
        "conflicts_resolved": [],
        "gaps": [
            {"missing": reason, "blocks": ["design_spec"], "next_evidence": "retry role output"}
            for reason in reasons
        ],
        "validation_plan": [],
        "authorization": "REPORT_ONLY",
    }


def _validate_evidence(value: Any, *, path: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path} must be a non-empty evidence array")
        return
    for index, evidence in enumerate(value):
        if not isinstance(evidence, dict):
            errors.append(f"{path}[{index}] must be an object")
            continue
        for field in ("source", "locator", "observation"):
            if not _nonempty_string(evidence.get(field)):
                errors.append(f"{path}[{index}].{field} must be a non-empty string")


def _validate_specialist(role: str, raw: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if raw.get("specialist") != role:
        errors.append(f"specialist must be {role}")
    status_value = raw.get("status") if isinstance(raw.get("status"), str) else ""
    if status_value not in {"READY", "PARTIAL", "INCONCLUSIVE"}:
        errors.append("status must be READY, PARTIAL, or INCONCLUSIVE")
    if not _nonempty_string(raw.get("summary")):
        errors.append("summary must be a non-empty string")

    strengths = raw.get("strengths")
    if not isinstance(strengths, list):
        errors.append("strengths must be an array")
        strengths = []
    for index, strength in enumerate(strengths):
        if not isinstance(strength, dict) or not _nonempty_string(strength.get("claim")):
            errors.append(f"strengths[{index}] must contain a claim")
            continue
        _validate_evidence(strength.get("evidence"), path=f"strengths[{index}].evidence", errors=errors)

    impact_fields = {
        "ux": "user_impact",
        "visual": "design_impact",
        "conversion": "business_and_user_impact",
    }
    id_prefixes = {"ux": "UX-", "visual": "VIS-", "conversion": "CONV-"}
    findings = raw.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be an array")
        findings = []
    ids: set[str] = set()
    for index, finding in enumerate(findings):
        label = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{label} must be an object")
            continue
        finding_id = finding.get("id")
        if not _nonempty_string(finding_id) or not finding_id.startswith(id_prefixes[role]):
            errors.append(f"{label}.id must start with {id_prefixes[role]}")
        elif finding_id in ids:
            errors.append(f"duplicate finding id: {finding_id}")
        else:
            ids.add(finding_id)
        if finding.get("severity") not in {"critical", "high", "medium", "low"}:
            errors.append(f"{label}.severity is invalid")
        for field in ("area", "problem", impact_fields[role], "recommendation"):
            if not _nonempty_string(finding.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string")
        _validate_evidence(finding.get("evidence"), path=f"{label}.evidence", errors=errors)
        if not _string_list(finding.get("acceptance_checks"), nonempty=True):
            errors.append(f"{label}.acceptance_checks must be a non-empty string array")
        if finding.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{label}.confidence is invalid")

    coverage = raw.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("coverage must be an object")
        coverage = {"inspected": [], "not_inspected": []}
    if not _string_list(coverage.get("inspected")):
        errors.append("coverage.inspected must be a string array")
    if not _string_list(coverage.get("not_inspected")):
        errors.append("coverage.not_inspected must be a string array")
    gaps = raw.get("gaps")
    if not _string_list(gaps):
        errors.append("gaps must be a string array")
        gaps = []

    inspected_text = " ".join(coverage.get("inspected", [])).lower()
    if status_value == "READY":
        if not strengths and not findings:
            errors.append("READY requires at least one evidenced strength or finding")
        if "desktop" not in inspected_text or "mobile" not in inspected_text:
            errors.append("READY requires explicit desktop and mobile coverage")
    if status_value == "PARTIAL" and not (coverage.get("not_inspected") or gaps):
        errors.append("PARTIAL requires explicit coverage gaps")

    canonical = {
        "specialist": role,
        "status": status_value,
        "summary": raw.get("summary"),
        "strengths": strengths,
        "findings": findings,
        "coverage": coverage,
        "gaps": gaps,
    }
    return errors, canonical


SYSTEM_FIELDS = (
    "information_architecture",
    "journeys_and_interactions",
    "responsive_behavior",
    "art_direction",
    "typography_color_grid",
    "component_language",
    "content_cta_trust",
    "accessibility_performance",
)


def _validate_director(raw: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if raw.get("director") != "site-design-director":
        errors.append("director must be site-design-director")
    status_value = raw.get("status") if isinstance(raw.get("status"), str) else ""
    if status_value not in {"READY", "PARTIAL", "INCONCLUSIVE"}:
        errors.append("status must be READY, PARTIAL, or INCONCLUSIVE")
    if not _nonempty_string(raw.get("summary")):
        errors.append("summary must be a non-empty string")
    if raw.get("authorization") != "REPORT_ONLY":
        errors.append("authorization must be REPORT_ONLY")

    integrity = raw.get("input_integrity")
    if not isinstance(integrity, dict):
        errors.append("input_integrity must be an object")
        integrity = {}
    allowed_integrity = {"valid", "partial", "invalid", "missing"}
    for role in SPECIALIST_ROLES:
        if integrity.get(role) not in allowed_integrity:
            errors.append(f"input_integrity.{role} is invalid")

    design_spec = raw.get("design_spec")
    if not isinstance(design_spec, dict):
        errors.append("design_spec must be an object")
        design_spec = {}
    intent = design_spec.get("intent")
    principles = design_spec.get("principles")
    priorities = design_spec.get("priorities")
    system = design_spec.get("system")
    if not isinstance(priorities, list):
        errors.append("design_spec.priorities must be an array")
        priorities = []
    if not isinstance(system, dict):
        errors.append("design_spec.system must be an object")
        system = {}
    for field in SYSTEM_FIELDS:
        if not _string_list(system.get(field)):
            errors.append(f"design_spec.system.{field} must be a string array")

    priority_ids: set[str] = set()
    ranks: set[int] = set()
    for index, priority in enumerate(priorities):
        label = f"design_spec.priorities[{index}]"
        if not isinstance(priority, dict):
            errors.append(f"{label} must be an object")
            continue
        rank = priority.get("rank")
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1 or rank in ranks:
            errors.append(f"{label}.rank must be a unique positive integer")
        else:
            ranks.add(rank)
        priority_id = priority.get("id")
        if not _nonempty_string(priority_id) or not priority_id.startswith("DS-") or priority_id in priority_ids:
            errors.append(f"{label}.id must be a unique DS- identifier")
        else:
            priority_ids.add(priority_id)
        for field in ("decision", "rationale"):
            if not _nonempty_string(priority.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string")
        for field in ("source_findings", "scope", "acceptance_checks", "dependencies"):
            if not _string_list(priority.get(field), nonempty=field != "dependencies"):
                errors.append(f"{label}.{field} must be a string array")
        _validate_evidence(priority.get("evidence"), path=f"{label}.evidence", errors=errors)
        if priority.get("confidence") not in {"high", "medium", "low"}:
            errors.append(f"{label}.confidence is invalid")

    conflicts = raw.get("conflicts_resolved")
    if not isinstance(conflicts, list):
        errors.append("conflicts_resolved must be an array")
        conflicts = []
    for index, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            errors.append(f"conflicts_resolved[{index}] must be an object")
            continue
        for field in ("topic", "resolution", "reason"):
            if not _nonempty_string(conflict.get(field)):
                errors.append(f"conflicts_resolved[{index}].{field} must be a non-empty string")
        if not _string_list(conflict.get("positions"), nonempty=True):
            errors.append(f"conflicts_resolved[{index}].positions must be non-empty")

    gaps = raw.get("gaps")
    if not isinstance(gaps, list):
        errors.append("gaps must be an array")
        gaps = []
    for index, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            errors.append(f"gaps[{index}] must be an object")
            continue
        for field in ("missing", "next_evidence"):
            if not _nonempty_string(gap.get(field)):
                errors.append(f"gaps[{index}].{field} must be a non-empty string")
        if not _string_list(gap.get("blocks"), nonempty=True):
            errors.append(f"gaps[{index}].blocks must be non-empty")
    validation_plan = raw.get("validation_plan")
    if not _string_list(validation_plan):
        errors.append("validation_plan must be a string array")
        validation_plan = []

    if status_value == "READY":
        if any(integrity.get(role) != "valid" for role in SPECIALIST_ROLES):
            errors.append("READY requires three valid specialist inputs")
        if not _nonempty_string(intent) or not _string_list(principles, nonempty=True) or not priorities:
            errors.append("READY requires a coherent non-empty design specification")
        if not validation_plan:
            errors.append("READY requires a validation plan")
    elif status_value == "PARTIAL":
        if any(integrity.get(role) in {"invalid", "missing"} for role in SPECIALIST_ROLES):
            errors.append("missing or invalid specialist input requires INCONCLUSIVE")
        if not gaps:
            errors.append("PARTIAL requires explicit gaps")

    canonical = {
        "director": "site-design-director",
        "status": status_value,
        "summary": raw.get("summary"),
        "input_integrity": integrity,
        "design_spec": {
            "intent": intent,
            "principles": principles if isinstance(principles, list) else [],
            "priorities": priorities,
            "system": {field: system.get(field, []) for field in SYSTEM_FIELDS},
        },
        "conflicts_resolved": conflicts,
        "gaps": gaps,
        "validation_plan": validation_plan,
        "authorization": "REPORT_ONLY",
    }
    return errors, canonical


def normalize_payload(role: str, payload: Any, *, parse_error: str | None = None) -> dict[str, Any]:
    if role not in ALL_ROLES:
        raise DesignMoaError(f"unknown role: {role}")
    if parse_error:
        return _inconclusive(role, [parse_error])
    if not isinstance(payload, dict):
        return _inconclusive(role, ["top-level JSON must be an object"])
    if payload.get("timed_out") is True or payload.get("timeout") is True:
        return _inconclusive(role, ["agent timed out"])
    errors, canonical = (
        _validate_specialist(role, payload)
        if role in SPECIALIST_ROLES
        else _validate_director(payload)
    )
    return _inconclusive(role, errors, payload) if errors else canonical


def normalize_file(role: str, path: str | Path) -> dict[str, Any]:
    try:
        raw = _read_regular(path)
        payload = json.loads(raw.decode("utf-8"))
    except DesignMoaError as error:
        return _inconclusive(role, [str(error)])
    except UnicodeDecodeError:
        return _inconclusive(role, ["input is not UTF-8"])
    except json.JSONDecodeError as error:
        return _inconclusive(role, [f"invalid JSON: {error.msg}"])
    return normalize_payload(role, payload)


def _validate_preflight(preflight: Any, root: Path) -> dict[str, Any]:
    if not isinstance(preflight, dict):
        raise DesignMoaError("preflight must be a JSON object")
    if preflight.get("kind") != "website-design-preflight":
        raise DesignMoaError("unexpected preflight kind")
    repository = preflight.get("repository")
    if not isinstance(repository, dict) or not _nonempty_string(repository.get("root")):
        raise DesignMoaError("preflight is missing repository.root")
    recorded = Path(repository["root"]).expanduser().resolve()
    if recorded != root:
        raise DesignMoaError(f"preflight root mismatch: {recorded} != {root}")
    return preflight


def _write_at(directory_fd: int, name: str, content: bytes) -> None:
    if "/" in name or name in {"", ".", ".."}:
        raise DesignMoaError(f"unsafe artifact name: {name}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(name, flags, 0o600, dir_fd=directory_fd)
    try:
        offset = 0
        while offset < len(content):
            offset += os.write(fd, content[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def _default_report(
    run_id: str,
    root: Path,
    preflight: dict[str, Any],
    specialists: dict[str, dict[str, Any]],
    director: dict[str, Any],
) -> str:
    repository = preflight["repository"]
    lines = [
        "# Website Design MOA Report",
        "",
        f"- Run: `{run_id}`",
        f"- Repository: `{root}`",
        f"- HEAD: `{repository.get('head') or 'not-git'}`",
        f"- Coverage: `{preflight.get('coverage', 'PARTIAL')}`",
        f"- Director: `{director['status']}`",
        "",
        "## Specialists",
        "",
    ]
    for role in SPECIALIST_ROLES:
        result = specialists[role]
        summary = result.get("summary") or "No valid summary."
        lines.extend([f"### {role.title()} — {result['status']}", "", str(summary), ""])
    lines.extend(["## Director", "", director.get("summary") or "Inconclusive.", ""])
    return "\n".join(lines)


def create_run(
    *,
    repo: str | Path | None,
    preflight_path: str | Path,
    specialist_paths: dict[str, str | Path],
    director_path: str | Path,
    artifact_root: str | Path,
    run_id: str | None = None,
    report_path: str | Path | None = None,
) -> Path:
    try:
        preflight_payload = json.loads(_read_regular(preflight_path).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DesignMoaError(f"invalid preflight JSON: {error}") from error
    repository = preflight_payload.get("repository") if isinstance(preflight_payload, dict) else None
    recorded_root = repository.get("root") if isinstance(repository, dict) else None
    if not _nonempty_string(recorded_root):
        raise DesignMoaError("preflight is missing repository.root")
    root = Path(recorded_root).expanduser().resolve()
    if not root.is_dir():
        raise DesignMoaError(f"recorded repository root is not a directory: {root}")
    if repo is not None:
        requested = Path(repo).expanduser().resolve()
        if not requested.is_dir():
            raise DesignMoaError(f"repository path is not a directory: {requested}")
        actual_root = _git_root(requested) or requested
        if actual_root != root:
            raise DesignMoaError(f"preflight root mismatch: {root} != {actual_root}")
    preflight = _validate_preflight(preflight_payload, root)

    root_artifacts = _assert_no_symlink_components(artifact_root, allow_missing=True)
    canonical_artifacts = root_artifacts.resolve(strict=False)
    if _is_within(canonical_artifacts, root):
        raise DesignMoaError("artifact root must be outside the repository")
    _secure_makedirs(root_artifacts)

    if run_id is None:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        run_id = f"{stamp}-{uuid.uuid4().hex[:10]}"
    if not SAFE_RUN_ID.fullmatch(run_id):
        raise DesignMoaError("run id contains unsafe characters")

    missing = set(SPECIALIST_ROLES) - set(specialist_paths)
    if missing:
        raise DesignMoaError(f"missing specialist outputs: {', '.join(sorted(missing))}")
    specialists = {
        role: normalize_file(role, specialist_paths[role]) for role in SPECIALIST_ROLES
    }
    director = normalize_file("director", director_path)

    if report_path is None:
        report = _default_report(run_id, root, preflight, specialists, director)
    else:
        try:
            report = _read_regular(report_path, max_bytes=4 * MAX_INPUT_BYTES).decode("utf-8")
        except UnicodeDecodeError as error:
            raise DesignMoaError("report must be UTF-8") from error

    artifacts: dict[str, bytes] = {
        "preflight.json": _json_text(preflight).encode("utf-8"),
        "director-result.json": _json_text(director).encode("utf-8"),
        "report.md": report.encode("utf-8"),
    }
    for role, result in specialists.items():
        artifacts[f"specialists/{role}.json"] = _json_text(result).encode("utf-8")

    nofollow = getattr(os, "O_NOFOLLOW", 0)
    root_fd = os.open(root_artifacts, os.O_RDONLY | os.O_DIRECTORY | nofollow)
    run_fd: int | None = None
    specialists_fd: int | None = None
    try:
        os.mkdir(run_id, mode=0o700, dir_fd=root_fd)
        run_fd = os.open(run_id, os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=root_fd)
        os.mkdir("specialists", mode=0o700, dir_fd=run_fd)
        specialists_fd = os.open(
            "specialists", os.O_RDONLY | os.O_DIRECTORY | nofollow, dir_fd=run_fd
        )
        for name in ("preflight.json", "director-result.json", "report.md"):
            _write_at(run_fd, name, artifacts[name])
        for role in SPECIALIST_ROLES:
            _write_at(specialists_fd, f"{role}.json", artifacts[f"specialists/{role}.json"])
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "kind": "website-design-run-manifest",
            "run_id": run_id,
            "repository_root": str(root),
            "repository_head": preflight["repository"].get("head"),
            "artifacts": {
                name: {"sha256": _sha256_bytes(content), "bytes": len(content)}
                for name, content in sorted(artifacts.items())
            },
        }
        _write_at(run_fd, "manifest.json", _json_text(manifest).encode("utf-8"))
        os.fsync(run_fd)
    except FileExistsError as error:
        raise DesignMoaError(f"run already exists: {run_id}") from error
    finally:
        if specialists_fd is not None:
            os.close(specialists_fd)
        if run_fd is not None:
            os.close(run_fd)
        os.close(root_fd)
    return root_artifacts / run_id


def _cmd_preflight(args: argparse.Namespace) -> int:
    preflight = build_preflight(args.repo)
    root = Path(preflight["repository"]["root"]).resolve()
    output = _absolute_lexical(args.output)
    if _is_within(output.resolve(strict=False), root):
        raise DesignMoaError("preflight output must be outside the repository")
    _atomic_write(output, _json_text(preflight).encode("utf-8"))
    print(_json_text({"output": str(output), "coverage": preflight["coverage"]}), end="")
    return 0


def _cmd_normalize(args: argparse.Namespace) -> int:
    result = normalize_file(args.role, args.input)
    output = _atomic_write(args.output, _json_text(result).encode("utf-8"))
    print(_json_text({"output": str(output), "status": result["status"]}), end="")
    return 0


def _cmd_create_run(args: argparse.Namespace) -> int:
    run = create_run(
        repo=args.repo,
        preflight_path=args.preflight,
        specialist_paths={
            "ux": args.ux,
            "visual": args.visual,
            "conversion": args.conversion,
        },
        director_path=args.director,
        artifact_root=args.artifact_root,
        run_id=args.run_id,
        report_path=args.report,
    )
    print(_json_text({"run_directory": str(run)}), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preflight = subparsers.add_parser("preflight", help="inventory a web project without executing it")
    preflight.add_argument("--repo", required=True)
    preflight.add_argument("--output", required=True)
    preflight.set_defaults(func=_cmd_preflight)

    normalize = subparsers.add_parser("normalize", help="normalize an untrusted agent result")
    normalize.add_argument("--role", required=True, choices=ALL_ROLES)
    normalize.add_argument("--input", required=True)
    normalize.add_argument("--output", required=True)
    normalize.set_defaults(func=_cmd_normalize)

    create = subparsers.add_parser("create-run", help="persist a complete design review run")
    create.add_argument("--repo")
    create.add_argument("--preflight", required=True)
    create.add_argument("--ux", required=True)
    create.add_argument("--visual", required=True)
    create.add_argument("--conversion", required=True)
    create.add_argument("--director", required=True)
    create.add_argument("--report")
    create.add_argument("--run-id")
    create.add_argument(
        "--artifact-root",
        default=str(Path.home() / ".codex" / "design-runs"),
    )
    create.set_defaults(func=_cmd_create_run)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except DesignMoaError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
