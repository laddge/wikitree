import requests
from bs4 import BeautifulSoup


def get_wiki(q):
    url = "https://ja.wikipedia.org/wiki/" + q
    res = requests.get(url)  # GETリクエストを送信
    soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
    title = soup.select("#firstHeading")[0].text  # 記事のタイトルを取得
    rels = soup.select("#関連項目")[0].parent.find_next_sibling("ul").find_all("a")  # 関連項目に含まれるaタグを全て取得
    pairs = []
    for rel in rels:
        pairs.append((title, rel.text))  # その記事のタイトルと関連項目のタイトルのペアをリストに追加
    print(pairs)


if __name__ == "__main__":
    get_wiki("夏休み")  # stdout: [('夏休み', 'お盆'), ('夏休み', '春休み'), ('夏休み', '秋休み'), ('夏休み', '冬休み')]
