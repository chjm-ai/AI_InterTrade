# Chatwoot 本地部署

## 当前目标

在本机先起一个可用于 demo 的 Chatwoot 实例，供后续接网站表单、WhatsApp 和 webhook。

## 版本

- Chatwoot: `v4.10.1`
- 参考时间：`2026-03-18`

## 目录说明

- `.env`：本地运行变量，不提交
- `docker-compose.local.yml`：本地 pinned 版 compose
- `prepare-env.sh`：生成本地 `.env`
- `up.sh`：启动并初始化数据库

## 启动前提

本机需要可用的 Docker Engine。

当前这台机器上我正在补：

- `colima`
- `docker`
- `docker-compose`

## 启动命令

```bash
cd /Users/wesley/Desktop/Repos/AI_InterTrade/demos/inquiry-intake/chatwoot
./prepare-env.sh
./up.sh
```

首次初始化完成后，访问：

```text
http://127.0.0.1:3000
```

## 默认本地配置

| 项目 | 值 |
| --- | --- |
| URL | `http://127.0.0.1:3000` |
| Rails 环境 | `production` |
| 注册开关 | `false` |
| 存储 | `local` |
| Redis / Postgres | Compose 内置容器 |

## 说明

这个目录基于 Chatwoot 官方 Docker 生产模板整理，但把镜像固定到了 `v4.10.1`，避免 demo 期间被 `latest` 变更影响。
