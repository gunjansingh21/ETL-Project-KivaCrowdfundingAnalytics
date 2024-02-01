# Databricks notebook source
dbutils.fs.ls("/mnt/silver")

# COMMAND ----------

table_name  = []
for i in dbutils.fs.ls('mnt/silver/'):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

print(table_name)

# COMMAND ----------

for name in table_name:
    input_path = '/mnt/silver/' + name  
    print(input_path)
    df = spark.read.format('csv').option('header', 'true').load(input_path)
    display(df)

# COMMAND ----------

for name in table_name:
    input_path = '/mnt/silver/' + name  
    print(input_path)
    df = spark.read.format('csv').option('header', 'true').load(input_path)

    # Get the list of column names
    column_names = df.columns

    for old_column_name in column_names:
        # Change the column names to lowercase
        new_column_name = old_column_name.lower()

        # Change the column name using withColumnRenamed
        df = df.withColumnRenamed(old_column_name, new_column_name)

    output_path = '/mnt/gold/' + name 
    df.repartition(1).write.format('csv').mode("overwrite").option('header', 'true').save(output_path)
    

# COMMAND ----------


