#!/usr/bin/env python3
"""
Apify TikTok Scraper 测试脚本
阶段1：技术可行性验证
"""

import requests
import json
import time
from datetime import datetime

# Apify API 配置
APIFY_API_BASE = "https://api.apify.com/v2"

class TikTokScraperTest:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        self.actor_id = "clockworks/tiktok-scraper"  # TikTok Scraper Actor (热门)
    
    def get_actor_info(self):
        """获取 Actor 信息"""
        url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def run_scraper(self, search_keyword: str, max_results: int = 50):
        """
        运行 TikTok Scraper
        
        Args:
            search_keyword: 搜索关键词（如 "phone case" 或 "furniture"）
            max_results: 最大抓取数量
        """
        # 构建输入参数
        run_input = {
            "searchQueries": [search_keyword],  # clockworks 用这个参数
            "resultsPerPage": max_results,
            "maxProfilesPerQuery": 1,  # 至少1个用户（>=1）
            "shouldDownloadVideos": False,  # 不下载视频文件，只抓元数据
            "shouldDownloadCovers": False,
            "shouldDownloadSlideshowImages": False,
        }
        
        # 启动 Actor Run
        url = f"{APIFY_API_BASE}/acts/clockworks~tiktok-scraper/runs"
        response = requests.post(
            url,
            headers=self.headers,
            json=run_input
        )
        
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
    
    def analyze_fields(self, data: list):
        """分析返回的字段结构"""
        if not data:
            print("⚠️ 没有数据")
            return
        
        print(f"\n📊 抓取结果统计:")
        print(f"   总条数: {len(data)}")
        
        # 获取第一条数据的所有字段
        sample = data[0]
        print(f"\n🔍 字段结构分析:")
        
        for key, value in sample.items():
            value_type = type(value).__name__
            preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            print(f"   - {key} ({value_type}): {preview}")
        
        # 保存完整数据供人工检查
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research/viral-content-test/tiktok_sample_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 数据已保存到: {filename}")
        
        return {
            "total_count": len(data),
            "fields": list(sample.keys()),
            "sample": sample
        }

def main():
    """
    测试流程：
    1. 读取 API Token
    2. 运行抓取测试
    3. 分析返回数据
    """
    print("="*60)
    print("🚀 TikTok Scraper 测试")
    print("="*60)
    
    # 读取 API Token
    import os
    api_token = os.environ.get("APIFY_API_TOKEN")
    
    if not api_token:
        print("\n⚠️  请先设置环境变量 APIFY_API_TOKEN")
        print("   获取方式：https://console.apify.com/account#/integrations")
        print("\n   设置命令:")
        print('   export APIFY_API_TOKEN="your_token_here"')
        return
    
    # 初始化测试
    tester = TikTokScraperTest(api_token)
    
    # 测试关键词（外贸相关）
    test_keywords = [
        "phone case",      # 手机配件
        "home decor",      # 家居装饰
        "fashion accessories"  # 时尚配饰
    ]
    
    print(f"\n📝 将测试以下关键词: {', '.join(test_keywords)}")
    print(f"   每个关键词抓取 20 条视频（测试用）\n")
    
    # 运行测试
    all_results = []
    for keyword in test_keywords:
        print(f"\n{'='*60}")
        print(f"🔍 测试关键词: {keyword}")
        print(f"{'='*60}")
        
        # 启动抓取
        run_id = tester.run_scraper(keyword, max_results=20)
        
        if run_id:
            # 等待完成
            run_data = tester.wait_for_run(run_id)
            
            if run_data:
                dataset_id = run_data["defaultDatasetId"]
                print(f"📦 Dataset ID: {dataset_id}")
                
                # 获取数据
                data = tester.get_dataset(dataset_id)
                
                if data:
                    # 分析字段
                    analysis = tester.analyze_fields(data)
                    all_results.append({
                        "keyword": keyword,
                        "analysis": analysis
                    })
    
    # 生成测试报告
    print(f"\n{'='*60}")
    print("📋 测试总结")
    print(f"{'='*60}")
    
    for result in all_results:
        keyword = result["keyword"]
        analysis = result["analysis"]
        
        if analysis:
            print(f"\n✅ {keyword}:")
            print(f"   抓取数量: {analysis['total_count']}")
            print(f"   字段数量: {len(analysis['fields'])}")
            print(f"   关键字段: {', '.join(analysis['fields'][:10])}")

if __name__ == "__main__":
    main()
