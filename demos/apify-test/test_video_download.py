#!/usr/bin/env python3
"""
Apify TikTok 视频下载测试
测试两种模式：
1. 不下载视频（默认）- 只获取元数据
2. 下载视频 - 获取视频文件 URL
"""

import requests
import json
import time
import os

APIFY_API_BASE = "https://api.apify.com/v2"


def test_video_download():
    api_token = os.environ.get("APIFY_API_TOKEN")
    if not api_token:
        print("请先设置 APIFY_API_TOKEN")
        return

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    print("=" * 60)
    print("🎬 TikTok 视频下载测试")
    print("=" * 60)

    # 测试配置：启用视频下载
    run_input = {
        "searchQueries": ["phone case"],
        "resultsPerPage": 3,  # 只抓3条，测试用
        "maxProfilesPerQuery": 1,
        "shouldDownloadVideos": True,  # ✅ 启用视频下载
        "shouldDownloadCovers": True,  # 下载封面
        "shouldDownloadSlideshowImages": False,
    }

    print("\n📋 测试配置:")
    print(f"   关键词: phone case")
    print(f"   抓取数量: 3")
    print(f"   下载视频: True")

    # 启动 Actor
    url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper/runs"
    response = requests.post(url, headers=headers, json=run_input)

    if response.status_code != 201:
        print(f"❌ 启动失败: {response.status_code}")
        print(response.text)
        return

    run_id = response.json()["data"]["id"]
    print(f"\n✅ Run 已启动: {run_id}")

    # 等待完成
    run_url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper/runs/{run_id}"
    start_time = time.time()

    while time.time() - start_time < 600:  # 10分钟超时
        run_resp = requests.get(run_url, headers=headers)
        if run_resp.status_code == 200:
            data = run_resp.json()["data"]
            status = data["status"]

            if status == "SUCCEEDED":
                print(f"✅ Run 完成！")
                break
            elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                print(f"❌ Run 失败: {status}")
                return
            else:
                print(f"⏳ 状态: {status}...")
                time.sleep(10)

    # 获取数据集
    dataset_id = data["defaultDatasetId"]
    dataset_url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
    data_resp = requests.get(dataset_url, headers=headers)

    if data_resp.status_code != 200:
        print(f"❌ 获取数据失败")
        return

    items = data_resp.json()

    print(f"\n📊 抓取结果:")
    print(f"   总条数: {len(items)}")

    # 分析 mediaUrls 字段
    for i, item in enumerate(items):
        print(f"\n🎥 视频 {i + 1}:")
        print(f"   ID: {item['id']}")
        print(f"   文案: {item['text'][:50]}...")
        print(f"   webVideoUrl: {item['webVideoUrl']}")

        media_urls = item.get("mediaUrls", [])
        if media_urls:
            print(f"   mediaUrls: {len(media_urls)} 个")
            for j, media_url in enumerate(media_urls[:2]):  # 只显示前2个
                print(f"      [{j + 1}] {media_url[:80]}...")
        else:
            print(f"   mediaUrls: [] (空)")

    # 保存完整数据
    output_dir = "/Users/wesley/Desktop/Repos/AI_InterTrade/AI_InterTrade/demos/apify-test/results"
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/tiktok_video_download_test_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"\n💾 数据已保存: {filename}")

    # 生成报告
    print(f"\n{'=' * 60}")
    print("📋 视频下载能力报告")
    print(f"{'=' * 60}")

    has_video_urls = any(item.get("mediaUrls") for item in items)

    if has_video_urls:
        print("\n✅ 发现 mediaUrls 字段包含视频链接")
        print("   这些链接可以直接下载视频文件")
    else:
        print("\n⚠️ mediaUrls 为空")
        print("   原因分析:")
        print("   1. clockworks/tiktok-scraper 默认不提供原始视频 URL")
        print("   2. shouldDownloadVideos=True 会尝试下载视频到 Apify 存储")
        print("   3. 需要通过 Key-Value Store 获取下载的视频文件")

    # 检查 Key-Value Store
    key_value_store_id = data.get("defaultKeyValueStoreId")
    if key_value_store_id:
        print(f"\n🔑 Key-Value Store ID: {key_value_store_id}")
        print("   视频文件可能存储在这里")

        # 尝试列出 Key-Value Store 中的文件
        kv_url = f"{APIFY_API_BASE}/key-value-stores/{key_value_store_id}/keys"
        kv_resp = requests.get(kv_url, headers=headers)
        if kv_resp.status_code == 200:
            keys_data = kv_resp.json()
            print(f"   存储中的键: {keys_data}")


if __name__ == "__main__":
    test_video_download()
