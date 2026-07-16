# GitHub Settings

## Organization settings

In `abuzucom`, allow the consuming private repositories to access the private
`agamben` repository's Actions workflows. Restrict access to the
repositories that need the protection when organization settings permit that
choice.

## Repository settings

For each consuming repository:

- Require pull requests before merging the protected branch.
- Require the `Protected file review` status check.
- Require the normal build and test checks.
- Dismiss stale approvals when new commits are pushed.
- Restrict direct pushes to the protected branch.
- Confirm Actions can access the private reusable workflow repository.

Do not treat `CODEOWNERS` as a substitute for required branch protection. The
custom check is what implements the owner-authored exception.
