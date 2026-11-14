# 第三方来源与许可证说明

本仓的代码、文档和评测产物按 [Apache-2.0](LICENSE) 发布。下面的材料保留各自的条款，不受根许可证改变。

## 评测用的样本文本

- 《红楼梦》、鲁迅作品：Public Domain（公版），来自中文维基文库。
- Mark Twain 随笔（*On the Decay of the Art of Lying*、*Taming the Bicycle*、*The Danger of Lying in Bed*、*How to Tell a Story*）：美国公版，来自 Project Gutenberg 和英文维基文库。
- 中文维基新闻报道：CC BY 2.5。

每篇材料的来源 URL、用途和 SHA-256 摘要记录在 [`marketing/writing-skill-trainer/data/scenarios.json`](marketing/writing-skill-trainer/data/scenarios.json) 和 [`marketing/writing-skill-trainer/evals/vs-deai/scenarios.json`](marketing/writing-skill-trainer/evals/vs-deai/scenarios.json)，以及各 Demo 的“来源与许可”表。

## 评测中对照的 skill

对照评测使用了下面两个项目，只记录了 commit，没有把它们的文件复制进本仓：

- [`hardikpandya/stop-slop`](https://github.com/hardikpandya/stop-slop)，commit `8da1f03`，MIT。
- [`op7418/dsh-guizang-design`](https://github.com/op7418/dsh-guizang-design) 的 `skills/humanizer-zh`，commit `e275f1e`，该目录 MIT。

[`marketing/writing-skill-trainer/evals/vs-deai/tells.py`](marketing/writing-skill-trainer/evals/vs-deai/tells.py) 里的正则参考了这两个项目公开的禁用清单。
