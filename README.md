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

 - **Azure Data Lake Storage Gen2** : This is the storage account where we store the data coming from our source, ingested in its raw format. Azure Data Lake Storage Gen2 offers a scalable and secure platform for managing large volumes of data, enabling effective access and analysis.

We will organize the data into three layers:

BRONZE: This layer stores the raw format of the data.
SILVER: This layer contains the data after the first level of transformations.
GOLD: This layer holds the data following the second level of transformations.

 - **Azure Databricks**: Azure Databricks is a fast, scalable, and collaborative analytics platform based on Apache Spark, provided by Microsoft Azure. It combines the power of Apache Spark with the ease of a fully managed cloud service.

For data transformations, such as modifying table schemas and adjusting specific columns, we leverage Azure Databricks alongside PySpark. In this step, we utilize Azure Databricks built on Apache Spark, using PySpark to write our transformations in a notebook. Executing the notebook automatically spins up the Spark cluster, providing the necessary compute resources for our data transformations.

Before proceeding with the transformations, it’s essential to ensure that your Databricks workspace has the required permissions to connect to the Azure Data Lake Storage (ADLS) Gen2. The transformed data is then stored in separate folders within the silver and gold containers, organized by respective table names.

 - **Azure Synapse Analytics** : We have utilized Azure Synapse Analytics to derive valuable insights from the transformed data and perform visualizations based on the data stored in the gold container. I created a lake database by accessing the files in ADLS Gen2. Once the database was established, I developed a notebook to conduct analytics on the data and create various charts and graphs.

Azure Synapse Analytics is a scalable, cloud-based data warehousing solution from Microsoft and represents the next iteration of Azure SQL Data Warehouse. It offers a unified environment by integrating SQL data warehousing, big data analytics capabilities with Spark, and data integration technologies, facilitating seamless movement of data between these components and external sources.

It's essential to ensure that the necessary roles and permissions are granted to your Synapse workspace, allowing it to access the storage account.

 - **Azure Key Valut** : We have utilized Azure Key Vault to securely manage and encrypt our secrets. Azure Key Vault is a cloud service that provides a secure repository for storing keys, passwords, certificates, and other sensitive information. Key vaults are created and managed through the Azure portal, making it a widely used solution for security management and data encryption.

# Project Overiew

 - **Data Ingestion** - This marks the initial phase of our project, where we are transferring data from a SQL Server database to Azure Data Lake Storage Gen2. The data ingestion process was executed using Azure Data Factory. My objective for this project was to create a pipeline that would read all tables from the SQL Server database and load them into Azure Data Lake Gen2.

To facilitate this, I established three storage containers—gold, silver, and bronze—in Azure Data Lake Storage Gen2. The bronze container is designed to store data directly from the ingestion process, with tables being moved from the source to the destination.

To read all the tables in the database, I employed a lookup activity that queries the SQL database to list the tables for ingestion. Following this, I implemented a ForEach activity in the pipeline to iterate over the results from the lookup activity, enabling the copying of each table. Within this ForEach loop, I created a Copy Data activity to transfer data from the source to the destination. I configured the source and destination to save the data as CSV files and specified dataset paths to ensure that each copied table is stored in its respective folder with a designated file name.

The data ingestion pipeline reads and stores data from the SQL Server into the bronze container, retaining the raw format. After configuring the pipeline successfully, I utilized the debug option to test its functionality and verify that it operated without errors. Additionally, I used the "Add Trigger" option to run the pipeline immediately for testing purposes. As the pipeline is intended to fetch tables from the on-premises SQL Server each time it runs, every successful execution overwrites the existing folder in the bronze container. Consequently, at the conclusion of the data ingestion process, the data is now stored in the bronze container, ready for transformation. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/3041d2c9-06c2-4f9f-9a43-43094c68ac7f)

  - **Data Storage** - This is the subsequent step following data ingestion, utilizing Azure Data Lake Storage Gen2. For this, we have established three layers within the storage account:

Bronze Layer: This layer contains data in its raw format.
Silver Layer: This layer holds transformed data, including date type conversions and the removal of null values and duplicates.
Gold Layer: This layer stores aggregated data, which may involve altering column names and data types.

We configured our sink to be Azure Data Lake Storage Gen2, where the data is loaded into the bronze container in its original format. The silver container contains data resulting from level 1 transformations applied to the bronze container, while the gold container holds the cleaned and further transformed data sourced from the silver container.

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/f7845689-ebee-47e5-b330-d49a4141ac47)

  - **Data Transformations** - After completing the preliminary data movement and successfully storing the data in the bronze container of our storage account, we proceed to the next step: transforming the data. Before doing so, we first create a compute cluster to enable various jobs to run in the notebooks.

Once the cluster is set up, we utilize the fs utility under dbutils to mount the data from Azure Data Lake Storage Gen2 to the Databricks Workspace using a service principal. With the storage mounted on DBFS, we execute two levels of transformations.

The first transformation level, Bronze_to_Silver, focuses on changing the date format from datetime to date type. This transformation is applied across all tables and columns that contain date data. The transformed data is then moved to the silver container.

In the second transformation level, Silver_to_Gold, I change the column names to lowercase to ensure a consistent naming convention across the different tables. The transformed data is subsequently stored in separate folders within the gold container, each named according to the respective table.

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/b720dadd-5bcd-4638-9e7c-bdfcec851286)

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/ff08e6e0-32af-4505-a8b4-51e183b67514)

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/0586b5ae-4087-4e9c-927c-13bd4557e91d)

 - **Data Analytics** - Azure Synapse Analytics is a scalable, cloud-based data warehousing solution from Microsoft, representing the next iteration of Azure SQL Data Warehouse. It offers a unified environment by integrating SQL data warehousing, big data analytics capabilities with Spark, and data integration technologies, facilitating the movement of data between these components and external data sources. In this project, we are utilizing it for data warehousing and analytics purposes.

First, I created a linked service to connect my Azure Data Lake Storage (ADLS) Gen2 to my Synapse Workspace. Once this connection was established, I created a lake database using the files from the gold container in the ADLS Gen2 storage account.

After the database was set up, I wanted to conduct analytics on the clean data. To do this, I created an Apache Spark Pool, as a compute resource is required to run jobs or notebooks—this can be either a dedicated or serverless SQL pool or an Apache Spark Pool.

Next, I developed a notebook for KivaCrowdfundingAnalytics and performed a series of analytics and visualizations on the data stored in the gold container. It's essential to ensure that the necessary roles and permissions are granted to your Synapse Workspace, enabling it to access the storage account.

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/dba040fc-c628-4619-9d1c-b9bb28cb73f8)

 - **Data Visualisation** : This is the final step, where we create visualizations based on our gold layer data. By generating charts and graphs, we can help the business better understand the data, facilitating informed decision-making. We can create various types of graphs like bar chart, scatter plot, column chart, line chart, pie charts etc. using various tools. 

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/ad3170f3-a0e9-4744-800b-2d412e2f37e1)

# Data Architecture Flow Diagram

![image](https://github.com/gunjansingh21/ETL-Project-KivaCrowdfundingAnalytics/assets/29482753/dbe7cb4d-aca0-46ff-b1aa-ff6061625a51)

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
  
