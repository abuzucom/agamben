# Copyable Templates

Use the templates when a repository should vendor the protection instead of
depending on a private reusable workflow.

Copy these files:

- `templates/protected-file-review.yml` as the caller workflow, then replace
  the reusable call with the local checker steps.
- `templates/CODEOWNERS` as `.github/CODEOWNERS` and adjust its paths.
- `templates/policy.json` as the repository's policy file.
- `checker/check_protected_files.py` into a trusted `checker/` directory.

The checker must run from trusted base-branch code under `pull_request_target`.
Do not combine it with a checkout of the pull request ref.
