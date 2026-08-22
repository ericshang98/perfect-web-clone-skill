# Perfect Web Clone Skill

把任意网页复刻成带测量门禁的 Vite + React 项目。

本仓是**剧本**。抽页 / 切 section / 打分在
[Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone)。

```bash
pip install "git+https://github.com/ericshang98/Perfect-Web-Clone.git"
playwright install chromium
```

Claude Code：把 `SKILL.md` 放到 `~/.claude/skills/perfect-web-clone/`。

DeepSeek Harness：

```bash
npx @deepseek-ai/dsh web
dsh plugin --profile web add github:ericshang98/Perfect-Web-Clone
```

然后说 `clone https://example.com`。

过不过看门禁，不看模型自夸。
