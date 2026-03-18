# XPOZ 社媒测试记录

**测试时间**: 2026-03-18  
**测试范围**: Twitter/X + Instagram + TikTok + Reddit  
**查询关键词**: `phone case`

---

## 结论

`XPOZ` 当前公开的 4 个内容平台能力已全部实测：

- `Twitter/X`
- `Instagram`
- `TikTok`
- `Reddit`

四个平台都能返回有效结果。

和 `Apify Tweet Scraper V2` 对比：

- `XPOZ` 更适合小样本快速查询、直接给 agent 用
- `Apify` 更适合结构化落库、批量抓取、后续清洗分析
- `Apify` 跨平台字段不会完全一致，`XPOZ` 的接口风格更统一

---

## 统一性判断

### Apify

- 不同平台通常对应不同 Actor
- 不同 Actor 往往是不同开发者维护
- 字段命名、嵌套结构、时间格式、媒体字段差异会比较大
- 如果要跨平台统一分析，通常需要自己再做一层字段标准化

### XPOZ

- `Twitter/X` 和 `Instagram` 都是同一套 MCP 协议
- 都支持 `getPostsByKeywords`
- 都支持 `fields` 精选字段
- 都支持 `fast / paging / csv`
- 返回都有 `count / query / guidance / operationId`

结论：

- **跨平台一致性**：`XPOZ` 更好
- **字段深度与落库灵活性**：通常还是 `Apify` 更强

---

## XPOZ 实测返回内容

### Twitter/X

**测试方式**: `getTwitterPostsByKeywords`  
**返回数量**: 10

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

### Instagram

**测试方式**: `getInstagramPostsByKeywords`  
**返回数量**: 10

### 已抓到字段

| 字段 | 说明 |
|------|------|
| `id` | Instagram post id |
| `postType` | 帖子类型 |
| `username` | 用户名 |
| `fullName` | 昵称 |
| `caption` | 文案 |
| `createdAtDate` | 发布时间 |
| `likeCount` | 点赞数 |
| `commentCount` | 评论数 |
| `reshareCount` | 转发数 |
| `videoPlayCount` | 播放数 |
| `mediaType` | 媒体类型 |
| `codeUrl` | Instagram 帖子 URL |
| `imageUrl` | 封面图 |
| `videoUrl` | 视频地址 |
| `videoDuration` | 视频时长 |

### Instagram 样本特点

- 返回更像“结构化行数据”
- 直接带 `codeUrl`，可回跳帖子页
- 视频结果直接带 `videoUrl`
- 内容里出现高热视频、带货帖子、DIY 内容、商家内容
- `createdAtDate` 这次样本里大多是 `null`，说明字段稳定性还要继续看
- 一些图文结果没有 `videoUrl/videoDuration`

### Instagram 样本例子

```text
username: aiedaofficial
caption: Immersive sharing of a super cute 3D Hello Kitty...
likeCount: 831287
commentCount: 9899
videoPlayCount: 43613811
codeUrl: https://instagram.com/p/T...
videoUrl: 直接可用
```

---

### TikTok

**测试方式**: `getTiktokPostsByKeywords`  
**返回数量**: 10

### 已抓到字段

| 字段 | 说明 |
|------|------|
| `id` | TikTok post id |
| `postType` | 帖子类型 |
| `username` | 用户名 |
| `nickname` | 昵称 |
| `description` | 文案 |
| `descriptionLanguage` | 文案语言 |
| `createdAtDate` | 发布时间 |
| `likeCount` | 点赞数 |
| `commentCount` | 评论数 |
| `playCount` | 播放数 |
| `forwardCount` | 转发数 |
| `collectCount` | 收藏数 |
| `downloadCount` | 下载数 |
| `videoThumbnail` | 视频缩略图 |

### TikTok 样本特点

- 返回速度快
- 内容结果偏消费内容、带货内容、UGC 内容混合
- 有播放/收藏/下载等短视频核心指标
- 这次样本里 `username / nickname` 多数为 `null`
- 没有直接给帖子 URL 或视频直链

### TikTok 样本例子

```text
description: My favorite phone case everrrrrr...
createdAtDate: 2026-03-08
likeCount: 2040
commentCount: 16
playCount: 159838
collectCount: 426
```

---

### Reddit

**测试方式**: `getRedditPostsByKeywords`  
**返回数量**: 10

### 已抓到字段

| 字段 | 说明 |
|------|------|
| `id` | Reddit post id |
| `title` | 标题 |
| `selftext` | 正文 |
| `url` | 原始链接 |
| `permalink` | 站内 permalink |
| `postUrl` | Reddit 页面链接 |
| `thumbnail` | 缩略图 |
| `authorUsername` | 作者 |
| `subredditName` | 子版块 |
| `score` | 分数 |
| `upvotes` | 赞成票 |
| `downvotes` | 反对票 |
| `upvoteRatio` | 赞成率 |
| `commentsCount` | 评论数 |
| `createdAtDate` | 发布时间 |
| `domain` | 来源域名 |

