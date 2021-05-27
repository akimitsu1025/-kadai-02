## ライブラリのインポート
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

# ファイルの準備
LOG_FILE_PATH = "./log/log_{datetime}.log"
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()
    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')
    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito') # シークレットモード
    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

# ログファイルおよびコンソール出力
def log(txt):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log', now, txt)
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

# テーブル要素の繰り返し
def find_table_target_word(th_elms, td_elms, target: str):
    for th_elm, td_elm in zip(th_elms, td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理
def main():
    search_keyword = "高収入"
    log('検索キーワード:{}'.format(search_keyword))
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get('https://tenshoku.mynavi.jp/list/kw%E9%AB%98%E5%8F%8E%E5%85%A5/?jobsearchType=14&searchType=18')
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # ⑨変更
    #driver.get('https://tenshoku.mynavi.jp/list/kw%E9%AB%98%E5%8F%8E%E5%85%A5/?jobsearchType=14&searchType=18')
    #time.sleep(5)
    
    # 検索窓に入力
    # driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    # driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    # exp_name_list = []
    ### ①検索結果の一番上の会社名を取得
    # name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

    # 1ページ分繰り返し
    # print(len(name_list))
    # for name in name_list:
    #    exp_name_list.append(name.text)
    #    print(name.text)

    ### ②for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_salary_list = []
    count = 0
    success = 0
    fail = 0

    while True:
        name_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .cassetteRecruit__name')
        copy_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .cassetteRecruit__copy')
        status_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .labelEmploymentStatus')
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 給与
        print(len(name_list), len(copy_list), len(status_list), len(table_list))
        for name, copy, status, table in zip(name_list, copy_list, status_list, table_list):
            try:
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                # 給与をtableから探す
                salary = find_table_target_word(table.find_elements_by_tag_name('th'), table.find_elements_by_tag_name('td'), '給与')
                exp_salary_list.append(salary)
                log(f'{count}件目成功 : {name.text}')
                success += 1
            except Exception as e:
                log(f'{count}件目失敗 ： {name.text}')
                log(e)
                fail += 1
            finally:
                count += 1

        ### ③２ページ目以降の情報も含めて取得できるようにしてみましょう
        # 次のページボタンがあればクリックなければ終了
        next_page = driver.find_elements_by_class_name('iconFont--arrowLeft')
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute('href')
            driver.get(next_page_link)
        else:
            print('最終ページです。終了します。')
            break

### ④任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう　→50行目周辺を編集。

### ⑤取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう
     # CSV出力
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame({'企業名': exp_name_list, 'キャッチコピー': exp_copy_list, 'ステータス': exp_status_list, '給与': exp_salary_list})
    df.to_csv(EXP_CSV_PATH.format(search_keyword=search_keyword, datetime=now), encoding='utf-8-sig')
    log(f'処理完了 成功件数:{success}件 / 失敗件数:{fail}件')


### ⑥エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)　→102行目周辺を編集。（try〜except文）

### ⑦処理の経過が分かりやすいようにログファイルを出力してみましょう　→37行目周辺
### ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。
### ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。
### (今何件目、エラー内容、等を表示)

### ⑧Chromeドライバーがバージョンアップの際に自動で更新されるようにしてみましょう。  →9行目
### 参考：https://qiita.com/YoshikiIto/items/000f241f6d917178981c

### ⑨検索時等にWeb画面を更新する処理はurlにより制御されます。　→58行目周辺
### そのため、検索窓を使用せずにURLを直接変更することでも検索結果を取得することが可能です。
### URLのうち、検索ワードを制御している部分を見つけて、直接プログラムにて修正し
### 検索結果を表示させてみましょう。
### 参考：https://webtan.impress.co.jp/e/2012/04/26/12663

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()