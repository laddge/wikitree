import requests
from bs4 import BeautifulSoup


def get_wiki(q):
    url = "https://ja.wikipedia.org/wiki/" + q
    res = requests.get(url)  # GETリクエストを送信
    soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
    title = soup.select("#firstHeading")[0].text  # 記事のタイトルを取得
    rels = soup.select("#関連項目")  # 関連項目の見出しを取得
    if not rels:
        return None  # 記事が存在しない || 関連項目がない ときはNoneを返す
    rels =  rels[0].parent.find_next_sibling("ul").find_all("a")  # 関連項目に含まれるaタグを全て取得
    pairs = []
    for rel in rels:
        pairs.append((title, rel.text))  # その記事のタイトルと関連項目のタイトルのペアをリストに追加
        rel_pairs = get_wiki(rel.text)  # 再帰的に処理
        if rel_pairs:
            pairs.extend(rel_pairs)  # 結果を結合
    return pairs


def main(q):
    pairs = get_wiki(q)  # タイトルのペアのリストを取得
    print(pairs)


if __name__ == "__main__":
    main("夏休み")
