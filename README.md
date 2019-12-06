# ElasticSearch-WordCloud
Course Project Of 数据库与数据仓库 Fudan University
### 数据库与数据仓库课程论文

### ElasticSearch

#### 基本介绍

Elasticsearch是建立在Apache Lucene这个开源的搜索引擎基础之上，一个实时分布式搜索引擎。更准确地来说，ElasticSearch的功能可以总结为：

- 一个分布式实时文档存储，每个字段都可以被索引与搜索
- 一个分布式实时分析搜索引擎
- 能够胜任上百个服务节点的扩展，支持PB级的结构化或者非结构化数据

#### 核心概念

- 索引 index

具有某些类似特征的文档集合，可以理解为关系型数据库中的一个数据库(database)

- 文档 document

文档是构建索引的基本单元，例如可以理解为关系型数据库中的一行数据

- 字段 field

相当于数据库中的字段，对文档数据根据不同属性进行分类标识

- 映射 mapping

mapping是对数据方式和规则方面做限制，按照最优规则处理数据对性能提高非常大。因此需要建立合适的映射

- 节点 node

一个节点就是集群中的一个服务器，提供存储数据，参与集群中的索引和搜搜功能。

- 集群 cluster

一个集群由一个或者多个节点组织而成，共同持有整个数据，一起提供索引和搜索功能。

- 分片 shard

考虑到索引对应的数据量可能会超出单个节点的硬件存储容量，因此可以把索引中的数据划分为多个分片(Shard) 每个分片放到不同的服务器上。当查询的索引分布在多个分片上的时候，es会把查询分发给每个相关的分片，然后把结果组合在一起返回给客户端。每一个分片实际上是Lucene的一个索引。

- 副本

es会为每个分片生成一个或者多个副本，存储在不同的服务器上，保证服务器的高可用。

#### 设计原理

Es之所以能实现非常高的搜索性能，个人从架构设计上总结出三个原因：使用倒排索引组织数据映射关系，充分利用内存缓存以减少磁盘IO与寻道次数以及使用高性能的压缩算法来压缩数据结构。

##### 倒排索引

是文档检索系统中常用的数据结构，对应着存储在全文中的某个单词以及包含这个单词的所有文档的映射关系。

具体到ElasticSearch的实现，倒排索引具体拆分为三个数据结构：Term Index， Term Dictionary 与 Posting List.



