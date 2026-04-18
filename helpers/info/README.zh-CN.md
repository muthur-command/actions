# Muthur Command Helper: Info

从配置文件中提取构建元数据（支持架构、Docker 镜像与版本）。

## 输入参数

| 输入 | 必填 | 默认值 | 说明 |
|--------|----------|---------|----------------------------------------------------|
| `path` | 否 | `.` | 配置文件所在的相对目录路径 |

## 输出参数

| 输出 | 说明 |
|-----------------|--------------------------------------------------|
| `architectures` | 支持架构的 JSON 数组 |
| `image`         | 从应用配置文件读取的 Docker 镜像（可选） |
| `version`       | 从应用配置文件读取的版本（必需） |
| `name`          | 从应用配置文件读取的名称（必需） |
| `slug`          | 从应用配置文件读取的 slug（必需） |
| `description`   | 从应用配置文件读取的描述（必需） |
| `url`           | 从应用配置文件读取的 URL（可选） |

## 配置文件解析规则

Action 会在给定 `path` 下按扩展名顺序查找：`json`、`yml`、`yaml`。**先匹配到的文件优先生效**。

### 架构（Architectures）

按下方表格，从首个存在的文件解析：

| 优先级 | 文件 | 来源 | 说明 |
|----------|--------------|----------------------|---------------------------------------------------------------------------------------|
| 1 | `build.*` | `.build_from`（键名） | **已弃用** — 基础镜像、构建参数与标签应迁移到 Dockerfile |
| 2 | `config.*` | `.arch` | 应用配置 — 架构直接列在 `arch` 字段中 |

若两类文件都不存在，`architectures` 默认值为 `[]`。

### 应用元数据（App Metadata）

从 `config.*`（应用配置，按扩展名首个匹配）读取：

| 字段 | 必填 | 输出示例 |
|----------------|----------|------------------------------------------------|
| `.name`        | 是 | `"Example App"` |
| `.version`     | 是 | `"2024.12.1"` |
| `.slug`        | 是 | `"example_app"` |
| `.description` | 是 | `"An example Muthur Command app"` |
| `.arch`        | 是 | `["amd64","aarch64"]` |
| `.image`       | 否 | `"ghcr.io/muthur-command/{arch}-app-example"` |
| `.url`         | 否 | `"https://github.com/muthur-command/addons-example"` |

每个缺失或为 null 的必填字段都会输出一条 warning。完整说明见 [应用配置](https://www.muthur-command.com/docs/docs/add-ons/configuration)。

若不存在任何 `config.*` 文件，所有字符串输出字段默认值为 `""`。

## 使用示例

```yaml
- uses: muthur-command/actions/helpers/info@mc
  id: info
  with:
    path: my-app

- run: |
    echo "Architectures: ${{ steps.info.outputs.architectures }}"
    echo "Image: ${{ steps.info.outputs.image }}"
    echo "Version: ${{ steps.info.outputs.version }}"
    echo "Name: ${{ steps.info.outputs.name }}"
    echo "Slug: ${{ steps.info.outputs.slug }}"
    echo "Description: ${{ steps.info.outputs.description }}"
    echo "URL: ${{ steps.info.outputs.url }}"
```
