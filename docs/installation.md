# Installation

## Reusable workflow

Copy `templates/protected-file-review.yml` to
`.github/workflows/protected-file-review.yml` in the consuming repository.
Commit it to the default branch before testing the protection.

The caller must use `pull_request_target`, because a normal `pull_request`
workflow would not provide the trusted-base execution model used here.

## Policy customization

Copy `templates/policy.json` to a path such as
`.github/protected-files-policy.json`. Pass that path to the reusable workflow:

```yaml
with:
  owner: itsjustatank
  allow-owner-authored: true
  policy-file: .github/protected-files-policy.json
```

The policy file must be present on the trusted default branch. Changes to it
are protected by the workflow's owner review requirement.

## Local copy

For repositories that cannot access private reusable workflows, copy the
checker directory, policy file, and workflow implementation from `checker/`,
`templates/`, and `.github/workflows/`. Keep the checker on the default branch
and do not execute a version from the pull request.
