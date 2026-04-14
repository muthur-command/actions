# Muthur Command Helper: Version

根据构建类型与 GitHub 事件触发方式，计算 Muthur Command 构建产物的 **version**、**stable**、**channel** 与 **publish** 状态。

## 输入参数

| 输入 | 必填 | 默认值 | 说明 |
|--------|----------|-----------|----------------------------------------------------------|
| `type` | 否 | `generic` | 目标类型：`core`、`supervisor`、`plugin` 或 `generic` |

## 输出参数

| 输出 | 说明 |
|-----------|------------------------------------------------------|
| `version` | 解析后的版本字符串 |
| `stable`  | 稳定版本时为 `"true"`，否则为 `"false"` |
| `channel` | 建议更新通道（`dev`、`beta` 或 `stable`） |
| `publish` | 是否应发布构建产物（`"true"` / `"false"`） |

## 手动覆盖（workflow_dispatch）

所有输出都可通过 `github.event.inputs` 覆盖：

| 输入项 | 覆盖字段 |
|---------------------------------|-----------|
| `github.event.inputs.version`   | `version` |
| `github.event.inputs.stable`    | `stable`  |
| `github.event.inputs.channel`   | `channel` |
| `github.event.inputs.publish`   | `publish` |

只要上述任一输入被设置，即对后续自动计算结果拥有**最高优先级**。

---

## 构建类型：`plugin` / `supervisor`

这两种类型的输出逻辑一致。

| 触发方式 | version | stable | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `<commit SHA>`                   | `false` | `dev`   | `false` |
| **Push 到 master**   | CalVer 开发版 `YYYY.MM.X.devDDNN` | `false` | `dev`   | `true`  |
| **Release（tag）**   | 标签名（如 `2024.12.1`）          | `true`  | `beta`  | `true`  |
| **Push 到 tag**      | 标签名                            | `false` | `dev`   | `true`  |
| **workflow_dispatch** | 来自 inputs 或 ref              | 来自 inputs 或 `false` | 来自 inputs 或自动计算 | 来自 inputs 或 `false` |

### 说明
- **PR 构建永不发布。** 只要存在 `github.head_ref`（PR 事件会设置），就会强制 `publish=false`。
- **Push 到 master** 会生成 [CalVer](https://calver.org/) 开发版本：基线是 `YYYY.MM.N`（从最近匹配 tag 递增），后缀为 `.devDDNN`，其中 `DD` 为 UTC 日期，`NN` 为当天 UTC 零点后的提交计数（补零）。
- **稳定发布** 的 channel 为 `beta`（不是 `stable`），这是 plugin/supervisor 的既定行为。
- **说明：** `supervisor` 过去会在版本解析后额外修改 `supervisor/const.py` 里的 `SUPERVISOR_VERSION`，该副作用已移除。

---

## 构建类型：`core`

| 触发方式 | version | stable | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `merge`（ref 末段字面值）        | `false` | _(未设置)_ | `false` |
| **Push 到 `dev` 分支** | Nightly 递增（经 `version_bump.py`） | `false` | `dev` | `false` |
| **Release（tag `X.Y.Z`）** | `X.Y.Z`                   | `true`  | `stable` | `true`  |
| **Release（tag `X.Y.ZbN`）** | `X.Y.ZbN`               | `true`  | `beta`  | `true`  |
| **Push 到 tag `X.Y.ZdevN`** | `X.Y.ZdevN`             | `false` | `dev`   | `false` |
| **workflow_dispatch** | 来自 inputs 或 ref              | 来自 inputs 或 `false` | 来自 inputs 或自动计算 | 来自 inputs 或 `false` |

### 说明
- **channel 由版本字符串本身推导：**
  - 包含 `dev` -> `dev`
  - 包含 `b` -> `beta`
  - 其他情况 -> `stable`
- **仅 release 事件会发布**（`event_name == release`）。push、PR 及其他事件均为 `publish=false`。
- **Nightly 开发构建** 在 push 到 `dev` 分支时触发：使用 `uv` 安装依赖后执行 `script/version_bump.py nightly`，基于 `pyproject.toml` 计算下一个开发版本。
- plugin/supervisor/generic 使用的 CalVer 开发版本规则**不适用于** core。

---

## 构建类型：`generic`

| 触发方式 | version | stable | channel | publish |
|----------------------|----------------------------------|---------|---------|---------|
| **Pull Request**     | `<commit SHA>`                   | `false` | _(未设置)_ | _(未设置)_ |
| **Push 到 master**   | CalVer 开发版 `YYYY.MM.X.devDDNN` | `false` | _(未设置)_ | _(未设置)_ |
| **Release（tag）**   | 标签名                            | `true`  | _(未设置)_ | _(未设置)_ |
| **Push 到 tag**      | 标签名                            | `false` | _(未设置)_ | _(未设置)_ |
| **workflow_dispatch** | 来自 inputs 或 ref              | 来自 inputs 或 `false` | 来自 inputs 或 _(未设置)_ | 来自 inputs 或 _(未设置)_ |

### 说明
- `generic` 类型下，**channel 与 publish 仅在 workflow_dispatch 手动传入时才会设置**；action 不会自动计算这两项。
- master/main 的 version 计算沿用 plugin/supervisor 的 CalVer 开发版规则。
- PR 构建会解析为 commit SHA（与 plugin/supervisor 一致）。

---

## Version 解析流程图

```
github.event.inputs.version 是否已设置？
├─ 是  -> 直接使用该值
└─ 否
   ├─ ref 是 master/main 且 type 为 supervisor/plugin/generic？
   │  └─ 是 -> CalVer 开发版：YYYY.MM.X.devDDNN
   ├─ ref 是 "merge" 且 type 为 supervisor/plugin/generic？
   │  └─ 是 -> commit SHA
   ├─ ref 是 "dev" 且 type 为 core？
   │  └─ 是 -> 通过 version_bump.py 做 nightly 递增
   └─ 其他 -> 从 ref 提取版本（路径最后一段）
```

## CalVer 开发版格式

`supervisor`、`plugin`、`generic` 在 push 到 master/main 时使用：

```
YYYY.MM.N.devDDNN
│    │  │     │ └─ UTC 零点后提交计数（补零）
│    │  │     └─── UTC 日
│    │  └───────── patch 号（从最近匹配 tag 递增，否则从 0）
│    └──────────── 月
└───────────────── 年
```

示例：`2024.12.3.dev1405` = 2024 年 12 月，patch=3，UTC 当月第 14 天，当天零点后第 5 次提交。
