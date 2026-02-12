import streamlit as st
import json
import base64
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Standby List", page_icon="📋", layout="centered")

# ── GitHub helpers ────────────────────────────────────────────────────────────
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO  = st.secrets["GITHUB_REPO"]
FILE_PATH    = st.secrets.get("FILE_PATH", "data.json")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

@st.cache_data(ttl=60)   # refresh every 60 seconds
def get_problems():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 404:
        return []
    r.raise_for_status()
    content = base64.b64decode(r.json()["content"]).decode("utf-8")
    return json.loads(content)

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("📋 Standby List")

problems = get_problems()

# ── Filters ───────────────────────────────────────────────────────────────────
STATUS_ORDER = {"To Do": 0, "Learn": 1, "Done": 2}
STATUS_EMOJI = {"To Do": "🔴", "Learn": "🟡", "Done": "🟢"}
STATUS_COLOR = {
    "To Do": "#FF4B4B",
    "Learn": "#FFA500",
    "Done":  "#21C354",
}

col1, col2 = st.columns([2, 1])
with col1:
    search = st.text_input("🔍 Search", placeholder="Filter by title…")
with col2:
    filter_status = st.multiselect(
        "Status filter",
        options=["To Do", "Learn", "Done"],
        default=["To Do", "Learn", "Done"],
    )

# Apply filters
filtered = [
    p for p in problems
    if p["status"] in filter_status
    and search.lower() in p["title"].lower()
]

# Sort: To Do → Learn → Done
filtered = sorted(filtered, key=lambda x: STATUS_ORDER.get(x["status"], 9))

# ── Stats row ─────────────────────────────────────────────────────────────────
todo_count  = sum(1 for p in problems if p["status"] == "To Do")
learn_count = sum(1 for p in problems if p["status"] == "Learn")
done_count  = sum(1 for p in problems if p["status"] == "Done")

c1, c2, c3 = st.columns(3)
c1.metric("🔴 To Do",  todo_count)
c2.metric("🟡 Learn",  learn_count)
c3.metric("🟢 Done",   done_count)

st.divider()

# ── Problem list ──────────────────────────────────────────────────────────────
if not filtered:
    st.info("No problems found. Try adjusting your filters.")
else:
    current_status = None
    for prob in filtered:
        # Section header when status changes
        if prob["status"] != current_status:
            current_status = prob["status"]
            emoji = STATUS_EMOJI[current_status]
            st.markdown(f"### {emoji} {current_status}")

        # Problem card
        has_link = bool(prob.get("link", "").strip())
        title_display = (
            f"[{prob['title']}]({prob['link']})" if has_link else prob["title"]
        )

        badge_color = STATUS_COLOR.get(prob["status"], "#888")
        added = prob.get("added", "")
        added_str = f"<span style='color:#888;font-size:0.8em;'>Added: {added}</span>" if added else ""

        st.markdown(
            f"""
            <div style="
                border-left: 4px solid {badge_color};
                padding: 10px 16px;
                margin-bottom: 8px;
                background: #1e1e1e;
                border-radius: 4px;
            ">
                <span style="font-size:1.05em;font-weight:600;">{title_display if not has_link else prob['title']}</span>
                {"&nbsp;&nbsp;<a href='" + prob['link'] + "' target='_blank' style='font-size:0.85em;'>🔗 Open</a>" if has_link else ""}
                <br/>{added_str}
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Refresh ───────────────────────────────────────────────────────────────────
st.divider()
if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()
