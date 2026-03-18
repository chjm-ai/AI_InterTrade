#!/usr/bin/env python3
"""
XPOZ Instagram MCP 测试脚本

用法：
    export XPOZ_API_KEY=...
    python3 demos/xpoz-test/test_xpoz_instagram.py --keyword "phone case" --limit 10
"""

import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime


MCP_URL = "https://mcp.xpoz.ai/mcp"
PROTOCOL_VERSION = "2025-03-26"


def _json_rpc_body(method, params=None, req_id=1):
    body = {"jsonrpc": "2.0", "method": method}
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
        lines = []
        for line in text.splitlines():
            if line.startswith("data:"):
                lines.append(line[len("data:") :].strip())
        if lines:
            text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"_raw": text}


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
                **({"Mcp-Session-Id": self.session_id} if self.session_id else {}),
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.session_id = resp.headers.get("Mcp-Session-Id", self.session_id)
                parsed = _parse_response_body(resp.read())
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
            raise RuntimeError("HTTP %s %s" % (exc.code, body))

    def initialize(self):
        result = self._request(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "ai-intertrade-xpoz-instagram", "version": "0.1.0"},
            },
        )
        self._request("notifications/initialized", expect_response=False)
        return result

    def list_tools(self):
        return self._request("tools/list", {})

    def call_tool(self, name, arguments):
        return self._request("tools/call", {"name": name, "arguments": arguments})


def summarize_payload(tool_response):
    result = (tool_response or {}).get("result") or {}
    content = result.get("content") or []
    text = ""
    if content and isinstance(content[0], dict):
        text = content[0].get("text") or ""
    lines = [line for line in text.splitlines() if line.strip()]
    sample = "\n".join(lines[:60])
    return {
        "content_type": "text",
        "preview": sample,
    }


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
    insta_resp = client.call_tool(
        "getInstagramPostsByKeywords",
        {
            "query": args.keyword,
            "responseType": "fast",
            "limit": args.limit,
            "fields": [
                "id",
                "postType",
                "username",
                "fullName",
                "caption",
                "createdAtDate",
                "likeCount",
                "commentCount",
                "reshareCount",
                "videoPlayCount",
                "mediaType",
                "codeUrl",
                "imageUrl",
                "videoUrl",
                "videoDuration",
            ],
            "userPrompt": 'Search Instagram posts for "%s" and return sample results for comparison.' % args.keyword,
        },
    )

    output = {
        "keyword": args.keyword,
        "limit": args.limit,
        "initialize": init_resp,
        "tools": tools_resp,
        "final_response": insta_resp,
        "payload_summary": summarize_payload(insta_resp),
    }

    os.makedirs(args.output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(args.output_dir, "xpoz_instagram_%s.json" % ts)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("保存结果到: %s" % filename)
    print(json.dumps(output["payload_summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
