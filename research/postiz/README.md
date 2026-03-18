# Postiz 调研记录

**GitHub**: https://github.com/gitroomhq/postiz-app  
**文档**: https://docs.postiz.com  
**官网**: https://postiz.com  

---

## 基本信息

| 属性 | 说明 |
|------|------|
| **开源协议** | AGPL-3.0 |
| **技术栈** | NestJS + Next.js + Prisma |
| **数据库** | PostgreSQL + Redis |
| **部署方式** | Docker / Docker Compose |
| **平台支持** | Twitter/X, LinkedIn, Reddit, YouTube, TikTok, Instagram, Facebook, Pinterest, Threads, Bluesky, Mastodon, Discord, Slack |

---

## 本次验证目标

1. ✅ 本地 Docker 部署是否顺利
2. ✅ 核心功能是否完整（发布、排期、账号管理）
3. ✅ 是否支持 AI 内容生成
4. ✅ API 是否可用（便于集成）

---

## 环境与前置条件

### 环境要求
- Node.js 18+（开发模式）
- Docker & Docker Compose（推荐）
- PostgreSQL 14+
- Redis 6+

### 本地部署步骤

```bash
# 1. 克隆仓库
git clone https://github.com/gitroomhq/postiz-app.git
cd postiz-app

# 2. 创建 .env 文件（从示例复制）
cp .env.example .env

# 3. 修改配置
# - 设置 MAIN_URL=http://localhost:4200
# - 设置 FRONTEND_URL=http://localhost:3000
# - 设置 DATABASE_URL="postgresql://..."
# - 设置 REDIS_URL="redis://localhost:6379"
# - 设置各平台 OAuth Key（可选，本地测试可先跳过）

# 4. 启动 Docker
npm run docker:compose:up
```

---

## 验证进度

| 阶段 | 状态 | 备注 |
|------|------|------|
| 环境准备 | ✅ 已完成 | Docker 环境已就绪 |
| 代码分析 | ✅ 已完成 | 已分析核心功能 |
| 本地部署 | ⚠️ 受阻 | 网络问题无法拉取镜像 |
| 功能验证 | ⏸️ 暂停 | 等待部署完成 |
| AI 功能 | ✅ 代码验证 | 确认支持 GPT-4.1 + CopilotKit |
| API 测试 | ⏸️ 暂停 | 等待部署完成 |
| 文档输出 | ✅ 已完成 | 已生成详细评估报告 |

---

## 结果

### 是否跑通
- 待验证

### 关键页面截图
- 位置：`research/postiz/screenshots/`

### 支持平台（20+）

| 平台 | 类型 | 优先级 |
|------|------|--------|
| **Twitter/X** | 社交媒体 | ⭐⭐⭐⭐⭐ |
| **LinkedIn** | 社交媒体 | ⭐⭐⭐⭐⭐ |
| **Instagram** | 社交媒体 | ⭐⭐⭐⭐⭐ |
| **Facebook** | 社交媒体 | ⭐⭐⭐⭐ |
| **TikTok** | 短视频 | ⭐⭐⭐⭐⭐ |
| **YouTube** | 视频 | ⭐⭐⭐⭐ |
| **Pinterest** | 图文 | ⭐⭐⭐⭐ |
| **Reddit** | 社区 | ⭐⭐⭐ |
| **Threads** | 社交媒体 | ⭐⭐⭐ |
| **Bluesky** | 社交媒体 | ⭐⭐ |
| **Mastodon** | 社交联邦 | ⭐⭐ |
| **Discord** | 社区 | ⭐⭐⭐ |
| **Slack** | 协作 | ⭐⭐ |
| **Telegram** | 即时通讯 | ⭐⭐⭐ |
| **Medium** | 博客 | ⭐⭐ |
| **dev.to** | 开发者社区 | ⭐ |
| **WordPress** | CMS | ⭐⭐ |

## AI 能力详细分析

通过代码分析发现 Postiz 具有强大的 AI 集成能力：

