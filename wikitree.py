import requests
from bs4 import BeautifulSoup
from graphviz import Graph


class WikiTree:
    def __init__(self, q, d=3):
        self.q = q
        self.d = d  # 深さを指定
        self.pairs = []  # 親子関係のペアを格納するリスト
        self.history = []  # 処理済みタイトルのリスト

    def get_wiki(self, q, d):
        if d < 1:
            return
        url = "https://ja.wikipedia.org/wiki/" + q
        res = requests.get(url)  # GETリクエストを送信
        soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
        title = soup.select("#firstHeading")[0].text  # 記事のタイトルを取得
        rels = soup.select("#関連項目")  # 関連項目の見出しを取得
        if not rels:
            return  # 記事が存在しない || 関連項目がない ときはスキップ
        lis = rels[0].parent.find_next_sibling("ul").find_all("li")  # 関連項目に含まれるliタグを全て取得
        rels = []
        for li in lis:
            rels.append(li.find("a"))  # li要素内の最初のa要素のみ追加
        self.history.append(title)  # ヒストリに追加
        for rel in rels:
            self.pairs.append((title, rel.text))  # その記事のタイトルと関連項目のタイトルのペアをリストに追加
            if rel.text in self.history:
                continue  # 無限ループを防止
            self.get_wiki(rel.text, d - 1)  # 再帰的に処理

    def start(self):
        self.get_wiki(self.q, self.d)

    def render(self, fname="output.png"):
        g = Graph(format='png', engine="sfdp")
        g.attr("node", fontname="sans-serif")
        for p in self.pairs:
            g.edge(*p)
        g.render(outfile=fname, cleanup=True)


def main(q):
    wt = WikiTree(q)  # WikiTreeオブジェクトを作成
    wt.start()  # 処理開始
    wt.render("output.png")  # グラフを保存


if __name__ == "__main__":
    main("夏休み")
