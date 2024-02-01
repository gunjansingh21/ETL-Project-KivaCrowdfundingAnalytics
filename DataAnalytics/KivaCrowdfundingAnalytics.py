#!/usr/bin/env python
# coding: utf-8

# ## KivaCrowdfundingAnalytics
# 
# 
# 

# In[3]:


from pyspark.sql import SparkSession

#Initialize spark sessiom
spark = SparkSession.builder.appName('kivacrowdfunding').getOrCreate()


# In[4]:


#Loading the datasets

df_kiva_loans = spark.read.csv('abfss://gold@storagekivacrowdfunding.dfs.core.windows.net/kiva_loans/part-00000-tid-6896789896720136033-0c0a1f00-301f-4e4f-8851-5d30a26b11b8-93-1-c000.csv', header=True, inferSchema=True)
df_kiva_mpi = spark.read.csv('abfss://gold@storagekivacrowdfunding.dfs.core.windows.net/kiva_mpi_region_locations/part-00000-tid-1602687252335220343-b2e81bdb-0a75-4284-bd2c-f3672d5f0e39-96-1-c000.csv', header=True, inferSchema=True)
df_loan_region = spark.read.csv('abfss://gold@storagekivacrowdfunding.dfs.core.windows.net/loan_themes_by_region/part-00000-tid-579055140622907197-fe85b544-e89b-4579-983c-e8393667e82c-110-1-c000.csv', header=True, inferSchema=True)
df_loan_ids = spark.read.csv('abfss://gold@storagekivacrowdfunding.dfs.core.windows.net/loan_theme_ids/part-00000-tid-6739617069467121763-74bbbff7-d2c1-40d6-841d-7af4d7e973a5-105-1-c000.csv', header=True, inferSchema=True)


# In[5]:


display(df_kiva_loans)


# In[6]:


display(df_kiva_mpi)


# In[7]:


display(df_loan_ids)


# In[8]:


display(df_loan_region)


# **Let's get the information about the missing values and nulls**

# In[6]:


from pyspark.sql.functions import col

#Check null values
null_value = df_kiva_loans.select([col(c).alias(c) for c in 
df_kiva_loans.columns]).na.drop().count()

#Calculate percentage of null values
null_percentage = (null_value / df_kiva_loans.count()) * 100

#Displaying the results
null_per_df = spark.createDataFrame([(col_name, null_value, null_percentage)
for col_name in df_kiva_loans.columns],["Columns","NumberOfNullValues","PercentageOfNullValue"])

display(null_per_df)


# _So the data looks clean. As we have already done transformations on the data in the previous stages using Databricks._

# #### **LOAN ANALYSIS**

# <mark>**Top 10 Countires that got maximum number of times Loan.**</mark>

# In[19]:


from pyspark.sql import functions as F

#Counting the number of loans by country
loan_counts = df_kiva_loans.groupBy('country').count()

#Ordering the count and sort in descending order and selecting top 10
top_countries = loan_counts.orderBy(F.desc('count')).limit(10)

display(top_countries)


# <mark>**Top 10 Countries that got maximum amount of total loan**</mark>

# In[20]:


#Grouping by country and summing the funded amount
country_totals = df_kiva_loans.groupBy('country').agg(F.sum('funded_amount').alias('total_funded_amount'))

#Ordering the total_funded_amount and sort in descending order and selecting top 10
top_countries_totals = country_totals.orderBy(F.desc('total_funded_amount')).limit(10)

display(top_countries_totals)


# <mark>**Top 10 Sectors that got maximum amount of total loan**</mark>

# In[21]:


#Grouping by sector and summing the funded amount
sector_totals = df_kiva_loans.groupBy('country').agg(F.sum('funded_amount').alias('total_funded_amount'))

#Ordering the total_funded_amount and sort in descending order and selecting top 10
top_sectors_totals = sector_totals.orderBy(F.desc('total_funded_amount')).limit(10)

display(top_sectors_totals)


# <mark>**Top 10 Activity that got maximum amount of total loan**</mark>

# In[22]:


#Grouping by activity and summing the funded amount
activity_totals = df_kiva_loans.groupBy('activity').agg(F.sum('funded_amount').alias('total_funded_amount'))

#Ordering the total_funded_amount and sort in descending order and selecting top 10
top_activity_totals = activity_totals.orderBy(F.desc('total_funded_amount')).limit(10)

display(top_activity_totals)