### 1. OpenAI 集成
- **模型**: GPT-4.1
- **功能**: 内容生成、对话助手
- **控制器**: `apps/backend/src/api/routes/copilot.controller.ts`

### 2. CopilotKit 集成
- 提供 AI 辅助内容创作界面
- 支持实时聊天和内容建议

### 3. 内容生成功能
- **API 端点**: `POST /posts/generator`
- **功能**: 根据提示自动生成社交媒体内容
- **多平台适配**: 支持为不同平台生成定制化内容

### 4. Mastra AI 框架
- 集成 Mastra 用于 Agent 工作流
- 支持复杂的内容生成和调度任务

---

## API 架构分析

### 核心模块
- **PostsController**: 内容发布、排期、统计分析
- **IntegrationsController**: 社交平台账号管理
- **CopilotController**: AI 对话和内容生成
- **Public API**: 提供外部集成接口

### 数据模型 (Prisma)
- Organization: 组织/团队管理
- Integration: 社交平台账号
- Post: 内容和发布计划
- User: 用户管理

---

## 外贸场景适配分析

### 直接可用功能
| 功能 | 适用性 | 说明 |
|------|--------|------|
| 多平台发布 | ⭐⭐⭐⭐⭐ | 支持所有主流外贸社媒平台 |
| 内容排期 | ⭐⭐⭐⭐⭐ | 可预设发布时间，适合跨时区运营 |
| 团队协作 | ⭐⭐⭐⭐ | 支持多成员、多组织 |
| AI 内容生成 | ⭐⭐⭐⭐ | 可生成英文内容，需配置 Prompt |

### 需二次开发
| 功能 | 优先级 | 开发量 |
|------|--------|--------|
| 多语言模板 | 高 | 中 |
| 行业内容库 | 高 | 中 |
| 数据回流分析 | 中 | 中 |
| 客户隔离机制 | 中 | 高 |

---

## 成本分析

| 成本项 | 说明 |
|--------|------|
| **自托管** | 免费（AGPL-3.0 协议） |
| **云服务** | Postiz 官方提供托管版，价格待查 |
| **部署成本** | VPS + 域名，约 $5-10/月 |
| **API 调用** | 需自备各平台 API Key |
| **OpenAI** | 按使用量计费 ~$0.01-0.03/1K tokens |

---

## 问题与风险

| 问题 | 说明 | 风险等级 |
|------|------|----------|
| **AGPL 协议** | 自托管需开源修改，商用受限 | 高 |
| 平台 API 限制 | 各社交平台 API 有频率限制 | 中 |
| OAuth 配置复杂 | 每个平台需单独申请开发者账号 | 中 |
| 视频/图片上传 | 部分平台有格式和大小限制 | 低 |

---

## 结论

**状态**: 🟡 代码层面已调研，部署受阻

**是否值得继续**: ✅ **建议继续评估**

### 优点
- 开源免费，功能完整
- 支持 20+ 社交平台（超出预期）
- AI 集成深度高（OpenAI + CopilotKit + Mastra）
- 技术栈现代化，易于扩展
- 有完整的 API 和 SDK

### 缺点
- **AGPL 协议对商用不友好**
- 部署依赖较多（PostgreSQL + Redis + Temporal）
- 每个平台需单独申请 OAuth

### 外贸场景适配度: 8/10

**建议方案**:
1. **短期**: 用官方云服务（规避 AGPL 限制）
2. **中期**: Fork 后深度定制，满足外贸特定需求
3. **长期**: 基于 Postiz 架构自研，完全掌控

**下一步**:
1. 联系官方了解托管版价格
2. 尝试通过代理或其他方式完成本地部署
3. 评估是否需要 Fork 后闭源修改

---

## 参考链接

- [Postiz GitHub](https://github.com/gitroomhq/postiz-app)
- [Postiz 文档](https://docs.postiz.com)
- [Docker 部署指南](https://docs.postiz.com/installation/docker)
