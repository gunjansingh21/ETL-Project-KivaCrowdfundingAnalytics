# ETL-Project-KivaCrowdfundingAnalytics

Kiva is an online crowdfunding organization that offers loan services to underserved and unbanked populations worldwide. Some of the use cases of these loans include starting a business, paying school fees, and investing in farming. The datasets available at Kiva show the loans issued to borrowers between January 2014 and July 2017. This information will be valuable in defining some Key Performance Indicators (KPIs) to evaluate the organization’s performance over time. Kiva lenders have provided over 1 billion dollars in loans to over 2 million people. In order to set investment priorities, help inform lenders, and understand their target communities, knowing the level of poverty of each borrower is critical. This project is designed to showcase how various Azure services can be utilized and leveraged to perform ETL operations like data ingestion, data transformation and data analytics on this dataset. 

# Data
The loan dataset provided by kiva contains a set of information for each loan application: dollar value of loan funded on Kiva.org; total dollar amount of loan; loan activity type; sector of loan activity as shown to lenders; country name; name of location within country; repayment interval, which is the frequency at which lenders are scheduled to receive installments, and loan theme, as well as Kiva’s estimates as to the various geolocations in which a loan theme has been offered. This data is in CSV format; hence, you need to load the data into the database for storage. I used the SQL server database as the data source for the project.

I'm unable to add the dataset here becuase of the size. The size of the dataset is quite huge. Please use the link in DATA SOURCE section to download or refer to the dataset. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/632a1da9-34a8-4124-a4f8-aacc3d3a6303)

