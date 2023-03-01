
import json
from pipes import quote
from typing import Optional
import httpx

"Scraping instagram by HashTag"
def scrape_hashtag(hashtag: str, session: httpx.AsynClient, page_size=12, page_limit:Optional[int] = None):
    """scrape user's post data"""
    base_url = "https://www.instagram.com/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&variables="
    variables = {
        "tag_name": hashtag,
        "first": page_size,
        "after": None,
    }
    page = 1
    while True:
        result = session.get(base_url + quote(json.dumps(variables)))
        posts = json.loads(result.content)["data"]["hashtag"]["edge_hashtag_to_media"]
        for post in posts['edges']:
            yield post["node"]
        page_info = posts["page_info"]
        if not page_info["has_next_page"]:
            break
        variables["after"] = page_info["end_cursor"]
        page += 1
        if page > page_limit:
            break

"Scraping instagran by Location"
def find_location_id(query: str, session: httpx.Client):
    """Finds most likely location ID from given location name"""
    resp = session.get(f"https://www.instagram.com/web/search/topsearch/?query={query}")
    data = resp.json()
    try:
        first_result = sorted(data["places"], key=lambda place: place["position"])[0]
        return first_result["place"]["location"]["pk"]
    except IndexError:
        print(f'no locations matching query "{query}" were found')
        return

def scrape_users_by_location(location_id: str, session: httpx.Client, page_limit=None):
    url = f"https://www.instagram.com/explore/locations/{location_id}/?__a=1"
    page = 1
    next_id = ""
    while True:
        resp = session.get(url + (f"&max_id={next_id}" if next_id else ""))
        data = resp.json()["native_location_data"]
        print(f"scraped location {location_id} page {page}")
        for section in data["recent"]["sections"]:
            for media in section["layout_content"]["medias"]:
                yield media["media"]["user"]["username"]
        next_id = data["recent"]["next_max_id"]
        if not next_id:
            print(f"no more results after page {page}")
            break
        if page_limit and page_limit < page:
            print(f"reached page limit {page}")
            break
        page += 1