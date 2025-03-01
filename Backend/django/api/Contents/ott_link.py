# selenium 불러오기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 각각의 OTT 플랫폼 로그인 불러오기
from api.models import UserInterworking
from api.Netflix.Login import n_login
from api.DisneyPlus.Login import d_login
from api.Tving.Login import t_login
from api.Watcha.Login_2 import wat_login
from api.Wavve.Login import wav_login

def netflix_url(title, driver): #제목으로 netflix에 있는 해당 컨텐츠 시청 url 리턴
    try:
        url_home = "https://www.netflix.com/kr/"
        driver.get(url_home)

        URL = "https://www.netflix.com/search?q=" + title
        driver.get(URL)

        first_content = driver.find_element(By.XPATH, '//*[@id="row-0"]/div/div/div/div/div/div[1]')
        first_content.click()

        time.sleep(2)
        return driver.current_url
    except:
        driver.quit()
        return "contents"



def disney_url(title, driver): #제목으로 disney plus에 있는 해당 컨텐츠 시청 url 리턴
    #######################ERROR#######################
    try:
        btn_search = driver.find_element(By.XPATH, '//*[@id="nav-list"]/span[2]')
        btn_search.click()
        time.sleep(2)
        driver.implicitly_wait(5)

        input_bar = driver.find_element(By.XPATH, '//*[@id="search-input"]')
        input_bar.send_keys(title)
        time.sleep(2)
        driver.implicitly_wait(5)

        try:
            content = driver.find_element(By.XPATH, '//*[@id="section_index"]/div/div/div[2]/section/div/div/div/a')
        except:
            content = driver.find_element(By.XPATH, '//*[@id="section_index"]/div/div/div[2]/section/div/div/div[1]/a')
        content.click()
        time.sleep(2)
        driver.implicitly_wait(5)

        cu = driver.current_url
        return cu

    except:
        driver.quit()
        return "contents"



def wavve_url(title, driver, c_type): #제목으로 wavve에 있는 해당 컨텐츠 시청 url 리턴
    try:
        xbox = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/section/div[1]')
        xbox.click()
        ##Content = TV일 때
        if c_type == "tv":
            tv_search_url = "https://www.wavve.com/search/search?category=program&searchWord=" + title
            driver.get(tv_search_url)
            time.sleep(2)
            driver.implicitly_wait(5)

        ##Content = Movie일 때
        elif c_type == "movie":
            movie_search_url = "https://www.wavve.com/search/search?category=movie&searchWord=" + title
            driver.get(movie_search_url)
            time.sleep(2)
            driver.implicitly_wait(5)

            search_box = driver.find_element(By.XPATH, '//*[@id="search"]')
            search_box.send_keys(Keys.RETURN)


        first_content = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div[1]')
        first_content.click()
        time.sleep(2)
        driver.implicitly_wait(5)

        return driver.current_url

    except:
        driver.quit()
        return "contents"



def watcha_url(title, driver, c_type): #제목으로 watcha에 있는 해당 컨텐츠 시청 url 리턴
    try:
        ##Content = TV일 때
        if c_type == "tv":
            tv_search_url = "https://watcha.com/search?query=" + title + "&domain=tv"
            driver.get(tv_search_url)
            time.sleep(3)
            driver.implicitly_wait(5)

            tv_content = driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div[1]/main/div[2]/section/div[1]/div/ul/li[1]')
            tv_content.click()
            time.sleep(3)
            driver.implicitly_wait(5)

        ##Content = Movie일 때
        elif c_type == "movie":
            movie_search_url = "https://watcha.com/search?query=" + title + "&domain=movie"
            driver.get(movie_search_url)
            time.sleep(3)
            driver.implicitly_wait(5)

            movie_content = driver.find_element(By.XPATH,
                                                '//*[@id="root"]/div[1]/main/div[2]/section/div[1]/div/ul/li[1]')
            movie_content.click()
            time.sleep(3)
            driver.implicitly_wait(5)

        return driver.current_url

    except:
        driver.quit()
        return "contents"



def tving_url(title, driver, c_type): #제목으로 tving에 있는 해당 컨텐츠 시청
                                      # url 리턴 제목서칭이 이상함!!!!!!!!
    try:
        if c_type == "tv":
            search_url = "https://www.tving.com/search/tv?keyword=" + title
            driver.get(search_url)
            time.sleep(2)
            driver.implicitly_wait(5)

        elif c_type == "movie":
            search_url = "https://www.tving.com/search/movie?keyword=" + title
            driver.get(search_url)
            time.sleep(2)
            driver.implicitly_wait(5)

        first_content = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/section/div/div/section/section/div[2]/div[1]')
        first_content.click()
        time.sleep(2)
        driver.implicitly_wait(5)

        return driver.current_url

    except:
        driver.quit()
        return "contents"



def ott_link(email, title, c_type, platform):

    # chrome창(웹드라이버) 열기  (Docker 경로 : "/webserver/chromedriver")
    path = "/webserver/chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('disable-gpu')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(path, chrome_options=options)

    user_interworking = dict()

    interworking = UserInterworking.objects.values().filter(u_email=email)

    for i in interworking:
        if i['platform'] == platform:
            user_interworking = i
            break

    if len(user_interworking) == 0:
        return "interworking"

    if platform == "netflix":
        n_login(user_interworking['id'], user_interworking['passwd'], user_interworking['profile_name'], driver)
        link = netflix_url(title, driver)
        driver.quit()
        return link

    elif platform == "disney":
        d_login(user_interworking['id'], user_interworking['passwd'], user_interworking['profile_name'], driver)
        link = disney_url(title, driver)
        driver.quit()
        return link

    elif platform == "wavve":
        wav_login(user_interworking['id'], user_interworking['passwd'], user_interworking['profile_name'], driver)
        link = wavve_url(title, driver, c_type)
        driver.quit()
        return link

    elif platform == "watcha":
        wat_login(user_interworking['id'], user_interworking['passwd'], user_interworking['profile_name'], driver)
        link = watcha_url(title, driver, c_type)
        driver.quit()
        return link

    elif platform == "tving":
        t_login(user_interworking['id'], user_interworking['passwd'], user_interworking['profile_name'], driver)
        link = tving_url(title, driver, c_type)
        driver.quit()
        return link