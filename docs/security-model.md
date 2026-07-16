# Security Model

## Trust boundary

The pull request branch is untrusted. A contributor or agent may change the
workflow, checker, policy, or any other file in the pull request. Therefore the
enforcement workflow is triggered with `pull_request_target` and checks out the
consuming repository's default branch, not the pull request branch.

The workflow only uses the pull request event and read-only GitHub API calls.
It does not execute scripts, install dependencies, or load configuration from
the pull request branch.

## Decision

The checker obtains the complete changed-file list and review list from the
GitHub API. A protected path requires an approval by the configured owner whose
review commit matches the current pull request head SHA. An approval for an
older commit is not accepted.

Owner-authored pull requests are allowed by default because `abuzucom` has no
second reviewer. Set `allow-owner-authored` to `false` in organizations with a
second-reviewer requirement.

## Defense in depth

This process must be combined with required pull requests, required status
checks, direct-push restrictions, least-privilege workflow permissions, and
secret protection. `CODEOWNERS` routes review requests; it does not enforce a
merge requirement unless branch protection requires it.
