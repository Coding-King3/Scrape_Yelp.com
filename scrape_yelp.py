from time import sleep
import logging
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import pickle
import os
import sys
from datetime import datetime
from datetime import timedelta
import subprocess
import time
import platform
from random import randint
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.common.keys import Keys


def find_cookie_name():
    # Finding Cookies to check whether to generate a new one or run script with old one.

    try:
        all_files = os.listdir(os.getcwd())
        search_string = 'cookies_'
        append_file_name = []

        for file in all_files:
            if search_string in file:
                append_file_name.append(file)
                break
        string_val = append_file_name[0]
    except Exception as no_cookie_found:
        string_val = None

    return string_val


def time_difference_checker():
    # This function checks time difference between current time and cookied downloaded time.
    # If the downloaded cookie time is greater than 1 hour, It will tell the scrript to generate new cookie

    #
    first_replace = cookie_name.replace('.pkl', '')
    then_split = first_replace.split('_')

    cookie_time = then_split[1]

    today_date_time = datetime.now()
    # current_date = today_date_time.strftime('%Y-%m-%d %H:%M-%S')

    cleaned_cookie_time = datetime.strptime(cookie_time, "%Y-%m-%d %H-%M-%S")

    time_difference = today_date_time - cleaned_cookie_time

    sixty_minutes = timedelta(minutes=60)
    if time_difference <= sixty_minutes:
        generate_cookie = 0
    else:
        generate_cookie = 1
        os.remove(cookie_name)
    return generate_cookie


def launch_chrome_debug(port=9222, profile_dir="chrome_1"):
    # This function loads opens chrome in debugging port,
    # We also need to create a new empty folder named chrome_1 in temp folder of C drive
    #  "C:\\temp\\chrome_profile"
    # As user chrome profile is disabled in selenium, it doesnt perform any task if user profile loaded.

    try:

        # Determine the appropriate Chrome executable path based on the OS
        if platform.system()  "Windows":
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            # On Windows, you might want a path like C:\temp\chrome_debug_profile
            user_data_dir = f"C:\\temp\\{profile_dir}"
        elif platform.system() == "Darwin":  # macOS
            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            user_data_dir = f"/tmp/{profile_dir}"
        else:  # Linux
            chrome_path = "google-chrome"  # Assumes it's in PATH, or specify full path
            user_data_dir = f"/tmp/{profile_dir}"

        command = [
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}"
        ]

        print(f"Launching Chrome with command: {' '.join(command)}")

        # Use subprocess.Popen to run the command in the background
        # This returns a Popen object, allowing your script to continue
        # running while Chrome is open.
        chrome_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Chrome launched. PID: {chrome_process.pid}")
        print(f"User data directory: {user_data_dir}")
    except Exception as chrome_load_error:
        chrome_process = None
        logging.error(chrome_load_error, exc_info=True)

    return chrome_process


def user_agent_options():
    # Below code provides and selects user agnet, important for scraping scenarios.
    #

    try:

        time.sleep(5)  # Give Chrome some time to fully launch and open the port

        list_of_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"]
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        #

        random_user_agent = random.choice(list_of_user_agents)

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        options.add_argument('--deny-permission-prompts')

        # options.add_argument(f"user-agent={random_user_agent}")
    except Exception as ua_error:
        options = None
        random_user_agent = None
        logging.error(ua_error, exc_info=True)

    return options, random_user_agent


