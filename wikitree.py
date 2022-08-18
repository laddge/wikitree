import requests
from bs4 import BeautifulSoup


def get_wiki(q):
    url = "https://ja.wikipedia.org/wiki/" + q
    res = requests.get(url)  # GETリクエストを送信
    soup = BeautifulSoup(res.text, "html.parser")  # htmlを解析
    print(soup.select("#firstHeading")[0].text)  # 記事のタイトルを取得


if __name__ == "__main__":
    get_wiki("夏休み")  # stdout: 夏休み
