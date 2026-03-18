# Apify TikTok Scraper 测试报告

**测试时间**: 2026-03-18 16:55  
**测试工具**: clockworks/tiktok-scraper (Apify Actor)  
**测试关键词**: phone case

---

## ✅ 测试结论：已验证

Apify TikTok Scraper 可以成功抓取 TikTok 搜索数据，数据完整性良好。

### 关键发现

| 指标 | 结果 |
|------|------|
| 成功抓取 | ✅ 10 条视频 |
| API 响应时间 | ~30 秒 |
| 数据字段完整度 | 24 个字段 |
| 包含互动数据 | ✅ 点赞、评论、分享、播放数 |
| 包含作者信息 | ✅ 粉丝数、获赞数、简介 |

### 可用字段（24个）

**基础信息**
- `id` - 视频唯一ID
- `text` - 视频文案
- `textLanguage` - 文案语言
- `createTime` / `createTimeISO` - 发布时间
- `webVideoUrl` - 视频链接

**互动数据** ⭐（爆款分析关键）
- `diggCount` - 点赞数
- `shareCount` - 分享数
- `playCount` - 播放数
- `collectCount` - 收藏数
- `commentCount` - 评论数
- `repostCount` - 转发数

**作者信息**
- `authorMeta` - 包含昵称、粉丝数、获赞数、简介等

**内容元数据**
- `videoMeta` - 视频分辨率、时长、封面
- `hashtags` - 标签列表
- `musicMeta` - 背景音乐信息
- `isAd` - 是否为广告

### 样本数据

**热门视频示例**:
- ID: 7611697361722625298
- 文案: "High-quality Samsung S26 Ultra phone case..."
- 播放: 99,800 | 点赞: 821 | 分享: 210 | 评论: 28
- 作者粉丝: 97,800

**第二个视频**:
- ID: 7608917960744340754
- 文案包含详细产品描述（ Glossy Maroon Case...）
- 尼泊尔商家，1.28万粉丝

---

## 适用场景

✅ **爆款内容拆解**: 可获取互动数据、文案、标签  
✅ **竞品分析**: 可追踪特定账号/话题的表现  
✅ **关键词研究**: 搜索任意关键词查看热门内容

## 限制与注意事项

⚠️ 每条数据约 1KB，大量抓取需注意存储  
⚠️ 视频 URL 有有效期限制（x-expires 参数）  
⚠️ 部分字段可能为 null（如 commentsDatasetUrl）

## 文件位置

```
demos/apify-test/results/
├── tiktok_phone_case_20260318_165550.json     # 原始数据 (50KB)
├── report_phone_case_20260318_165550.json     # 分析报告
└── test_summary_20260318_165550.json          # 测试总结
```

---

## 成本估算

- Actor 运行时间: ~30 秒
- 抓取 10 条视频: 约 $0.01 USD
- 估算每 1000 条: ~$1 USD

## 下一步建议

1. ✅ 数据可用性已验证
2. 可扩展测试：多关键词、多语言、长期追踪
3. 可开发：爆款指标计算脚本
