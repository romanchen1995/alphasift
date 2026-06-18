import json
import os
import urllib.request

run_file = os.environ.get('RUN_FILE', '')
token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')

with open(run_file) as f:
    data = json.load(f)

picks = data.get("picks", [])[:5]
strategy = data.get("strategy", "unknown")
run_id = data.get("run_id", "")
snapshot_count = data.get("snapshot_count", 0)
after_filter_count = data.get("after_filter_count", 0)

lines = [
    f"📊 *{strategy.upper()} 选股结果*",
    f"🗂 扫描: {snapshot_count} → {after_filter_count} 只",
    f"⏱ Run: `{run_id}`",
    "",
    "🏆 *Top 5 Picks:*",
    ""
]

for p in picks:
    change = p.get("change_pct", 0) or 0
    emoji = "🔴" if change < 0 else ("🟢" if change > 0 else "⚪")
    lines.append(f"{p.get('rank', '?')}. *{p.get('name', '')}* ({p.get('code', '')})")
    lines.append(f"   {emoji} {change:+.2f}% | ¥{p.get('price', 0):.2f} | Score: {p.get('final_score', 0):.1f}")
    lines.append(f"   PE: {p.get('pe_ratio', 0):.1f} | PB: {p.get('pb_ratio', 0):.2f}")
    tags = p.get("post_analysis_tags", [])
    if tags:
        lines.append(f"   🏷 {' | '.join(tags)}")
    lines.append("")

payload = json.dumps({"chat_id": chat_id, "text": "\n".join(lines), "parse_mode": "Markdown"}).encode()
req = urllib.request.Request(
    f"https://api.telegram.org/bot{token}/sendMessage",
    data=payload,
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    print(resp.read().decode())
