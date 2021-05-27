'''
## １　難易度★★☆☆☆
会社名を取得して画面にprint文で表示してみましょう。

## ２　難易度★★★☆☆
for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう

## ３　難易度★★★☆☆
２ページ目以降の情報も含めて取得できるようにしてみましょう

## ４　難易度★★☆☆☆
任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう

## ５　難易度★★★★☆
取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう

## ６　難易度★★☆☆☆
エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう<br>
(try文)

## ７　難易度★★☆☆☆
処理の経過が分かりやすいようにログファイルを出力してみましょう<br>
ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。
ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。
(今何件目、エラー内容、等を表示)

## ８　難易度★☆☆☆☆
Chromeドライバーがバージョンアップの際に自動で更新されるようにしてみましょう。  
参考：https://qiita.com/YoshikiIto/items/000f241f6d917178981c

### ９ 難易度★★☆☆☆
検索時等にWeb画面を更新する処理はurlにより制御されます。
そのため、検索窓を使用せずにURLを直接変更することでも検索結果を取得することが可能です。
URLのうち、検索ワードを制御している部分を見つけて、直接プログラムにて修正し
検索結果を表示させてみましょう。
参考：https://webtan.impress.co.jp/e/2012/04/26/12663
'''

# ここからコードを書いていく。
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# 変数driverを作り、URLを取得＆アクセス。
driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://tenshoku.mynavi.jp/'
driver.get(url)
time.sleep(3)
print('処理1完了')

## １　難易度★★☆☆☆
## 会社名を取得して画面にprint文で表示してみましょう。

# ポップアップを閉じる。
try:
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)
    # ポップアップを閉じる。
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)
except:
    pass
print('処理2完了')

# 検索する文字を自動入力＆検索クリック。
search_keyword = driver.find_element_by_class_name('topSearch__text')
search_keyword.send_keys('高収入')
time.sleep(3)
search_keyword_btn = driver.find_element_by_class_name('topSearch__button') #topSearch__button js__searchRecruitTop　の　「js__searchRecruitTop」があるとクリックできない。どういうこと？
search_keyword_btn.click()
print('処理3完了')

# 【練習】1社のみを取得。（会社名を取得して画面にprint文で表示してみましょう。）✔︎
company = driver.find_element_by_class_name('cassetteRecruit__name')
print(company.text)
print('処理4完了')

## ２　難易度★★★☆☆
## for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう

# 【練習】まずは1つ目の項目（name）を取得してみる。それをfor文で繰り返す。
name_list = driver.find_elements_by_class_name('cassetteRecruit__name') #複数形の時はelements！
for name in name_list:
    print(name.text)
print('処理5完了')

# 【練習】2つ目の項目（copy）を抽出してみる。それをfor文で繰り返す。
copy_list = driver.find_elements_by_class_name('cassetteRecruit__copy')
for copy in copy_list:
    print(copy.text)
print('処理6完了')















'''
# 【自主練】3つ目の項目（job_info：仕事内容）を抽出してみる。トライ１→×
job_info_list = driver.find_elements_by_css_selector('.cassetteRecruit .tableCondition') # 「仕事内容」のみを抽出したかったけど、テーブル内の要素が全部抽出された。
for job_info in job_info_list:
    print(job_info.text)
print('処理7完了')
'''

'''
# 【自主練】3つ目の項目（job_info：仕事内容）を抽出してみる。→テーブル内の「仕事内容」のみを抽出できない。トライ２：tagnameで「th」と「td」→×
job_info_list = driver.find_elements_by_tag_name('th'), find_elements_by_tag_name('td'), '仕事内容'
for job_info in job_info_list:
    print(job_info.text)
print('処理7完了')
'''

'''
# 【自主練】3つ目の項目（job_info：仕事内容）を抽出してみる。→関数「find_table_target_word」を使う。トライ３→×
def find_table_target_word(th_elms, td_elms, target:str):
    for th_elm, td_elm in zip(th_elms, td_elms):
        if th_elm.text == target:
            return td_elm.text

table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 仕事内容
for table in table_list:

job_info_list = find_table_target_word(table.find_elements_by_tag_name('th'), table.find_elements_by_tag_name('td'), '仕事内容')
for job_info in job_info_list:
print(job_info.text)
print('処理7完了')
'''

'''
# 【自主練】3つ目の項目（job_info：仕事内容）を抽出してみる。→関数「find_table_target_word」を使う②。トライ４→×
def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

job_info_list = []

table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 仕事内容

for table in table_list:
    # 仕事内容をtableから探す
    job_info = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "仕事内容")
    job_info_list.append(job_info)
    print(job_info_list)
print('処理7完了')
'''

# 【練習】のマイナビサイトの1ページ目のテーブル「仕事内容」のみを取得し、for文で繰り返し処理。
# ☝上記はできなかったので、課題にある4つを一気に取得し、繰り返し処理をしてみる。3つ：name、copy、status、仕事内容