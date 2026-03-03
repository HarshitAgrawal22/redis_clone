# Python Redis Clone

## Getting Started

### Start the Server

```bash
python -m python_redis.main
```

### Connect to the Server (TCP)

```bash
telnet localhost 12345
```

You can directly type commands in the TCP connection, and the output will be displayed in the terminal.

### Optional: Use socat for Better TCP Handling (Linux)

```bash
socat TCP4-LISTEN:12345,reuseaddr,fork TCP:172.25.128.1:5001,sourceport=40000
```

---

## About

This project is a Redis-like in-memory database implemented fully in Python.
It supports multiple advanced data structures with efficient algorithms and TCP-based client communication.

---

# Supported Data Structures

* HashMap
* Graph
* Binary Search Tree
* Queue
* List
* Stack
* Set

---

# HashMap

## Features

* Stores data in key-value format
* Supports object-like structured storage
* Field existence checks
* Supports increment, delete, length, and multiple field operations

## HashMap Commands

### 1. Set a Field-Value Pair

**Command**

```redis
HSET key value
```

**Example**

```redis
HSET name John
```

---

### 2. Set Multiple Field-Value Pairs

**Command**

```redis
HMSET field1 value1 field2 value2
```

**Example**

```redis
HMSET user harshit age 30 country USA
```

---

### 3. Get the Value of a Field

**Command**

```redis
HGET key
```

**Example**

```redis
HGET name
```

---

### 4. Get Multiple Field Values

**Command**

```redis
HMGET key field1 field2
```

**Example**

```redis
HMGET user name age
```

---

### 5. Set Multiple Fields and Values

**Command**

```redis
HSETM key1 value1 key2 value2
```

**Example**

```redis
HSETM name harshit age 20
```

---

### 6. Delete a Field

**Command**

```redis
HDEL key
```

**Example**

```redis
HDEL age
```

---

### 7. Get Number of Fields

**Command**

```redis
HLEN key
```

**Example**

```redis
HLEN user
```

---

### 8. Increment a Field Value

**Command**

```redis
HINCRBY key field increment
```

**Example**

```redis
HINCRBY user age 1
```

---

# Graph

## Features

* Directed and weighted graph
* BFS traversal
* DFS traversal
* Dijkstra shortest path algorithm
* Vertex data stored as dictionary

## Graph Commands

### 1. Add Vertex

```redis
gaddv name harshit age 20 sec k
```

---

### 2. Add Edge

```redis
gadde harshit tiwari 12
```

---

### 3. Get Vertex

```redis
ggetvv harshit
```

---

### 4. Remove Vertex

```redis
gremv harshit
```

---

### 5. Remove Edge

```redis
greme harshit tiwari
```

---

### 6. Breadth First Search

```redis
gbfs harshit
```

---

### 7. Depth First Search

```redis
gdfs harshit
```

---

### 8. Get Shortest Distance

```redis
gdijdis harshit
```

---

### 9. Get Shortest Path

```redis
gdijpa harshit tiwari
```

---

# Binary Search Tree

## Features

* Tree-based structured storage
* Key-based ordering
* Traversals supported
* Node deletion and insertion

## Tree Commands

### 1. Set Tree Key

```redis
tset name
```

---

### 2. Insert Node

```redis
tins name harshit sec k age 19
```

---

### 3. Delete Node

```redis
tdel harshit
```

---

### 4. Pre-Order Traversal

```redis
tpre
```

---

### 5. Post-Order Traversal

```redis
tpost
```

---

### 6. In-Order Traversal

```redis
tin
```

---

### 7. Display Tree

```redis
tshow
```

---

# Summary

This Redis clone provides efficient in-memory storage with support for multiple advanced data structures.

Key capabilities include:

* Fast key-value storage
* Graph traversal and shortest path algorithms
* Tree-based ordered storage
* TCP-based command interface
* Efficient Python implementation

---

# Author

Harshit Agrawal

---

# Summary
Redis is versatile and efficient for storing and accessing related fields, making them ideal for representing objects and managing small datasets. These commands provide robust functionality for CRUD operations and manipulation within hash data structures in Redis.
