# Actions

用于 **MCOS** / **muthur-command** CI 工作流的可复用 **GitHub Actions** 与辅助组件。

## 辅助组件

| 组件 | 路径 |
|--------|------|
| git-init | [helpers/git-init](./helpers/git-init/action.yml) |
| info | [helpers/info](./helpers/info/action.yml) |
| jq | [helpers/jq](./helpers/jq/action.yml) |
| verify-version | [helpers/verify-version](./helpers/verify-version/action.yml) |
| version | [helpers/version](./helpers/version/action.yml) |
| version-push | [helpers/version-push](./helpers/version-push/action.yml) |
| find-addons | [helpers/find-addons](./helpers/find-addons/action.yml) |
| lock-issues | [helpers/lock-issues](./helpers/lock-issues/action.yml) |

这些 helper 为 **muthur-command** 组织内部使用；行为可能在没有主版本公告的情况下变更。生产工作流中请固定 tag 或 SHA。

## 衍生说明

源自上游的组件保持 **Apache-2.0**（见 **LICENSE**）。MCOS 的 **NOTICE** 文件待法务批准后补充。
