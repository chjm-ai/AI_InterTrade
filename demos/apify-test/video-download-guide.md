# Apify TikTok 视频下载指南

**测试时间**: 2026-03-18  
**测试结论**: ✅ 视频可以顺利下载

---

## 视频下载能力验证

### 测试配置

```python
run_input = {
    "searchQueries": ["phone case"],
    "resultsPerPage": 3,
    "shouldDownloadVideos": True,      # ✅ 启用视频下载
    "shouldDownloadCovers": True,      # 同时下载封面
}
```

### 测试结果

| 指标 | 结果 |
|------|------|
| **视频下载** | ✅ 成功 (3个视频) |
| **视频格式** | MP4 |
| **视频大小** | 1.6MB - 2.3MB |
| **下载速度** | ~500KB/s |
| **存储位置** | Apify Key-Value Store |

---

## 视频下载方式

### 方式 1: 通过 mediaUrls 字段（推荐）

抓取结果中包含 `mediaUrls` 数组，每个视频提供一个直接下载链接：

```json
{
  "id": "7611697361722625298",
  "mediaUrls": [
    "https://api.apify.com/v2/key-value-stores/4OrmFsOoa0MDKDMGz/records/video-trainamhun-20260227235326-7611697361722625298.mp4"
  ]
}
```

**下载命令**:
```bash
curl -L -o video.mp4 "https://api.apify.com/v2/key-value-stores/.../records/video-xxx.mp4"
```

### 方式 2: 通过 Key-Value Store API

获取所有存储的文件列表：

```python
import requests

headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
store_id = "4OrmFsOoa0MDKDMGz"

# 列出所有文件
url = f"https://api.apify.com/v2/key-value-stores/{store_id}/keys"
response = requests.get(url, headers=headers)
files = response.json()["data"]["items"]

# 过滤视频文件
videos = [f for f in files if f["key"].endswith(".mp4")]
for video in videos:
    print(f"文件名: {video['key']}")
    print(f"大小: {video['size'] / 1024 / 1024:.2f} MB")
    print(f"下载链接: {video['recordPublicUrl']}")
```

---

## 存储结构说明

当启用视频下载时，Apify 会在 **Key-Value Store** 中存储以下文件：

```
Key-Value Store (4OrmFsOoa0MDKDMGz)
├── video-aiedacases-20260226114632-7611138930347461901.mp4 (2.3MB)
├── video-caseholicn-20260220120752-7608917960744340754.mp4 (1.6MB)
├── video-trainamhun-20260227235326-7611697361722625298.mp4 (2.1MB)
├── cover-aiedacases-20260226114632-7611138930347461901.jpg (172KB)
├── cover-caseholicn-20260220120752-7608917960744340754.jpg (393KB)
└── cover-trainamhun-20260227235326-7611697361722625298.jpg (197KB)
```

**命名规则**:
- `video-{username}-{timestamp}-{video_id}.mp4`
- `cover-{username}-{timestamp}-{video_id}.jpg`

---

## 视频 URL 有效期

⚠️ **重要**: Key-Value Store 中的文件 URL **有有效期限制**

从之前的抓取数据可以看到：
```
https://p16-common-sign.tiktokcdn-us.com/...?x-expires=1773993600&...
```

**有效期策略**:
- Key-Value Store 中的视频文件：长期有效（只要存储未删除）
- TikTok CDN 的原始链接：几小时到几天

**建议**:
1. 抓取后立即下载视频到本地存储
2. 不要依赖 `mediaUrls` 长期有效
3. 如需长期保存，使用 `recordPublicUrl` 并及时转存

---

## 批量下载脚本

```python
#!/usr/bin/env python3
"""批量下载 TikTok 视频"""

import requests
import os
import json

def download_tiktok_videos(api_token, store_id, output_dir="./videos"):
    headers = {"Authorization": f"Bearer {api_token}"}
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有文件列表
    url = f"https://api.apify.com/v2/key-value-stores/{store_id}/keys"
    response = requests.get(url, headers=headers)
    files = response.json()["data"]["items"]
    
    # 下载视频和封面
    for file_info in files:
        key = file_info["key"]
        if not (key.endswith(".mp4") or key.endswith(".jpg")):
            continue
            
        download_url = file_info["recordPublicUrl"]
        filename = os.path.join(output_dir, key)
        
        print(f"下载: {key} ({file_info['size'] / 1024:.1f} KB)")
        
        # 下载文件
        r = requests.get(download_url, headers=headers, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"\n✅ 下载完成！文件保存在: {output_dir}/")

# 使用示例
download_tiktok_videos(
    api_token="your_api_token",
    store_id="4OrmFsOoa0MDKDMGz",
    output_dir="./tiktok_videos"
)
```

