# Databricks notebook source
dbutils.fs.ls("/mnt/bronze")

# COMMAND ----------

table_name  = []
for i in dbutils.fs.ls('dbfs:/mnt/bronze'):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

print(table_name)

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

for i in table_name:
    input_path = '/mnt/bronze/' + i 
    df = spark.read.format('csv').option('header', 'true').load(input_path)
    print(i)
    for col in df.columns:
        if "date" in col or "time" in col:
            df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

    output_path = '/mnt/silver/' + i 
    df.repartition(1).write.format('csv').mode("overwrite").option('header', 'true').save(output_path)

# COMMAND ----------

dbutils.fs.ls("/mnt/silver")