def loading_webdriver_with_stealth():
    try:
        # proxy_string = "http://:4yrqg3yv7mq7@23.95.150.145:6123"

        # chrome_options.add_argument(
        #     f'--proxy-server={proxy_string}')

        # Adding stealth functionality in the script which makes our script more undecteable
        # You can also un comment above proxy line for using proxy for this script

        web_driver = webdriver.Chrome(options=chrome_options)

        # driver.find_element()

        stealth(web_driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32" if "Windows" in user_agent else "Linux x86_64" if "Linux" in user_agent else "MacIntel",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
    except Exception as proxy_error:
        web_driver = None
        logging.error(proxy_error, exc_info=True)

    return web_driver


def visiting_yelp_page():
    # This function visits yelp page in a human way,
    # it visits google, searches for keyword related to yelp and then
    # hits enter.
    # This function increases chance of not getting blocked by chrome or yelp.com

    try:

        driver.get("https://www.google.com")

        time.sleep(5)

        random_keyword = ['Yelp', 'Yelp Website', 'Yelp Webpage', 'yelp restaurants']
        pick_keyword = random.choice(random_keyword)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[title = 'Search']")))

        driver.find_element(By.CSS_SELECTOR, "[title = 'Search']").click()
        sleep(randint(1, 3))

        driver.find_element(By.CSS_SELECTOR, "[title = 'Search']").send_keys(pick_keyword)

        time.sleep(3)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role = 'listbox'] li:nth-of-type(1)")))

        # Not necessary to log below exception as the keys are not send that's why it's sending them again in chrome search box

        except:
            driver.find_element(By.CSS_SELECTOR, "[title = 'Search']").send_keys(f'{pick_keyword}')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role = 'listbox'] li:nth-of-type(1)")))

        driver.find_element(By.CSS_SELECTOR, "[title = 'Search']").send_keys(Keys.ENTER)
        sleep(randint(3, 4))

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "(//*[contains(text(), 'Restaurant')])[1]")))
        time.sleep(1)

        try:
            driver.find_element(By.XPATH, "(//*[contains(text(), 'Restaurant')])[1]").click()
            sleep(randint(1, 3))
        except ElementNotInteractableException:
            pass
            logging.error(ElementNotInteractableException, exc_info=True)

        google_visit = 1

    except Exception as problem_in_visiting_yelp:
        google_visit = None
        logging.error(problem_in_visiting_yelp, exc_info=True)

    return google_visit


def generating_yelp_cookie():
    # This function generates cookies and is connected with visiting yelp function.
    # This script has scrolling feature so that we visit yelp.com
    # it detect the script has human and doesn't throw any captcha.

    try:
        #
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Yelp: Restaurants')]/..")))
        # time.sleep(1)
        # get_yelp_url = driver.find_element(By.XPATH, "//h3[contains(text(), 'Yelp: Restaurants')]/..").get_attribute(
        #     'href')
        # time.sleep(2)
        # driver.get(get_yelp_url)

        time.sleep(1)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class = ' y-css-1w17o7m']")))
        sleep(randint(3, 5))
        height = driver.execute_script("return document.body.scrollHeight")

        find_random_divisible = randint(5, 7)

        scroll_times = height / find_random_divisible

        increase_scroll_value = scroll_times

        for scrolling_ in range(1, find_random_divisible + 1):
            driver.execute_script(f"window.scrollTo(0, {scroll_times});")
            sleep(randint(1, 3))

            scroll_times += increase_scroll_value

        driver.execute_script("window.scrollTo(0, 0);")

        cookie = driver.get_cookies()
        current_datetime = datetime.now()
        # formatted_datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        cleaned_formatted_data = current_datetime.strftime("%Y-%m-%d %H-%M-%S")

        file_name = f'cookies_{cleaned_formatted_data}.pkl'

        pickle.dump(cookie, open(file_name, 'wb'))
        driver.close()
        driver.quit()

        cookie = 1
    except Exception as cookie_not_generated:
        cookie = None
        logging.error(cookie_not_generated, exc_info=True)

    return cookie


def chromedriver_with_port():
    # This function is same as user agent options function with some basic modification
    try:

        options = Options()
        # proxy_string = "http://:4yrqg3yv7mq7@23.95.150.145:6123"
        # options.add_argument(
        #     f'--proxy-server={proxy_string}')

        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        options.add_argument("--disable-session-crashed-bubble")

        web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    except Exception as problem_in_web_driver:
        web_driver = None
        logging.error(problem_in_web_driver, exc_info=True)

    return web_driver