# Table of Contents
1. [Introduction to Azure Services](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/blob/main/README.md#introduction-to-azure-services-step-by-step)
2. [Project Overview](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/blob/main/README.md#project-overiew)
3. [Data Architecture Flow Diagram](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/blob/main/README.md#data-architecture-flow-diagram)
4. [Data Sources & Visualisations](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/blob/main/README.md#data-sources-and-visualisations)
5. [Pre-Requisites](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/blob/main/README.md#pre-requisites)

# Introduction to Azure Services (Step by Step)

 - **Azure Data Factory**: Azure Data Factory (ADF) is a fully managed, serverless data integration solution for ingesting, preparing, and transforming all your data at scale. In this project, we are migrating the data from SQL server (source) to Azure DataLake Storage Gen2 (sink). For the creation of the pipeline for data movement, we are using three activities - Lookup activity (), ForEach activity () and copy activity.

 - **Azure Data Lake Storage Gen2** : This is the storage account where we are storing the data coming from our sorce. The data ingested here is in raw format. Azure Data Lake Storage Gen2 provides a scalable and secure platform for storing large volumes of data. It enables us to manage, access. and analyze data effectively. We'll be storing the data in three layers.
   - BRONZE : This is where the raw format of the data will be stored
   - SILVER : This is where the data will be stored after first level of transformations.
   - GOLD : This is where the data will be stored after second level of transformations.

 - **Azure Databricks**: Azure Databricks is a fast, scalable, and collaborative Apache Spark-based analytics platform provided by Microsoft Azure. It combines Apache Spark’s capabilities with the comfort and simplicity of a fully managed cloud service. For data transformation like changing or modifying the schema of the tables, changing and modifying few columns we have leveraged Azure Databricks with PySpark. n this step, we are using Azure Databricks build on Apache Spark and we are using PySPark to write the transformations in the Notebook. We can then execute the Notebook that will automatically spin up the spark cluster and provide you the necessary compute to carry out your data transformations. But before transformations, make sure to provide necessary permissions for your Databricks workspace to connect with storage account (ADLS Gen2). The transformed data was then stored in different folders in the silver and gold container with respective table names.

 - **Azure Synapse Analytics** : We have used Azure Synapse Analytics to gain some valuable insights from the transformed data and performed some visualisations on top of the transformed data in gold container. We created a lake database by accessing the files on ADLS Gen2. Once the database was created, I then created a notebook to peform some analytics on the data and created some charts and graphs out of it. Azure Synapse Analytics is a scalable and cloud-based data warehousing solution from Microsoft. It is the next iteration of the Azure SQL data warehouse. It provides a unified environment by combining the data warehouse of SQL, the big data analytics capabilities of Spark, and data integration technologies to ease the movement of data between both, and from external data sources. Make sure you provide the necessary roles and permissions to your Synapse workspace that it can access the storage account. 

 - **Azure Key Valut** : We have used this service to maintain and keep our secrets encrypted. Azure Key Vault is a cloud service that provides a secure store for secrets. You can securely store keys, passwords, certificates, and other secrets. Azure key vaults are created and managed through the Azure portal. It is widely used for security management and data encryption.

# Project Overiew

 - **Data Ingestion** - This is the first step in the project where we are ingesting the data from SQL Server DB and moving it to the Azure Data Lake Storage Gen2. The data ingestion process was carried out using Azure Data Factory. For this project, I was interested in creating a pipeline that would read all the tables from the SQL server database and load them in Azure Data Lake Gen 2. I created three storage containers (gold, silver, and bronze) in the Azure Data Lake Storage Gen2, where the bronze container will derive data from the data ingestion activity and the tables will be moved from source to sink. To create a pipeline to read all the tables in the database, I used the lookup activity to look up all the tables from the SQL database. In this lookup activity, I use a query to list the tables to ingest in Azure Data Lake Gen 2. Thereafter, I created a ForEach item in the pipeline to iterate from the Lookup activity to copy all the tables. The ForEach item would loop through all the tables and copy the items listed from the lookup table. Under the ForEach item, I created the Copy data item to copy data from the source. I configured the source of the data and the sink to save the data as CSV files. I also specified the path of the datasets so that each copied table would be stored separately in a folder and a path with the file name. Furthermore, the data ingestion pipeline was used to read and store the data from the SQL server to the bronze container, where the data was in the raw format. After the successful configuration of the pipeline, I ran using the debug option to test whether it was working without any errors. Besides, I used the add trigger option to run the pipeline and tested with the current time. Since the pipeline was meant to fetch the tables from the on-prem SQL server every time it runs, every successful run would overwrite the existing folder in the bronze container. At the end of the data ingestion, the data was now stored in the bronze container ready for transformation. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/3041d2c9-06c2-4f9f-9a43-43094c68ac7f)

  - **Data Storage** - This is the immediate step after data ingestion where we are using Azure Data Lake Storage Gen2. There are three layers build on the storage account for this project - bronze layer that will contain the data in its raw format, silver layer that will have the transformed data like date type conversions & removing null and duplicates and gold layer that will store all the aggregated data or altering the column names and types. We configured our sink as Azure Data Lake Storage Gen2 where the data will come and load into bronze container and the data will be in the exact same format as the source. The silver container would contain data from level 1 transformation from the bronze container while the gold container would contain the cleaned and transformed data from the silver container. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/f7845689-ebee-47e5-b330-d49a4141ac47)

  - **Data Transformations** - After the preliminary data movement is done and we finally have the data in storage account - bronze container, we move on to the next step of transforming the data. But before that, we need to create a compute cluster to allow different jobs to run in the notebooks. After that, we used the fs utility under dbutils to mount the data from ADLS Gen2 to Databricks Workspace using service principal. After the storage has been mounted on DBFS, we performed two levels of transformations. The first level of transformations is Bronze_to_Silver and the second level of transformations is Silver_to_Gold. I focused the first level of transformation on changing the date format from date-time to date type. At this level, I wanted the transformation to apply to all the tables and the columns of the date data type. The transformed data was then moved to the silver container. I performed another set of transformations from data in the silver container by changing the column names to lowercase. This transformation was to ensure there is a uniform naming convention for the data across the different tables. The transformed data was then stored in different folders in the gold container with respective table names. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/b720dadd-5bcd-4638-9e7c-bdfcec851286)

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/ff08e6e0-32af-4505-a8b4-51e183b67514)

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/0586b5ae-4087-4e9c-927c-13bd4557e91d)

 - **Data Analytics** - Azure Synapse Analytics is a scalable and cloud-based data warehousing solution from Microsoft. It is the next iteration of the Azure SQL data warehouse. It provides a unified environment by combining the data warehouse of SQL, the big data analytics capabilities of Spark, and data integration technologies to ease the movement of data between both, and from external data sources. In this project, we are using it for data warehousing and data analytics purposes. Firstly. I created a linked service for my ADLS Gen2 and connected the storage account to my Synapse Workspace. Once that was done, I created a lake database by using the files in the gold container of ADLS Gen2 storage account. Once the db was created, I wanted to perform some analytics on the clean data, so before creating a notebook I created an Apache Spark Pool. To run your jobs or notebook, you need to have some sort of compute available, that can either be SQL pool(dedicated or serverless) or Apache Spark Pool. After that, I created a notebook for KivaCrowdfundingAnalytics and did a series of analytics and visualisations on the data present in the gold container. Make sure you provide the necessary roles and permissions to your Synapse workspace that it can access the storage account. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/dba040fc-c628-4619-9d1c-b9bb28cb73f8)

 - **Data Visualisation** : This is the last step where we can create visualisations on top of our gold layer data. We create charts and graphs to help business understand the data clearly and easily. It's an important step in making informed business decisions. We can create various types of graphs like bar chart, scatter plot, column chart, line chart, pie charts etc. using various tools. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/ad3170f3-a0e9-4744-800b-2d412e2f37e1)

