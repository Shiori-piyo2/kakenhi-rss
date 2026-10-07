import requests

url = "https://www.jsps.go.jp/include/news/inform_ja.json"

data = requests.get(url).json()

count = 0

for item in data:
    site_url = item.get("site_url", "")

    if "/j-grantsinaid/" in site_url:
        count += 1

        print(item["news_date"])
        print(item["title"])
        print(site_url)
        print("-" * 50)

print(f"科研費記事: {count}件")
