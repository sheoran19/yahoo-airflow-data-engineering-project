
# Yahoo Data Pipeline using Airflow
===========================================


    .
    ├── ...
    ├── test                    # Test files (alternatively `spec` or `tests`)
    │   ├── benchmarks          # Load and stress tests
    │   ├── integration         # End-to-end, integration tests (alternatively `e2e`)
    │   └── unit                # Unit tests
    └── ...

    
│.              
├── airflow  
|   └── airflow.cfg                           
│   └── dags 
|       └── yahoo_dag.py
│
├── app                                 
│   ├── main.py                            
│   ├── models.py                          
│   └── database.py 
│
├── docker    
│   ├── Dockerfile                        
│   └── docker-compose.yaml                           
│
└── etl                                 
|   └── yahoo_data_etl.py 
|
├── .env                               
├── README.md                          
├── application_default_credentials.json 
├── architecture_diagram.png            
├── market_codes.csv                  
├── requirements.txt     

## Overview

This project creates a dynamic, scalable, and secure pipeline for processing Yahoo API data, using GCP services, Airflow, FastAPI, and Docker. It seamlessly ingests, validates, transforms, and delivers data, providing actionable insights through well-defined APIs.


## Key Objectives

- Efficiently process vast amounts of data from Yahoo APIs.
- Ensure data integrity and quality through rigorous validation.
- Deliver scalable solutions with GCP's computing and storage services.
- Facilitate data-driven decision-making for clients via FastAPI endpoints.
- Maintain high system reliability and instant alerting mechanisms.


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
