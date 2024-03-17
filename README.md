
# Yahoo Data Pipeline using Airflow

## Overview

This project creates a dynamic, scalable, and secure pipeline for processing Yahoo API data, using GCP services, Airflow, FastAPI, and Docker. It seamlessly ingests, validates, transforms, and delivers data, providing actionable insights through well-defined APIs.


## Project Objectives and Goals

- **Data Ingestion and Validation**: The project aims to build a robust mechanism to ingest data from Yahoo APIs and other sources, ensuring the accuracy and quality of source data through stringent validation processes, utilizing Great Expectations. This ensures that only reliable data is processed and stored, laying a solid foundation for insightful analysis.

- **Efficient ETL Processes**: Leveraging Airflow for orchestration, the project transforms raw data using Python and Pandas, aligning it with client requirements. This transformation process is key to converting vast amounts of raw data into structured, usable formats that drive decision-making.

- **Scalability and Cloud Integration**: With the anticipated increase in data volume, the project is designed to scale seamlessly, utilizing GCP's Compute Engine and CloudSQL. This ensures that the infrastructure grows with the data, maintaining performance and reliability without compromising on processing speed or data integrity.

- **Secure and Fast Data Access**: By employing FastAPI and deploying it on GCP Cloud Run, the project provides secure, efficient, and scalable endpoints for data access. This facilitates easy and quick data retrieval by clients, enabling them to make informed decisions based on the latest insights.

- **Real-Time Alerts and Monitoring**: Integration with Slack Webhooks allows for real-time alerts and monitoring of the system's health and data processing activities. This proactive approach ensures any issues are swiftly addressed, maintaining high system reliability and uptime.

- **Containerization for Consistency**: Docker is utilized to containerize the project components, ensuring that the development, testing, and production environments are consistent. This reduces discrepancies between environments, streamlines deployment processes, and enhances overall project maintainability.

The culmination of these objectives and goals is to create a data pipeline that not only meets the current needs but is also future-proof, accommodating new data sources, expanding client requirements, and evolving technological landscapes.


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
