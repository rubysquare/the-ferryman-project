"""
Unit tests for Ferryman packaging, distribution, and repository governance.
Verifies pyproject.toml, install.sh, Homebrew formula, and issue templates.
"""

import os
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from ferryman.cli import VERSION

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPackagingAndDistribution(unittest.TestCase):

    def test_pyproject_toml_exists_and_valid(self) -> None:
        pyproject_path = REPO_ROOT / "pyproject.toml"
        self.assertTrue(pyproject_path.exists(), "pyproject.toml must exist")

        content = pyproject_path.read_text(encoding="utf-8")
        self.assertIn('[project]', content)
        self.assertIn('name = "ferryman"', content)
        self.assertIn(f'version = "{VERSION}"', content)
        self.assertIn('dependencies = []', content)
        self.assertIn('ferryman = "ferryman.cli:main"', content)
        self.assertIn('AGPL', content)

    def test_setup_py_exists_and_valid(self) -> None:
        setup_path = REPO_ROOT / "setup.py"
        self.assertTrue(setup_path.exists(), "setup.py must exist for backward compatibility")
        content = setup_path.read_text(encoding="utf-8")
        self.assertIn('name="ferryman"', content)
        self.assertIn(f'version="{VERSION}"', content)
        self.assertIn('"ferryman = ferryman.cli:main"', content)
        self.assertIn('exclude=["tests*", "connectors*"]', content)

    def test_package_module_execution(self) -> None:
        # Test python3 -m ferryman --version
        proc_ver = subprocess.run(
            [sys.executable, "-m", "ferryman", "--version"],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(proc_ver.returncode, 0, f"-m ferryman --version failed: {proc_ver.stderr}")
        self.assertIn(f"The Ferryman Project v{VERSION}", proc_ver.stdout)

        # Test python3 -m ferryman --help
        proc_help = subprocess.run(
            [sys.executable, "-m", "ferryman", "--help"],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(proc_help.returncode, 0, f"-m ferryman --help failed: {proc_help.stderr}")
        self.assertIn("Usage:", proc_help.stdout)
        self.assertIn("python3 -m ferryman", proc_help.stdout)

    def test_cli_argument_parsing(self) -> None:
        from ferryman.cli import parse_args, get_help_text

        # Test space-separated and equals-separated flags
        args, voice, rate, fast, window = parse_args(["dawn", "--rate=180", "--window=07:00-09:00", "--fast", "--voice"])
        self.assertEqual(args, ["dawn"])
        self.assertTrue(voice)
        self.assertEqual(rate, 180)
        self.assertTrue(fast)
        self.assertEqual(window, "07:00-09:00")

        # Test space-separated flags
        args, voice, rate, fast, window = parse_args(["pause", "--rate", "200", "--window", "12:00-13:00", "--no-delay"])
        self.assertEqual(args, ["pause"])
        self.assertFalse(voice)
        self.assertEqual(rate, 200)
        self.assertTrue(fast)
        self.assertEqual(window, "12:00-13:00")

        # Test help text generation
        help_text = get_help_text("ferryman")
        self.assertIn("ferryman [command] [options]", help_text)

    def test_homebrew_formula_exists_and_valid(self) -> None:
        formula_path = REPO_ROOT / "Formula" / "ferryman.rb"
        self.assertTrue(formula_path.exists(), "Formula/ferryman.rb must exist")
        content = formula_path.read_text(encoding="utf-8")
        self.assertIn("class Ferryman < Formula", content)
        self.assertIn("AGPL-3.0-or-later", content)
        self.assertIn("formula_opt_bin", content)
        self.assertNotIn('desc "An ', content, "Homebrew desc must not start with an article")
        self.assertNotIn('desc "The ', content, "Homebrew desc must not start with an article")
        self.assertIn("def install", content)
        self.assertIn("test do", content)

    def test_install_script_lifecycle(self) -> None:
        install_sh = REPO_ROOT / "install.sh"
        self.assertTrue(install_sh.exists(), "install.sh must exist")
        self.assertTrue(os.access(str(install_sh), os.X_OK), "install.sh must be executable")

        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Run install.sh with custom prefix containing a space
            target_prefix = os.path.join(temp_dir, "custom prefix")
            proc = subprocess.run(
                [str(install_sh), "--prefix", target_prefix],
                cwd=str(REPO_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc.returncode, 0, f"install.sh failed:\n{proc.stderr}")
            self.assertIn("The Ferryman has arrived", proc.stdout)

            # 2. Verify files created
            installed_bin = Path(target_prefix) / "bin" / "ferryman"
            installed_share = Path(target_prefix) / "share" / "ferryman" / "ferryman"
            self.assertTrue(installed_bin.exists(), "Launcher binary must exist")
            self.assertTrue(os.access(str(installed_bin), os.X_OK), "Launcher must be executable")
            self.assertTrue(installed_share.exists(), "Package directory must exist in share")
            self.assertTrue((installed_share / "__init__.py").exists(), "Package __init__.py must exist")

            # 3. Test running the installed binary
            proc_ver = subprocess.run(
                [str(installed_bin), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc_ver.returncode, 0)
            self.assertIn(f"The Ferryman Project v{VERSION}", proc_ver.stdout)

            proc_help = subprocess.run(
                [str(installed_bin), "--help"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc_help.returncode, 0)
            self.assertIn("Usage:", proc_help.stdout)

            # 4. Run uninstall
            proc_un = subprocess.run(
                [str(install_sh), "--prefix", target_prefix, "--uninstall"],
                cwd=str(REPO_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc_un.returncode, 0)
            self.assertFalse(installed_bin.exists(), "Launcher binary must be removed")
            self.assertFalse(installed_share.parent.exists(), "Share directory must be removed")

    def test_install_script_piped_execution(self) -> None:
        """Tests executing install.sh via pipe with FERRYMAN_SOURCE_DIR set."""
        install_sh = REPO_ROOT / "install.sh"
        pkg_dir = REPO_ROOT / "ferryman"

        with tempfile.TemporaryDirectory() as temp_dir:
            target_prefix = os.path.join(temp_dir, "piped_install")
            env = dict(os.environ)
            env["FERRYMAN_SOURCE_DIR"] = str(pkg_dir)

            with open(install_sh, "r", encoding="utf-8") as f:
                script_content = f.read()

            proc = subprocess.run(
                ["sh", "-s", "--", "--prefix", target_prefix],
                input=script_content,
                env=env,
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc.returncode, 0, f"Piped install failed:\n{proc.stderr}")
            self.assertIn("The Ferryman has arrived", proc.stdout)

            installed_bin = Path(target_prefix) / "bin" / "ferryman"
            self.assertTrue(installed_bin.exists(), "Installed binary from pipe must exist")

            proc_ver = subprocess.run(
                [str(installed_bin), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc_ver.returncode, 0)
            self.assertIn(f"The Ferryman Project v{VERSION}", proc_ver.stdout)

            # Uninstall via piped execution
            proc_un = subprocess.run(
                ["sh", "-s", "--", "--prefix", target_prefix, "--uninstall"],
                input=script_content,
                env=env,
                cwd=temp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.assertEqual(proc_un.returncode, 0)
            self.assertFalse(installed_bin.exists())

    def test_contributing_and_governance(self) -> None:
        contrib_path = REPO_ROOT / "CONTRIBUTING.md"
        self.assertTrue(contrib_path.exists(), "CONTRIBUTING.md must exist")
        content = contrib_path.read_text(encoding="utf-8")
        self.assertIn("Anti-Feature Charter", content)
        self.assertIn("Rejection-by-Design Checklist", content)
        self.assertIn("Streaks", content)
        self.assertIn("Zero telemetry", content)

    def test_github_issue_templates(self) -> None:
        templates_dir = REPO_ROOT / ".github" / "ISSUE_TEMPLATE"
        self.assertTrue(templates_dir.exists(), ".github/ISSUE_TEMPLATE must exist")

        bug_report = templates_dir / "bug_report.yml"
        self.assertTrue(bug_report.exists(), "bug_report.yml must exist")
        bug_content = bug_report.read_text(encoding="utf-8")
        self.assertIn("Bug Report", bug_content)

        proposal = templates_dir / "feature_proposal.yml"
        self.assertTrue(proposal.exists(), "feature_proposal.yml must exist")
        prop_content = proposal.read_text(encoding="utf-8")
        self.assertIn("Feature Proposal", prop_content)
        self.assertIn("Guardrail Defense Checklist", prop_content)

        config = templates_dir / "config.yml"
        self.assertTrue(config.exists(), "config.yml must exist")
        cfg_content = config.read_text(encoding="utf-8")
        self.assertIn("blank_issues_enabled: false", cfg_content)


if __name__ == "__main__":
    unittest.main()
