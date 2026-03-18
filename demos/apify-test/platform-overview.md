# Apify 平台调研报告

**调研时间**: 2026-03-18  
**调研目的**: 了解 Apify Store 支持的平台、数据类型及收费模式，并与 XPOZ 做轻量对比

---

## 一、Apify 是什么

Apify 是一个 **无服务器爬虫平台 (Serverless Web Scraping Platform)**，提供：
- **20,000+ 现成的爬虫工具** (称为 Actors)
- 覆盖社交媒体、电商、搜索引擎、地图等多种数据源
- 无需自建服务器，按用量付费

---

## 二、支持的主流平台

### 社交媒体平台

| 平台 | Actor 数量 | 主要功能 | 代表 Actor |
|------|-----------|---------|-----------|
| **TikTok** | 多款 | 视频、用户、标签、评论 | clockworks/tiktok-scraper |
| **Instagram** | 多款 | 帖子、Reels、用户、标签、评论 | apify/instagram-scraper |
| **Twitter/X** | 多款 | 推文、用户、搜索、时间线 | apidojo/tweet-scraper |
| **Facebook** | 多款 | 帖子、广告库、页面 | apify/facebook-posts-scraper |
| **YouTube** | 多款 | 视频、频道、评论 | streamers/youtube-scraper |
| **LinkedIn** | 多款 | 个人资料、职位、帖子 | dev_fusion/linkedin-profile-scraper |
| **Reddit** | 多款 | 帖子、评论、社区 | macrocosmos/reddit-scraper |
| **Lemon8** | 少量 | 帖子、用户 | tictechid/vanzi-lemon8-scraper |

### 电商平台

| 平台 | Actor 数量 | 主要功能 |
|------|-----------|---------|
| **Amazon** | 多款 | 产品、价格、评论、卖家 |
| **eBay** | 多款 | 商品、价格、卖家 |
| **Shopify** | 多款 | 店铺、产品 |
| **Walmart** | 多款 | 商品数据 |
| **通用电商爬虫** | 多款 | 支持任意电商网站 |

### 地图与本地商业

| 平台 | Actor 数量 | 主要功能 |
|------|-----------|---------|
| **Google Maps** | 多款 | 商家、评论、位置 |
| **Tripadvisor** | 少量 | 评论、商家 |
| **2GIS** | 少量 | 俄罗斯/东欧地图数据 |

### 搜索引擎与趋势

| 平台 | Actor 数量 | 主要功能 |
|------|-----------|---------|
| **Google Search** | 多款 | SERP、关键词 |
| **Google Trends** | 少量 | 趋势数据 |
| **Google Flights** | 少量 | 航班数据 |

### 其他

| 类别 | 示例 |
|------|------|
| **招聘** | LinkedIn Jobs、Indeed |
| **房地产** | Idealista、Zillow |
| **评论网站** | Trustpilot、Yelp |
| **金融** | Flippa、股票数据 |
| **新闻** | 通用新闻爬虫 |

---

## 三、各平台可抓取的数据类型

### TikTok (以 clockworks/tiktok-scraper 为例)

**已验证字段** (24个):
- ✅ 视频基础: id, text, createTime, webVideoUrl
- ✅ 互动数据: diggCount, shareCount, playCount, collectCount, commentCount
- ✅ 作者信息: authorMeta (粉丝数、获赞数、简介)
- ✅ 内容元数据: videoMeta, hashtags, musicMeta
- ✅ 搜索关联: searchQuery

**抓取方式**:
- 关键词搜索
- 用户主页
- 标签页
- 视频 URL

### Instagram

**可抓取数据**:
- 帖子、Reels、Stories
- 用户资料 (粉丝数、关注数、帖子数)
- 评论
- 标签页
- 地理位置

### Twitter/X

**可抓取数据**:
- 推文内容
- 点赞、转发、回复数
- 用户信息
- 搜索时间线
- 列表成员

### Facebook

**可抓取数据**:
- 页面帖子 (文字、图片、视频)
- 互动数据 (点赞、评论、分享)
- 广告库 (广告主、投放内容)

### LinkedIn

**可抓取数据**:
- 个人资料 (教育、工作经历、技能)
- 职位信息
- 帖子动态
- ⚠️ 部分 Actor 需要 Cookies，部分无需