# <mark>**Reypayment Interval of Loans**</mark>

# In[23]:


#Grouping by repayment intervals and counting the occurences
repayment_interval_counts = df_kiva_loans.groupBy('repayment_interval').count()

display(repayment_interval_counts)


# <mark>**Let's get information about the lender count**</mark>
# 
# lender count = number of lenders giving loan to a borrower

# In[8]:


#Filtering data for lender counts less than 200
lender_filtered = df_kiva_loans.filter(col('lender_count')<200)

display(lender_filtered)


# <mark>**Gender Distribution of Borrower.**</mark>

# In[13]:


from pyspark.sql import functions as F

#Extracting the borrowers gender and counting occurences
gender_counts = df_kiva_loans.select('borrower_genders').groupBy('borrower_genders').count()

#ordering the count in descending order and selecting top 2
top_gender_counts = gender_counts.orderBy(F.desc('count')).limit(2)

display(top_gender_counts)


# 1. Participation of females much higher than males.
# 2. Female with 76% and male with 24%

# <mark>**For which durations(month) maximum number of loans are there.**</mark>

# In[14]:


#Grouping by term_in_months and count the occurences
term_counts = df_kiva_loans.groupBy('term_in_months').count()

#Ordering by count in descending order and selecting top 10 
top_term_counts = term_counts.orderBy(F.desc('count')).limit(10)

display(top_term_counts)


# #### **MPI ANALYSIS**

# <mark>**Top 10 Countries with highest MPI (Multidimentional Poverty Index)**</mark>

# In[46]:


#Grouping by country and count the occurences
high_mpi_totals = df_kiva_mpi.groupBy('country').agg(F.sum('MPI').alias('highest_MPI'))

#Ordering by MPI in descending order and selecting top 10
highest_mpi = high_mpi_totals.orderBy(F.desc('highest_MPI')).limit(10)

display(highest_mpi)


# <mark>**Top 10 Countries with low MPI (Multidimentional Poverty Index)**</mark>

# In[47]:


#Grouping by country and count the occurences
lowest_mpi_totals = df_kiva_mpi.groupBy('country').agg(F.sum('MPI').alias('lowest_MPI'))


#Ordering by MPI in ascending order order and selecting the top 10
lowest_mpi = lowest_mpi_totals.filter(col('lowest_MPI').isNotNull()).orderBy('lowest_MPI').limit(10)

display(lowest_mpi)


# #### **INDIA AND IT'S NEIGHBOURS ANALYSIS**

# <mark>**Creating new DataFrame which only contains data of India and it's neighbour**</mark>

# In[61]:


#List of neighbouring countries
neighbour = ['India' ,'Pakistan', 'China', 'Nepal', 'Bangladesh', 'Bhutan', 'Myanmar (Burma)', 'Afghanistan', 'Sri Lanka' ]

#Filter the dataframe for the specified countries in the neighbours dataframe 
df_neighbours = df_kiva_loans.filter(col('country').isin(neighbour))

#Unique countries in the filtered dataframe
df_neighbours.select('country').distinct().show()

#Checking if SriLanka and Bangladesh are not there in the kiva's dataset
if not df_neighbours.filter((col('country') == 'Sri Lanka') | (col('country') == 'Bangladesh')).count():
    print("SriLanka and Bangladesh are not there in Kiva's dataset")


# <mark>**India's Loan distribution with neighbour countries.**</mark>

# In[69]:


#Filter the dataframe for the specified countries in the neighbours dataframe 
df_neighbours = df_kiva_loans.filter(col('country').isin(neighbour))
res = df_neighbours.select('country','funded_amount')

#Counting the number of loans by country
loan_counts_neighbours = df_neighbours.groupBy('country').count()

#Ordering the count and sort in descending order and selecting top 10
top_countries_neighbours = loan_counts_neighbours.orderBy(F.desc('count')).limit(10)

display(top_countries_neighbours)


# <mark>**Top 10 sectors that got maximum amount of loan in India.**</mark>

# In[ ]:


#Filter the dataframe for the specified countries in the neighbours dataframe 
df_neighbours = df_kiva_loans.filter(col('country').isin(neighbour))

tmpDf =  


# <mark>**Top 10 Activities that got maximum amount of loan in India.**</mark>

# <mark>**Top 10 Cities that got maximum amount of loan in India**</mark>

# <mark>**Number of Times Loans were given to India and its neighbour**</mark>
