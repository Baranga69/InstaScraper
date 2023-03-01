import json
import httpx
from typing import Optional
from urllib.parse import quote

def scrape_user_posts(user_id:str, session:httpx.Client, page_size=12):
    base_url = "https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables="
    variables = {
        "id": user_id,
        "first": page_size,
        "after": None,
    }
    while True:
        resp = session.get(base_url + quote(json.dumps(variables)))
        posts = resp.json()["data"]["user"]["edge_owner_to_timeline_media"]
        for post in posts["edges"]:
            yield post["node"]
        page_info = posts["page_info"]
        if not page_info["has_next_page"]:
            break
        variables["after"] = page_info["end_cursor"]


if __name__ == "__main__":
    with httpx.Client(
        timeout=httpx.Timeout(20.0),
    ) as session:
        user = scrape_user_posts("google", session)