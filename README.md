# ETL-Project-KivaCrowdfundingAnalytics

Kiva is an online crowdfunding organization that offers loan services to underserved and unbanked populations worldwide. Some of the use cases of these loans include starting a business, paying school fees, and investing in farming. The datasets available at Kiva show the loans issued to borrowers between January 2014 and July 2017. This information will be valuable in defining some Key Performance Indicators (KPIs) to evaluate the organization’s performance over time. Kiva lenders have provided over 1 billion dollars in loans to over 2 million people. In order to set investment priorities, help inform lenders, and understand their target communities, knowing the level of poverty of each borrower is critical. However, this requires inference based on a limited set of information for each borrower.

# Data
The loan dataset provided by kiva contains a set of information for each loan application: dollar value of loan funded on Kiva.org; total dollar amount of loan; loan activity type; sector of loan activity as shown to lenders; country name; name of location within country; repayment interval, which is the frequency at which lenders are scheduled to receive installments, and loan theme, as well as Kiva’s estimates as to the various geolocations in which a loan theme has been offered. This data is in CSV format; hence, you need to load the data into the database for storage. I used the SQL server database as the data source for the project.

# Table of Contents
1. Introduction to Azure Services
2. Project Overview
3. Data Architecture Flow Diagram
4. Data Sources & Visualisations
5. Pre-Requisites

# Introduction to Azure Services (Step by Step)

- **Azure Data Factory**: Azure Data Factory (ADF) is a fully managed, serverless data integration solution for ingesting, preparing, and transforming all your data at scale. For this project, I was interested in creating a pipeline that would read all the tables in the SQL server and load them in Azure Data Lake Gen 2. I created three storage containers, (gold, silver, and bronze) where the bronze container will store the raw data as it was from the source. The silver container would contain data from level 1 transformation from the bronze container while the gold container would contain the cleaned and transformed data from the silver container. To create a pipeline to read all the tables in the database, I used the lookup activity to look up all the tables from the SQL database. In this lookup activity, I use a query to list the tables to ingest in Azure Data Lake Gen 2. Thereafter, I created a ForEach item in the pipeline to iterate from the Lookup activity to copy all the tables. The ForEach item would loop through all the tables and copy the items listed from the lookup table. Under the ForEach item, I created the Copy data item to copy data from the source. I configured the source of the data and the sink to save the data as CSV files. I also specified the path of the datasets so that each copied table would be stored separately in a folder and a path with the file name. Furthermore, the data ingestion pipeline was used to read and store the data from the SQL server to the bronze container, where the data was in the raw format. After the successful configuration of the pipeline, I ran using the debug option to test whether it was working without any errors. Besides, I used the add trigger option to run the pipeline and tested with the current time. Since the pipeline was meant to fetch the tables from the on-prem SQL server every time it runs, every successful run would overwrite the existing folder in the bronze container. At the end of the data ingestion, the data was now stored in the bronze container ready for transformation. 

- **Azure Data Lake Storage Gen2** : This is the storage account where we are storing the data coming from our sorce. The data ingested here is in raw format. Azure Data Lake Storage Gen2 provides a scalable and secure platform for storing large volumes of data. It enables us to manage, access. and analyze data effectively. We'll be storing the data in three layers.
   - BRONZE : This is where the raw format of the data will be stored
   - SILVER : This is where the data will be stored after first level of transformations.
   - GOLD : This is where the data will be stored after second level of transformations.

- **Azure Databricks**: Azure Databricks is a fast, scalable, and collaborative Apache Spark-based analytics platform provided by Microsoft Azure. It combines Apache Spark’s capabilities with the comfort and simplicity of a fully managed cloud service. For data transformation like changing or modifying the schema of the tables, changing and modifying few columns we have leveraged Azure Databricks with PySpark. But before that, we need to create a compute cluster to allow different jobs to run in the notebooks.After that, we used the fs utility under dbutils to mount the data from ADLS Gen2 to Databricks Workspace and after the storage mount  using service principal was done, we did two levels of transformations. I focused the first level of transformation on changing the date format from date-time to date type. At this level, I wanted the transformation to apply to all the tables and the columns of the date data type. The transformed data was then moved to the silver container. I performed another transformation from data in the silver container by changing the column names to lowercase. This transformation was to ensure there is a uniform naming convention for the data across the different tables. The transformed data was then stored in different folders in the gold container with respective table names. 

