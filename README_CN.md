# Perfect Web Clone Skill

**这就是像素级克隆的 harness。** 一句话 `clone https://example.com`，当前 coding agent 必须走完：抓取、切块、写组件、构建、测量、修复，再交给你验收。

产品是这份 [`SKILL.md`](SKILL.md)：

- Agent 是运行时
- [`pwc`](https://github.com/ericshang98/Perfect-Web-Clone) 是手和眼（不调模型）
- 完美复刻是门禁表：抓取完整性、结构齐全、交互能重放、指纹、体积、逐 section 视觉分
- 长得像但不能点，算失败
- 只允许停在 `ready_for_user_review` 或 `failed_with_residuals`

测量核心在 [Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone)。

```bash
pip install "git+https://github.com/ericshang98/Perfect-Web-Clone.git"
playwright install chromium
mkdir -p ~/.claude/skills/perfect-web-clone/references
cp SKILL.md ~/.claude/skills/perfect-web-clone/
cp references/harness-contract.md ~/.claude/skills/perfect-web-clone/references/
```

然后说 `clone https://example.com`。
