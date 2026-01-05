# Perfect Web Clone

<div align="center">

**一个用于克隆网页的 Claude Code Skill**

[English](README.md) | 中文

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](https://claude.ai)

</div>

---

一个 Claude Code Skill，能够将任意网页克隆为像素级还原的 React/Next.js/Vue 代码。

> 由 [Nexting.ai](https://nexting.ai) 创建

---

## 这是什么？

这是一个 Claude Code 的 **Skill**（技能）—— 一套教会 Claude Code 如何克隆网页的指令集。安装后，你只需要告诉 Claude Code：

```
克隆 https://stripe.com
```

它会自动：
1. 使用 Playwright 提取页面
2. 将页面切分为可管理的区块
3. 并行生成 React/Next.js/Vue 组件
4. 组装成完整可运行的项目

**你不需要手动运行任何脚本** —— Claude Code 会处理一切。

---

## 安装

### 方式一：个人安装（所有项目可用）

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone

# 安装依赖
cd ~/.claude/skills/perfect-web-clone/scripts
pip install -r requirements.txt
playwright install chromium
```

### 方式二：项目安装（团队共享）

```bash
# 克隆到你的项目
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone

# 安装依赖（同上）
```

重启 Claude Code，Skill 会被自动检测到。

---

## 使用方法

直接用自然语言告诉 Claude Code：

| 你说的话 | 效果 |
|----------|------|
| `克隆 https://stripe.com` | 用 Next.js 克隆（默认） |
| `用 React 克隆 https://linear.app` | 用 React 克隆 |
| `Clone https://example.com with Vue` | 用 Vue 3 克隆 |
| `用 5 个并行 agent 克隆 https://example.com` | 更多 agent 更快 |
| `最快速度克隆 https://example.com` | 最大并行度 |

克隆完成后，运行：
```bash
npm install && npm run dev
```

---

## 克隆内容

| 方面 | 覆盖范围 |
|------|----------|
| **布局** | Flexbox、Grid、定位 |
| **样式** | 颜色、排版、间距、阴影、边框 |
| **图片** | 所有图片，保留原始 URL |
| **动画** | CSS 动画、过渡、悬停效果 |
| **主题** | 明/暗模式检测 |
| **响应式** | 保留断点 |

---

## 工作原理（概览）

```
你的命令: "克隆 https://example.com"
                    ↓
    ┌───────────────────────────────┐
    │  1. 提取页面 (Playwright)     │
    │  2. 切分为区块               │
    │  3. 生成组件                 │  ← Claude Code 自动完成
    │  4. 组装项目                 │
    └───────────────────────────────┘
                    ↓
         可运行的项目
```

这个 Skill 使用：
- **Playwright** 抓取 DOM、样式、截图
- **三原则** 分块算法（不重叠、完整覆盖、大小可控）
- **并行 Agent** 加速代码生成

技术细节见 [工作原理（详细）](#工作原理详细)。

---

## 支持的框架

| 框架 | 样式 | 命令 |
|------|------|------|
| Next.js（默认） | Tailwind CSS | `克隆 https://...` |
| React | Tailwind CSS | `用 React 克隆 https://...` |
| Vue 3 | Tailwind CSS | `用 Vue 克隆 https://...` |
| HTML | 原生 CSS | `克隆 https://... 为静态 HTML` |

---

## 环境要求

- Claude Code
- Python 3.8+
- Node.js 18+

---

## 常见问题

### Playwright 未找到
```bash
pip install playwright && playwright install chromium
```

### 页面未完全抓取（SPA/动态内容）
告诉 Claude Code：
```
克隆 https://example.com，等待 5 秒让内容加载
```

### Next.js 图片不显示
在 `next.config.js` 中添加：
```js
module.exports = {
  images: {
    remotePatterns: [{ protocol: 'https', hostname: '**' }]
  }
}
```

---

## 工作原理（详细）

<details>
<summary>点击展开</summary>

### Phase 1: 页面提取

Skill 使用 Playwright 抓取：
- 完整的 DOM 树和计算样式
- 全页截图
- CSS 变量、动画、过渡
- 主题检测（明/暗模式）
- 所有图片和资源

### Phase 2: 智能分块

页面按照 **三原则** 切分：

1. **互斥性** - 分块之间不重叠
2. **完整性** - 所有分块组合 = 整个页面
3. **可控性** - 每个分块 < 50K tokens

### Phase 3: 并行代码生成

多个 Claude Agent 同时工作：
- 每个 Agent 处理一个区块
- 生成独立的 React/Vue 组件
- 使用 Tailwind CSS 样式

### Phase 4: 项目组装

所有组件整合为：
```
project/
├── src/components/   # 生成的组件
├── src/app/page.tsx  # 主页面
├── tailwind.config.js
└── package.json
```

更多细节：
- [docs/EXTRACTION.md](docs/EXTRACTION.md)
- [docs/CHUNKING.md](docs/CHUNKING.md)
- [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md)

</details>

---

## 关于 Nexting.ai

**Perfect Web Clone** 是 [Nexting.ai](https://nexting.ai) 开源的 Claude Code Skill。

想要可视化体验、实时预览、差异对比、一键部署？访问 [nexting.ai](https://nexting.ai)。

---

## 许可证

MIT 许可证

---

<div align="center">

**如果对你有帮助，请给个 ⭐！**

[Nexting.ai](https://nexting.ai) · [反馈问题](https://github.com/anthropics/perfect-web-clone-skill/issues)

</div>
