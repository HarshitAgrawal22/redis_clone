
# Getting Started

Start Server by 
``` 
 python -m python_redis.main
```
Access the Server by tcp connection 

```
telnet localhost  12345
```
- the commands can be directly written on the tcp connection and the output will be  seen on the tcp terminal 

Mediator linux command for better use
``` 
 socat TCP4-LISTEN:12345,reuseaddr,fork TCP:172.25.128.1:5001,sourceport=40000
```
## About

This project is a clone of redis in memory database with a bit better algorithms fully implemented in python

## Data-Structures

### HashMap
  * stores data in key value pair format  
  * can store object data with all attributes
  * key can be checked if exists or not
  * have more features like len, incryby and hdel
  
### Redis HashMap Operations


- [1. Set a Field-Value Pair]()
- [2. Set Multiple Field-Value Pairs]()
- [3. Get the Value of a Field]()
- [3. Get Multiple Field Values]()
- [4. Get lenth of value of key]()
- [5. Delete a Field]()
- [6.  Get the Number of Fields]()
- [7. Set multiple attributes of a object]()- 
    



#### 1. Set a Field-Value Pair

* **Command**: `HSET key value`
* **Description**: Sets the specified  `key` to `value`. If the field already exists, it updates the value; otherwise, it creates the field.
* **Example**:

  ```redis
  HSET name John
  ```

#### 2. Set Multiple Field-Value Pairs

* **Command**: `HMSET field1 value1 field2 value2`
* **Description**: Sets multiple field-value pairs in the hash stored at key.
* **Example**:

   ```redis
   HMSET user harshit age 30 country USA
   ```

#### 3. Get the Value of a Field

* **Command**: HGET key field
* **Description**: Retrieves the value associated with the specified field in the hash stored at key.
* **Example**:

   ```redis
   HGET name
   ```

#### 3. Get Multiple Field Values

* **Command**: HMGET key field1 field2 ...
* **Description**: Retrieves the values associated with the specified fields in the hash stored at key.
* **Example**:
  
   ``` rediss
   HGETATTR user name age 
   ```

#### 4. Get All Fields and Values

* **Command**: HSETM key value key2 value2
* **Description**: Retrieves all fields and values in the hash stored at key.
* **Example**:
   ``` redis
   HSETM name harshit age 20
   ```

#### 5. Delete a Field

* **Command**: HDEL key 
* **Description**: Deletes one or more specified fields from the hash stored at key.
* **Example**:
  ```   redis
   HDEL age
   ```
  

#### 6.  Get the Number of Fields

* **Command**: HLEN key
* **Description**: Returns the number of fields in the hash stored at key.
* **Example**:
  ```    redis
    HLEN user
    ```

#### 7. Increment the Value of a Field (Integer)

* **Command**: HINCRBY key field increment
* **Description**: Increments the integer value of field by the specified increment. Useful for counters and numeric fields.
* **Example**:
   ``` redis
    HINCRBY user age 1
   ```


## Graph
  * stores data in a graph with vertex and edges  
  * graph is directed and weighted 
  * have more features like bfs, dfs and dijkistra 
  * data in each node is stored in dictionary format
  
### Redis Graph Operations

- [1. Add vertex to graph]()
- [2. Add edge to graph]()
- [3. Get vertex by value]()
- [3. Remove a vertex by value]()
- [4. Remove edge by vertex values]()
- [5. Get shortest distance between vertices by dijkista]()
- [6. Display graph]()
- [7. Get distance dict]()
- [8. Get previous dict]()
- [9. Get bfs of graph]()
- [10. Get dfs of graph]()
- [11. Get all edges of vertex]()
- [12. Get set-key]() 
   



#### 1. Beadth First Search 

* **Command**: `gbfs start-vertex`
* **Description**: Will start to traverse the graph in bfs format starting from given vertex 
* **Example**:

  ```redis
  gbfs start-vertex
  ```

#### 2.Depth First Search 


* **Command**: `gdfs starting-vertex`
* **Description**: Will start to traverse the graph in dfs format starting from given vertex 
* **Example**:

   ```redis
   gdfs starting-vertex
   ```

#### 3. Get the Vertex by value

* **Command**: ggetvv harshit
* **Description**: Retrieves the vertex by the value
* **Example**:

   ```redis
   ggetvv harshit
   ```

#### 3. Add Vertex to Graph

* **Command**: gaddv name harshit age 20 sec k 
* **Description**: Will add a new vertex to graph with this key-val pairs stored in a dictionary within the node
* **Example**:
  
   ``` rediss
   gaddv name harshit age 20 sec k 
   ```

#### 4. Add Edge to Graph

* **Command**: gadde harshit tiwari 12
* **Description**: Will add a edge between the nodes harshit and tiwari where harshit and tiwari are keys of nodes adn 12 is weight
* **Example**:
   ``` redis
   gadde harshit tiwari 12
   ```

#### 5. Delete a Vertex

* **Command**: gremv key
* **Description**: will delete the vertex with given key
* **Example**:
  ```   redis
   gremv harshit
   ```
   

#### 6.  Remove a Edge between two Vertices

* **Command**: greme v1 v2
* **Description**: Will remove the edge between the two given nodes
* **Example**:
  ```    redis
    greme harshit samosa
    ```

#### 7. Get shortest disance between two Vertices

* **Command**: gdijdis v1
* **Description**: will tell the shortest path length from given vertex to all other vertices
* **Example**:
   ``` redis
    gdijdis harshit tiwari
   ```
#### 8. Get shortest path between two Vertices

* **Command**: gdijpa v1 v2
* **Description**: will give shortest path and shortest dstance between both vertices
* **Example**:
   ``` redis
    gdispa samosa tiwari
   ```

### Binary Search Tree
  * stores data in a graph with vertex and edges  
  * graph is directed and weighted 
  * have more features like bfs, dfs and dijkistra 
  * data in each node is stored in dictionary format
  
### Redis Binary Search Tree Operations

   



#### 1. Insert Node

* **Command**: `tins key1 value1 key2 value2`
* **Description**: Will add create a new node and add that to tree with name as main key
* **Example**:

  ```redis
   tins name harshit sec k age 19  
  ```

#### 2 Set Key


* **Command**: `tset key`
* **Description**: will set tree key, according to this key the tree operations will be done 
* **Example**:

   ```redis
   tset name
   ```

#### 3. Delete Key

* **Command**: tdel key
* **Description**: will search and delete the node with given key
* **Example**:

   ```redis
   tdel samosa
   ```

#### 3. Pre-Traversal 

* **Command**: tpre
* **Description**:will return the pre trevarsal of tree
* **Example**:
  
   ``` rediss
   tpre
   ```

#### Post-traversal

* **Command**: tpost
* **Description**: Will return the post order traversal of tree
* **Example**:
   ``` redis
   tpost
   ```

#### 5. In Order Traversal

* **Command**:tin
* **Description**: will return the inorder traversal of tree
* **Example**:
  ```   redis
   tin
   ```
   

#### 6. Display Tree

* **Command**: tshow
* **Description**: Will display the whole tree on tcp connection
* **Example**:
  ```    redis
    tshow
    ```

    # Summary
    Redis is versatile and efficient for storing and accessing related fields, making them ideal for representing objects and managing small datasets. These commands provide robust functionality for CRUD operations and manipulation within hash data structures in Redis.