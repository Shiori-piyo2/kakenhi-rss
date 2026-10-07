import requests
from feedgen.feed import FeedGenerator

JSON_URL = "https://www.jsps.go.jp/include/news/inform_ja.json"

data = requests.get(JSON_URL).json()

fg = FeedGenerator()
fg.title("科研費 新着情報")
fg.link(href="https://www.jsps.go.jp/j-grantsinaid/")
fg.description("JSPS 科研費関連情報")

for item in data:

    site_url = item.get("site_url", "")

    if "/j-grantsinaid/" not in site_url:
        continue

    title = item["title"]

    link = "https://www.jsps.go.jp" + site_url

    entry = fg.add_entry()
    entry.title(title)
    entry.link(href=link)
    entry.guid(link)

fg.rss_file("docs/feed.xml")

print("feed.xml を生成しました")