![在这里插入图片描述](https://img-blog.csdnimg.cn/20191111214940524.png)

- Term Dict 单词字典

存储着文档数据经过文法分析之后生成的单词，可以理解为单词的集合。每一个单词项都会有一个指针指向其对应的倒排列表。

- Posting List 倒排列表

记录了出现过的某个单词的所有文档的文档列表以及单词在该文档出现的位置信息，出现次数，偏移量等。每一条记录称为一个倒排项。

- Term Index 单词索引

类似于关系型数据库中的索引，把term组织成一个类前缀树结构的索引。term index会包括term的前缀，可以通过term index快速定位到单词字典的某个offset，然后就可以根据term dict的某一个term找到其对应的倒排列表，进而就会找到出现过搜索单词的所有文档ID列表。

![1575204702768](https://img-blog.csdnimg.cn/2019111122121176.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODQ5OTIxNQ==,size_16,color_FFFFFF,t_70)

##### 充分利用缓存

传统数据库的索引文件是放置在外存的，当发生缺失命中的时候，需要进行磁盘IO把外存上的索引节点加载到内存中。每一次加载都会涉及到一次操作系统中页置换操作，所以性能会受到严重影响。

而ElasticSearch通过使用高性能的压缩算法来对Term Index Tree来进行高效压缩，使其能够直接存储在内存中，极大地减少了磁盘IO与寻道次数，提高了效率。在下一小节中将会介绍如何压缩Term Index和Posting List

##### 压缩数据结构

- Finite State Transducer 

Lucene中使用FST来压缩Term Index,FST是一种变种的Trie树，

我们知道，Trie通过共享前缀来大大提高压缩的效率，而FST不仅实现了共享前缀，还实现了共享后缀，使得压缩索引的功能更加强大。

![1575206360572](https://img-blog.csdnimg.cn/20191111221549192.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODQ5OTIxNQ==,size_16,color_FFFFFF,t_70)

具体来说，FST可以把{mop, moth, pop, star, stop, top}压缩成如上图的带权重的状态机。那么每一条从初始态到终态的路径的权重和就是这个单词所对应在源列表中的序号。这种类状态机的结构以共享前后缀的方法极大地节省了存储字符串所需要的字节数目。

- 增量编码压缩

Es通过增量编码压缩的技巧对posting list进行压缩，核心思想是把大数变成小数，尽可能减少存储每个数字所花费的字节数，以下图为例：

![Alt text](https://img-blog.csdnimg.cn/2019111122390814.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODQ5OTIxNQ==,size_16,color_FFFFFF,t_70)



对于es来说，倒排列表所存储的文档必须是按序排列的。这也方便了我们提取文档id之间的增量关系，就以[73,300,302,332,343,372]文档ID列表来讲：

如果不做压缩，需要24bytes来存储这6个数据。增量压缩的步骤如下：

- Step1:提取出增量关系

73 227 2 30 11 29

这么做就是为了实现把大数变成小数，节省存储数字所需要的字节数

- Step2:分块存储

减轻对单个服务器存储的压力

- Step3:分配字节

对于[73 227 2]这一分块来说，存储最大所需要的位数为8(227至少需要8个bits来存储)

而对于[30 11 29]这一分块来说，存储最大所需要的位数为5(30至少需要5个bits来存储)

每一个分块还需要额外一个byte来说明这个分块的每个数字需要用多少个bit来存储。

因此最终通过增量压缩，就可以把24个bytes的数字压缩为7bytes。



#### 原生支持强大的地理查询能力

- geo_point

在logstash中增加下列转化规则：

```yaml
if [latitude] and [longitude] {
    mutate {
      add_field => {
        "coords" => ["%{longitude}", "%{latitude}"]
      }
    }

    mutate {
      convert => [ "coords", "float" ]
    }
```

Es会自动把float类型的coords转化为Es内置支持的geo_point数据结构。

结合geo_point数据结构，我们可以在Kibana可视化的地图模块进一步对数据进行有趣的探索：

#### ELK栈

除了ElasticSearch之外，本课程项目还使用了ElasticSearch生态中另外两个重要的开源组件：

- Logstash 

一个开源的数据收集引擎，具有实时数据传输的能力。可以统一过滤来自不同源的数据，并且按照开发者制定的规范来把数据输出到目的地。

本项目中，使用logstash接受来自源csv文件的输入，并且设定建立索引的规则以及进行冗余字段的删减，最后把数据实时传输到ElasticSearch中。

- Kibana

Kibana 是为 Elasticsearch设计的开源分析和可视化平台。你可以使用 Kibana 来搜索，查看存储在 Elasticsearch 索引中的数据并与之交互。你可以很容易实现高级的数据分析和可视化，以图标的形式展现出来。

#### 性能调优

所谓性能调优，实际上是对logstash写入es的性能以及es查询的性能的调优。

##### 建立索引调优

主要从建立索引的优化来分析核心思想是通过减少要分析以及存储的索引数量，删除冗余字段，进而减少不同分块之间进行传输的字节量，提高传输速度，从而提高搜寻效率。

- 把经纬度数据合并成es内置支持的数据结构geo_point，然后把荣誉的latitude,longitude 字段删除。
- 原本日期时间Date字段格式为“Year-Month-Day:00:00:00“，在进行日期数据格式转换的时候会生成一些中间无用的字段，也要把这些字段给删除掉。
- 不需要建立索引的，即**不参加检索，排序和聚合分析的**，需要在logstash直接声明，如剔除location,tags等冗余字段。
- 如果不需要分词的字段可以设为”not_analyzed”，可以减少es读写时候额外的资源开销。

##### 搭建集群

| 服务器 | ip          | 配置         |
| ------ | ----------- | ------------ |
| admin  | 172.101.8.2 | 8cpu 16G内存 |
| node1  | 172.101.8.3 | 8cpu 16G内存 |
| node2  | 172.101.8.4 | 8cpu 16G内存 |

admin: 作为Master Node协调分片的分发与路由，同时作为Data Node,存储分片Shared和Segment。

node1: 作为Data Node，存储分片Shared和Segment。

node2: 作为Data Node，存储分片Shared和Segment。

与单节点查询效率比较，理论上DataNode和MasterNode的分离能减轻单个datanode的分片存储与检索压力。

##### 增加文件句柄数

在“万物皆文件”的Linux中，每个进程默认打开的最大文件句柄数是1000,对于服务器进程来说，显然太小，通过修改/etc/security/limits.conf来增大打开最大句柄数.

```
* - nofile 65535
```

##### 性能对比

写入性能：

优化前logstash把大小为1.6G,含有700W行的csv数据写入到ES集群大概耗时45分钟，优化后耗时大概30分钟。

查询性能：

对同一查询语句：

```json
GET chicago_crime/crime/_search
{
    "query": {
        "bool": {
            "must": {
                "match_all" : {}
            },
            "filter": {
                "geo_bounding_box": {
                    "coords": {
                        "top_left": {
                            "lat": 41.8,
                            "lon": -88
                        },
                        "bottom_right": {
                            "lat": 41.75,
                            "lon": -87.5
                        }
                    }
                }
            }
        }
    }
}
```

性能优化前大概耗时30ms，优化后平均耗时19-30ms。

性能提高不算明显，经分析可能原因如下：

- 数据量不算特别大，差距不算特别明显，总数据量只有700W，每个分片占用内存大小大约为1G,与日常生产中分片大小10G~50G差距较大，因此性能提升不明显。
- 由于搭建了集群，分片路由过程中涉及到不同主机的网络传输。因此网络带宽可能是ElasitcSearch搜索的重要瓶颈。


### 可视化分析——Demo应用

#### 2001-2019各月度犯罪数量变化

![2001-2019各月度犯罪数量变化](https://github.com/AlexanderChiuluvB/ElasticSearch-WordCloud/blob/master/image/pic1.png?raw=true)

#### 所有犯罪类型犯罪数量随时间变化

![1](https://github.com/AlexanderChiuluvB/ElasticSearch-WordCloud/blob/master/image/%E5%9B%BE%E7%89%871.png?raw=true)

![2](https://github.com/AlexanderChiuluvB/ElasticSearch-WordCloud/blob/master/image/%E5%9B%BE%E7%89%872.png?raw=true)

#### 犯罪时间与犯罪类型关系图

![3](https://github.com/AlexanderChiuluvB/ElasticSearch-WordCloud/blob/master/image/%E5%9B%BE%E7%89%873.png?raw=true)

### ref

[FST原理介绍](<https://web.cs.ucdavis.edu/~rogaway/classes/120/spring13/eric-transducers.pdf>)
