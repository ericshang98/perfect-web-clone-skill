# Perfect Web Clone

<div align="center">

**AI 驱动的网页克隆工具 - 一句话，像素级复刻任意网页**

[English](README.md) | 中文

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](https://claude.ai)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Powered-45ba4b.svg)](https://playwright.dev)

</div>

---

**Perfect Web Clone** 是一个开源的 Claude Code Skill，能够将任意网页转换为可运行的 React/Next.js/Vue 代码。它使用 Playwright 进行页面提取，采用三原则算法进行智能分块，并通过并行 Agent 生成代码。

> 由 [Nexting.ai](https://nexting.ai) 创建

---

## 目录

- [核心特性](#核心特性)
- [工作原理 - 完整流程详解](#工作原理---完整流程详解)
  - [Phase 1: 环境准备](#phase-1-环境准备)
  - [Phase 2: 页面提取](#phase-2-页面提取)
  - [Phase 3: 智能分块](#phase-3-智能分块)
  - [Phase 4: 并行代码生成](#phase-4-并行代码生成)
  - [Phase 5: 项目组装](#phase-5-项目组装)
- [快速开始](#快速开始)
  - [方式一：个人全局安装](#方式一个人全局安装)
  - [方式二：项目级安装](#方式二项目级安装)
- [使用示例](#使用示例)
- [三原则详解](#三原则详解)
  - [原则一：互斥性](#原则一互斥性)
  - [原则二：完整性](#原则二完整性)
  - [原则三：可控性](#原则三可控性)
- [并行配置](#并行配置)
- [支持的技术栈](#支持的技术栈)
- [常见问题](#常见问题)
- [进阶文档](#进阶文档)
- [关于 Nexting.ai](#关于-nextingai)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 核心特性

| 特性 | 描述 |
|------|------|
| **像素级复刻** | 忠实还原原始设计，包括计算样式、颜色、间距和排版 |
| **智能分块** | 三原则算法确保分块完整、不重叠、大小可控 |
| **并行生成** | 多个 Claude Agent 同时工作，大幅提升速度 |
| **30+ 数据类型** | 提取 DOM、样式、动画、CSS 变量、主题、悬停状态等 |
| **多框架支持** | 输出 Next.js、React、Vue 3 或纯 HTML |
| **主题检测** | 自动检测并保留明/暗模式支持 |

---

## 工作原理 - 完整流程详解

本节提供整个克隆流程的**详细拆解**。

```
用户输入: URL
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 1: 环境准备                   │  ← 检查依赖、安装 Playwright
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 2: 页面提取                   │  ← Playwright 抓取 DOM、样式、截图
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 3: 智能分块                   │  ← 三原则算法切分页面
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 4: 并行代码生成               │  ← 多个 Agent 同时生成组件
└─────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────┐
│  Phase 5: 项目组装                   │  ← 整合为完整项目
└─────────────────────────────────────┘
      │
      ▼
   npm run dev → 查看效果
```

---

### Phase 1: 环境准备

**目标**：确保所有依赖已安装就绪。

#### 步骤详解

| 步骤 | 命令 | 说明 |
|------|------|------|
| 1.1 | `python --version` | 确认已安装 Python 3.8+ |
| 1.2 | `python -c "from playwright.sync_api import sync_playwright"` | 检查 Playwright 是否可用 |
| 1.3 | `pip install playwright beautifulsoup4` | 安装 Python 依赖（如需要） |
| 1.4 | `playwright install chromium` | 下载 Playwright 使用的 Chromium 浏览器 |

#### 常见问题

| 问题 | 解决方案 |
|------|----------|
| "playwright not found" | 执行 `pip install playwright && playwright install chromium` |
| macOS 权限被拒绝 | 使用 `pip install --user playwright` 或创建虚拟环境 |
| Linux 上 Chromium 下载失败 | 安装系统依赖：`sudo apt-get install libnss3 libatk1.0-0 libatk-bridge2.0-0` |

---

### Phase 2: 页面提取

**目标**：使用 Playwright 抓取网页的完整数据。

#### 执行命令

```bash
python scripts/extract_page.py "<URL>" --output page_data.json
```

#### 提取的数据类型（30+）

| 类别 | 数据项 | 描述 |
|------|--------|------|
| **页面元数据** | | |
| | `url` | 目标 URL |
| | `title` | 页面标题 |
| | `viewport` | 浏览器视口尺寸 |
| | `page_dimensions` | 完整页面宽高 |
| | `load_time_ms` | 页面加载时间（毫秒） |
| **DOM 结构** | | |
| | `dom_tree` | 完整的递归元素树 |
| | `tag`, `id`, `classes` | 元素标识信息 |
| | `rect` | 边界框（x, y, width, height） |
| | `children` | 嵌套的子元素 |
| **计算样式** | | |
| | 布局 | `display`, `position`, `float`, `z_index` |
| | Flexbox | `flex_direction`, `justify_content`, `align_items`, `gap` |
| | Grid | `grid_template_columns`, `grid_template_rows` |
| | 尺寸 | `width`, `height`, `min_width`, `max_width` |
| | 间距 | `margin`, `padding`（四个方向） |
| | 视觉 | `background_color`, `background_image`, `color`, `border`, `border_radius`, `box_shadow`, `opacity` |
| | 排版 | `font_family`, `font_size`, `font_weight`, `line_height`, `text_align` |
| | 变换 | `transform` |
| **CSS 数据** | | |
| | `variables` | CSS 自定义属性（如 `--primary: #3b82f6`） |
| | `animations` | @keyframes 动画定义 |
| | `transitions` | 每个选择器的过渡属性 |
| | `pseudo_elements` | ::before 和 ::after 内容 |
| **截图** | | |
| | `screenshot` | 视口截图（base64 PNG） |
| | `full_page_screenshot` | 完整页面截图 |
| **主题检测** | | |
| | `support` | "light"、"dark" 或 "both" |
| | `current_mode` | 当前激活的主题 |
| | `has_significant_difference` | 主题是否有明显视觉差异 |
| **资源** | | |
| | `images` | 所有图片 URL（img src 和 background-image） |
| | `fonts` | Web 字体 URL |
| | `scripts` | JavaScript 文件 URL |
| | `stylesheets` | CSS 文件 URL |
| **交互状态** | | |
| | `hover_states` | :hover 时的样式变化 |
| | `focus_states` | :focus 时的样式变化 |

#### 命令选项

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `--output`, `-o` | `page_data.json` | 输出文件路径 |
| `--viewport` | `1920x1080` | 浏览器视口尺寸 |
| `--wait` | `3000` | 页面加载后等待时间（毫秒） |
| `--full-screenshot` | `false` | 捕获完整页面截图 |
| `--download-images` | `false` | 下载图片到本地 |

#### 懒加载处理

提取器会自动滚动整个页面以触发：
- 懒加载图片
- 无限滚动内容
- 基于 IntersectionObserver 的元素

---

### Phase 3: 智能分块

**目标**：按照三原则将页面切分为独立、可管理的区块。

#### 执行命令

```bash
python scripts/chunk_content.py page_data.json --output chunks/ --max-tokens 50000
```

#### 三原则

**每个分块必须满足全部三个原则：**

```
┌─────────────────────────────────────────────────────────────────┐
│  原则 1: 互斥性 (MUTUAL EXCLUSIVITY)                            │
│  ───────────────────────────────────                            │
│  分块之间绝不重叠。每个 DOM 区域只属于一个分块。                   │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │  分块 1  │  │  分块 2  │  │  分块 3  │   ✓ 无重叠           │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  原则 2: 完整性 (COMPLETE COVERAGE)                             │
│  ──────────────────────────────────                             │
│  所有分块组合 = 整个页面。没有内容遗漏。                          │
│                                                                 │
│  页面高度: 5000px                                               │
│  分块 1: 0-800px    ┐                                          │
│  分块 2: 800-2000px │→ 总计: 5000px ✓                          │
│  分块 3: 2000-3500px│                                           │
│  分块 4: 3500-5000px┘                                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  原则 3: 可控性 (SIZE CONTROL)                                  │
│  ────────────────────────────                                   │
│  每个分块 < 50,000 tokens。大区块自动拆分。                       │
│                                                                 │
│  原始: 200K tokens                                              │
│       ↓ 递归拆分                                                │
│  ┌─────────┬─────────┬─────────┬─────────┐                     │
│  │  50K    │   50K   │   50K   │   50K   │  ✓ 可管理           │
│  └─────────┴─────────┴─────────┴─────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

#### 输出结构

```
chunks/
├── section_0_header.json       # 导航/头部
├── section_1_hero.json         # Hero 区域
├── section_2_features.json     # 功能特性区
├── section_3_pricing.json      # 定价区
├── section_4_testimonials.json # 用户评价区
└── section_5_footer.json       # 底部
```

#### 每个分块包含的内容

```json
{
  "id": "section-2",
  "name": "section_2",
  "selector": "section.features",
  "rect": {
    "x": 0, "y": 680, "width": 1920, "height": 800
  },
  "styles": {
    "background_color": "rgb(249, 250, 251)",
    "padding": "96px 0px"
  },
  "html": "<section class=\"features\">...</section>",
  "images": [
    {"src": "https://example.com/icon1.svg", "alt": "Feature 1"}
  ],
  "estimated_tokens": 2500
}
```

---

### Phase 4: 并行代码生成

**目标**：多个 Claude Agent 同时工作，各自生成一个组件。

#### 工作原理

```
┌───────────────────────────────────────────────────────────────────┐
│                     Claude Code（调度器）                          │
│                              │                                    │
│         ┌────────────────────┼────────────────────┐              │
│         ▼          ▼         ▼         ▼          ▼              │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│    │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent 4 │ │ Agent 5 │   │
│    │  头部   │ │  Hero   │ │  功能区  │ │  定价   │ │  底部   │   │
│    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│         ▼          ▼         ▼         ▼          ▼              │
│    Header.tsx  Hero.tsx  Features.tsx Pricing.tsx Footer.tsx     │
└───────────────────────────────────────────────────────────────────┘
```

#### 每个 Agent 接收的数据

| 字段 | 描述 |
|------|------|
| `html` | 该区块的 HTML 片段 |
| `styles` | 计算后的 CSS 样式 |
| `rect` | 边界框位置和尺寸 |
| `images` | 该区块内的图片列表 |
| `estimated_tokens` | 内容大小估算 |

#### Agent Prompt 模板

每个 Agent 收到的指令如下：

```
你是一个专注于像素级复刻的前端开发者。

## 任务
实现网页克隆的 [Features] 区块。

## 输入数据
- 区块 HTML: [来自 chunks/section_2_features.json]
- 区块样式: [计算后的样式]
- 图片: [图片列表及 URL]
- 边界框: [位置信息]

## 要求
1. 像素级还原：精确复刻视觉设计
2. 使用原始 URL：保持所有图片 src 不变
3. Tailwind CSS：使用 Tailwind 工具类，仅在必要时使用内联样式
4. 独立运行：组件必须能独立工作
5. 响应式：实现合理的断点

## 输出
写一个 React/Next.js 组件到: src/components/Features.tsx
```

#### 生成的组件示例

```tsx
// src/components/Features.tsx
import Image from 'next/image'

interface FeaturesProps {
  className?: string
}

export default function Features({ className = '' }: FeaturesProps) {
  const features = [
    {
      icon: 'https://example.com/icon1.svg',
      title: '极速性能',
      description: '闪电般的加载速度...'
    },
    // ... 更多功能
  ]

  return (
    <section className={`py-24 bg-gray-50 ${className}`}>
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16">功能特性</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, i) => (
            <div key={i} className="p-6 bg-white rounded-xl shadow-sm">
              <img src={feature.icon} alt="" className="w-12 h-12 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

### Phase 5: 项目组装

**目标**：将所有生成的组件整合为完整、可运行的项目。

#### 生成的文件结构

```
project/
├── src/
│   ├── app/
│   │   ├── page.tsx           # 主页面，导入所有区块
│   │   ├── layout.tsx         # 根布局
│   │   └── globals.css        # 全局样式
│   └── components/
│       ├── Header.tsx
│       ├── Hero.tsx
│       ├── Features.tsx
│       ├── Pricing.tsx
│       ├── Testimonials.tsx
│       └── Footer.tsx
├── tailwind.config.js
├── next.config.js
├── package.json
└── tsconfig.json
```

#### 主页面组装

```tsx
// src/app/page.tsx
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Features from '@/components/Features'
import Pricing from '@/components/Pricing'
import Testimonials from '@/components/Testimonials'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main>
      <Header />
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <Footer />
    </main>
  )
}
```

#### 最后一步

```bash
npm install && npm run dev
# 打开 http://localhost:3000
```

---

## 快速开始

### 方式一：个人全局安装

个人使用，在所有项目中可用：

```bash
# 步骤 1: 克隆到 Claude Code skills 目录
git clone https://github.com/anthropics/perfect-web-clone-skill.git ~/.claude/skills/perfect-web-clone

# 步骤 2: 安装 Python 依赖
cd ~/.claude/skills/perfect-web-clone/scripts
pip install -r requirements.txt

# 步骤 3: 安装 Playwright 浏览器
playwright install chromium

# 步骤 4: 重启 Claude Code
# Skill 会被自动检测
```

### 方式二：项目级安装

团队项目使用，团队成员都可用：

```bash
# 步骤 1: 克隆到项目目录
git clone https://github.com/anthropics/perfect-web-clone-skill.git .claude/skills/perfect-web-clone

# 步骤 2-4: 同上
```

---

## 使用示例

### 基础用法

```
克隆 https://stripe.com
```

### 指定框架

```
用 React 克隆 https://linear.app
```

```
Clone https://example.com with Vue
```

### 控制并行度

```
用 5 个并行 agent 克隆 https://example.com
```

```
最快速度克隆 https://example.com
```

### 组合使用

```
用 Next.js 和 10 个并行 agent 克隆 https://example.com
```

---

## 三原则详解

### 为什么需要三原则？

没有这些原则会导致问题：

| 缺少原则 | 问题 |
|----------|------|
| 没有互斥性 | 重复代码、合并冲突、组件重叠 |
| 没有完整性 | 遗漏区块、克隆不完整、视觉缺失 |
| 没有可控性 | 上下文溢出、Agent 失败、输出不完整 |

### 原则一：互斥性

**规则**：任意两个分块不能共享 DOM 区域。

**实现方式**：
- 计算每对区块的边界框重叠
- 如果重叠 > 100px²，保留较大的区块，丢弃另一个
- 验证确保最终输出零重叠

**好处**：每个 Agent 处理真正隔离的内容，没有冲突。

### 原则二：完整性

**规则**：所有分块组合 = 整个页面（y=0 到 y=pageHeight）。

**实现方式**：
- 按 Y 坐标排序区块（从上到下）
- 检测相邻区块之间的间隙
- 扩展区块边界以填充间隙
- 最终覆盖率必须等于 100%

**好处**：不会丢失任何内容。克隆在视觉上完整。

### 原则三：可控性

**规则**：每个分块 < 50,000 tokens。

**实现方式**：
- 估算 tokens：`字符数 / 4`
- 如果区块超过限制，递归拆分为子元素
- 持续直到所有分块都在阈值以下

**好处**：每个 Agent 收到可管理的上下文，确保可靠生成。

---

## 并行配置

| 用户命令 | Agent 数量 | 使用场景 |
|----------|------------|----------|
| `"克隆这个页面"` | 3（默认） | 平衡速度和资源使用 |
| `"用 N 个并行克隆"` | N | 精确控制 |
| `"最快速度克隆"` | 所有区块 | 最大速度 |
| `"逐个克隆"` | 1 | 调试、仔细审查 |

---

## 支持的技术栈

| 框架 | 样式 | 命令示例 |
|------|------|----------|
| Next.js（默认） | Tailwind CSS | `用 Next.js 克隆 https://...` |
| React | Tailwind CSS | `用 React 克隆 https://...` |
| Vue 3 | Tailwind CSS | `用 Vue 克隆 https://...` |
| HTML | 原生 CSS | `克隆 https://... 为静态 HTML` |

---

## 常见问题

### Playwright 安装问题

**macOS:**
```bash
brew install chromium
playwright install chromium
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install chromium-browser
playwright install chromium
```

**Windows:**
```bash
playwright install chromium
```

### 页面太大（100+ 区块）？

使用最大并行度：
```
最快速度克隆 https://large-site.com
```

### 动态内容没有被抓取？

增加等待时间：
```bash
python scripts/extract_page.py "https://spa-site.com" --wait 5000
```

### 页面需要登录？

目前不支持。请克隆公开可访问的页面，或在提取脚本中实现 cookie 注入。

### 克隆后图片不显示？

对于 Next.js，添加域名配置：
```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**' }
    ]
  }
}
```

---

## 进阶文档

| 文档 | 内容 |
|------|------|
| [SKILL.md](SKILL.md) | 核心 Skill 指令定义 |
| [docs/EXTRACTION.md](docs/EXTRACTION.md) | 30+ 提取数据类型详解 |
| [docs/CHUNKING.md](docs/CHUNKING.md) | 三原则算法实现 |
| [docs/CODE_GENERATION.md](docs/CODE_GENERATION.md) | 组件生成策略 |

---

## 关于 Nexting.ai

**Perfect Web Clone** 是由 [Nexting.ai](https://nexting.ai) 创建的开源 Claude Code Skill。

想要完整的可视化体验？
- 浏览器内实时预览
- 可视化差异对比
- 一键部署
- 团队协作

访问 [nexting.ai](https://nexting.ai) 试用我们的全功能 AI Web 开发平台。

---

## 贡献指南

欢迎贡献！

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 发起 Pull Request

---

## 许可证

MIT 许可证 - 可免费用于个人和商业用途。

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ 支持一下！**

[GitHub](https://github.com/anthropics/perfect-web-clone-skill) · [Nexting.ai](https://nexting.ai) · [反馈问题](https://github.com/anthropics/perfect-web-clone-skill/issues)

</div>
