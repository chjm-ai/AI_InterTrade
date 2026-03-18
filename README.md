# AI_InterTrade

用于分析和测试外贸行业工具的调研型工作台。

这里不承担正式产品开发，核心用途是：
- 梳理产品思路
- 验证技术可行性
- 跑通第三方工具 demo
- 沉淀截图、视频、配置流程和结论

## 当前目标

围绕 4 个候选能力，尽快完成可交付级别的验证材料：

| 能力 | 优先级 | 月底目标 | 当前判断 |
| --- | --- | --- | --- |
| 多平台发布 | 中 | 功能截图 | 可快速出图，但差异化需要重新定义 |
| 爆款内容拆解 | 中 | 功能截图 | 有技术路径，成本和数据格式待摸清 |
| 多平台多语种询盘承接 | 高 | demo + 视频 | 最接近实际商业价值，应优先跑通 |
| 评论截流 | 低 | 功能截图 | 可做但验证成本高，且平台风控风险高 |

## 项目定位

不是从零造轮子，而是把成熟工具做轻改造、轻封装、轻交付。

核心价值：
- 降低传统行业老板的使用门槛
- 把复杂配置流程变成可交付方案
- 沉淀为后续平台化的通用能力

## 建议优先级

1. 先打通“多平台多语种询盘承接”
2. 再做“爆款内容拆解”
3. 然后补“多平台发布”
4. 最后再评估“评论截流”是否值得前置

原因：
- 询盘承接更接近客户真实付费场景
- 更容易形成 demo、视频、流程 SOP
- 后续还能反向带动内容分析和自动回复能力

## 仓库结构

```text
.
├── AGENTS.md
├── README.md
├── docs
│   ├── project-overview.md
│   ├── delivery-plan.md
│   ├── validation-framework.md
│   └── capabilities
│       ├── multi-platform-publishing.md
│       ├── viral-content-analysis.md
│       ├── inquiry-intake.md
│       └── comment-interception.md
├── research
│   ├── README.md
│   └── templates
│       └── tool-evaluation-template.md
├── demos
│   └── README.md
└── assets
    └── README.md
```

## 使用方式

- 新调研先看 [`docs/project-overview.md`](/Users/wesley/Desktop/Repos/AI_InterTrade/docs/project-overview.md)
- 某个能力要推进时，直接更新对应 `docs/capabilities/*.md`
- 跑第三方工具测试时，把过程记录放到 `research/`
- 截图、录屏、素材统一归档到 `assets/` 或 `demos/`

