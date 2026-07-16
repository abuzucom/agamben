# Agent Authentication

Agents opening pull requests must use a separate bot or GitHub App identity,
not `itsjustatank`'s personal token. This makes the owner-authored exception
meaningful: agent changes to protected files require an explicit approval from
`itsjustatank`.

The agent identity should have only the permissions needed to create branches
and pull requests. It should not be allowed to bypass branch protection or
push directly to the protected branch.

After an agent pushes a new commit, the owner must approve that current commit.
The checker intentionally rejects an approval attached to an earlier head SHA.