---

## 四、收费模式详解（Apify）

### 1. 平台使用费 (Apify Platform)

| 套餐 | 月费 | 预付费额度 | 计算单元(CU)单价 |
|------|------|-----------|----------------|
| **Free** | $0 | $5 | $0.3/CU |
| **Starter** | $29 | $29 | $0.3/CU |
| **Scale** | $199 | $199 | $0.25/CU |
| **Business** | $999 | $999 | $0.2/CU |
| **Enterprise** | 定制 | 定制 | 定制 |

**什么是 Compute Unit (CU)?**
- 1 CU = 1 GB 内存运行 1 小时
- 相当于运行资源消耗的计算单位
- 抓取速度越快、内存占用越高，消耗的 CU 越多

### 2. Actor 定价模式

Apify Store 中的 Actor 采用以下几种收费方式：

#### A. 免费 (Free)
- 只收取平台使用费
- 适合：试用、小规模数据抓取

#### B. 按结果付费 (Pay-per-result, PPR) ⭐推荐
- **用户按抓取的数据条数付费**
- 开发者定价：通常 $0.25-$1/1000条
- 平台使用费已包含在内
- 优点：成本可预测、无隐藏费用
- 示例:
  - Twitter Scraper: $0.25/1000 条推文
  - Leads Scraper: $1/1000 条线索

#### C. 按事件付费 (Pay-per-event, PPE)
- 开发者自定义计费事件
- 灵活性最高
- 适合：复杂任务、多步骤流程

#### D. 租赁模式 (Rental)
- 月付固定费用使用 Actor
- 额外收取平台使用费
- 适合：高频使用场景

### 3. 附加服务费用

| 服务 | 价格 |
|------|------|
| **住宅代理 (Residential Proxy)** | $7-8/GB |
| **数据中心代理 (Datacenter Proxy)** | $0.6-1/IP |
| **并发运行 (Concurrent Runs)** | $5/次 |
| **内存扩展** | $2/GB |
| **优先支持** | $100/月 |

### 4. 各平台成本估算

#### TikTok Scraper
- **clockworks/tiktok-scraper**: 免费 (只收平台费)
- 抓取 1000 条视频约消耗: 0.5-1 CU
- **成本**: ~$0.15-0.30/1000条 (Starter 套餐)

#### Twitter/X Scraper
- **apidojo/tweet-scraper**: $0.40/1000条 (PPR模式)
- 平台费已包含
- **成本**: ~$0.40/1000条

#### Instagram Scraper
- **apify/instagram-scraper**: 免费
- 抓取 1000 条帖子约消耗: 1-2 CU
- **成本**: ~$0.30-0.60/1000条

#### LinkedIn Scraper
- **dev_fusion/linkedin-profile-scraper**: 租赁模式
- 月费: ~$30-50/月
- 平台费另计
- **成本**: ~$0.05-0.10/条 (高频使用时)

#### Google Maps Scraper
- **compass/crawler-google-places**: 免费
- 抓取 1000 条商家约消耗: 2-3 CU
- **成本**: ~$0.60-0.90/1000条

---

## 五、XPOZ 对比补充

### XPOZ 当前公开定价

| 套餐 | 月费 | credits | 超量价格 | 持续跟踪数 |
|------|------|---------|---------|-----------|
| **Free** | $0 | 5,000（一次性） | - | 1 |
| **Pro** | $20 | 30,000/月 | $0.80 / 1K credits | 10 |
| **Max** | $200 | 600,000/月 | $0.40 / 1K credits | 30 |
| **Enterprise** | 定制 | 定制 | 定制 | 无限 |

**计费公式**:

```text
credits = (queries × 5) + (results × 0.005)
```

**产品定位差异**:

| 维度 | Apify | XPOZ |
|------|------|------|
| 核心定位 | 通用 web 数据抓取平台 | 社媒搜索与情报分析平台 |
| 数据源 | 社媒 + 电商 + 地图 + 任意网页 | Twitter/X、Instagram、Reddit、TikTok 为主 |
| 主要交付 | 原始数据、API、数据集 | 搜索结果、监控、情绪/趋势/影响力分析 |
| AI 结合方式 | 需自己搭 LLM 分析层 | 原生偏 MCP / agent 工作流 |
| 是否适合做抓取底座 | 是 | 一般 |
| 是否适合快速出洞察 | 中 | 高 |

