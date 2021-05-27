import os
from selenium.webdriver import Chrome, ChromeOptions # 「selenium」の「webdriver」モジュールの、「Chrome」クラスと「ChromeOptions」クラスをインポートしているってこと？
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver # 「selenium」の「webdriver」の「chrome」の「webdriver」モジュールの、「WebDriber」クラスをインポートしているってこと？「from webdriver import WebDriver」ではダメ？「webdriver」が2回？「webdriver」と「WebDriver」の違いは？
from selenium.webdriver.remote.webelement import WebElement # 「selenium」の「webdriver」の「remote」の「webelement」モジュールの、「WebElement」クラスをインポートしているってこと？
from webdriver_manager.chrome import ChromeDriverManager #「webdriver_manager」の「chrome」モジュールの、「ChromeDriverManager」クラスをインポートしているってこと？
LOG_FILE_PATH = './log/log_{datetime}.log' # PATHを指定してログファイルを作成し、定数LOG_FILE_PATHに代入？
EXP_CSV_PATH = './exp_list_{search_keyword}_{datetime}.csv' # PATHを指定してCSVファイルを作成し、定数EXP_CSV_PATHに代入？111行目で処理されている。
log_file_path = LOG_FILE_PATH.format(datetime = datetime.datetime.now().strftime('%Y-&m-%d-%H-%M-%S')) # 時刻表示のための処理？
### Chromeを起動する関数
def set_driver(driver_path, headless_flg): # 関数set_driverは47行目で呼び出されている。別の関数:main()の中で使われている？
    # Chromeドライバーの読み込み
    options = ChromeOptions()
    # ヘッドレスモード（画面非表示モード）の設定
    if headless_flg ==  True: #　13行目の関数set_driverの第２引数headless_flgと結びつく？　（True→画面が表示されない。False→画面が表示される。)

        options.add_argument('--headless')
    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36') # 設定しないとbotのように見られるかも。
    # options.add_argument('log-level=3')   # 'log-level=3'とは？
    options.add_argument('--ignore-Certificate - errors')
    options.add_argument('--ignoreIgnore ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与：記録を残さない。キャッシュなし。
    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options = options) # Chromeを動かす処理？これも定型文のように覚えた方がいいか？
### ログファイルおよびコンソール出力
def log(txt): # log（履歴）ファイルを出力するための関数？引数txtの意味は？
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log', now, txt) # 引数の意味は？
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f: # 11行目で定義した変数log_file_pathのファイルを開く？
        f.write(logStr + '\n')
    print(logStr)
def find_table_target_word(th_elms, td_elms, target:str): #この関数の役割はテーブル箇所の判別？引数の意味は？引数のtarget:strとは？一連の処理もわからない。
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm, td_elm in zip(th_elms, td_elms):
        if th_elm.text == target: # targetとは何か？
            return td_elm.text
### main処理
def main():
    log('処理開始') # 29行目で定義した関数log。。引数の'処理開始'は何を意味する？
    search_keyword = input('検索キーワードを入力してください：')
    log('検索キーワード：{}'.format(search_keyword)) # 29行目で定義した関数log。。引数の文字列は何を意味する？
    # driverを起動
    driver = set_driver('chromedriver.exe', False) #　第２引数'False'は何を意味する？←headless_flgがFalseという意味：画面表示。
    # webサイトを開く
    driver.get('https://tenshoku.mynavi.jp/')
    time.sleep(5)
    try:
        # ポップアップを閉じる（seleniumだけではクローズできない）
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    # 検索窓に入力
    driver.find_element_by_class_name('topSearch__text').send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name('topSearch__button').click() # class_nameは「topSearch__button js__searchRecruitTop」なのでは？「 js__searchRecruitTop」はなぜ付けないのか？
    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_copy_list = []
    exp_status_list = []
    exp_first_year_fee_list = []
    count = 0
    success = 0
    fail = 0
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        name_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .cassetteRecruit__name')   # 「cassetteRecruit__name」だけではだめなのか？「.」の探し方。（「.」はクラスを表す。「 .」はその要素の配下、という意味。）　←広告以外を取得するためにheadingの部分も必要。
        copy_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .cassetteRecruit__copy')   # 「cassetteRecruit__copy」だけではだめなのか？
        status_list = driver.find_elements_by_css_selector('.cassetteRecruit__heading .labelEmploymentStatus') # 「labelEmploymentStatus」だけではだめなのか？
        table_list = driver.find_elements_by_css_selector('.cassetteRecruit .tableCondition') #初年度年収　      #　「.cassetteRecruit__main .tableCondition__body」ではないのか？「__main」と「__body」は付けないのか？　←テーブル全体を指定している。＋後ほど、前述のメソッドで初年度年収を取得。
        # 1ページ分繰り返し
        for name, copy, status, table in zip(name_list, copy_list, status_list, table_list):
            try:
                # try〜exceptはエラーの可能性が高い箇所に配置
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                exp_status_list.append(status.text)
                # 初年度年収をtableから探す
                first_year_fee = find_table_target_word(table.find_elements_by_tag_name('th'), table.find_elements_by_tag_name('td'), '初年度年収') #　この処理がわからない。解説をお願いしたい。36行目で定義した関数find_table_target_wordが出てきて、引数に３つの対応する値を入れる？
                exp_first_year_fee_list.append(first_year_fee)
                log(f'{count}件目成功：{name.text}') # 29行目で定義した関数logがまた出てきた。。log()の引数はlogファイルに書き込まれている。tryはエラーが起きても大丈夫。という意味。エラーはexceptの方に流す。
                success += 1
            except Exception as e: # 例外処理。どういうこと？print()文と似たようなイメージ。ファイルにも書き込んでいるだけ。
                log(f'{count}件目失敗：{name.text}')
                log(e) # どういうこと？
                fail += 1
            finally:
                # finallyは成功でもエラーでも必ず実行
                count += 1
        # 次のページボタンがあればクリックなければ終了
        next_page = driver.find_elements_by_class_name('iconFont--arrowLeft') # ここには「.」がつかないのか？
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute('href') # どういうこと？
            driver.get(next_page_link)
        else:
            log('最終ページです。終了します。')
            break
    # CSV出力
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    df = pd.DataFrame({'企業名': exp_name_list,
                    'キャッチコピー': exp_copy_list,
                    'ステータス': exp_status_list,
                    '初年度年収': exp_first_year_fee_list})
    df.to_csv(EXP_CSV_PATH.format(search_keyword = search_keyword,datetime = now), encoding='utf-8-sig')
    log(f'処理完了 成功件数： {success}件 / 失敗件数： {fail}件')
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()


'''
Q1 課題２では、ターミナルでインストールするのは以下でよいか？
pip3 install selenium
pip3 install webdriver_manager
pip3 install pandas

Q2 【cassetteRecruit__name】だけでなく、
それを包んでいる【cassetteRecruit__heading】も入力する必要があるということでしょうか？（73.74.75行目）
（Slack質問中）

Q3 css_selectorの抽出方法確認。

Q4 この処理はたくさん実行してもパソコンに負担はかからないか？
ファイルの読み込み件数が多い場合など。

Q5 最短の学方法は？
わからないことが多すぎる。
調べてもわからないことが多い。。
米谷さんはプログラミングやり始めの頃、どのように学習していたか？

Q6 自分のレベルは低すぎでは？
出直した方がいいか？出直しは可能か？
質問は遠慮せずにたくさんして大丈夫？（みなさん少ない気が。。）
'''