# Data Architecture Flow Diagram

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/e6fc0f9c-2f69-4525-a4ab-00bdc2ce4519)

# Data Sources and Visualisations

Data Source : **https://www.kaggle.com/datasets/kiva/data-science-for-good-kiva-crowdfunding**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/632a1da9-34a8-4124-a4f8-aacc3d3a6303)

Visualisation 1: **Top 10 Countires that got maximum number of times Loan**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/04958022-5718-4e0e-9543-1d1a13966bb9)

Visualisation 2: **Top 10 Countries that got maximum amount of total loan**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/16e6e555-7664-4e0c-a0a8-aae145e82f6b)

Visualisation 3: **Top 10 Sectors that got maximum amount of total loan**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/bd9cac20-0d2e-4326-9855-b6bb21f3262a)

Visualisation 4: **Top 10 Activity that got maximum amount of total loan**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/30027da6-f227-400d-9b8b-21404149b8b4)

Visualisation 5: **India's Loan distribution with neighbour countries**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/cee9ce0a-f0e9-425a-9e9a-3a185d989cd9)

Visualisation 6: **Reypayment Interval of Loans**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/88087dfd-14f5-496e-bfaf-06bc9e83147c)

Visualisation 7: **Number of Times Loans were given to India and its neighbour**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/5e9d3727-95c9-45db-b95e-1bdecb028617)

Visualisation 8: **Gender Distribution of Borrower**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/d03326d9-8415-40a7-863f-ae08b6065972)

Visualisation 9: **Top 10 Activities that got maximum amount of loan in India**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/ea3d3d1c-79e0-432a-a331-52396e67a676)

Visualisation 10: **Top 10 cities that got maximum amount of total loan**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/59bbb19f-1e16-47cb-ad7d-ba3508bd7416)

Visualisation 11: **Top 10 Countries with highest MPI (Multidimentional Poverty Index)**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/c7d94e5f-89a5-48b2-9deb-16b98d376f32)

Visualisation 12: **Top 10 Countries with low MPI (Multidimentional Poverty Index)**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/29760ac2-4f2a-45a3-8f05-ed19d5e0292a)

Visualisation 13: **Top 10 sectors that got maximum amount of loan in India**
![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/2814b288-67fc-45e3-a6cd-b27925cbe79b)

# Pre-Requisites

1. You need to have an active Azure subscription to provision these required services.
2. You need to have an account on Azure Portal to access and manage these resources for your ETL project.
3. Make sure you have your source data sets ready and in place to start the project.
  
