implemented code guidelines to prevent malicious timies
(multiple timmy(hacker)) to enter in my code

# Redis Hash Operations

1. [Set a Field-Value Pair](#1-set-a-field-value-pair)
2. [Set Multiple Field-Value Pairs](#2-set-multiple-field-value-pairs)
3. [Get the Value of a Field](#3-get-the-value-of-a-field)
4. [Get Multiple Field Values](#4-get-multiple-field-values)
5. [Get All Fields and Values](#5-get-all-fields-and-values)
6. [Get All Fields](#6-get-all-fields)
7. [Get All Values](#7-get-all-values)
8. [Check if a Field Exists](#8-check-if-a-field-exists)
9. [Delete a Field](#9-delete-a-field)
10. [Get the Number of Fields](#10-get-the-number-of-fields)
11. [Increment the Value of a Field (Integer)](#11-increment-the-value-of-a-field-integer)
12. [Increment the Value of a Field (Float)](#12-increment-the-value-of-a-field-float)
13. [Get the Length of a Field’s Value](#13-get-the-length-of-a-fields-value)
14. [Scan Fields and Values in Large Hashes](#14-scan-fields-and-values-in-large-hashes)

Redis hashes are used to store field-value pairs within a key, making them ideal for representing objects or collections of related attributes. Here are the primary operations you can perform on hashes in Redis:

## 1. Set a Field-Value Pair

- **Command**: `HSET key field value`
- **Description**: Sets the specified `field` in the hash stored at `key` to `value`. If the field already exists, it updates the value; otherwise, it creates the field.
- **Example**:
  ```redis
  HSET user:1000 name "John Doe"
  ```

2. Set Multiple Field-Value Pairs
   Command: HMSET key field1 value1 field2 value2 ...
   Description: Sets multiple field-value pairs in the hash stored at key.
   Example:
   redis
   Copy code
   HMSET user:1000 age 30 country "USA"
3. Get the Value of a Field
   Command: HGET key field
   Description: Retrieves the value associated with the specified field in the hash stored at key.
   Example:
   redis
   Copy code
   HGET user:1000 name
4. Get Multiple Field Values
   Command: HMGET key field1 field2 ...
   Description: Retrieves the values associated with the specified fields in the hash stored at key.
   Example:
   redis
   Copy code
   HMGET user:1000 name age
5. Get All Fields and Values
   Command: HGETALL key
   Description: Retrieves all fields and values in the hash stored at key.
   Example:
   redis
   Copy code
   HGETALL user:1000
6. Get All Fields
   Command: HKEYS key
   Description: Retrieves all field names in the hash stored at key.
   Example:
   redis
   Copy code
   HKEYS user:1000
7. Get All Values
   Command: HVALS key
   Description: Retrieves all values in the hash stored at key.
   Example:
   redis
   Copy code
   HVALS user:1000
8. Check if a Field Exists
   Command: HEXISTS key field
   Description: Checks if the specified field exists in the hash stored at key.
   Example:
   redis
   Copy code
   HEXISTS user:1000 age
   Output: Returns 1 if the field exists, 0 otherwise.
9. Delete a Field
   Command: HDEL key field [field ...]
   Description: Deletes one or more specified fields from the hash stored at key.
   Example:
   redis
   Copy code
   HDEL user:1000 age
   Output: Returns the number of fields removed.
10. Get the Number of Fields
    Command: HLEN key
    Description: Returns the number of fields in the hash stored at key.
    Example:
    redis
    Copy code
    HLEN user:1000
11. Increment the Value of a Field (Integer)
    Command: HINCRBY key field increment
    Description: Increments the integer value of field by the specified increment. Useful for counters and numeric fields.
    Example:
    redis
    Copy code
    HINCRBY user:1000 age 1
12. Increment the Value of a Field (Float)
    Command: HINCRBYFLOAT key field increment
    Description: Increments the floating-point value of field by the specified increment.
    Example:
    redis
    Copy code
    HINCRBYFLOAT user:1000 score 0.5
13. Get the Length of a Field’s Value
    Command: HSTRLEN key field
    Description: Returns the length of the value associated with the specified field in bytes (useful for string fields).
    Example:
    redis
    Copy code
    HSTRLEN user:1000 name
14. Scan Fields and Values in Large Hashes
    Command: HSCAN key cursor [MATCH pattern] [COUNT count]
    Description: Iterates over the fields in the hash, useful for handling large hashes without blocking the server. The command returns a new cursor and a subset of fields based on the specified pattern and count.
    Example:
    redis
    Copy code
    HSCAN user:1000 0 MATCH _name_ COUNT 10
    Summary
    Redis hashes are versatile and efficient for storing and accessing related fields, making them ideal for representing objects and managing small datasets. These commands provide robust functionality for CRUD operations and manipulation within hash data structures in Redis.
