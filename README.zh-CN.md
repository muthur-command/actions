# actions

面向 **Muthur Command** 工作流的可复用 **GitHub Actions** 与各 helper。

## 辅助组件

_下列 GitHub Action helper 视为 **Muthur Command** 在 GitHub 上的组织内部工具，可能在没有事先公告的情况下发生变更。_

- [git-init](./helpers/git-init/action.yml)
- [info](./helpers/info/action.yml)
- [jq](./helpers/jq/action.yml)
- [verify-version](./helpers/verify-version/action.yml)
- [version](./helpers/version/action.yml)
- [version-push](./helpers/version-push/action.yml)

## 来源

- **上游：** [home-assistant/actions](https://github.com/home-assistant/actions) — 面向 Home Assistant 工作流的 GitHub Actions，本目录由其移植而来。
- **本仓库：** **Muthur Command** 在此维护该副本，供 **Muthur Command OS** 的 CI 使用；helpers 及行为可能随时间与上游产生差异。
- **许可：** 自上游继承的代码仍为 **Apache-2.0**；见 [`LICENSE`](./LICENSE)。