def human_behavior():
    # This function is designed for mimicking human behavior in the code ,
    # Where if 1 is selected it will perform a scroll over some images in the webpage

    # If 2 is selected it will press like or comment button and try to close it

    select_random_number = randint(1, 2)

    height = driver.execute_script("return document.body.scrollHeight")

    find_random_divisible = randint(5, 7)

    scroll_times = height / find_random_divisible

    increase_scroll_value = scroll_times

    for scrolling_ in range(1, find_random_divisible + 1):
        driver.execute_script(f"window.scrollTo(0, {scroll_times});")
        sleep(randint(1, 3))

        scroll_times += increase_scroll_value

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    try:

        if select_random_number == 1:
            driver.find_element(By.CSS_SELECTOR, "[class = ' y-css-ghs0gd']").click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class = ' y-css-1le0wnc']")))
            time.sleep(3)
            try:

                find_image_len = driver.find_elements(By.XPATH, "(//*[@class = 'y-css-764wx4'])").__len__()
                time.sleep(1)

                scroll_div = driver.find_element(By.XPATH, f"(//*[@class = 'y-css-764wx4'])[{find_image_len}]")
                time.sleep(1)

                driver.execute_script("arguments[0].scrollIntoView()", scroll_div)
                time.sleep(3)

                first_image = driver.find_element(By.XPATH, "(//*[@class = 'y-css-764wx4'])[1]")
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView()", first_image)
                time.sleep(3)

            except Exception as human_logic_1:
                logging.error(human_logic_1, exc_info=True)

            driver.find_element(By.CSS_SELECTOR, "[class = 'icon--24-close-v2 y-css-1pj8rar']").click()
            time.sleep(3)

            driver.execute_script("window.scrollTo(0, 0);")

    except Exception as random_1:
        logging.error(random_1, exc_info=True)
        pass

    try:
        if select_random_number == 2:
            driver.execute_script(f"window.scrollTo(0, 400);")

            time.sleep(0.5)
            driver.find_element(By.XPATH,
                                f"((//*[@class = 'y-css-1kri69a'])[1]//*[@role = 'button'])[{select_random_number}]").click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[class = 'y-css-6iv8cq']")))
            time.sleep(2)
            driver.find_element(By.XPATH, "//*[contains(@class, 'dismi')]//button").click()
            time.sleep(2)

            driver.execute_script(f"window.scrollTo(400, 0);")
    except Exception as human_logic_2:
        logging.error(human_logic_2, exc_info=True)


