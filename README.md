## Narrow and Wide Transformations in Apache Spark 🚀
Understanding the difference helps in optimizing Spark applications.

### 🔹 Narrow Transformation

A narrow transformation occurs when each partition of the parent RDD is used by at most one partition of the child RDD. This means there is no shuffling of data across the nodes in the cluster. Examples: `map()`, `filter()`, `flatMap()`

### 🔹 Wide Transformation

A wide transformation occurs when data is shuffled across multiple partitions. This happens when data needs to be rearranged among the nodes. Examples: `groupByKey()`, `reduceByKey()`, `join()`, `distinct()`

### 📌 Narrow vs. Wide Transformations

| Transformation    | Type    | Description | Example Usage |
|------------------|---------|-------------|--------------|
| `map()`         |  Narrow | Transforms each element independently, without shuffling data. | `rdd.map(lambda x: x * 2)` |
| `filter()`      |  Narrow | Filters data without moving it across partitions. | `rdd.filter(lambda x: x > 10)` |
| `flatMap()`     |  Narrow | Similar to `map()`, but flattens the output. | `rdd.flatMap(lambda x: x.split(" "))` |
| `union()`       |  Narrow | Merges two RDDs without shuffling data. | `rdd1.union(rdd2)` |
| `coalesce()`    |  Narrow | Reduces partitions without shuffling. | `rdd.coalesce(2)` |
| `distinct()`    |  Wide | Requires shuffling to remove duplicate elements. | `rdd.distinct()` |
| `groupByKey()`  |  Wide | Shuffles all values for the same key to a single partition. | `rdd.groupByKey()` |
| `reduceByKey()` |  Wide | Reduces values within partitions before shuffling, optimizing performance. | `rdd.reduceByKey(lambda a, b: a + b)` |
| `sortByKey()`   |  Wide | Sorts data, requiring a full shuffle. | `rdd.sortByKey()` |
| `join()`        |  Wide | Requires shuffling to combine matching keys. | `rdd1.join(rdd2)` |
| `repartition()` |  Wide | Redistributes data across partitions, causing a shuffle. | `rdd.repartition(4)` |


### 🎯 Sample Data
```python
data = [("Alice", 25), ("Bob", 38), ("Charlie", 32), ("David", 40)]
rdd = sc.parallelize(data)
```

### 📌 Before map() (Original RDD)

Let's say we have an RDD with two partitions

| Partition 1         | Partition 2         |
|---------------------|---------------------|
| ("Alice", 25)       | ("Charlie", 32)     |
| ("Bob", 28)         | ("David", 40)       |



###  🟢 Narrow Transformation
```python
# Narrow Transformation: map() (Each element is processed independently)
mapped_rdd = rdd.map(lambda x: (x[0], x[1] + 5))  # Increase age by 5
```

📌 After map() (Transformed RDD, Still Two Partitions)

| Partition 1         | Partition 2         |
|---------------------|---------------------|
| ("Alice", 30)       | ("Charlie", 37)     |
| ("Bob", 33)         | ("David", 45)       |

✅ Notice: Each partition remains unchanged, and no data is moved!



### 📌 **Before `groupByKey()`**

| Partition 1                   | Partition 2                   |
|-------------------------------|-------------------------------|
| (0, "Alice") → Age 30 (Even)   | (1, "Charlie") → Age 37 (Odd) |
| (1, "Bob") → Age 33 (Odd)      | (0, "David") → Age 45 (Odd)   |


###  🔵 Wide Transformation
```python
# Wide Transformation: groupByKey() (Data shuffling across partitions)
pair_rdd = mapped_rdd.map(lambda x: (x[1] % 2, x[0]))  # Group names by even/odd age
grouped_rdd = pair_rdd.groupByKey()
```

### 📌 Step 3: After groupByKey() (Shuffling Happens!)

| Partition 1                         | Partition 2                            |
|-------------------------------------|----------------------------------------|
| (0, ["Alice"]) → (Even)             | (1, ["Charlie", "Bob", "David"]) → (Odd) |
| (0, ["David"]) → (Even)             |                                        |

🔥 Notice: Some values had to move across partitions, causing network communication and shuffling, which makes groupByKey() a wide transformation.