### Reddit 样本特点

- 返回最结构化，最接近传统论坛帖子数据
- 有 `title + selftext + subreddit + commentsCount`
- 很适合做需求洞察、痛点讨论、品牌舆情
- 这次样本里 `createdAtDate` 多数为 `null`
- 查询结果包含讨论帖、求助帖、分享帖，不只是商品内容

### Reddit 样本例子

```text
title: Are expensive phone cases actually worth it?
subredditName: BuyItForLife
score: 151
commentsCount: 297
domain: self.BuyItForLife
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

### Apify 实跑补充

#### Twitter/X

- Actor: `apidojo/tweet-scraper`
- 输入: `searchTerms=["phone case"]`, `maxItems=10`
- 结果: run 成功，但 dataset 返回 10 条 `{"noResults": true}`
- 说明: 这个 Actor 的搜索行为和 `XPOZ Twitter` 不同，至少当前这组输入下没有直接拿到可用内容

#### Instagram

- Actor: `apify/instagram-scraper`
- 输入1: `search="phone case"`, `searchType="hashtag"`, `resultsType="posts"`
- 输入2: `search="phonecase"`, `searchType="hashtag"`, `resultsType="posts"`
- 结果: 两次 run 都卡在 `https://i.instagram.com/api/v1/tags/search/`，持续 500 重试，最终人工中止
- 说明: 这个 Actor 当前更像“标签页抓取器”，不是 `XPOZ` 那种“关键词搜帖子正文/字幕”的统一内容检索

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

### Instagram 视角补充

| 维度 | XPOZ Instagram 实测 | Apify Instagram 常见情况 |
|------|---------------------|--------------------------|
| 查询入口 | 关键词搜索统一接口 | 依赖具体 Instagram Actor |
| 结果字段 | caption / username / like / comment / play / codeUrl / videoUrl | 通常也能拿到，但字段名和结构因 Actor 不同会变 |
| URL 可用性 | 有 `codeUrl` | 一般有，但字段名未必一致 |
| 媒体字段 | `imageUrl / videoUrl / videoDuration` | 有，但命名/层级可能不同 |
| 跨平台复用感 | 高 | 中低 |

### 这轮实跑后的判断

| 维度 | XPOZ | Apify |
|------|------|------|
| Twitter 关键词可用性 | 已拿到 10 条内容 | 本轮输入下仅返回 `noResults` |
| Instagram 关键词可用性 | 已拿到 10 条内容 | 当前 actor 在 hashtag 搜索阶段反复 500 |
| TikTok 关键词可用性 | 已拿到 10 条内容 | 旧链路已验证可抓，但字段口径与 XPOZ 不同 |
| Reddit 关键词可用性 | 已拿到 10 条内容 | 本轮未补跑 |
| 接口统一性 | 高 | 低 |
| 适合先做统一分析层 | 是 | 一般 |

### 结论

- **看搜索结果内容本身**：两者都够用
- **看结构化程度**：`Apify` 更强
- **看直接给 AI 用**：`XPOZ` 更顺手
- **看后续做数据管道**：`Apify` 更合适
- **看跨平台统一接口**：`XPOZ` 更好
- **看跨平台“同样关键词直接可跑”**：这轮实际是 `XPOZ` 明显更稳

---

## 全平台总表

| 平台 | 查询状态 | 主要字段质量 | 适合场景 |
|------|----------|--------------|----------|
| Twitter/X | ✅ 成功 | 正文 + 作者 + 互动 + 曝光 + 收藏 + 媒体 | 热点、竞品传播、内容表现 |
| Instagram | ✅ 成功 | caption + 账号 + 点赞评论播放 + codeUrl + 视频直链 | 爆款内容、带货内容、账号观察 |
| TikTok | ✅ 成功 | description + 播放点赞评论收藏下载 | 短视频爆款分析 |
| Reddit | ✅ 成功 | title + selftext + subreddit + score + comments | 需求洞察、社区讨论、痛点分析 |

### 当前判断

- `XPOZ` 现在已经够做一个“统一搜索层”
- `Twitter/X` 和 `Instagram` 的商业内容价值最高
- `TikTok` 能做爆款监控，但用户字段完整性略弱
- `Reddit` 最适合做外贸买家需求/吐槽/选品洞察

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
├── test_xpoz_platform.py
├── test_xpoz_instagram.py
├── test_xpoz_twitter.py
└── results/
    ├── xpoz_instagram_20260318_182032.json
    ├── xpoz_reddit_20260318_183249.json
    ├── xpoz_tiktok_20260318_183250.json
    ├── xpoz_twitter_20260318_181331.json
    └── xpoz_twitter_20260318_181433.json
```

---

## 备注

- 本次已补跑 `Apify Twitter / Instagram`，但结果不如 `XPOZ` 稳定
- `Apify` 字段对比部分仍结合了官方 Actor 输出示例与本轮实跑结果
