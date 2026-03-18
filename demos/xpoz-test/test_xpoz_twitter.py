#!/usr/bin/env python3
"""
XPOZ Twitter/X MCP 测试脚本

用途：
1. 验证 XPOZ MCP 是否可正常调用
2. 拉取 Twitter/X 关键词结果
3. 输出原始响应与简要字段摘要

用法：
    export XPOZ_API_KEY=...
    python3 demos/xpoz-test/test_xpoz_twitter.py --keyword "phone case" --limit 10
"""

import argparse
import getpass
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime


MCP_URL = "https://mcp.xpoz.ai/mcp"
PROTOCOL_VERSION = "2025-03-26"


def _json_rpc_body(method, params=None, req_id=1):
    body = {
        "jsonrpc": "2.0",
        "method": method,
    }
    if req_id is not None:
        body["id"] = req_id
    if params is not None:
        body["params"] = params
    return json.dumps(body).encode("utf-8")


def _parse_response_body(raw_bytes):
    if not raw_bytes:
        return None

    text = raw_bytes.decode("utf-8", errors="replace").strip()
    if not text:
        return None

    if "data:" in text:
        payload_lines = []
        for line in text.splitlines():
            if line.startswith("data:"):
                payload_lines.append(line[len("data:") :].strip())
        if payload_lines:
            text = "\n".join(payload_lines).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "_raw": text,
        }


class XpozMcpClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session_id = None
        self.request_id = 1

    def _request(self, method, params=None, expect_response=True):
        req_id = self.request_id if expect_response else None
        if expect_response:
            self.request_id += 1

        req = urllib.request.Request(
            MCP_URL,
            data=_json_rpc_body(method, params=params, req_id=req_id),
            method="POST",
            headers={
                "Authorization": "Bearer %s" % self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Protocol-Version": PROTOCOL_VERSION,
                **(
                    {"Mcp-Session-Id": self.session_id}
                    if self.session_id
                    else {}
                ),
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.session_id = resp.headers.get("Mcp-Session-Id", self.session_id)
                body = resp.read()
                if not expect_response:
                    return None
                parsed = _parse_response_body(body)
                if isinstance(parsed, dict):
                    parsed.setdefault(
                        "_meta",
                        {
                            "status": resp.status,
                            "content_type": resp.headers.get("Content-Type"),
                        },
                    )
                return parsed
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                "HTTP %s when calling %s: %s" % (exc.code, method, body)
            )

    def initialize(self):
        result = self._request(
            "initialize",
            params={
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {
                    "name": "ai-intertrade-xpoz-test",
                    "version": "0.1.0",
                },
            },
        )
        self._request("notifications/initialized", expect_response=False)
        return result

    def list_tools(self):
        return self._request("tools/list", params={})

    def call_tool(self, name, arguments):
        return self._request(
            "tools/call",
            params={
                "name": name,
                "arguments": arguments,
            },
        )


def extract_operation_id(tool_response):
    if not tool_response:
        return None

    result = tool_response.get("result") or {}
    structured = result.get("structuredContent") or {}
    if isinstance(structured, dict):
        for key in ("operationId", "operation_id"):
            if structured.get(key):
                return structured[key]

    for item in result.get("content") or []:
        text = item.get("text") if isinstance(item, dict) else None
        if not text:
            continue
        try:
            parsed = json.loads(text)
        except Exception:
            continue
        if isinstance(parsed, dict):
            for key in ("operationId", "operation_id"):
                if parsed.get(key):
                    return parsed[key]

    return None


def extract_payload(tool_response):
    if not tool_response:
        return None

    result = tool_response.get("result") or {}
    structured = result.get("structuredContent")
    if structured:
        return structured

    for item in result.get("content") or []:
        text = item.get("text") if isinstance(item, dict) else None
        if not text:
            continue
        try:
            return json.loads(text)
        except Exception:
            return text
    return None


def poll_operation(client, operation_id, poll_interval=2, max_wait=120):
    start = time.time()
    last_response = None

    while time.time() - start < max_wait:
        last_response = client.call_tool(
            "checkOperationStatus",
            {"operationId": operation_id},
        )
        payload = extract_payload(last_response)
        if isinstance(payload, dict):
            status = (payload.get("status") or "").lower()
            if status in {"completed", "succeeded", "success", "done"}:
                return last_response
            if status in {"failed", "error", "cancelled", "canceled"}:
                raise RuntimeError("operation failed: %s" % json.dumps(payload))
        time.sleep(poll_interval)

    raise TimeoutError("operation timeout: %s" % operation_id)


def summarize_posts(payload):
    if not isinstance(payload, dict):
        return {
            "payload_type": type(payload).__name__,
        }

    posts = None
    for key in ("results", "items", "data", "posts", "tweets"):
        value = payload.get(key)
        if isinstance(value, list):
            posts = value
            break

    if posts is None and isinstance(payload.get("data"), dict):
        nested = payload["data"]
        for key in ("results", "items", "posts", "tweets"):
            value = nested.get(key)
            if isinstance(value, list):
                posts = value
                break

    summary = {
        "top_level_keys": sorted(list(payload.keys())),
        "count": len(posts) if isinstance(posts, list) else None,
        "sample_keys": sorted(list(posts[0].keys())) if posts else [],
        "sample": posts[:3] if posts else [],
    }
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output-dir", default="demos/xpoz-test/results")
    args = parser.parse_args()

    api_key = os.environ.get("XPOZ_API_KEY")
    if not api_key:
        api_key = getpass.getpass("XPOZ_API_KEY: ").strip()
    if not api_key:
        print("缺少 XPOZ_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = XpozMcpClient(api_key)

    init_resp = client.initialize()
    tools_resp = client.list_tools()

    tool_resp = client.call_tool(
        "getTwitterPostsByKeywords",
        {
            "query": args.keyword,
            "responseType": "fast",
            "limit": args.limit,
            "fields": [
                "id",
                "text",
                "authorId",
                "authorUsername",
                "createdAt",
                "retweetCount",
                "replyCount",
                "likeCount",
                "quoteCount",
                "impressionCount",
                "bookmarkCount",
                "lang",
                "hashtags",
                "mentions",
                "mediaUrls",
                "source",
            ],
            "userPrompt": 'Search Twitter posts for "%s" and return sample results for comparison.' % args.keyword,
        },
    )

    op_id = extract_operation_id(tool_resp)
    final_resp = poll_operation(client, op_id) if op_id else tool_resp
    payload = extract_payload(final_resp)
    summary = summarize_posts(payload)

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "keyword": args.keyword,
        "limit": args.limit,
        "initialize": init_resp,
        "tools": tools_resp,
        "initial_call": tool_resp,
        "final_response": final_resp,
        "payload_summary": summary,
    }
    filename = os.path.join(args.output_dir, "xpoz_twitter_%s.json" % ts)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("保存结果到: %s" % filename)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
