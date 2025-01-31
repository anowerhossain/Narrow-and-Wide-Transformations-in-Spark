from pyspark.sql import SparkSession

# 🚀 Initialize Spark Session
spark = SparkSession.builder.appName("NarrowWideExample").getOrCreate()
sc = spark.sparkContext

# 🎯 Sample Data
data = [("Alice", 20), ("Bob", 30), ("Charlie", 25), ("David", 40)]
rdd = sc.parallelize(data)

# 🟢 Narrow Transformation: map() (Each element is processed independently)
mapped_rdd = rdd.map(lambda x: (x[0], x[1] + 5))  # Increase age by 5

# 🔵 Wide Transformation: groupByKey() (Data shuffling across partitions)
pair_rdd = mapped_rdd.map(lambda x: (x[1] % 2, x[0]))  # Group names by even/odd age
grouped_rdd = pair_rdd.groupByKey()

# 🔍 Collect Results
print("Mapped RDD (Narrow Transformation):")
print(mapped_rdd.collect())

print("\nGrouped RDD (Wide Transformation):")
print({key: list(value) for key, value in grouped_rdd.collect()})

# 🛑 Stop Spark Session
spark.stop()
