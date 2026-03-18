#!/usr/bin/env python3
"""
Apify TikTok Scraper 测试脚本
用于验证 clockworks/tiktok-scraper Actor 的数据获取能力
"""

import requests
import json
import time
from datetime import datetime
import os

APIFY_API_BASE = "https://api.apify.com/v2"


class TikTokScraperTest:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.actor_id = "clockworks/tiktok-scraper"

    def run_scraper(self, search_keyword: str, max_results: int = 20):
        """运行 TikTok Scraper"""
        run_input = {
            "searchQueries": [search_keyword],
            "resultsPerPage": max_results,
            "maxProfilesPerQuery": 1,
            "shouldDownloadVideos": False,
            "shouldDownloadCovers": False,
            "shouldDownloadSlideshowImages": False,
        }

        url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper/runs"
        response = requests.post(url, headers=self.headers, json=run_input)

        if response.status_code == 201:
            run_data = response.json()
            run_id = run_data["data"]["id"]
            print(f"✅ Run 已启动，ID: {run_id}")
            return run_id
        else:
            print(f"❌ 启动失败: {response.status_code}")
            print(response.text)
            return None

    def wait_for_run(self, run_id: str, timeout: int = 300):
        """等待 Run 完成"""
        url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper/runs/{run_id}"
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()["data"]
                status = data["status"]

                if status == "SUCCEEDED":
                    print(f"✅ Run 完成！")
                    return data
                elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                    print(f"❌ Run 失败: {status}")
                    return None
                else:
                    print(f"⏳ 状态: {status}...")
                    time.sleep(5)

        print("⏰ 超时")
        return None

    def get_dataset(self, dataset_id: str):
        """获取抓取结果"""
        url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 获取数据失败: {response.status_code}")
            return None

    def analyze_and_save(self, data: list, keyword: str, output_dir: str):
        """分析数据并保存"""
        if not data:
            print("⚠️ 没有数据")
            return None

        print(f"\n📊 抓取结果统计:")
        print(f"   总条数: {len(data)}")

        # 分析字段结构
        sample = data[0]
        print(f"\n🔍 字段结构分析:")
        fields_summary = []

        for key, value in sample.items():
            value_type = type(value).__name__
            preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"   - {key} ({value_type})")
            fields_summary.append({"field": key, "type": value_type})

        # 保存完整数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/tiktok_{keyword.replace(' ', '_')}_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 数据已保存到: {filename}")

        # 生成报告
        report = {
            "keyword": keyword,
            "timestamp": timestamp,
            "total_count": len(data),
            "fields": fields_summary,
            "sample": sample,
        }

        report_file = (
            f"{output_dir}/report_{keyword.replace(' ', '_')}_{timestamp}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report


def main():
    print("=" * 60)
    print("🚀 Apify TikTok Scraper 测试")
    print("=" * 60)

    # 从环境变量读取 token
    api_token = os.environ.get("APIFY_API_TOKEN")

    if not api_token:
        print("\n⚠️  请先设置环境变量 APIFY_API_TOKEN")
        return

    # 创建输出目录
    output_dir = "/Users/wesley/Desktop/Repos/AI_InterTrade/AI_InterTrade/demos/apify-test/results"
    os.makedirs(output_dir, exist_ok=True)

    # 初始化测试
    tester = TikTokScraperTest(api_token)

    # 测试关键词（外贸相关）
    test_keywords = ["phone case"]

    all_reports = []

    for keyword in test_keywords:
        print(f"\n{'=' * 60}")
        print(f"🔍 测试关键词: {keyword}")
        print(f"{'=' * 60}")

        # 启动抓取
        run_id = tester.run_scraper(keyword, max_results=10)

        if run_id:
            # 等待完成
            run_data = tester.wait_for_run(run_id)

            if run_data:
                dataset_id = run_data["defaultDatasetId"]
                print(f"📦 Dataset ID: {dataset_id}")

                # 获取数据
                data = tester.get_dataset(dataset_id)

                if data:
                    # 分析并保存
                    report = tester.analyze_and_save(data, keyword, output_dir)
                    if report:
                        all_reports.append(report)

    # 生成测试总结
    print(f"\n{'=' * 60}")
    print("📋 测试总结")
    print(f"{'=' * 60}")

    summary_file = (
        f"{output_dir}/test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "test_time": datetime.now().isoformat(),
                "total_tests": len(all_reports),
                "reports": all_reports,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"✅ 测试完成！结果保存在: {output_dir}/")
    print(f"   总结报告: {summary_file}")


if __name__ == "__main__":
    main()
