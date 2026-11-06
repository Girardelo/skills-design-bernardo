from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import design_moa


def write(path: Path, value: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    else:
        path.write_text(value, encoding="utf-8")


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, check=True, capture_output=True, text=True)


def evidence() -> list[dict[str, str]]:
    return [
        {
            "source": "render",
            "locator": "home desktop 1440px hero",
            "observation": "The primary action is visible above the fold.",
        }
    ]


def specialist(role: str, status: str = "READY") -> dict[str, object]:
    impact = {
        "ux": "user_impact",
        "visual": "design_impact",
        "conversion": "business_and_user_impact",
    }[role]
    prefix = {"ux": "UX", "visual": "VIS", "conversion": "CONV"}[role]
    result: dict[str, object] = {
        "specialist": role,
        "status": status,
        "summary": f"Evidence-backed {role} assessment.",
        "strengths": [{"claim": "The primary action is prominent.", "evidence": evidence()}],
        "findings": [
            {
                "id": f"{prefix}-1",
                "severity": "medium",
                "area": "hierarchy",
                "problem": "Secondary content competes with the primary action.",
                impact: "Users may take longer to identify the next step.",
                "evidence": evidence(),
                "recommendation": "Reduce secondary emphasis while retaining the content.",
                "acceptance_checks": ["Primary action is first in the visual hierarchy."],
                "confidence": "high",
            }
        ],
        "coverage": {
            "inspected": ["home desktop 1440px", "home mobile 390px"],
            "not_inspected": [],
        },
        "gaps": [],
    }
    if status == "PARTIAL":
        result["coverage"] = {
            "inspected": ["home desktop 1440px"],
            "not_inspected": ["checkout mobile"],
        }
        result["gaps"] = ["Checkout mobile render was unavailable."]
    return result


def director(status: str = "READY") -> dict[str, object]:
    system = {field: [f"Concrete {field.replace('_', ' ')} rule."] for field in design_moa.SYSTEM_FIELDS}
    result: dict[str, object] = {
        "director": "site-design-director",
        "status": status,
        "summary": "Prioritize a direct journey with a restrained visual hierarchy.",
        "input_integrity": {"ux": "valid", "visual": "valid", "conversion": "valid"},
        "design_spec": {
            "intent": "Make the primary task unmistakable across desktop and mobile.",
            "principles": ["One dominant action per decision point."],
            "priorities": [
                {
                    "rank": 1,
                    "id": "DS-1",
                    "decision": "Give the primary action dominant hierarchy.",
                    "rationale": "All three roles cite direct hierarchy evidence.",
                    "source_findings": ["UX-1", "VIS-1", "CONV-1"],
                    "evidence": evidence(),
                    "scope": ["home desktop and mobile hero"],
                    "acceptance_checks": ["The action is first in hierarchy."],
                    "dependencies": [],
                    "confidence": "high",
                }
            ],
            "system": system,
        },
        "conflicts_resolved": [],
        "gaps": [],
        "validation_plan": ["Render home at 1440px and 390px."],
        "authorization": "REPORT_ONLY",
    }
    if status == "PARTIAL":
        result["input_integrity"] = {"ux": "valid", "visual": "partial", "conversion": "valid"}
        result["gaps"] = [
            {
                "missing": "Mobile checkout render",
                "blocks": ["DS-1"],
                "next_evidence": "Capture the checkout at 390px.",
            }
        ]
    return result


class DesignMoaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.repo = self.base / "site"
        self.repo.mkdir()
        write(self.repo / "AGENTS.md", "# Fixture instructions\n")
        write(
            self.repo / "package.json",
            json.dumps(
                {
                    "dependencies": {"next": "15.0.0", "react": "19.0.0"},
                    "scripts": {"test": "vitest run", "build": "next build", "dev": "next dev"},
                }
            ),
        )
        write(self.repo / "package-lock.json", "{}\n")
        write(self.repo / "app" / "page.tsx", "export default function Page(){return <main/>}\n")
        write(self.repo / "components" / "Hero.tsx", "export function Hero(){return <section/>}\n")
        write(self.repo / "styles" / "globals.css", ":root { --space: 8px; }\n")
        write(self.repo / "styles" / "tokens.json", '{"space": 8}\n')
        write(self.repo / "public" / "logo.svg", "<svg/>\n")
        run(["git", "init", "-q"], self.repo)
        run(["git", "add", "."], self.repo)
        run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.test",
                "commit",
                "-qm",
                "fixture",
            ],
            self.repo,
        )
        write(self.repo / "app" / "page.tsx", "export default function Page(){return <main>dirty</main>}\n")
        self.outside = self.base / "outside"
        self.outside.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_preflight_file(self) -> Path:
        path = self.outside / "preflight.json"
        write(path, json.dumps(design_moa.build_preflight(self.repo)))
        return path

    def make_agent_files(self) -> dict[str, Path]:
        paths: dict[str, Path] = {}
        for role in design_moa.SPECIALIST_ROLES:
            paths[role] = self.outside / f"{role}.json"
            write(paths[role], json.dumps(specialist(role)))
        paths["director"] = self.outside / "director.json"
        write(paths["director"], json.dumps(director()))
        return paths

    def test_preflight_detects_web_inventory_and_dirty_git(self) -> None:
        result = design_moa.build_preflight(self.repo)
        repository = result["repository"]
        inventory = result["inventory"]
        self.assertTrue(repository["is_git"])
        self.assertTrue(repository["head"])
        self.assertTrue(repository["dirty"])
        self.assertIn("app/page.tsx", repository["dirty_paths"]["items"])
        self.assertIn("Next.js", {item["name"] for item in inventory["frameworks"]["items"]})
        self.assertIn("npm", {item["name"] for item in inventory["package_managers"]["items"]})
        self.assertIn("app/page.tsx", inventory["routes_and_pages"]["items"])
        self.assertIn("components/Hero.tsx", inventory["components"]["items"])
        self.assertIn("styles/tokens.json", inventory["styles_and_tokens"]["items"])
        self.assertIn("public/logo.svg", inventory["assets"]["items"])
        commands = inventory["commands"]["items"]
        self.assertEqual({item["kind"] for item in commands}, {"build", "test"})
        self.assertTrue(all(isinstance(item["argv"], list) for item in commands))
        instruction_paths = {Path(item["path"]) for item in result["instructions"]["items"]}
        self.assertIn((self.repo / "AGENTS.md").resolve(), instruction_paths)

    def test_preflight_supports_non_git_directory(self) -> None:
        plain = self.base / "plain"
        plain.mkdir()
        write(plain / "index.html", "<!doctype html>")
        result = design_moa.build_preflight(plain)
        self.assertFalse(result["repository"]["is_git"])
        self.assertIsNone(result["repository"]["head"])
        self.assertIsNone(result["repository"]["dirty"])
        self.assertEqual(result["inventory"]["frameworks"]["items"][0]["name"], "Static HTML")
        self.assertEqual(result["inventory"]["routes_and_pages"]["items"], ["index.html"])

    def test_preflight_lists_are_bounded(self) -> None:
        for index in range(design_moa.MAX_ITEMS + 12):
            write(self.repo / "app" / f"route-{index}" / "page.tsx", "export default 1\n")
        result = design_moa.build_preflight(self.repo)
        routes = result["inventory"]["routes_and_pages"]
        self.assertEqual(len(routes["items"]), design_moa.MAX_ITEMS)
        self.assertTrue(routes["truncated"])
        self.assertGreater(routes["total"], design_moa.MAX_ITEMS)
        self.assertEqual(result["coverage"], "PARTIAL")

    def test_preflight_cli_refuses_output_inside_repository(self) -> None:
        output = self.repo / "preflight.json"
        code = design_moa.main(["preflight", "--repo", str(self.repo), "--output", str(output)])
        self.assertEqual(code, 2)
        self.assertFalse(output.exists())

    def test_invalid_json_normalizes_to_inconclusive_contract(self) -> None:
        source = self.outside / "invalid.json"
        write(source, "{not-json")
        result = design_moa.normalize_file("ux", source)
        self.assertEqual(result["specialist"], "ux")
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertIn("invalid JSON", result["summary"])
        self.assertEqual(result["findings"], [])

    def test_timeout_normalizes_to_inconclusive(self) -> None:
        result = design_moa.normalize_payload("visual", {"timed_out": True})
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertIn("timed out", result["gaps"][0])

    def test_status_vocabulary_is_case_sensitive(self) -> None:
        raw = specialist("ux")
        raw["status"] = "ready"
        result = design_moa.normalize_payload("ux", raw)
        self.assertEqual(result["status"], "INCONCLUSIVE")

    def test_partial_specialist_is_preserved(self) -> None:
        raw = specialist("conversion", "PARTIAL")
        result = design_moa.normalize_payload("conversion", raw)
        self.assertEqual(result, raw)

    def test_ready_without_mobile_coverage_becomes_inconclusive(self) -> None:
        raw = specialist("ux")
        raw["coverage"] = {"inspected": ["home desktop"], "not_inspected": []}
        result = design_moa.normalize_payload("ux", raw)
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertTrue(any("mobile" in gap for gap in result["gaps"]))

    def test_approval_vocabulary_never_creates_implicit_approval(self) -> None:
        result = design_moa.normalize_payload(
            "director", {"director": "site-design-director", "status": "APPROVE"}
        )
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertEqual(result["authorization"], "REPORT_ONLY")

    def test_ready_director_requires_report_only_and_preserves_contract(self) -> None:
        raw = director()
        self.assertEqual(design_moa.normalize_payload("director", raw), raw)
        wrong = dict(raw)
        wrong["authorization"] = "IMPLEMENT"
        normalized = design_moa.normalize_payload("director", wrong)
        self.assertEqual(normalized["status"], "INCONCLUSIVE")
        self.assertEqual(normalized["authorization"], "REPORT_ONLY")

    def test_partial_director_with_missing_input_becomes_inconclusive(self) -> None:
        raw = director("PARTIAL")
        raw["input_integrity"] = {"ux": "valid", "visual": "missing", "conversion": "valid"}
        result = design_moa.normalize_payload("director", raw)
        self.assertEqual(result["status"], "INCONCLUSIVE")

    def test_create_run_persists_normalized_payloads_and_manifest(self) -> None:
        preflight = self.make_preflight_file()
        agents = self.make_agent_files()
        report = self.outside / "custom.md"
        write(report, "# Relatório\n\nResultado consolidado.\n")
        run_directory = design_moa.create_run(
            repo=None,
            preflight_path=preflight,
            specialist_paths={role: agents[role] for role in design_moa.SPECIALIST_ROLES},
            director_path=agents["director"],
            artifact_root=self.outside / "runs",
            run_id="safe-run",
            report_path=report,
        )
        self.assertEqual(json.loads((run_directory / "specialists" / "ux.json").read_text()), specialist("ux"))
        self.assertEqual(json.loads((run_directory / "director-result.json").read_text()), director())
        self.assertEqual((run_directory / "report.md").read_text(), report.read_text())
        manifest = json.loads((run_directory / "manifest.json").read_text())
        for relative, metadata in manifest["artifacts"].items():
            content = (run_directory / relative).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), metadata["sha256"])
        self.assertFalse((self.repo / "report.md").exists())

    def test_create_run_cli_derives_repo_from_preflight(self) -> None:
        preflight = self.make_preflight_file()
        agents = self.make_agent_files()
        code = design_moa.main(
            [
                "create-run",
                "--preflight",
                str(preflight),
                "--ux",
                str(agents["ux"]),
                "--visual",
                str(agents["visual"]),
                "--conversion",
                str(agents["conversion"]),
                "--director",
                str(agents["director"]),
                "--artifact-root",
                str(self.outside / "runs"),
                "--run-id",
                "cli-run",
            ]
        )
        self.assertEqual(code, 0)
        self.assertTrue((self.outside / "runs" / "cli-run" / "report.md").is_file())

    def test_artifact_root_inside_repository_is_rejected(self) -> None:
        preflight = self.make_preflight_file()
        agents = self.make_agent_files()
        with self.assertRaisesRegex(design_moa.DesignMoaError, "outside the repository"):
            design_moa.create_run(
                repo=self.repo,
                preflight_path=preflight,
                specialist_paths={role: agents[role] for role in design_moa.SPECIALIST_ROLES},
                director_path=agents["director"],
                artifact_root=self.repo / ".design-runs",
                run_id="blocked",
            )

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unsupported")
    def test_symlink_artifact_root_is_rejected(self) -> None:
        preflight = self.make_preflight_file()
        agents = self.make_agent_files()
        real_runs = self.outside / "real-runs"
        real_runs.mkdir()
        link = self.outside / "linked-runs"
        link.symlink_to(real_runs, target_is_directory=True)
        with self.assertRaisesRegex(design_moa.DesignMoaError, "symlink"):
            design_moa.create_run(
                repo=self.repo,
                preflight_path=preflight,
                specialist_paths={role: agents[role] for role in design_moa.SPECIALIST_ROLES},
                director_path=agents["director"],
                artifact_root=link,
                run_id="blocked",
            )

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unsupported")
    def test_normalize_refuses_symlink_output(self) -> None:
        source = self.outside / "ux.json"
        write(source, json.dumps(specialist("ux")))
        real_output = self.outside / "real.json"
        write(real_output, "{}")
        linked_output = self.outside / "linked.json"
        linked_output.symlink_to(real_output)
        code = design_moa.main(
            ["normalize", "--role", "ux", "--input", str(source), "--output", str(linked_output)]
        )
        self.assertEqual(code, 2)
        self.assertEqual(real_output.read_text(), "{}")

    def test_unsafe_run_id_is_rejected(self) -> None:
        preflight = self.make_preflight_file()
        agents = self.make_agent_files()
        with self.assertRaisesRegex(design_moa.DesignMoaError, "unsafe"):
            design_moa.create_run(
                repo=self.repo,
                preflight_path=preflight,
                specialist_paths={role: agents[role] for role in design_moa.SPECIALIST_ROLES},
                director_path=agents["director"],
                artifact_root=self.outside / "runs",
                run_id="../escape",
            )

    def test_preflight_root_mismatch_is_rejected(self) -> None:
        preflight_payload = design_moa.build_preflight(self.repo)
        preflight_payload["repository"]["root"] = str(self.base)
        preflight = self.outside / "wrong-preflight.json"
        write(preflight, json.dumps(preflight_payload))
        agents = self.make_agent_files()
        with self.assertRaisesRegex(design_moa.DesignMoaError, "mismatch"):
            design_moa.create_run(
                repo=self.repo,
                preflight_path=preflight,
                specialist_paths={role: agents[role] for role in design_moa.SPECIALIST_ROLES},
                director_path=agents["director"],
                artifact_root=self.outside / "runs",
                run_id="wrong-root",
            )


if __name__ == "__main__":
    unittest.main()
