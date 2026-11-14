# 贡献指南

感谢你改进 Writing Skill Trainer。一次 PR 只解决一个明确问题。

## 提交前

1. 阅读 `skills/writing-skill-trainer/SKILL.md` 和它引用的 `references/`。
2. 保持 skill 自包含：从自身目录解析 `scripts/` 和 `references/`，不要写入个人机器的固定路径。
3. 运行 `python3 scripts/check.py`，并在 PR 中粘贴实际命令与结果。
4. 改动评测协议时，说明它解决了哪次真实训练里的什么问题。

## 隐私与来源

- 只提交合成、公版或明确获准公开的样本，并写明来源 URL 和许可证。
- 不提交密钥、会话正文、私人文章、未公开草稿或可识别个人的本地路径。
- 评测结果连同失败案例一起提交，不按输赢挑样。

发现漏洞或秘密时不要放进 issue 或 PR；按 [`SECURITY.md`](SECURITY.md) 私下报告。

## 许可证

提交的内容按 [Apache-2.0](LICENSE) 授权。