---

## 视频质量

从抓取的视频元数据可以看到：

```json
{
  "videoMeta": {
    "height": 1024,
    "width": 576,
    "duration": 16,
    "definition": "540p",
    "format": "mp4"
  }
}
```

| 参数 | 值 | 说明 |
|------|-----|------|
| **分辨率** | 576x1024 | 竖屏视频 |
| **清晰度** | 540p | 标准清晰度 |
| **时长** | 16秒 | 示例视频 |
| **格式** | MP4 | 通用格式 |

**注意**: 
- TikTok 网页版默认提供 540p 视频
- 如需更高清晰度 (720p/1080p)，可能需要其他下载方式

---

## 成本分析

### 视频下载的成本组成

| 费用项 | 费用 | 说明 |
|--------|------|------|
| **Actor 运行** | ~0.5-1 CU/100条 | 抓取 + 下载视频 |
| **存储费用** | $1/1000 GB-hours | Key-Value Store |
| **数据传输** | $0.2/GB | 下载到本地 |

### 示例成本计算

抓取并下载 100 个视频：
- 平均视频大小: 2MB
- 总大小: 200MB
- Actor 运行: ~1 CU = $0.30
- 存储 1 小时: 0.2 GB-hours = $0.0002
- 下载流量: 0.2 GB = $0.04
- **总成本**: ~$0.34

**结论**: 下载视频的成本非常低，主要消耗是 Actor 运行的 CU。

---

## 限制与注意事项

### ⚠️ 技术限制

1. **视频质量**: 默认 540p，非最高清
2. **无水印**: 下载的视频通常无 TikTok 水印
3. **文件大小**: 单视频通常 1-5MB
4. **下载速度**: 取决于 Apify 服务器带宽

### ⚠️ 法律合规

1. **版权问题**: 下载视频仅供个人研究，不可商用
2. **平台政策**: 遵守 TikTok 的使用条款
3. **隐私保护**: 不要传播用户私人视频
4. **数据留存**: 建议设置自动清理策略

### ⚠️ 技术建议

1. **及时下载**: 抓取后立即下载到本地存储
2. **分批处理**: 大量视频时分批抓取和下载
3. **存储管理**: 定期清理 Key-Value Store
4. **备份策略**: 重要视频及时转存到 AWS S3 等持久存储

---

## 实用代码片段

### 检查视频是否可播放

```python
import cv2

def check_video(file_path):
    cap = cv2.VideoCapture(file_path)
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        print(f"✅ 视频可播放")
        print(f"   FPS: {fps}")
        print(f"   帧数: {frame_count}")
        print(f"   时长: {duration:.1f}秒")
    else:
        print("❌ 视频无法播放")
    cap.release()

check_video("test_video_1.mp4")
```

### 获取视频缩略图

```python
from PIL import Image
import cv2

def extract_thumbnail(video_path, output_path, time_sec=1):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, time_sec * 1000)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"✅ 缩略图已保存: {output_path}")
    cap.release()

extract_thumbnail("test_video_1.mp4", "thumbnail.jpg", time_sec=2)
```

---

## 结论

✅ **已验证**: Apify TikTok Scraper 可以顺利下载视频

- 启用 `shouldDownloadVideos: True` 即可获得视频文件
- 视频通过 `mediaUrls` 提供下载链接
- 视频存储在 Key-Value Store 中，可长期访问
- 格式为标准 MP4，质量 540p
- 下载成本低廉，约 $0.34/100条视频

**推荐做法**: 
1. 抓取时启用视频下载
2. 通过 `mediaUrls` 批量下载到本地
3. 及时转存到持久存储（如 S3）
4. 定期清理 Apify 存储以节省费用

---

**相关文档**:
- [平台概览](./platform-overview.md)
- [测试报告](./README.md)
- 测试脚本: `test_video_download.py`