### 外贸场景判断

- **做爆款内容拆解底座**: `Apify` 更稳，便于拿原始字段后自己算模型
- **做品牌监控/竞品舆情/找达人**: `XPOZ` 更省事，分析功能更强
- **预算敏感、先试跑**: `XPOZ Pro` 月费更低
- **需要平台更广**: `Apify` 明显更强

## 六、优缺点分析

### ✅ 优点

1. **即开即用**: 无需开发，数千个现成 Actor
2. **无需维护**: 平台处理代理、反爬虫、服务器
3. **按量付费**: 没有固定成本，用多少付多少
4. **API 友好**: 所有 Actor 都可通过 API 调用
5. **数据格式**: 统一输出 JSON/CSV/Excel
6. **调度功能**: 支持定时任务

### ⚠️ 限制

1. **成本随规模上升**: 大量数据时成本可能较高
2. **依赖平台**: Actor 更新滞后于网站改版
3. **免费套餐有限**: Free 套餐只有 $5/月额度
4. **部分平台受限**: LinkedIn、Facebook 等风控严格
5. **数据时效性**: 视频 URL 等有过期时间

---

## 七、适用场景建议

### 适合使用 Apify 的场景

✅ **小规模/间歇性需求**: 每月 <10万条数据  
✅ **多平台数据整合**: 需要同时抓取多个平台  
✅ **快速验证 MVP**: 无需投入开发成本  
✅ **非技术团队**: 没有爬虫开发能力  
✅ **临时项目**: 短期需求，不想维护代码

### 不适合的场景

❌ **超大规模**: 每天 >100万条数据（成本过高）  
❌ **深度定制**: 需要复杂的数据处理逻辑  
❌ **高频实时**: 需要秒级更新的场景  
❌ **敏感数据**: 涉及隐私或合规风险的数据

---

## 八、外贸场景推荐组合

| 需求 | 推荐方案 | 预估成本 |
|------|-----------|---------|
| **竞品监控 (TikTok)** | clockworks/tiktok-scraper | $0.15-0.30/1000条 |
| **竞品监控 (Instagram)** | apify/instagram-scraper | $0.30-0.60/1000条 |
| **品牌舆情监控** | XPOZ Pro | $20/月起 |
| **趋势/达人/线索发现** | XPOZ Pro / Max | $20-200/月 |
| **B2B 线索挖掘** | x_guru/leads-scraper | $1/1000条 |
| **Google Maps 商家** | compass/crawler-google-places | $0.60-0.90/1000条 |
| **网站内容爬取** | apify/website-content-crawler | $0.10-0.20/页 |

---

## 九、风险提示

1. **平台风控**: 社交媒体平台可能封禁抓取行为
2. **法律合规**: 需遵守目标平台的 robots.txt 和使用条款
3. **数据隐私**: 避免抓取个人敏感信息
4. **Actor 稳定性**: 第三方 Actor 可能停止维护
5. **XPOZ 字段透明度**: 官网以能力描述为主，字段深度需实测确认

---

## 十、测试记录

**已验证**: TikTok Scraper (clockworks/tiktok-scraper)
- 抓取 10 条视频: 成功
- 数据字段: 24个完整字段
- 运行时间: ~30 秒
- 成本: ~$0.01

---

## 十一、结论

**已验证**: Apify 是外贸场景数据抓取的 **高性价比方案**，特别适合：
- 快速验证产品需求
- 中小规模数据监控
- 多平台数据整合

**新增判断**:
- 如果目标是“抓取层 + 自定义分析层”，优先 `Apify`
- 如果目标是“社媒情报层 + 直接给 AI 用”，优先 `XPOZ`

**建议起步方案**:
- 数据抓取验证：`Apify Free / Starter`
- 洞察验证：`XPOZ Pro`

---

**相关文档**:
- [TikTok Scraper 测试报告](./README.md)
- 测试脚本: `test_apify_tiktok.py`
- 原始数据: `results/`
