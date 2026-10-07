import requests
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

JSON_URL = "https://www.jsps.go.jp/include/news/inform_ja.json"

# JSON取得
data = requests.get(JSON_URL)
data.raise_for_status()
data = data.json()

# 科研費記事のみ抽出
kakenhi_items = [
    item
    for item in data
    if "/j-grantsinaid/" in item.get("site_url", "")
]

# 日付の新しい順に並べ替え
kakenhi_items.sort(
    key=lambda x: datetime.strptime(
        x["news_date"],
        "%Y-%m-%d %H:%M:%S"
    ),
    reverse=True
)

# RSS作成
fg = FeedGenerator()
fg.title("科研費 新着情報")
fg.link(href="https://www.jsps.go.jp/j-grantsinaid/")
fg.description("JSPS 科研費関連情報")

for item in kakenhi_items:

    title = item["title"]

    link = "https://www.jsps.go.jp" + item["site_url"]

    # 日付変換
    pub_date = datetime.strptime(
        item["news_date"],
        "%Y-%m-%d %H:%M:%S"
    ).replace(tzinfo=timezone.utc)

    entry = fg.add_entry()
    entry.title(title)
    entry.link(href=link)
    entry.guid(link)
    entry.pubDate(pub_date)

# RSS出力
fg.rss_file("docs/feed.xml")

print(f"科研費記事 {len(kakenhi_items)} 件を出力しました")