def scrape_page_data():
    # This function scrapes the data and prints it in the terminal

    # time.sleep(4)
    try:
        try:
            cookies = pickle.load(open(cookie_name, "rb"))

            driver.get('https://www.yelp.com')

            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, "(//*[contains(text(), 'Log in') or contains(text(), 'Log In')])[1]")))
            sleep(randint(3, 5))

            for cookie in cookies:
                # cookie['domain'] = '.yelp.com'
                driver.add_cookie(cookie)
        except FileNotFoundError:
            logging.error(FileNotFoundError, exc_info=True)

        driver.refresh()
        sleep(randint(3, 6))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, "(//*[contains(text(), 'Log in') or contains(text(), 'Log In')])[1]")))
        sleep(randint(3, 5))

        # driver.get('https://www.yelp.com/biz/troy-restaurant-wolfville')

        driver.get('https://www.yelp.com/biz/polana-smak%C3%B3w-warszawa')

        sleep(randint(5, 6))

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label = 'Location & Hours']")))

        human_behavior()

        time.sleep(3)

        try:
            name = driver.find_element(By.CSS_SELECTOR, "[class = 'headingLight__09f24__N86u1 y-css-74ugvt'] h1").text
            time.sleep(1)
        except NoSuchElementException:
            name = None
            logging.error(NoSuchElementException, exc_info=True)

        try:

            rating_val = driver.find_element(By.CSS_SELECTOR,
                                             "[data-testid = 'BizHeaderReviewCount'] [class = 'y-css-1x1e1r2']").text
        except NoSuchElementException:
            rating_val = None
            logging.error(NoSuchElementException, exc_info=True)

        time.sleep(1)

        try:
            address_text = driver.find_element(By.CSS_SELECTOR,
                                               "[aria-label = 'Location & Hours'] [class  = ' y-css-dx7fqt']").text
        except NoSuchElementException:
            address_text = None
            logging.error(NoSuchElementException, exc_info=True)

        time.sleep(1)

        try:
            city_text = driver.find_element(By.CSS_SELECTOR,
                                            "[aria-label = 'Location & Hours'] address  p:last-of-type").text
            post_code = city_text.split(',')

            if len(post_code) == 1:

                get_city_text = post_code[0]
                get_post_code = "Pin Code Not available"
            else:
                get_city_text = post_code[0]
                get_post_code = post_code[1]

        except NoSuchElementException:
            get_city_text = None
            get_post_code = None
            logging.error(NoSuchElementException, exc_info=True)

        time.sleep(1)

        try:
            open_timings = driver.find_elements(By.XPATH,
                                                "//*[@class = 'hours-table__09f24__KR8wh y-css-16hyog2']//*[@class = ' y-css-29kerx']")
        except NoSuchElementException:
            open_timings = None
            logging.error(NoSuchElementException, exc_info=True)

        time.sleep(1)
        try:
            get_image_for_longitude = driver.find_element(By.CSS_SELECTOR,
                                                          "[aria-label = 'Location & Hours'] img").get_attribute('src')
            time.sleep(0.5)
            split_center = get_image_for_longitude.split('center=')
            get_lati_longi = split_center[1].split('&')
            final_split = get_lati_longi[0].split('%2C')
            latitude = final_split[0] + ','
            longitude = final_split[1]

        except NoSuchElementException:
            latitude = None
            longitude = None
            logging.error(NoSuchElementException, exc_info=True)

        store_opening = []
        for get_timing in open_timings:
            text = get_timing.text.split('-')
            open_text = text[0].strip('')

            store_opening.append(open_text)

        remove_brackets = ''.join(store_opening).strip('')

        print('Name :', name)
        print('Rating :', rating_val)
        print('Address :', address_text)
        print('City :', get_city_text)
        print('Post Code :', get_post_code)
        print('Latitude :', latitude)
        print('Longitude :', longitude)
        print('Store Open Timing :', remove_brackets)

        scraped_all_values = 1
    except Exception as problem_in_scraper:
        scraped_all_values = None
        logging.error(problem_in_scraper, exc_info=True)

    return scraped_all_values


if __name__ == '__main__':
    logging.basicConfig(
        filename='app.text',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True  # Add this argument (Python 3.8+)
    )

    cookie_name = find_cookie_name()
    if cookie_name is None:
        run_cookie_driver = 1
    else:
        run_cookie_driver = time_difference_checker()

    if run_cookie_driver == 1:
        terminate_process = launch_chrome_debug()
        if terminate_process is not None:
            chrome_options, user_agent = user_agent_options()
            if chrome_options is not None:
                driver = loading_webdriver_with_stealth()
                if driver is not None:
                    yelp_main_page = visiting_yelp_page()
                    if yelp_main_page is not None:
                        cookie_generated = generating_yelp_cookie()
                        if cookie_generated is not None:
                            if terminate_process:
                                terminate_process.terminate()
                            if driver:
                                driver.quit()

    terminate_process = launch_chrome_debug()
    if terminate_process is not None:
        driver = chromedriver_with_port()
        if driver is not None:
            cookie_name = find_cookie_name()
            if cookie_name is not None:
                data = scrape_page_data()
                if data is not None:
                    if terminate_process:
                        terminate_process.terminate()
                    if driver:
                        driver.quit()
            else:
                if terminate_process:
                    terminate_process.terminate()
                if driver:
                    driver.quit()
                sys.exit()




