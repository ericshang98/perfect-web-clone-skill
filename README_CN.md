# Perfect Web Clone

> 将任意网页完美克隆为可运行的生产级代码

一个 Claude Code Skill，使用 Playwright 提取网页，基于三原则智能分块内容，并行生成 React/Next.js/Vue 组件。

## 特性

- **像素级复刻** - 忠实还原原始设计
- **智能分块** - 三原则算法确保完整性
- **并行生成** - 多个 Agent 同时工作
- **多框架支持** - Next.js、React、Vue 等
- **完整数据提取** - 30+ 种数据类型，包括 CSS 动画、主题、交互状态

## 安装

### 1. 克隆到 Claude Code skills 目录

**个人使用（所有项目可用）：**
```bash
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone
```

**项目使用（团队成员可用）：**
```bash
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone
```

### 2. 安装 Python 依赖

```bash
cd ~/.claude/skills/perfect-web-clone/scripts  # 或 .claude/skills/...
pip install -r requirements.txt
playwright install chromium
```

### 3. 重启 Claude Code

Skill 会被自动检测到。

## 使用方法

直接告诉 Claude Code 你想克隆什么：

```
用 Next.js 克隆 https://stripe.com
```

```
复制这个落地页：https://linear.app，使用 React 和 Tailwind
```

```
克隆 https://example.com，用 5 个并行 agent 加速生成
```

## 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│  1. 页面提取 (Playwright)                                   │
│     - DOM 树及计算样式                                       │
│     - 全页截图                                               │
│     - CSS 变量、动画、过渡效果                                │
│     - 主题检测（明/暗模式）                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 智能分块（三原则）                                       │
│     - 互斥性：块之间绝不重叠                                  │
│     - 完整性：块组合后覆盖整个页面                            │
│     - 可控性：每块 < 50K tokens                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 并行代码生成                                             │
│     ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│     │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent N │        │
│     │  头部   │ │  Hero   │ │  功能区  │ │  底部   │        │
│     └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘        │
│          ↓           ↓           ↓           ↓              │
│     Header.tsx  Hero.tsx  Features.tsx  Footer.tsx          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 项目组装                                                 │
│     - 生成导入所有组件的主页面                                │
│     - 配置 Tailwind CSS                                      │
│     - 用户运行：npm install && npm run dev                   │
└─────────────────────────────────────────────────────────────┘
```

## 三原则

### 1. 互斥性
块之间**绝不重叠**。页面的每个部分只由一个 Agent 处理，不会有冲突。

### 2. 完整性
所有块组合起来等于**整个页面**。不会丢失或遗漏任何内容。

### 3. 可控性
每个块**小于 50,000 tokens**。大的 section 会自动拆分成可管理的小块。

## 并行配置

| 命令 | 行为 |
|------|------|
| "克隆这个页面" | 默认：3 个并行 agent |
| "用 5 个并行克隆" | 精确 5 个 agent |
| "最快速度克隆" | 所有 section 并行 |
| "逐个克隆" | 串行（1 个 agent）|

## 支持的技术栈

| 框架 | 样式 | 说明 |
|------|------|------|
| Next.js | Tailwind CSS | 默认，推荐 |
| React | Tailwind CSS | Create React App |
| Vue 3 | Tailwind CSS | Composition API |
| HTML | 原生 CSS | 静态网站 |

## 文档

- [SKILL.md](SKILL.md) - 主要 Skill 说明
- [docs/EXTRACTION.md](docs/EXTRACTION.md) - 页面提取详情
- [docs/CHUNKING.md](docs/CHUNKING.md) - 三原则算法
- [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md) - 组件生成指南

## 环境要求

- Python 3.8+
- Node.js 18+
- Claude Code

## 关于

**Perfect Web Clone** 是由 [Nexting.ai](https://nexting.ai) 开源的 Claude Code Skill。

想要完整的可视化体验？包括：
- 浏览器内实时预览
- 可视化差异对比
- 一键部署
- 团队协作

访问 [nexting.ai](https://nexting.ai) 试用我们的全功能 AI Web 开发平台。

## 许可证

MIT 许可证 - 可免费用于个人和商业用途。

## 贡献

欢迎贡献！提交 PR 前请阅读我们的贡献指南。

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 支持

- [GitHub Issues](https://github.com/anthropics/perfect-web-clone-skill/issues)
- [Nexting.ai Discord](https://discord.gg/nexting)
