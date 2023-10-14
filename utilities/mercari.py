from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import re
import os
from .money import *
from .custom_exception import *
import logging

def mercari_brief_info(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    try:
        # driver = webdriver.Remote("http://localhost:4444/wd/hub", options=chrome_options)
        driver = webdriver.Remote(
            f"http://{os.environ['SELENIUM_URL']}:4444/wd/hub", options=chrome_options)
        driver.get(url)
        time.sleep(float(1.5))
        item_name, img_url = parseMercariMetadata(driver)
        formatted_price_jpy, shipping_fee_tag, sold_out_flag, description = parseMercariDetails(
            driver)
        driver.quit()
    except Exception as e:
        print(f"Crashed: {e}",flush=True)
        driver.quit()
        raise

    formatted_final_price_cny = calculateFinalCNYPrice(formatted_price_jpy)
    data = {
        'item_url': url,
        'price_jpy': formatted_price_jpy,
        'price_cny': formatted_final_price_cny,
        'item_name': item_name,
        'img_url': img_url,
        'shipping_fee_tag': shipping_fee_tag,
        'sold_out_flag': sold_out_flag,
        'discription': description}
    return data


def parseMercariDetails(driver, timeout=10):
    start_time = time.time()
    price = None
    item_type = None
    sold_out_element = None
    description = None
    while time.time()-start_time < timeout:
        try:
            price = driver.find_element('xpath',
                                        "//div[@data-testid='price']/span[2]").text
            print("price:" + price,flush=True)
            item_type = driver.find_element('xpath',
                                            "//p[contains(@class,'caption')]").text
            print("type: " + item_type,flush=True)
            sold_out_element = driver.find_element('xpath',
                                                   "//div[@data-testid='checkout-button']/button").text
            print("sold status:" + sold_out_element, flush=True)
            description = driver.find_element(
                'xpath', "//pre[@data-testid='description']").text
            print(f"description: {description}",flush=True)
            break
        except NoSuchElementException:
            print("Page is loading now, wait 0.1s", flush=True)
            time.sleep(0.1)

    if time.time()-start_time >= timeout and not (price and item_type and sold_out_element and description):
        raise TimeoutError('Fail to find elements in this page.')

    if ("送料込み" in item_type):
        shipping_fee_tag = True
    else:
        shipping_fee_tag = False

    formatted_price = re.sub('\D', '', price)

    sold_out_flag = False
    if (sold_out_element is not None):
        if (sold_out_element == "売り切れました"):
            sold_out_flag = True

    return int(formatted_price), shipping_fee_tag, sold_out_flag, description


def parseMercariMetadata(driver, timeout=10):
    start_time = time.time()
    item_name = None
    img_url = None
    while time.time()-start_time < timeout:
        try:
            item_name = driver.find_element(
                'xpath', "//h1[contains(@class, 'heading_')]").text
            print("item_name: " + item_name,flush=True)
            img_url = driver.find_element('xpath',
                                          "//div[@data-testid='image-0']/figure/div[@aria-label]/picture/img").get_attribute('src')
            print("img_url:" + img_url,flush=True)
            break
        except NoSuchElementException:
            print("Page is loading now, wait 0.3s", flush=True)
            time.sleep(0.3)
    if time.time()-start_time >= timeout and not item_name and not img_url:
        raise TimeoutError('Fail to find elements in this page.')
    return item_name, img_url


if __name__ == '__main__':
    output = mercari_brief_info("https://jp.mercari.com/item/m20026412045")
    print(output)
