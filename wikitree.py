import requests
from bs4 import BeautifulSoup


def get_wiki(q):
    url = "https://ja.wikipedia.org/wiki/" + q
    res = requests.get(url)  # GETリクエストを送信
    soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
    title = soup.select("#firstHeading")[0].text  # 記事のタイトルを取得
    rels = soup.select("#関連項目")[0].parent.find_next_sibling("ul").find_all("a")  # 関連項目に含まれるaタグを全て取得
    print("{}, {}".format(title, rels))


if __name__ == "__main__":
    get_wiki("夏休み")  # stdout: 夏休み, [<a href="/wiki/%E3%81%8A%E7%9B%86" title="お盆">お盆</a>, <a href="/wiki/%E6%98%A5%E4%BC%91%E3%81%BF" title="春休み">春休み</a>, <a href="/wiki/%E7%A7%8B%E4%BC%91%E3%81%BF" title="秋休み">秋休み</a>, <a href="/wiki/%E5%86%AC%E4%BC%91%E3%81%BF" title="冬休み">冬休み</a>]
