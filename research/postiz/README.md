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

| 本次验证目标 | 状态 | 说明 |
|-------------|------|------|
| 1. 本地 Docker 部署 | ⚠️ 受阻 | 网络问题无法拉取镜像 |
| 2. 核心功能完整性 | ✅ 代码验证 | 发布、排期、账号管理完整 |
| 3. AI 内容生成 | ✅ 文档验证 | GPT-4.1 + AI 图片/视频生成 |
| **4. API 可用性** | **✅✅ 完全可用** | **Public API + SDK + MCP** |

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
| API 测试 | ✅ 文档验证 | Public API + SDK + MCP 完整 |
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

## API 集成能力（关键发现 ⭐⭐⭐⭐⭐）

Postiz 提供**完整的 API 和 SDK 体系**，可以直接嵌入你的系统！

### 1. Public REST API

**认证方式**：
- **API Key**: `Authorization: your-api-key`
- **OAuth2 Token**: `Authorization: pos_your-oauth-token`

**Base URL**：
- 云服务: `https://api.postiz.com/public/v1`
- 自托管: `https://your-domain/api/public/v1`

**核心 API 端点**：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/integrations` | GET | 列出所有连接的社交账号 |
| `/integrations/:id` | DELETE | 删除社交账号 |
| `/posts` | GET | 获取帖子列表 |
| `/posts` | POST | **创建/排期/立即发布帖子** |
| `/posts/:id` | DELETE | 删除帖子 |
| `/upload` | POST | **上传图片/视频** |
| `/analytics/platform/:id` | GET | 获取平台分析数据 |
| `/analytics/post/:id` | GET | 获取单条帖子分析数据 |

### 2. SDK & 集成工具

| 工具 | 链接 | 用途 |
|------|------|------|
| **NodeJS SDK** | npm: `@postiz/node` | 在你的 Node.js 项目中直接调用 |
| **n8n Node** | npm: `n8n-nodes-postiz` | 自动化工作流集成 |
| **CLI 工具** | Postiz CLI | 命令行管理 |
| **Make.com** | 官方集成 | 无代码自动化 |

**Node.js SDK 示例**：
```javascript
import { PostizClient } from '@postiz/node';

const client = new PostizClient({
  apiKey: 'your-api-key',
  // 或者 baseUrl: 'https://your-selfhosted-instance.com'
});

// 获取所有社交账号
const integrations = await client.integrations.list();

// 创建帖子
await client.posts.create({
  type: 'schedule',
  date: '2024-12-14T10:00:00.000Z',
  posts: [{
    integration: { id: 'linkedin-integration-id' },
    value: [{
      content: 'Hello from API!',
      image: []
    }],
    settings: {
      __type: 'linkedin',
      post_as_images_carousel: false
    }
  }]
});
```

### 3. MCP (Model Context Protocol) - AI Agent 集成 ⭐

**可以直接让 AI Agent 操作 Postiz！**

Postiz 提供 MCP Server，AI agents（Claude, ChatGPT, Cursor）可以直接调用：

**MCP 工具列表**：
| 工具 | 功能 |
|------|------|
| `integrationList` | 列出所有社交账号 |
| `integrationSchema` | 获取平台发帖规则 |
| `triggerTool` | 执行平台特定操作（如列出 Discord 频道） |
| `schedulePostTool` | **排期/立即发布帖子** |
| `generateImageTool` | AI 生成图片 |
| `generateVideoTool` | AI 生成视频 |

**连接方式**：
```
URL: https://api.postiz.com/mcp
Authorization: Bearer your-api-key
```

### 4. 支持的平台（32 个）

**社交媒体**（12个）: X/Twitter, LinkedIn, LinkedIn Page, Facebook, Instagram, Instagram Standalone, Threads, Bluesky, Mastodon, Warpcast (Farcaster), Nostr, VK

**视频平台**（2个）: YouTube, TikTok

**社区平台**（7个）: Reddit, Lemmy, Discord, Slack, Telegram, Skool, Whop

**设计平台**（2个）: Pinterest, Dribbble

**博客平台**（4个）: Medium, Dev.to, Hashnode, WordPress

**商业工具**（2个）: Google My Business, Listmonk

**流媒体**（2个）: Twitch, Kick

### 5. 创建帖子示例

**最简单的帖子**（Threads, Mastodon, Bluesky, Telegram）：
```json
{
  "type": "schedule",
  "date": "2024-12-14T10:00:00.000Z",
  "posts": [{
    "integration": { "id": "threads-id" },
    "value": [{ "content": "Hello World!", "image": [] }],
    "settings": { "__type": "threads" }
  }]
}
```

**LinkedIn 帖子**：
```json
{
  "type": "schedule",
  "date": "2024-12-14T10:00:00.000Z",
  "posts": [{
    "integration": { "id": "linkedin-id" },
    "value": [{ "content": "Check out our product!", "image": [] }],
    "settings": { 
      "__type": "linkedin",
      "post_as_images_carousel": true
    }
  }]
}
```

**带图片的帖子**（先上传，再发布）：
```bash
# 1. 上传图片
curl -X POST "https://api.postiz.com/public/v1/upload" \
  -H "Authorization: your-api-key" \
  -F "file=@photo.jpg"

