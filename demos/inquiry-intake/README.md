# 询盘承接 Demo 执行说明

## demo 目标

在 1 个后台中演示：

- 2 个渠道进入统一收件箱
- 英文、西语询盘可被识别
- AI 生成中文摘要和回复建议
- 销售人工确认后发送
- 线索同步到台账

## 最小交付物

| 交付物 | 说明 |
| --- | --- |
| 配置完成的 Chatwoot 后台 | 可展示收件箱、标签、分配 |
| 1 条英文样本、1 条西语样本 | 用于演示多语种 |
| AI 处理流程截图 | 证明不是纯手工 |
| 线索台账 | Google Sheets / Airtable 均可 |
| 1 段 3 分钟录屏 | 用于客户展示 |

## 环境准备清单

| 项目 | 要求 | 备注 |
| --- | --- | --- |
| Chatwoot 实例 | 可登录后台 | 云版或自部署都可 |
| 网站表单页 | 可提交 name/email/message | 可以是静态页 |
| WhatsApp 测试号 | 能收发消息 | 若受阻可先跳过 |
| AI API | 可用的模型 key | 用于识别和生成草稿 |
| 自动化层 | n8n 或 webhook 服务 | 接 Chatwoot webhook |
| 线索表 | Google Sheets / Airtable | 保存演示结果 |

## 搭建步骤

## Step 1. 建收件箱

1. 在 Chatwoot 创建 `Demo Sales Inbox`
2. 创建测试客服账号
3. 新建标签：
   - `new-lead`
   - `price-request`
   - `sample-request`
   - `high-priority`

## Step 2. 接网站表单

1. 准备一个简单表单页面，字段为：
   - name
   - email
   - country
   - message
2. 表单提交到 webhook
3. webhook 将消息写入 Chatwoot 对话
4. 验证消息能进入 `Demo Sales Inbox`

## Step 3. 接第二渠道

优先顺序：

1. WhatsApp Cloud API
2. 若受阻，改为第二个 webhook 来源模拟“平台 B”

要求：

- 在 Chatwoot 中能看到不同渠道来源
- 至少能演示两条不同来源的消息进入同一后台

## Step 4. 配 AI 流程

Webhook 收到新消息后，输出以下字段：

```json
{
  "language": "en",
  "intent": "price_request",
  "summary_cn": "客户来自墨西哥，询问 MOQ、FOB 价格和交期",
  "reply_draft": "Thanks for your inquiry...",
  "priority": "high",
  "missing_info": ["target quantity", "destination port"]
}
```

回写动作：

1. 把 `summary_cn` 写进会话 note
2. 把 `intent` 映射成标签
3. 把 `priority=high` 映射成 `high-priority`
4. 把线索同步进表格

## Step 5. 准备测试样本

建议最少 3 条：

| 语言 | 样本目的 |
| --- | --- |
| 英文 | 标准报价询盘 |
| 西语 | 验证多语种承接 |
| 中英混合 | 验证真实场景容错 |

## Step 6. 录制 demo

录屏顺序：

1. 展示两个入口
2. 提交英文询盘
3. 提交西语询盘
4. 展示 Chatwoot 收件箱
5. 点开会话看 AI note、标签、建议回复
6. 人工编辑一句后发送
7. 展示线索表
8. 收尾说明可扩展到更多平台

## 验收清单

- [ ] 两个来源已接入
- [ ] 英文样本已跑通
- [ ] 西语样本已跑通
- [ ] AI note 已回写
- [ ] 标签已自动打上
- [ ] 至少 1 条回复已人工发送
- [ ] 线索表已新增记录
- [ ] 已录屏

## 输出文件

- 演示话术：[script.md](/Users/wesley/Desktop/Repos/AI_InterTrade/demos/inquiry-intake/script.md)
- 账号与依赖记录：[links.md](/Users/wesley/Desktop/Repos/AI_InterTrade/demos/inquiry-intake/links.md)
