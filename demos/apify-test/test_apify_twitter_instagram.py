#!/usr/bin/env python3
"""
Apify Twitter / Instagram 测试脚本

用法：
    source ~/.zshrc
    python3 demos/apify-test/test_apify_twitter_instagram.py --platform twitter --keyword "phone case" --limit 10
    python3 demos/apify-test/test_apify_twitter_instagram.py --platform instagram --keyword "phone case" --limit 10
"""

import argparse
import json
import os
import time
from datetime import datetime

import requests


APIFY_API_BASE = "https://api.apify.com/v2"


class ApifyActorRunner:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def start_run(self, actor_slug: str, run_input: dict):
        url = f"{APIFY_API_BASE}/acts/{actor_slug.replace('/', '~')}/runs"
        response = requests.post(url, headers=self.headers, json=run_input, timeout=60)
        response.raise_for_status()
        return response.json()["data"]

    def wait_for_run(self, actor_slug: str, run_id: str, timeout: int = 600):
        url = f"{APIFY_API_BASE}/acts/{actor_slug.replace('/', '~')}/runs/{run_id}"
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(url, headers=self.headers, timeout=60)
            response.raise_for_status()
            data = response.json()["data"]
            status = data["status"]
            if status == "SUCCEEDED":
                return data
            if status in {"FAILED", "ABORTED", "TIMED-OUT"}:
                raise RuntimeError("Run failed: %s" % status)
            print("⏳ 状态: %s" % status)
            time.sleep(5)
        raise TimeoutError("Run timeout")

    def get_dataset_items(self, dataset_id: str):
        url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
        response = requests.get(url, headers=self.headers, timeout=60)
        response.raise_for_status()
        return response.json()


def build_input(platform: str, keyword: str, limit: int):
    if platform == "twitter":
        return (
            "apidojo/tweet-scraper",
            {
                "searchTerms": [keyword],
                "sort": "Top",
                "maxItems": limit,
            },
        )

    if platform == "instagram":
        return (
            "apify/instagram-scraper",
            {
                "search": keyword,
                "searchType": "hashtag",
                "searchLimit": 1,
                "resultsType": "posts",
                "resultsLimit": limit,
            },
        )

    raise ValueError("unsupported platform: %s" % platform)


def summarize_items(items):
    if not items:
        return {"count": 0, "sample_keys": [], "sample": None}
    sample = items[0]
    return {
        "count": len(items),
        "sample_keys": sorted(list(sample.keys())),
        "sample": sample,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=["twitter", "instagram"], required=True)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", default="demos/apify-test/results")
    args = parser.parse_args()

    api_token = os.environ.get("APIFY_API_TOKEN")
    if not api_token:
        raise SystemExit("缺少 APIFY_API_TOKEN")

    actor_slug, run_input = build_input(args.platform, args.keyword, args.limit)
    runner = ApifyActorRunner(api_token)

    print("🚀 启动 Actor: %s" % actor_slug)
    run_info = runner.start_run(actor_slug, run_input)
    run_id = run_info["id"]
    print("✅ Run ID: %s" % run_id)

    final_run = runner.wait_for_run(actor_slug, run_id)
    dataset_id = final_run["defaultDatasetId"]
    items = runner.get_dataset_items(dataset_id)
    summary = summarize_items(items)

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        args.output_dir, "apify_%s_%s.json" % (args.platform, ts)
    )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            {
                "platform": args.platform,
                "keyword": args.keyword,
                "limit": args.limit,
                "actor": actor_slug,
                "run_input": run_input,
                "run": final_run,
                "summary": summary,
                "items": items,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("💾 保存结果到: %s" % filename)
    print(json.dumps(summary, ensure_ascii=False, indent=2)[:5000])


if __name__ == "__main__":
    main()
