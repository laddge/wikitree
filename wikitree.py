import requests
from bs4 import BeautifulSoup


class WikiTree:
    def __init__(self, q):
        self.q = q
        self.pairs = []  # 親子関係のペアを格納するリスト
        self.history = []  # 処理済みタイトルのリスト

    def get_wiki(self, q):
        url = "https://ja.wikipedia.org/wiki/" + q
        res = requests.get(url)  # GETリクエストを送信
        soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
        title = soup.select("#firstHeading")[0].text  # 記事のタイトルを取得
        rels = soup.select("#関連項目")  # 関連項目の見出しを取得
        if not rels:
            return None  # 記事が存在しない || 関連項目がない ときはNoneを返す
        rels = rels[0].parent.find_next_sibling("ul").find_all("a")  # 関連項目に含まれるaタグを全て取得
        self.history.append(title)  # ヒストリに追加
        for rel in rels:
            self.pairs.append((title, rel.text))  # その記事のタイトルと関連項目のタイトルのペアをリストに追加
            if rel.text in self.history:
                continue  # 無限ループを防止
            self.get_wiki(rel.text)  # 再帰的に処理

    def start(self):
        self.get_wiki(self.q)


def main(q):
    wt = WikiTree(q)  # WikiTreeオブジェクトを作成
    wt.start()  # 処理開始
    print(wt.pairs)


if __name__ == "__main__":
    main("夏休み")
