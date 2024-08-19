import hydra
from omegaconf import DictConfig
from src.scraper import scrape_products
from src.db import save_to_db
from src.utils import process_data
from src.logger import custom_logger as logger


@hydra.main(version_base=None, config_path="../config", config_name="config")
def main(cfg: DictConfig):
    logger.info("Starting main process")
    product_list = scrape_products(cfg.scraping.urls, cfg.scraping.wait_time)
    df = process_data(product_list)
    df.to_csv(cfg.scraping.output_file, index=False)
    logger.info(f"Data saved to {cfg.scraping.output_file}")
    logger.debug(f"DataFrame Head: \n{df.head()}")
    save_to_db(cfg, df)
    logger.info("Main process finished")


if __name__ == "__main__":
    main()
