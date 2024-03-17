
# Yahoo Data Pipeline using Airflow

## Overview

This project creates a dynamic, scalable, and secure pipeline for processing Yahoo API data, using GCP services, Airflow, FastAPI, and Docker. It seamlessly ingests, validates, transforms, and delivers data, providing actionable insights through well-defined APIs.


## Key Objectives and Project Goals

- **Efficient Data Processing**: Leverage Airflow, Python, and Pandas to efficiently ingest, validate, and transform data from **Yahoo APIs** into actionable insights.
- **Data Integrity and Quality**: Utilize **Great Expectations** for thorough data validation to ensure accuracy and reliability of source data before any processing.
- **Scalable Solutions**: Deploy on **GCP Compute Engine** and utilize **CloudSQL** to ensure the system scales seamlessly with increasing data volumes, maintaining high performance and availability.
- **Data-Driven Decision Making**: Provide clients with access to processed data through **FastAPI endpoints**, facilitating insightful analysis and informed decision-making.
- **System Reliability and Responsiveness**: Integrate **Slack Webhooks** for real-time alerts to monitor system health and notify of critical events, ensuring high system reliability.
- **Security and Compliance**: Ensure that the system adheres to the highest standards of data security and privacy, protecting sensitive information and complying with regulatory requirements.
- **Cloud-Based Architecture**: Leverage the power of cloud computing with **GCP** to handle vast amounts of data, offering a robust, secure, and flexible environment.
- **Client Reporting and Accessibility**: Build and maintain **FastAPI endpoints** for efficient data sharing with clients, ensuring data is accessible and actionable.

This comprehensive approach combines the project's overarching goals with specific objectives, laying a foundation for a robust, scalable, and efficient data processing pipeline.


## Architecture Highlights

- **Data Ingestion**: Utilizes **Yahoo APIs**, including **Insights API** and **Marketing API**, for source data.
- **Data Validation**: Employs **Great Expectations** to ensure data quality before processing.
- **ETL Processes**: Orchestrated by **Airflow**, leveraging **Python** and **Pandas** for data transformation, preparing it for analysis and reporting.
- **Computing and Storage**: Uses **GCP Compute Engine** for scalable computing resources and **CloudSQL** for robust data storage.
- **API Management**: **FastAPI** framework, deployed on **GCP Cloud Run**, exposes processed data through secure and efficient endpoints.
- **Real-Time Alerts**: Integrates **Slack Webhooks** to provide instant notifications for system alerts and updates.
- **Containerization**: **Docker** encapsulates the project's components, ensuring consistent environments and streamlined deployments.




## Architecture Diagram

![alt text](https://github.com/sheoran19/yahoo-airflow-data-engineering-project/blob/main/architecture_diagram.png)
