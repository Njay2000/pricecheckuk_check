# Web Scraper with AWS Cloud Integration

This project is a modular web scraping application designed to collect and store data from specified websites, leveraging the power of AWS cloud services for enhanced scalability and accessibility. It features an organized structure with separate components for scraping, logging, database interactions, and utility functions. The application is built with extensibility and maintainability in mind, leveraging Hydra for configuration management.

**Features**

* **Dynamic Web Scraping:** Easily configurable to scrape multiple URLs.
* **AWS RDS Integration:** Seamlessly stores scraped data into an Amazon RDS database instance.
* **AWS Lambda Deployment:**  Scraping logic is deployed as a Lambda function for serverless execution, triggered on schedule or by events.
* **API Gateway Exposure:**  Provides a REST API endpoint through Amazon API Gateway to access and query the scraped data.
* **Advanced Logging:** Comprehensive logging for robust debugging and monitoring, utilizing CloudWatch Logs.
* **Utility Functions:** Handy utilities to streamline the scraping process.
* **Hydra Configuration:** Flexible management of configurations through Hydra.

This architecture allows for a robust and scalable solution, enabling efficient data collection, storage, and retrieval. By utilizing AWS services, the application benefits from:

* **Scalability:** Lambda functions automatically scale to handle varying workloads.
* **Cost-efficiency:** Pay only for the compute time consumed by Lambda functions.
* **High Availability:** RDS and API Gateway offer built-in high availability and fault tolerance.
* **Easy Management:** AWS services provide a managed environment, reducing operational overhead.

This project provides a comprehensive solution for web scraping needs, combining the flexibility of custom code with the power and scalability of AWS cloud services.
