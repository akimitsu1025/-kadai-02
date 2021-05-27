import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
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
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

### ログファイルおよびコンソール出力
def log(txt):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ２　難易度★★★☆☆
    # for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_copy_list = []
    exp_jobinfo_list = []
    exp_salary_list = []
    count = 0
    succes = 0
    fail = 0
    while True:
        # 検索結果の一番上の会社名を取得(まれに１行目が広告の場合、おかしな動作をするためcassetteRecruit__headingで広告を除外している)
        name_list = driver.find_elements_by_css_selector('cassetteRecruit__heading .cassetteRecruit__name')
        copy_list = driver.find_elements_by_css_selector('cassetteRecruit__heading .cassetteRecruit__copy')
        table_list1 = driver.find_elements_by_css_selector('cassetteRecruit .tableCondition') # 仕事内容
        table_list2 = driver.find_elements_by_css_selector('cassetteRecruit .tableCondition') # 給与
        # 1ページ分繰り返し
        for name, copy, jobinfo, salary in zip(name_list, copy_list, table_list1, table_list2):
            try:
                exp_name_list.append(name.text)
                exp_copy_list.append(copy.text)
                # 仕事内容をtableから探す
                jobinfo = find_table_target_word(table.find_elemnts_by_tag_name('th'), table.find_elements_by_tag_name('td'), '仕事内容')
                exp_jobinfo_list.append(jobinfo)
                # 給与をtableから探す
                salary = find_table_target_word(table.find_elemnts_by_tag_name('th'), table.find_elements_by_tag_name('td'), '給与')
                exp_salary_list.append(salary)
                log(f'{count}件成功: {name.text}')
                succes += 1
            except Exception as e:
                log(f'{count}件失敗:{name.text}')
                log(e)
                fail += 1
            finally:
                count += 1

        ## ３　難易度★★★☆☆
        # ２ページ目以降の情報も含めて取得できるようにしてみましょう
        next_page = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div/nav[1]/ul/li[2]/a')
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute('href')
            driver.get(next_page_link)
        else:
            log('最終ページです。終了します。')
            break



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()