# 返回: { "id": "img-123", "path": "https://uploads..." }

# 2. 创建帖子时使用上传的图片 ID
{
  "value": [{
    "content": "Beautiful photo!",
    "image": [{ "id": "img-123", "path": "https://uploads..." }]
  }]
}
```

### 6. 限制与配额

- **API 限制**: 30 请求/小时（注意：每个 API 调用算一次请求，可以批量排期）
- **文件上传**: 支持图片、视频

---

## API 架构分析（内部实现）

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

**是否值得继续**: ✅✅ **强烈推荐！API 集成能力优秀**

### 核心优势 ⭐⭐⭐⭐⭐
- **API 体系完整**: REST API + Node.js SDK + n8n + Make.com + MCP
- **支持 32 个平台**: 覆盖所有主流外贸社媒
- **AI 集成深度高**: GPT-4.1 + CopilotKit + AI 生成图片/视频
- **可直接嵌入系统**: 通过 API Key 或 OAuth 轻松集成
- **AI Agent 支持**: MCP 协议让 Claude/ChatGPT 直接操作 Postiz

### 缺点
- **AGPL 协议**: 自托管需开源修改（可用官方云服务规避）
- **API 限制**: 30 请求/小时（建议批量操作）
- **部署复杂**: 需要 PostgreSQL + Redis + Temporal

### 外贸场景适配度: **9/10** ⭐

### 建议集成方案

**方案 1: 直接使用官方云服务（推荐短期）**
- ✅ 无需部署，立即使用
- ✅ 规避 AGPL 协议问题
- ✅ 获取 API Key 后直接调用
- ❓ 需了解价格

**方案 2: 自托管（推荐长期）**
- ✅ 完全掌控数据
- ⚠️ AGPL 协议限制（需开源修改）
- ⚠️ 需要解决部署问题

**方案 3: Fork + 重构（长期战略）**
- ✅ 参考 Postiz 架构自研
- ✅ 完全闭源，无协议限制
- ⚠️ 开发成本高

### 立即行动建议
1. **联系官方**了解云服务价格和 Enterprise 方案
2. **注册试用**获取 API Key 测试集成
3. **评估需求**确定是否需要多租户、客户隔离等功能
4. **技术预研**基于 Node.js SDK 开发原型

### 系统集成示例思路
```
你的外贸系统
    ↓ (调用 Postiz API)
Postiz (云服务或自托管)
    ↓ (OAuth 授权)
LinkedIn, Instagram, TikTok...
```

可以通过 API 实现：
- 一键发布产品内容到多个平台
- 定时排期发布营销内容
- AI 自动生成多语言内容
- 统一查看各平台数据表现

---

## 参考链接

- [Postiz GitHub](https://github.com/gitroomhq/postiz-app)
- [Postiz 文档](https://docs.postiz.com)
- [Docker 部署指南](https://docs.postiz.com/installation/docker)
