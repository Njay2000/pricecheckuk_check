from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(cfg: DictConfig):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Function to get the soup object for a given URL
    def get_soup(url):
        driver.get(url)
        WebDriverWait(driver, cfg.scraping.wait_time).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main"))
        )
        return BeautifulSoup(driver.page_source, "html.parser")

    # Function to scrape products from the current page
    def scrape_products(soup):
        product_links = [a["href"] for a in soup.select(".product-item-link")]
        for link in product_links:
            driver.get(link)
            WebDriverWait(driver, cfg.scraping.wait_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, "main"))
            )
            product_soup = BeautifulSoup(driver.page_source, "html.parser")
            product_name = product_soup.find("h1", class_="page-title").text.strip()
            product_info = {"Product Name": product_name}

            selectors = [
                "tr:nth-child(1) .bold",
                "tr:nth-child(2) td",
                "tr:nth-child(3) td",
                "tr:nth-child(4) td",
                "tr:nth-child(5) td",
                "tr:nth-child(6) td",
                "tr:nth-child(7) td",
                "tr:nth-child(8) td",
                "tr:nth-child(9) td",
                "tr:nth-child(10) td",
                "tr:nth-child(11) td",
                ".notranslate",
            ]

            for selector in selectors:
                elements = product_soup.select(selector)
                for element in elements:
                    key = (
                        element.previous_sibling.text.strip().replace(":", "")
                        if element.previous_sibling
                        else "Other"
                    )
                    value = element.text.strip()
                    product_info[key] = value

            image = product_soup.find("img", class_="fotorama__img")
            if image:
                product_info["Image URL"] = image["src"]

            product_list.append(product_info)

    # Function to get the next page URL
    def get_next_page(soup):
        next_button = soup.select_one("li.pages-item-next a.action.next")
        return next_button["href"] if next_button else None

    # Main scraping logic
    url = cfg.scraping.url
    product_list = []

    while True:
        soup = get_soup(url)
        scrape_products(soup)
        url = get_next_page(soup)
        if not url:
            break

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(product_list)
    df.to_csv(cfg.scraping.output_file, index=False)

    # Close the driver
    driver.quit()

    print("Scraped product information:")
    print(df)


if __name__ == "__main__":
    main()
