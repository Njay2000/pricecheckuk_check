from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from src.logger import custom_logger as logger


def get_driver():
    logger.info("Initializing WebDriver")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def get_soup(driver, url, wait_time):
    logger.info(f"Fetching URL: {url}")
    driver.get(url)
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main"))
    )
    return BeautifulSoup(driver.page_source, "html.parser")


def scrape_product(driver, url, wait_time):
    logger.info(f"Scraping product page: {url}")
    driver.get(url)
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main"))
    )
    product_soup = BeautifulSoup(driver.page_source, "html.parser")
    product_name = product_soup.find("h1", class_="page-title").text.strip()
    product_info = {"product_name": product_name}

    # Select table rows that contain product details
    rows = product_soup.select("table.table-bordered tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        key = cols[0].text.strip().replace(":", "").replace(" ", "_").lower()
        value = cols[1].text.strip()
        product_info[key] = value

    image = product_soup.find("img", class_="fotorama__img")
    if image:
        product_info["image_url"] = image["src"]

    if "barcode" not in product_info or not product_info["barcode"]:
        logger.warning("Skipping product due to missing barcode")
        return None

    logger.debug(f"Scraped product info: {product_info}")
    return product_info


def scrape_products(urls, wait_time):
    driver = get_driver()
    product_list = []
    try:
        for url in urls:
            while url:
                soup = get_soup(driver, url, wait_time)
                product_links = [a["href"] for a in soup.select(".product-item-link")]
                for link in product_links:
                    product_info = scrape_product(driver, link, wait_time)
                    if product_info:
                        product_list.append(product_info)
                url = get_next_page(soup)
    finally:
        driver.quit()
    logger.info(f"Scraped {len(product_list)} products")
    return product_list


def get_next_page(soup):
    next_button = soup.select_one("li.pages-item-next a.action.next")
    return next_button["href"] if next_button else None
