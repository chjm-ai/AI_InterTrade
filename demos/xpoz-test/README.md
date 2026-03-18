# XPOZ Twitter/X 测试记录

**测试时间**: 2026-03-18 18:14  
**测试方式**: XPOZ MCP `getTwitterPostsByKeywords`  
**查询关键词**: `phone case`  
**返回数量**: 10

---

## 结论

`XPOZ` 已验证可抓到 Twitter/X 搜索结果，适合做轻量搜索和情报分析。

和 `Apify Tweet Scraper V2` 对比：

- `XPOZ` 更适合小样本快速查询、直接给 agent 用
- `Apify` 更适合结构化落库、批量抓取、后续清洗分析

---

## XPOZ 实测返回内容

### 已抓到字段

| 字段 | 说明 |
|------|------|
| `id` | 推文 ID |
| `text` | 推文正文 |
| `authorId` | 作者 ID |
| `authorUsername` | 作者用户名 |
| `createdAt` | Unix 时间戳 |
| `retweetCount` | 转推数 |
| `replyCount` | 回复数 |
| `likeCount` | 点赞数 |
| `quoteCount` | 引用数 |
| `impressionCount` | 曝光数 |
| `bookmarkCount` | 收藏数 |
| `lang` | 语言 |
| `hashtags` | 标签 |
| `mentions` | 提及用户 |
| `mediaUrls` | 图片/视频 URL |
| `source` | 发布来源 |

### 样本特点

- 能拿到真实推文正文
- 能拿到互动指标，含 `impressionCount` 和 `bookmarkCount`
- 能拿到直接媒体链接，视频结果里包含 `m3u8` 和 `mp4`
- 返回是 `MCP content.text` 中的结构化文本，不是干净的 JSON 数组
- 当前结果里**没有直接返回推文 URL**
- 作者信息是扁平字段，没有完整嵌套 author 对象

### 样本例子

```text
id: 2030325563030966456
text: Do you like my new phone case?
authorUsername: autumnrxnae
likeCount: 7793
replyCount: 171
impressionCount: 134738
mediaUrls: 含视频 mp4
```

---

## 对比 Apify

### Apify 官方输出特点

参考 `apidojo/tweet-scraper` 官方输出示例，`Apify` 典型会返回：

- `url`
- `twitterUrl`
- `text`
- `retweetCount / replyCount / likeCount / quoteCount / bookmarkCount`
- `createdAt` 可读时间
- `quoteId`
- `isReply / isRetweet / isQuote`
- `author` 嵌套对象
- `author.followers / following / isVerified / profilePicture`

### 内容差异

| 维度 | XPOZ 实测 | Apify 官方示例 |
|------|-----------|----------------|
| 返回形态 | MCP 文本块 | 标准 JSON |
| 推文正文 | 有 | 有 |
| 推文 URL | 当前结果未见 | 有 |
| 作者信息 | 扁平字段 | 嵌套 author 对象，更完整 |
| 互动指标 | 点赞/回复/转推/引用/曝光/收藏 | 点赞/回复/转推/引用/收藏 |
| 媒体 URL | 有，且直接给图/视频链接 | 有媒体信息，但不同 Actor 结构可能不同 |
| 会话关系 | 本次结果未见 reply/quote 标记 | 有 `isReply/isQuote/isRetweet/quoteId` |
| 落库友好度 | 中 | 高 |

### 结论

- **看搜索结果内容本身**：两者都够用
- **看结构化程度**：`Apify` 更强
- **看直接给 AI 用**：`XPOZ` 更顺手
- **看后续做数据管道**：`Apify` 更合适

---

## 成本对比

### XPOZ 本次查询成本

官方公式：

```text
credits = queries × 5 + results × 0.005
```

本次：

```text
1 次查询 + 10 条结果 = 5.05 credits
```

按 `Pro` 套餐折算：

- `$20 / 30,000 credits`
- 本次约 `$0.00337`
- 单条约 `$0.000337`

按 `Pro` 超量价折算：

- `$0.80 / 1,000 credits`
- 本次约 `$0.00404`
- 单条约 `$0.000404`

### Apify Twitter 成本

`apidojo/tweet-scraper` 官方价格：

- `$0.40 / 1000 tweets`
- **每次查询至少返回 50 条**

所以：

- 理论单条：`$0.0004`
- 实际单次最小成本约：`$0.02`

### 成本判断

| 场景 | 更优 |
|------|------|
| 小样本搜索（10-20 条） | `XPOZ` |
| 大规模批量抓取 | `Apify` |
| 要求查询即出结果 | `XPOZ` |
| 要求标准 JSON 数据集 | `Apify` |

---

## 文件

```text
demos/xpoz-test/
├── README.md
├── test_xpoz_twitter.py
└── results/
    ├── xpoz_twitter_20260318_181331.json
    └── xpoz_twitter_20260318_181433.json
```

---

## 备注

- 本次 `Apify Twitter` 未做同轮实跑，因为当前环境未设置 `APIFY_API_TOKEN`
- `Apify` 对比基于官方 Actor 输出示例与官方定价页
