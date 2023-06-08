from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_images(queries, high_res=False):
    with ThreadPoolExecutor() as executor:
        return executor.map(fetch_images, queries, [1]*len(queries), [high_res]*len(queries))


def fetch_images(query, num_images, high_quality=False):
    driver_path = '/usr/local/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    try:
        url = f'https://www.google.com/search?q={query}&tbm=isch'
        driver.get(url)

        image_urls = []

        if high_quality:
            while len(image_urls) < num_images:
                image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')

                for element in image_elements:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img.rg_i')))
                    element.click()
                    time.sleep(0.5)
                    new_elements = driver.find_elements(By.CSS_SELECTOR, 'img.r48jcc')
                    for new_element in new_elements:
                        src = new_element.get_attribute('src')
                        if src and src.startswith('http'):
                            resolution = get_image_resolution(src)
                            if resolution and resolution[0] >= 1000:
                                image_urls.append(src)

                    if len(image_urls) >= num_images:
                        break

                last_height = driver.execute_script('return document.body.scrollHeight')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                while True:
                    new_height = driver.execute_script('return document.body.scrollHeight')
                    if new_height == last_height:
                        break
                    last_height = new_height

        else:
            while len(image_urls) < num_images:
                image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')

                for element in image_elements:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img.rg_i')))
                    element.click()
                    time.sleep(0.5)
                    new_elements = driver.find_elements(By.CSS_SELECTOR, 'img.r48jcc')
                    for new_element in new_elements:
                        src = new_element.get_attribute('src')
                        if src and src.startswith('http'):
                            image_urls.append(src)

                    if len(image_urls) >= num_images:
                        break

                last_height = driver.execute_script('return document.body.scrollHeight')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                while True:
                    new_height = driver.execute_script('return document.body.scrollHeight')
                    if new_height == last_height:
                        break
                    last_height = new_height

        return image_urls[:num_images]

    finally:
        driver.quit()



def get_image_resolution(image_url):
    driver_path = '/usr/local/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=chrome_options)

    try:
        driver.get(image_url)
        width = driver.execute_script('return document.querySelector("img").naturalWidth')
        height = driver.execute_script('return document.querySelector("img").naturalHeight')
        return width, height

    finally:
        driver.quit()