- **Azure Synapse Analytics** : We have used Azure Synapse Analytics to gain some valuable insights from the transformed data and performed some visualisations on top of the transformed data in gold container. We created a lake database by accessing the files on ADLS Gen2. Once the database was created, I then started a notebook to do visualisation and analytics on the tables and created some charts and graphs out of it.

- **Azure Key Valut** : We have used this service to maintain and keep our secrets encrypted. Azure Key Vault is a cloud service that provides a secure store for secrets. You can securely store keys, passwords, certificates, and other secrets. Azure key vaults are created and managed through the Azure portal. It is widely used for security management and data encryption.

# Project Overiew

- **Data Ingestion** - This is the first step in the project where we are ingesting the data from SQL Server DB and moving it to the Azure Data Lake Storage Gen2. The data ingestion process was carried out using Azure Data Factory. Use the lookup activity, for Each and copy activity under ADF and define your source and sink to carry out the data movement. You can monitor your pipeline runs for efficient copy. 



- **Data Storage** - This is the immediate step after data ingestion. We configured our sink as Azure Data Lake Storage Gen2 where the data will come and load into raw-data folder and the data will be in the exact same format as the source. There are three layers build on the storage account for this project - bronze layer that will contain the data in its raw format, silver layer that will have the transformed data like refining schema, removing null and duplicates, altering table structures etc. and gold layer that will store all the aggregated data that is built on our transformed data from the silver layer. 

![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/d7a0b572-0b28-4a50-877b-503fb15fdfe4)

- **Data Transformation** - After the preliminary data movement is done and we finally have the data on cloud, we move on to the next step of mounting the data and transforming and cleaning the data to make it more readable and structured. In this step, we are using Azure Databricks build on Apache Spark and we are using PySPark to write the transformations in the Notebook. We can then execute the Notebook that will automatically spin up the spark cluster and provide you the necessary compute to carry out your data transformations. But before transformations, make sure to provide necessary permissions for your Databricks workspace to connect with storage account (ADLS Gen2). 

![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/48bf9652-3ce3-486b-aaf5-838d2bf64232)

- **Data Analytics** - We are then using Azure Synapse Analytics for analytics. Here we create aggreagtions using SQL queries on the transformed data and store it in the gold layer. We are also creating external data sources, file formats and tables for querying the data to gain insights and understand patterns from the data. We can either do the analytics on Synapse using Synapse SQL or Apache Spark Pool. Make sure you provide the necessary roles and permissions to your Synapse workspace that it can access the storage account. 

![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/e06ed0e7-1966-4e7f-9751-41a82123067f)

- **Data Visualisation** : This is the last step where we are creating visualisations on top of our aggregated data. We create charts and graphs so that these visualisations can help business understand the data clearly and easily. It's an important step in making informed business decisions. We can create various types of graphs like bar chart, scatter plot, column chart, line chart, pie charts etc. using various tools. 

![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/27e09033-2f55-4445-9cc8-8a955377d2d8)

# Data Architecture Flow Diagram

![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/7cf41ae1-8d3a-4303-b9c0-ec7312314a50)

# Data Sources and Visualisations

Data Source
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/254341f1-f5e1-4dce-acb5-b7103c91a0ef)

Visualisation 1: **ageAnalysisOfAthletesbyDiscipline**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/2eabc000-3a4d-43ff-bca3-823b254f8e78)

Visualisation 2: **averageEntriesGenderbyDiscipline**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/80e39333-21c3-4926-870d-43c40b4d6a0b)

Visualisation 3: **coachWithMultipleEvents**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/c414c0e7-e9fa-44ba-9361-447760495255)

Visualisation 4: **performanceOfCountrybyOverallMedalsvsGoldMedals**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/519f8398-cae5-48f7-9dbb-4ca6273fb4e9)

Visualisation 5: **totalAthletesByCountry**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/5ab03752-b514-48d5-a737-9ec8e3c3565c)

Visualisation 6: **totalAthletesbyDiscipline**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/8800db4d-c202-48a7-9de2-5cda6a76dea3)

Visualisation 7: **totalMedalsbyCountry**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/4accaf0d-a189-4c6b-90a9-71f167291dba)

Visualisation 8: **genderDistributionDifferencebyDiscipline**
![image](https://github.com/gunjansingh21/ETL-Project-TokyoOlympicsData/assets/29482753/84b80ab5-1ace-4e84-a359-0c628e55eb9b)


# Pre-Requisites

1. You need to have an active Azure subscription to provision these required services.
2. You need to have an account on Azure Portal to access and manage these resources for your ETL project.
3. Make sure you have your source data sets ready and in place to start the project.
  
