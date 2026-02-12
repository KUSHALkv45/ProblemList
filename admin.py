

import streamlit as st
import json
import base64
import requests
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Admin – Standby List", page_icon="🔧", layout="centered")

# ── GitHub helpers ────────────────────────────────────────────────────────────
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO  = st.secrets["GITHUB_REPO"]
FILE_PATH    = st.secrets.get("FILE_PATH", "data.json")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_file():
    """Fetch data.json from GitHub. Returns (data_list, sha)."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 404:
        return [], None
    r.raise_for_status()
    info = r.json()
    content = base64.b64decode(info["content"]).decode("utf-8")
    return json.loads(content), info["sha"]

def save_file(data: list, sha):
    """Push updated data.json to GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    encoded = base64.b64encode(json.dumps(data, indent=2).encode()).decode()
    payload = {
        "message": f"Update standby list – {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        "content": encoded,
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=HEADERS, json=payload)
    r.raise_for_status()

# ── Password gate ─────────────────────────────────────────────────────────────
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Admin Login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password. Try again.")
    st.stop()

# ── Admin UI ──────────────────────────────────────────────────────────────────
st.title("🔧 Admin – Standby List")
st.caption("Add, edit, or delete problems in your standby list.")

# Load current data
with st.spinner("Loading data from GitHub…"):
    problems, sha = get_file()

# ── Add new problem ───────────────────────────────────────────────────────────
st.subheader("➕ Add a new problem")

with st.form("add_form", clear_on_submit=True):
    title  = st.text_input("Problem title *", placeholder="e.g. Two Sum")
    link   = st.text_input("Link (optional)", placeholder="https://leetcode.com/problems/two-sum/")
    status = st.selectbox("Status", ["To Do", "Learn", "Done"])
    submit = st.form_submit_button("Add Problem")

if submit:
    if not title.strip():
        st.error("Title is required.")
    else:
        new_entry = {
            "id":     datetime.utcnow().strftime("%Y%m%d%H%M%S%f"),
            "title":  title.strip(),
            "link":   link.strip(),
            "status": status,
            "added":  datetime.utcnow().strftime("%Y-%m-%d"),
        }
        problems.append(new_entry)
        with st.spinner("Saving to GitHub…"):
            save_file(problems, sha)
            problems, sha = get_file()
        st.success(f"✅ '{title.strip()}' added as **{status}**!")

# ── Existing problems ─────────────────────────────────────────────────────────
st.divider()
st.subheader(f"📋 All problems ({len(problems)})")

STATUS_ORDER = {"To Do": 0, "Learn": 1, "Done": 2}
sorted_problems = sorted(problems, key=lambda x: STATUS_ORDER.get(x["status"], 9))

STATUS_EMOJI = {"To Do": "🔴", "Learn": "🟡", "Done": "🟢"}

if not sorted_problems:
    st.info("No problems yet. Add one above!")
else:
    for prob in sorted_problems:
        emoji = STATUS_EMOJI.get(prob["status"], "⚪")
        with st.expander(f"{emoji} {prob['title']}  —  {prob['status']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_title  = st.text_input("Title",  value=prob["title"],  key=f"title_{prob['id']}")
                new_link   = st.text_input("Link",   value=prob["link"],   key=f"link_{prob['id']}")
                new_status = st.selectbox("Status", ["To Do", "Learn", "Done"],
                                          index=["To Do", "Learn", "Done"].index(prob["status"]),
                                          key=f"status_{prob['id']}")
            with col2:
                st.write("")
                st.write("")
                if st.button("💾 Save", key=f"save_{prob['id']}"):
                    orig_index = next(j for j, p in enumerate(problems) if p["id"] == prob["id"])
                    problems[orig_index].update({
                        "title":  new_title.strip(),
                        "link":   new_link.strip(),
                        "status": new_status,
                    })
                    with st.spinner("Saving…"):
                        save_file(problems, sha)
                        problems, sha = get_file()
                    st.success("Saved!")
                    st.rerun()

                if st.button("🗑️ Delete", key=f"del_{prob['id']}"):
                    problems = [p for p in problems if p["id"] != prob["id"]]
                    with st.spinner("Deleting…"):
                        save_file(problems, sha)
                        problems, sha = get_file()
                    st.success("Deleted!")
                    st.rerun()

# ── Logout ────────────────────────────────────────────────────────────────────
st.divider()
if st.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()
