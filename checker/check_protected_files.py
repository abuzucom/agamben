"""Require current owner approval for sensitive pull-request changes."""

from __future__ import annotations

import fnmatch
import json
import os
import sys
import urllib.request
from pathlib import PurePosixPath
from typing import Any


DEFAULT_POLICY = {
    "owner": "itsjustatank",
    "allow_owner_authored": True,
    "max_file_pages": 50,
    "max_review_pages": 50,
    "protected_file_names": [],
    "protected_prefixes": [],
    "protected_globs": [],
}


def load_event() -> dict[str, Any]:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as event_file:
        value = json.load(event_file)
    if not isinstance(value, dict):
        raise RuntimeError("GitHub event must be a JSON object")
    return value


def load_policy() -> dict[str, Any]:
    path = os.environ.get("PROTECTED_FILES_POLICY")
    policy = dict(DEFAULT_POLICY)
    if path:
        with open(path, encoding="utf-8") as policy_file:
            configured = json.load(policy_file)
        if not isinstance(configured, dict):
            raise RuntimeError("protected-file policy must be a JSON object")
        policy.update(configured)
    if os.environ.get("PROTECTED_FILES_OWNER"):
        policy["owner"] = os.environ["PROTECTED_FILES_OWNER"]
    if "PROTECTED_FILES_ALLOW_OWNER_AUTHORED" in os.environ:
        policy["allow_owner_authored"] = os.environ[
            "PROTECTED_FILES_ALLOW_OWNER_AUTHORED"
        ].lower() == "true"
    return policy


def is_protected(path: str, policy: dict[str, Any]) -> bool:
    normalized = path.replace("\\", "/").lstrip("/")
    name = PurePosixPath(normalized).name
    if name in policy["protected_file_names"]:
        return True
    if any(normalized.startswith(prefix) for prefix in policy["protected_prefixes"]):
        return True
    return any(fnmatch.fnmatch(normalized, pattern) for pattern in policy["protected_globs"])


def github_get(path: str) -> Any:
    token = os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def pull_request_details(event: dict[str, Any]) -> tuple[str, int, str]:
    pull_request = event.get("pull_request")
    repository = event.get("repository", {})
    if not isinstance(pull_request, dict) or not isinstance(repository, dict):
        raise RuntimeError("pull request event data is missing")
    repository_name = repository.get("full_name")
    number = pull_request.get("number")
    head = pull_request.get("head")
    head_sha = head.get("sha") if isinstance(head, dict) else None
    if not isinstance(repository_name, str) or not isinstance(number, int):
        raise RuntimeError("pull request repository or number is missing")
    if not isinstance(head_sha, str) or not head_sha:
        raise RuntimeError("pull request head SHA is missing")
    return repository_name, number, head_sha


def changed_files(event: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    repository, number, _ = pull_request_details(event)
    files: list[str] = []
    max_pages = int(policy["max_file_pages"])
    for page in range(1, max_pages + 1):
        batch = github_get(
            f"/repos/{repository}/pulls/{number}/files?per_page=100&page={page}"
        )
        if not isinstance(batch, list):
            raise RuntimeError("GitHub returned an invalid changed-files response")
        files.extend(item["filename"] for item in batch if isinstance(item, dict))
        if len(batch) < 100:
            return files
    raise RuntimeError(f"pull request file list exceeded {max_pages * 100} files")


def current_owner_approval(event: dict[str, Any], policy: dict[str, Any]) -> bool:
    repository, number, head_sha = pull_request_details(event)
    owner = str(policy["owner"]).lower()
    max_pages = int(policy["max_review_pages"])
    for page in range(1, max_pages + 1):
        reviews = github_get(
            f"/repos/{repository}/pulls/{number}/reviews?per_page=100&page={page}"
        )
        if not isinstance(reviews, list):
            raise RuntimeError("GitHub returned an invalid reviews response")
        if any(
            isinstance(review, dict)
            and review.get("user", {}).get("login", "").lower() == owner
            and review.get("state") == "APPROVED"
            and review.get("commit_id") == head_sha
            for review in reviews
        ):
            return True
        if len(reviews) < 100:
            return False
    raise RuntimeError(f"review list exceeded {max_pages * 100} reviews")


def requires_owner_approval(event: dict[str, Any], policy: dict[str, Any]) -> bool:
    pull_request = event.get("pull_request")
    user = pull_request.get("user") if isinstance(pull_request, dict) else None
    author = user.get("login", "") if isinstance(user, dict) else ""
    if not isinstance(author, str) or not author:
        raise RuntimeError("pull request author is missing")
    return not (
        policy["allow_owner_authored"]
        and author.lower() == str(policy["owner"]).lower()
    )


def main() -> int:
    event = load_event()
    policy = load_policy()
    protected = sorted(
        path for path in changed_files(event, policy) if is_protected(path, policy)
    )
    if not protected:
        print("No protected files changed.")
        return 0
    print("Protected files changed:")
    print("\n".join(f"- {path}" for path in protected))
    if not requires_owner_approval(event, policy):
        print(f"Owner-authored PR from @{policy['owner']}; no self-approval required.")
        return 0
    if current_owner_approval(event, policy):
        print(f"Current approval from @{policy['owner']} found.")
        return 0
    print(
        f"Approval from @{policy['owner']} on the current commit is required.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
