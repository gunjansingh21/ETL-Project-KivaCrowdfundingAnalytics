# Databricks notebook source
configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "2d8731f9-36d2-4b82-b0ac-72ca4a2e8c24",
"fs.azure.account.oauth2.client.secret": 'K-n8Q~vRyh-1sUBK9Bq1rwNImMhjWxqRmuKdYbkO',
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/b46aa8e3-1d91-428a-b230-f35159b85f42/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://bronze@storagekivacrowdfunding.dfs.core.windows.net/",
  mount_point = "/mnt/bronze",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("/mnt/bronze")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "2d8731f9-36d2-4b82-b0ac-72ca4a2e8c24",
"fs.azure.account.oauth2.client.secret": 'K-n8Q~vRyh-1sUBK9Bq1rwNImMhjWxqRmuKdYbkO',
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/b46aa8e3-1d91-428a-b230-f35159b85f42/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://silver@storagekivacrowdfunding.dfs.core.windows.net/",
  mount_point = "/mnt/silver",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("/mnt/silver")

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
"fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
"fs.azure.account.oauth2.client.id": "2d8731f9-36d2-4b82-b0ac-72ca4a2e8c24",
"fs.azure.account.oauth2.client.secret": 'K-n8Q~vRyh-1sUBK9Bq1rwNImMhjWxqRmuKdYbkO',
"fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/b46aa8e3-1d91-428a-b230-f35159b85f42/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://gold@storagekivacrowdfunding.dfs.core.windows.net/",
  mount_point = "/mnt/gold",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("/mnt/gold")

# COMMAND ----------


