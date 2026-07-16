# agamben

Reusable GitHub protections for repository files that can change automation,
agent behavior, dependencies, deployment, or runtime behavior.

This repository is intended for private repositories in the `abuzucom`
organization. The default policy owner is `itsjustatank`.

## Security model

The caller workflow must use `pull_request_target`. The reusable workflow checks
out only the consuming repository's trusted default branch and never executes
code from the pull request branch. It uses the GitHub API to inspect changed
files and reviews.

Protected changes pass when either:

- The pull request changes no protected files.
- The pull request is authored by `itsjustatank`.
- `itsjustatank` approved the current pull request head commit.

The owner-authored exception is intentional because this organization has no
second reviewer. A separate bot or GitHub App identity should be used for
agent-authored pull requests.

## Quick start

Add this workflow to the consuming repository on its default branch:

```yaml
name: Protected file review

on:
  pull_request_target:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: read

jobs:
  protected-file-review:
    uses: abuzucom/agamben/.github/workflows/protected-file-review.yml@v1
    with:
      owner: itsjustatank
      allow-owner-authored: true
```

Then enable the `Protected file review` check as a required status check on the
protected branch. See [docs/installation.md](docs/installation.md) and
[docs/github-settings.md](docs/github-settings.md).

## Agent conventions

`AGENTS.md` is the canonical instruction file. Tool-specific files are synced
copies. Run `make sync` after changing `AGENTS.md`; run `make check` in CI.

The instructions cover safe commands, tests, API compatibility, secrets,
dependencies, execution paths, resource bounds, logging, path traversal,
idempotency, performance, naming, and prose style.

Use a separate bot or GitHub App identity for agent-authored pull requests.
Protected-file changes from that identity require owner approval.

## Release policy

Use a version tag such as `v1` for convenience, but pin production consumers
to a reviewed commit SHA when practical. Changes to this repository's workflow,
action, policy, and templates require review from `itsjustatank`.

## Alternatives

Repositories that should not depend on a private reusable workflow can copy the
files in `templates/` and `checker/`. The local action is available at
`action/protected-file-review/action.yml`.
