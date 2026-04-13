# actions

Reusable **GitHub Actions** and helpers for **MCOS** / **muthur-command** CI workflows.

## Helpers

| Helper | Path |
|--------|------|
| git-init | [helpers/git-init](./helpers/git-init/action.yml) |
| info | [helpers/info](./helpers/info/action.yml) |
| jq | [helpers/jq](./helpers/jq/action.yml) |
| verify-version | [helpers/verify-version](./helpers/verify-version/action.yml) |
| version | [helpers/version](./helpers/version/action.yml) |
| version-push | [helpers/version-push](./helpers/version-push/action.yml) |
| find-addons | [helpers/find-addons](./helpers/find-addons/action.yml) |
| lock-issues | [helpers/lock-issues](./helpers/lock-issues/action.yml) |

These helpers are **internal** to the **muthur-command** org; behavior may change without a major announcement — pin by tag or SHA in production workflows.

## Derivative work

Upstream-derived components retain **Apache-2.0** (see **LICENSE**). Add a **NOTICE** for MCOS when legal approves.
