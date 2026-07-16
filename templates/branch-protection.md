# Branch Protection Checklist

Apply these settings to each protected default branch in `abuzucom`:

- Require a pull request before merging.
- Require the `Protected file review` status check.
- Require the normal build and test checks.
- Dismiss stale approvals when new commits are pushed.
- Restrict direct pushes to the protected branch.
- Do not rely on CODEOWNERS alone; the status check must be required.
- Confirm private reusable-workflow access is enabled for the repository.

The owner-authored exception is implemented by the custom check. Do not enable
a global code-owner approval rule if it would make `itsjustatank`'s protected
pull requests unmergeable.
