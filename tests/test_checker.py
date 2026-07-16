import unittest

from checker.check_protected_files import (
    DEFAULT_POLICY,
    is_protected,
    requires_owner_approval,
)


class ProtectedFileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = dict(DEFAULT_POLICY)
        self.policy.update(
            {
                "protected_file_names": ["AGENTS.md", "package.json"],
                "protected_prefixes": [".github/", "scripts/"],
                "protected_globs": ["**/*.html"],
            }
        )

    def test_protects_instruction_and_automation_files(self) -> None:
        for path in ("AGENTS.md", "nested/AGENTS.md", ".github/deploy.yml", "scripts/sync.py"):
            with self.subTest(path=path):
                self.assertTrue(is_protected(path, self.policy))

    def test_protects_configured_globs(self) -> None:
        self.assertTrue(is_protected("src/index.html", self.policy))

    def test_leaves_unconfigured_files_unprotected(self) -> None:
        self.assertFalse(is_protected("README.md", self.policy))
        self.assertFalse(is_protected("src/style.css", self.policy))

    def test_owner_authored_change_does_not_require_self_approval(self) -> None:
        event = {"pull_request": {"user": {"login": "itsjustatank"}}}
        self.assertFalse(requires_owner_approval(event, self.policy))

    def test_agent_authored_change_requires_owner_approval(self) -> None:
        event = {"pull_request": {"user": {"login": "automation-bot"}}}
        self.assertTrue(requires_owner_approval(event, self.policy))

    def test_owner_exception_can_be_disabled(self) -> None:
        self.policy["allow_owner_authored"] = False
        event = {"pull_request": {"user": {"login": "itsjustatank"}}}
        self.assertTrue(requires_owner_approval(event, self.policy))

    def test_missing_author_fails_closed(self) -> None:
        with self.assertRaises(RuntimeError):
            requires_owner_approval({"pull_request": {}}, self.policy)


if __name__ == "__main__":
    unittest.main()
