摘要——芝加哥被称为“犯罪之城”，存在大量的犯罪事件，也即提供了大量的犯罪数据。基于这些犯罪数据，我们对比了关系型和非关系型数据库的存储性能和开销，并设计了有意义的功能：分析挖掘犯罪数据，可视化犯罪信息，并尝试进行大数据犯罪预测。本文从存储开销和存储性能（增，删，改，查）比较关系型数据库PostgreSQL和非关系型数据MongoDB,ElasticSearch。在两种非关系型数据库内部也进行比较，分析不同类型数据库适合的应用场景和功能实现，如ElasticSearch适合查询，插入删除不方便，可以考虑用ElasticSearch查询，和MongoDB同步，MongoDB负责插入删除。再由果溯因，从三种数据库的架构设计和底层源码分析入手，分析它们呈现出最终结果的内部原因。最后，选择组合合适的数据库来完成应用实例，做了基于地理信息的犯罪数据可视化分析，特定场景分析（校园枪击，家庭暴力，毒品，特朗普言论…，）热力统计图，词云分析，犯罪预测分析等数据挖掘的工作，以便更好地解读芝加哥的犯罪行为。本文提出的分析解读可以给芝加哥警方做一个参考。

关键词：ElasticSearch,PostgreSQL,MongoDB,犯罪

1.研究背景和意义
芝加哥被称为“犯罪之城”，存在大量的犯罪事件，也即提供了大量的犯罪数据。这一点有利于我们基于芝加哥市犯罪数据，对比关系型和非关系型数据库的存储性能和开销。同时，设计有意义的功能，做有意义的数据分析，更好的理解和预测犯罪事件，从而预防和避免犯罪事件给人们带来的伤害。通过数据可视化，作为社会治安的成果量化演示。
2.研究目标和研究内容
从存储开销和存储性能（增，删，改，查）比较关系型数据库和非关系型数据库。在两种非关系型数据库内部也进行比较，分析不同类型数据库适合的应用场景和功能实现。再由果溯因，从三种数据库的架构设计和底层源码分析入手，分析它们呈现出最终结果的内部原因。最后，选择，组合合适的数据库来完成应用实例，进行数据分析。
研究内容如下：
1）基于地理信息的犯罪数据可视化分析
2）可视化分析
3）特定场景分析（校园枪击，家庭暴力，毒品，特朗普言论…）
4）热力统计图
5）词云分析
6）犯罪预测分析
3.研究方法
3.1数据集
数据集是来源于芝加哥市政府提供的芝加哥市自2001年起至今的犯罪数据。数据大小共6.99GB，有6989573条记录。
每条记录共有22个属性，具体信息如下。
a) ID：记录的ID
b) Case Number：犯罪事件编号
c) Updated On：记录更新时间
时间方面：
d) Date：犯罪发生的具体时间
e) Year：犯罪发生的年份
犯罪类型方面：
f) IUCR：芝加哥市犯罪类型编码
g) Primary Type：犯罪类型
h) Description：犯罪类型的具体描述
i) FBI Code：NIBRS标准下的犯罪类型
地点方面：
j) Block：隐藏了部分信息的犯罪地点
k) Location Description：犯罪地点类型
l) X Coordinate：犯罪地点横坐标（基于state plane Illinois NAD 1983 projection的标准）
m) Y Coordinate：犯罪地点纵坐标
n) Latitude：犯罪地点纬度
o) Longtitude：犯罪地点经度
p) Location：犯罪地点经纬度坐标
管辖范围方面：
q) Beat：犯罪发生地所属的三级警区
r) District：犯罪发生地所属的一级警区
s) Ward：犯罪发生地所属的市议会区
t) Community Area：犯罪发生地所属的社区
其它方面：
u) Arrest：罪犯是否被逮捕
v) Domestic：犯罪是否为家庭犯罪
其中我们尤其感兴趣的有以下部分：
时间方面的属性可以用于演变分析芝加哥市犯罪情况；犯罪类型的演变是一个值得关注的问题；地点方面的属性可用于可视化分析；此外，家庭犯罪属性可以进行关联分析。
元数据描述如附录1。

3.2数据存储
3.2.1PostgreSQL
PostgreSQL是"世界上最先进的开源关系型数据库"。它支持的数据类型灵活多样，在管理大数据量方面有良好的可扩展性，其复杂的查询优化器，不同的索引手段都具有研究分析价值。此次，它经典完备的功能和结构良好的开源特性是我们选择它来完成性能的比较的原因。在后续的分析中，通过PostgreSQL更加便于通过研究代码层面的实现原理来解释所得到的实验结果。
3.2.2MongoDB
MongoDB 是一个基于分布式文件存储的、面向集合的、模式自由的文档型数据库。MongoDB是非关系数据库当中功能最丰富，最像关系数据库的。他支持的数据结构非常松散，是类似 json 的 bjson 格式，因此可以存储比较复杂的数据类型 。MongoDB最大的特点是他支持的查询语言强大，其语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库的增删改查的绝大部分功能，而且还支持对数据建立索引。
3.2.3Elasticsearch
Elasticsearch是建立在Apache Lucene这个开源的搜索引擎基础之上，一个实时分布式搜索引擎。更准确地来说，ElasticSearch的功能可以总结为：
一个分布式实时文档存储，每个字段都可以被索引与搜索
一个分布式实时分析搜索引擎
能够胜任上百个服务节点的扩展，支持PB级的结构化或者非结构化数据

3.3数据操作
由于数据集主要是用于分析，所以会产生频繁的查询和读取，也会不定期进行更新和追加形式的插入。我们将主要研究方向投入query操作，其次兼顾append和update操作。
3.3.1PostgreSQL
数据清洗：
由于数据集中仍存在着不少非结构化数据，而PostgreSQL是一个具有严格类型描述的数据库，所以对数据作出清洗和预处理是必要的。
首先，对于需要特别的关注的Location属性，我们在PostgreSQL中创建了一个新的数据类型Tuple用以表示二元组；
其次，对于应存放为时间戳类型的若干属性，我们利用python的pandas库，对其进行了格式重整，使其满足PostgreSQL要求。
import pandas as pd

reader2=pd.read_csv('CrimeRecord_0_unique.csv')
for i in range(len(reader2['Date'])):
    if reader2['Date'][i][20]=='P':
        tmp=(int(reader2['Date'][i][11:13])+12)%24
        tmpstr=str(tmp)
        reader2['Date'][i]= reader2['Date'][i][:11]+tmpstr+ reader2['Date'][i][13:]
    if reader2['Updated On'][i][20]=='P':
        tmp=int(reader2['Updated On'][i][11:13])+12 
        tmpstr=str(tmp)
        reader2['Updated On'][i]= reader2['Updated On'][i][:11]+tmpstr+ reader2['Updated On'][i][13:]
    reader2['Date'][i]=reader2['Date'][i][0:19]
    reader2['Updated On'][i]=reader2['Updated On'][i][0:19]

reader2.drop_duplicates().to_csv("CrimeRecord_0_final.csv",index=False)
最后，为了节约存储开销，我们删除了一些对分析没有帮助的属性，如X Coordinate和Y Coordinate；对于空值进行统一化NULL处理。
建立E-R图
在将数据导入关系型数据库之前，要对需求分析阶段收集到的数据进行分类、组织，确定实体、实体的属性、实体之间的联系类型，形成E-R图。为了简便起见，用字母来代表属性，可将完整的表抽象为R(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,R,S,T,U,V)，
图片: https://uploader.shimo.im/f/98Us3Z3qnY8FwsOC.jpg
转换为关系模式：由于关系型数据库对数据的准确性和可靠性的强要求，设计时为确保数据存储规范化，通常需要按照范式设计数据。针对关系模式R,把它分解成3NF，使它具有保持函数依赖性，并且保持无损。
首先，找出所有的函数依赖：
K→L(Beat→District)
E→F,G,O(IUCR→Primary Type, Description, FBI Code)
C→R(Date→Year)（考虑到没有必要为date和year单独建一张表，在3NF分解的时候可以不考虑这个函数依赖）
V→T,U,D(Location→Latitude, Longitude, Block)
之后，利用函数依赖进行3NF分解，结果如下：
R1={ID, Case Number, Date, IUCR, Location Description, Arrest, Domestic, Beat, Ward, Community Area, update},R2={Beat, District},R3={ IUCR, Primary Type, Description, FBI Code },R4={ Location,Latitude, Longitude, Block}
推导过程如下：
R(A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,R,S,T,U,V)
K→L(Beat→District)
E→F,G,O(IUCR→Primary Type, Description, FBI Code)
C→R(Date→Year) 
V→T,U,D(Location→Latitude, Longitude, Block)
Fc={ C→R, E→F,G,O, K→L, V→T,U,D}
1)     R1={C,R}, R2={ A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,S,T,U,V}
2)     R21={E,F,G,O}, R22={A,B,C,D,E,H,I,J,K,L,M,N,S,T,U,V}
3)     R221={K,L},R222={A,B,C,D,E,H,I,J,K,M,N,S,T,U,V}
4)     R22221={V,T,U,D}, R22222={ A,B,C,E,H,I,J,K,M,N,S,V}
∴3NF分解为：
R1={ A,B,C,E,H,I,J,K,M,N,S,V}，R2={K,L},R3={E,F,G,O},R4={C,R},R5={V,T,U,D}
考虑到现实意义，日期和年份的依赖关系没必要单独分出一个属性，∴得到初步的关系模式如下：
R1={ID, Case Number, Date, IUCR, Location Description, Arrest, Domestic, Beat, Ward, Community Area, update},R2={Beat, District},R3={ IUCR, Primary Type, Description, FBI Code },R4={ Location,Latitude, Longitude, Block}
其次，考虑到数据利用，我们在数据的物理存储方面做了如下设计：
定义location属性，longitude和latitude是两个double类型的数据，占16字节。如果用户在经纬度上建索引，系统不好实现，因此，不能删除这里的冗余数据。但是，将这两个很大的double变量放在主表里会影响效率，因为频繁的查询操作主要在主表上进行，或者需要和主表连接。而block属性也与地理位置信息有关，可以放到location表中，减轻主表。
把没有价值的重属性放在联系集，减轻主表。如将location_description放入联系集venue中而不是放到location表中，是因为location并不能唯一决定location_description（十年前后功能发生变化），并且考虑到抵消冗余存储location的代价，将location_description存到联系集venue中。
考虑到属性之间的相关性，可以把主表中的ward和community area放到联系集charge里。
最终得到的关系模式如下：
 
图片: https://uploader.shimo.im/f/aFFuq5IASLIx1Fyo.jpg
确立了关系模式之后，我们在PostgreSQL中建表存储，同时确认各个表之间的外码关系以及一致性约束。建表脚本如下。
create type tuple as (
	x double,
	y double
)；

create table CrimeRecord
(
	id bigint primary key,
	case_number varchar(20),
	date timestamp not null,
	arrest boolean not null,
	domestic boolean not null,
	year smallint not null,
	update_time timestamp not null,
);

create table CrimeLocation
(	location tuple primary key,
	latitude double not null,
	longtitude double not null,
	block varchar(30),	
);


create table venue
(
	id bigint primary key,
	location tuple not null,
	location_description text,
	constraint fk_venue_id foreign key (id) references CrimeRecord
	on delete cascade,
	constraint fk_venue_location foreign key (location) references CrimeLocation
	on delete cascade
	on update cascade,
)
create table CrimeType
(
	IUCR char(4) primary key,
	primary_type varchar(25) not null,
	description varchar(50),
	FBI_code varchar(4) not null
)
create table Classification
(
	id bigint primary key,
	IUCR char(4) not null,
	constraint fk_classification_id foreign key (id) references CrimeRecord
	on delete cascade
	on update cascade,
	constraint fk_classification_IUCR foreign key (IUCR) references CrimeType
	on delete cascade
	on update cascade,
)
create table Police
(
	beat integer primary key,
	district integer,
)
create table Charge
(
	id bigint primary key,
	beat integer not null,
	community smallint,
	ward smallint not null,
	constraint fk_charge_id key (id) references CrimeRecord
	on delete cascade
	on update cascade,
	constraint fk_charge_beat foreign key (beat) references Police
	on delete cascade
	on update cascade,
);
CREATE INDEX ON  CrimeType(primary_type); 
CREATE INDEX ON  Venue(location); 
CREATE INDEX ON  CrimeRecord(domestic); 
利用以下测试样例进行性能测试：
use [Crimes-2001_to_present];
select year,sum(arrest) as arrest_count,sum(domestic) as domestic_count
from CrimeRecord
where year between 2007 and 2017
group by year;

select distinct block, location, date, arrest
from CrimeLocation natural join venue natural join CrimeRecord 
where location.x between 20 and 60 and location.y between -90 and -70;

select year, sum(domestic) 
from CrimeLocation natural join venue natural join CrimeRecord 
where location.x between 20 and 60 and location.y between -90 and -70
group by year;

select primary_type, count(id)
from CrimeType natural join Classification natural join CrimeRecord
where year between 2014 and 2019
group by primary_type;

select district, count(id)
from Police natural join Charge natural join CrimeRecord
where year between 2014 and 2019
group by district;
结果如下：
图片: https://uploader.shimo.im/f/5OoCNBDdyPMwv3rW.jpg
3.3.2Elasticsearch
Elasticsearch 的请求。任何查询，插入，删除操作都需要向ElasticSearch的服务器发起json格式的RESTful 风格请求。
查询操作：
把查询具体Json格式传入"query"参数，这里以统计左上角(-88,41.8)，右下角(-87.5,41.75)的矩形内的犯罪情况为例。
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
插入操作
在ElasticSearch中，文档是不可改变的，不能修改，因此要更新或者插入新文档，必须通过PUT操作把整个文档传上去。
PUT chicago_crime/crime/doc_1
{
    "_index": "chicago_crime",
    "_type": "crime",
    "_id": "doc_1",
}
删除操作
DELETE chicago_crime/crime/doc_1
{
    "_index": "chicago_crime",
    "_type": "crime",
    "_id": "doc_1",
}
Es不适合大量增删改的业务场景，其本质还是一个搜索引擎，适合大量查询的操作的业务场景。
另外，Es原生支持强大的地理查询能力
geo_point
Geo_point是Es原生支持的地理数据结构之一。允许你找到距离另一个坐标点一定范围内的坐标点、计算出两点之间的距离来排序或进行相关性打分、或者聚合到显示在地图上的一个网格。
我们使用logstash把csv文件导入到数据库的时候，可以增添下列转化规则
if [latitude] and [longitude] {
    mutate {
      add_field => {
        "coords" => ["%{longitude}", "%{latitude}"]
      }
    }

    mutate {
      convert => [ "coords", "float" ]
    }
Es会自动把float类型的coords转化为Es内置支持的geo_point数据结构。
结合geo_point数据结构，我们可以在Kibana可视化的地图模块进一步对数据进行有趣的探索。
具体数据操作
1.基于Docker启动Kibana 6.5.3与ElasticSearch 6.5.3
2.编写logstash.conf，负责把csv源文件按照指定的索引组织方式写入ElasticSearch
主要从建立索引的优化来分析核心思想是通过减少要分析以及存储的索引数量，删除冗余字段，进而减少不同分块之间进行传输的字节量，提高传输速度，从而提高搜寻效率。
把经纬度数据合并成es内置支持的数据结构geo_point，然后把荣誉的latitude,longitude 字段删除。
原本日期时间Date字段格式为“Year-Month-Day:00:00:00“，在进行日期数据格式转换的时候会生成一些中间无用的字段，也要把这些字段给删除掉。
不需要建立索引的，即不参加检索，排序和聚合分析的，需要在logstash直接声明，如剔除location,tags等冗余字段。
如果不需要分词的字段可以设为”not_analyzed”，可以减少es读写时候额外的资源开销。
input {
  	stdin {}
}
filter {
	csv {
		columns => ["id","case_number","date","block","iucr","primary_type","description","location_description","arrest","domestic","beat","district","ward","community_area","fbi_code","x_coord","y_coord","year","updated_on","latitude","longitude","location"]
	}
  # Perform lookup against mapping file to get community names
  translate {

    field => "community_area”
    destination => "community_area_name"

  }
  # Perform lookup against mapping file to get names of current aldermen

  translate {

    field => "ward"

    dictionary_path => "/Users/peter/source/chicago_crime_2/wards.yml"

    destination => "ward_alderman"
  }
	if [latitude] and [longitude] {
    mutate {
      add_field => {
        "coords" => ["%{longitude}", "%{latitude}"]
      }
    }
    mutate {
      convert => [ "coords", "float" ]
    }
	}
  grok {

    match => { "date" => "%{DATE_US:date_part} %{HOUR:hour_part}:%{MINUTE:min_part}:%{SECOND:sec_part} (?<ampm_part>AM|PM)" }

  }
	date {
		match => [ "date", "MM/dd/YYYY hh:mm:ss aa"]
		timezone => "America/Chicago“
	}
  # adjust for invalid times during DST transition
  if "_dateparsefailure" in [tags] and [hour_part] == "02" and [ampm_part] == "AM" {
    mutate {
      replace => ["hour_part", "03"]
    }
    mutate {
      replace => ["date", "%{date_part} %{hour_part}:%{min_part}:%{sec_part} %{ampm_part}"]
    }
    mutate {
      remove_field => ["tags"]
    }
    date {
  		match => [ "date", "MM/dd/YYYY hh:mm:ss aa"]
  		timezone => "America/Chicago"
  	}
  }
  # remove unnecessary fields
	mutate {
		remove_field => ["latitude", "longitude", "location", "message", "hour_part", "date_part", "min_part", "sec_part", "ampm_part", "x_coord", "y_coord"]
	}
}
output {
	# stdout { codec => rubydebug }
	stdout { codec => dots }
	elasticsearch {
		protocol => http
		host => "localhost"
		index => "chicago_crime"
    document_type => "crime"
    template => "index_template.json"
    template_name => "chicrime"
    template_overwrite => true
	}
}
3.执行，未优化前耗时约45分钟把700W数据写入Es的分片中。
~/elk/logstash-6.5.3/bin/logstash -f logstash.conf < Crimes_-_2001_to_present.csv

3.4性能比较
（给出比较思路）
比较三者在存储开销，增、删、改、查上的性能差异，并从内部架构设计上分析原因。
本节中，我们将从三种数据库的架构设计和底层源码分析入手，给出它们的性能比较分析。
3.4.1 存储开销性能差异
PostgreSQL：
在PostgreSQL中，数据库在建立之后，除了在内存系统表中注册相关信息，还要为每一个表空间创建目录。PostgreSQL中的表空间是指在逻辑上相关的一组对象，用户可以通过控制表空间的位置来决定数据库的各种对象在集群文件系统的布局。每个数据库在一个表空间目录中，以文件形式定义。每个表和索引都存储在独立的文件里。
PostgreSQL中，磁盘I/O的基本单位是页，数据文件被切分的基本单位也是页，页的大小默认为8KB。页分两种类型，一种是数据页面用来存储和用户数据，另一种是控制页面负责管理用户数据。页也是数据库共享缓存中的空间划分的基本单位，这样整页读取数据文件,并读取数据到Buffer中，从Buffer写入数据文件变得非常方便，无需在内存和外存的两种粒度之间缓冲，同时保证了缓存与数据文件结构上的一致性。
虽然磁盘I/O的基本单位是页，但是PostgreSQL数据文件分配和释放的基本单位要比页大，称为区。数据文件中8个连续的Page构成的空间称为一个区。每个表、索引、序列对象等都是由若干个区组成。数据文件被创建后，除自动保留部分控制区外，其他区全部处于未分配状态。当向这些区中插入数据时，若该区已满，系统就会在所属表空间中寻找一个尚未分配的区，并将其状态修改为数据区。
在页内部，除了页的头部描述了一些页的元数据和一些保留空间外，实体数据结构分成两个部分，由低文件偏移量向高文件偏移量增长的数据描述信息（偏移量加大小）和由高文件偏移量向低文件偏移量增长的实际数据。PostgreSQL采取传统行存储模式，会为每个记录的每个属性存放大小和位置，造成相当的空间浪费，优点是对于不同数据类型的灵活性较大。
PostgreSQL空间管理需要一些管理页面，这些管理页面对于PostgreSQL的存储和查询性能也有很大影响。
Page Free Space，即PFS页。用于记录本数据文件中页面的空间使用情况。为每个页面分配一个字节，用"ByteMap"结构管理数据文件中的页面。PFS页每隔8128个页面出现一次。
Global Allocation Map，即GAM页。用于记录所在数据文件的区的分配情况，为每个区分配一个比特，用"BitMap"结构管理数据文件中的分区。为1表示所关联的区已被分配出去，反之未被分配。GAM页每隔881288个页面出现一个。
Index Allocation Map，即IAM页。每个IAM页只隶属于一个数据库对象(例如:表)，但一个数据库对象可包含多个IAM页。IAM的结构与GAM页类似，除IAM头外，剩下空间的每一个比特均对应着一个与IAM相关的Extent。为1表示所关联的区已被分配给该IAM,反之未被分配。与GAM不同，IAM的出现位置不固定，只在在创建数据库对象的时候才分配。
根据以上分析，可以得到
PostgreSQL存储结构较为整齐，控制文件较少，空间利用甚至优于Linux文件系统等文件系统。本数据集均为结构化数据，有明确的数据类型和一定的长度上限，在关系型数据库中存储可以更好地利用空间。
我们的关系模式中，采用了3NF范式，表之间存在一定量的冗余存储，但是全部存于一整张表会导致查询性能减弱。在查询性能和存储开销之间有一定权衡。在本文的应用场景中，我们尽量使得查询性能更加优良，所以牺牲了相当一部分存储空间。如果追求极致的低存储开销，还可以通过减少表之间的冗余信息做到更少的空间占用。
ElasticSearch：
Es之所以能实现非常高的搜索与高效地压缩性能，从架构设计上总结出三个原因：使用倒排索引组织数据映射关系，充分利用内存缓存以减少磁盘IO与寻道次数以及使用高性能的压缩算法来压缩数据结构。
倒排索引
是文档检索系统中常用的数据结构，对应着存储在全文中的某个单词以及包含这个单词的所有文档的映射关系。
具体到ElasticSearch的实现，倒排索引具体拆分为三个数据结构：Term Index， Term Dictionary 与 Posting List.
图片: https://uploader.shimo.im/f/uYXgAN3jFfQ9EBUZ.png
Term Dict 单词字典
存储着文档数据经过文法分析之后生成的单词，可以理解为单词的集合。每一个单词项都会有一个指针指向其对应的倒排列表。
Posting List 倒排列表
记录了出现过的某个单词的所有文档的文档列表以及单词在该文档出现的位置信息，出现次数，偏移量等。每一条记录称为一个倒排项。
Term Index 单词索引
类似于关系型数据库中的索引，把term组织成一个类前缀树结构的索引。term index会包括term的前缀，可以通过term index快速定位到单词字典的某个offset，然后就可以根据term dict的某一个term找到其对应的倒排列表，进而就会找到出现过搜索单词的所有文档ID列表。
图片: https://uploader.shimo.im/f/uDlJ9F9gJAIM8cT3.png
充分利用内存
传统数据库的索引文件是放置在外存的，当发生缺失命中的时候，需要进行磁盘IO把外存上的索引节点加载到内存中。每一次加载都会涉及到一次操作系统中页置换操作，所以性能会受到严重影响。
而ElasticSearch通过使用高性能的压缩算法来对Term Index Tree来进行高效压缩，使其能够直接存储在内存中，极大地减少了磁盘IO与寻道次数，提高了效率。在下一小节中将会介绍如何压缩Term Index和Posting List
压缩数据结构
Finite State Transducer
Lucene中使用FST来压缩Term Index,FST是一种变种的Trie树，
我们知道，Trie通过共享前缀来大大提高压缩的效率，而FST不仅实现了共享前缀，还实现了共享后缀，使得压缩索引的功能更加强大。
图片: https://uploader.shimo.im/f/mV4Y9ymJbYw6NuCr.png

具体来说，FST可以把{mop, moth, pop, star, stop, top}压缩成如上图的带权重的状态机。那么每一条从初始态到终态的路径的权重和就是这个单词所对应在源列表中的序号。这种类状态机的结构以共享前后缀的方法极大地节省了存储字符串所需要的字节数目。
增量编码压缩
Es通过增量编码压缩的技巧对posting list进行压缩，核心思想是把大数变成小数，尽可能减少存储每个数字所花费的字节数，以下图为例：
图片: https://uploader.shimo.im/f/w0qymc1yz8g4tmPp.png

对于es来说，倒排列表所存储的文档必须是按序排列的。这也方便了我们提取文档id之间的增量关系，就以[73,300,302,332,343,372]文档ID列表来讲：
如果不做压缩，需要24bytes来存储这6个数据。增量压缩的步骤如下：
Step1:提取出增量关系
73 227 2 30 11 29
这么做就是为了实现把大数变成小数，节省存储数字所需要的字节数
Step2:分块存储
减轻对单个服务器存储的压力
Step3:分配字节
对于[73 227 2]这一分块来说，存储最大所需要的位数为8(227至少需要8个bits来存储)
而对于[30 11 29]这一分块来说，存储最大所需要的位数为5(30至少需要5个bits来存储)
每一个分块还需要额外一个byte来说明这个分块的每个数字需要用多少个bit来存储。
因此最终通过增量压缩，就可以把24个bytes的数字压缩为7bytes。

综上所述，我们可以在理论上分析得到PostgreSQL存储的文本索引相关信息更少，在存储方面的开销会更少。

3.4.2 查询性能差异
PostgreSQL查询流程分析：
概览：
图片: https://uploader.shimo.im/f/9pwGhTJEh649YYbR.png
第一阶段：生成计划树
这一阶段的目标是读取SQL语句，生成计划树。
语法分析，生成语法树（SQL语句理解部分）
parsetree_list = pg_parse_query(query_string);
这里产生的语法树是粗糙的，没有经过任何优化的，直接由SQL语句拆解得到的，直接使用性能不高。下图以一个简单的SQL查询为例，便于解释每一步的执行结果。
图片: https://uploader.shimo.im/f/e8nxCxyzEYMvfJeV.png
语义分析与计划树重写
querytree_list = pg_analyze_and_rewrite(parsetree, query_string, NULL, 0, NULL);
在这一步中，针对上一轮产生的语法树进行重构，达成对各个子模块的写入，将SQL写入数据库内部的数据结构。注意这一步涉及语法的检验，也可能对相应的表项上锁。
图片: https://uploader.shimo.im/f/mJ749FN413MenUf4.png
生成查询计划树
plantree_list = pg_plan_queries(querytree_list,CURSOR_OPT_PARALLEL_OK, NULL);
这一步同样依赖于前一步生成的计划树，并将其进一步重构，通过各种策略，例如将投影操作和选择操作前置，将连接操作、扫描操作、排序操作等滞后来达成执行的优化。应该注意到，在PostgreSQL中，各个进程可以看做是一个同步的分布式系统，时钟漂移律、进程每一步的执行最大时延和进程间通信时延都有一个上限。因此执行Query Optimization的时长可以控制在一定的范围内，通过上述的各种数据文件的控制信息，可以近似估算出进行各步操作的时长，进而得到一个较优解。注意，这里得到的只是一个较优解，未必是最优解。计算最优解的代价可能要超出预想的时间范围，那时得到一个最优解的意义就不大了。
与之相对应，在下文中提到的非关系型分布式部署的数据库中，难以进行如此细致的，意义非凡的查询优化，其原因在于存储方式和异步的部署结构使得性能优化的代价上升，并且异步通信的方式会使得优化结果存在很大的不可能性，尤其在对事物的支持和一致性的维护上，使得优化算法的开销变得难以接受。并且，非关系型数据库大部分不是原生支持SQL的，即使可以支持也是通过算法间接支持。综上所述，PostgreSQL作为传统的关系型数据库，对SQL的查询优化达到了一个较为纯熟的阶段；非关系型数据库虽不擅于对SQL进行查询优化，但在其它方面的改进和崭新的理念在特定场景下甚至可以使得其查询性能超过关系型数据库。

第二阶段：Portal准备
这一阶段的目标是准备一个Portal，规范执行，与我们的分析目标关系不大，将简要分析。
Portal创建
创建一个Portal，分配内存，设置内存上下文，资源跟踪器清理函数，但是sourceText, stmts字段还未设置。
为Portal赋予计划树
为刚刚创建的Portal设置sourceText，stmt等，并且设置Portal的状态为PORTAL_DEFINED。
启动Portal，开始执行
Portal策略选择，根据需求，此处会选PORTAL_ONE_SELECT：处理单个的SELECT语句，调用Executor模块。之后调用CreateQueryDesc为Portal创建查询描述符。

第三阶段：查询执行
Execprocnode准备
PostgreSQL执行由执行节点来完成，ExecutorRun()函数调用ExecutePlan(),使得portal执行计划中的各个原子操作可以通过执行节点中的功能函数完成。
ExecInitIndexScan扫描初始化
由于我们的应用目标上可以认为是拥有索引的，范围查询最重要的是Scan:遍历搜索操作，所以功能函数定位为ExecIndexScan。ExecInitIndexScan函数构造数据结构，分配内存，为功能函数执行作准备。

第四阶段：Scan操作
PostgreSQL中，任何方式的Scan都要通过Execscan()函数封装结果。Execscan()函数不断通过PlanState中规定的功能函数Fetch新的tuple，然后检验其是否符合条件标准。顺序扫描与索引扫描类似，复用了大部分代码，省去了索引查找的环节。下面将以索引扫描为例分析。

索引数据读取
这一部分代码从B+树索引中获取数据信息；
IndexNext()->

index_getnext_slot()->

index_fetch_heap()->

table_index_fetch_tuple()
谓词判断
取回数据后，将检验其是否满足谓词判断条件；
Recheck and Fetch Data
ExecReScanIndexScan()函数负责返回索引所关联的表fetch最终结果。


Elasticsearch
ElasticSearch 执行分布式检索过程分析：
查询阶段
在初始查询阶段时， 查询会广播到索引中每一个分片拷贝（主分片或者副本分片）。 每个分片在本地执行搜索并构建一个匹配文档的优先队列。一个优先队列仅仅是一个存有 top-n 匹配文档的有序列表。
图片: https://uploader.shimo.im/f/iJz0tm6fri4sYhoJ.png

以上图为例，查询阶段包含以下三个步骤:
客户端发送一个 search 请求到 Node 3 ， Node 3 会创建一个大小为 from + size 的空优先队列。
Node 3 将查询请求转发到索引的每个主分片或副本分片中。每个分片在本地执行查询并添加结果到大小为 from + size 的本地有序优先队列中。
每个分片返回各自优先队列中所有文档的 ID 和排序值给协调节点，也就是 Node 3 ，它合并这些值到自己的优先队列中来产生一个全局排序后的结果列表。
当一个搜索请求被发送到某个节点时，这个节点就变成了协调节点。 这个节点的任务是广播查询请求到所有相关分片并将它们的响应整合成全局排序后的结果集合，这个结果集合会返回给客户端。
第一步是广播请求到索引中每一个节点的分片拷贝。查询请求可以被某个主分片或某个副本分片处理， 这就是为什么更多的副本（当结合更多的硬件）能够增加搜索吞吐率。 协调节点将在之后的请求中轮询所有的分片拷贝来分摊负载。
每个分片在本地执行查询请求并且创建一个长度为 from + size 的优先队列—也就是说，每个分片创建的结果集足够大，均可以满足全局的搜索请求。 分片返回一个轻量级的结果列表到协调节点，它仅包含文档 ID 集合以及任何排序需要用到的值，例如 _score 。
一个索引可以由一个或几个主分片组成， 所以一个针对单个索引的搜索请求需要能够把来自多个分片的结果组合起来。协调节点将这些分片级的结果合并到自己的有序优先队列里，它代表了全局排序结果集合。至此查询过程结束。
取回阶段

图片: https://uploader.shimo.im/f/1JSA79Bizpkk1fpI.png

分布式取回阶段由以下步骤构成：
协调节点辨别出哪些文档需要被取回并向相关的分片提交多个 GET 请求。
每个分片加载并丰富文档，如果有需要的话，接着返回文档给协调节点。
一旦所有的文档都被取回了，协调节点返回结果给客户端。

经过以上分析，可以看出ElasticSearch进行查询时磁盘I/O次数更少，查询机制效率更高。

3.4.3 记录修改性能差异
PostgreSQL有一定缓存机制，具体说就是“预测读，延迟写”。对于数据库的修改，会把重量级的I/O操作推迟写入，仅在逻辑上更新就返回客户端，因此效率非常高。对于建立索引的记录，要先在B+树上进行调整，然后在数据文件中做出修改。在数据文件上的修改，也是延迟的。会先令相应指针作废，在合适的机会再压缩数据文件。
另外，延迟写不意味着延迟保护。PostgreSQL会同步执行数据库的一致性检查。例如，插入时，数据库会检查重复元组和函数依赖，确保数据的一致性和完整性得到满足。如果要求严格的完整性约束，可以增加触发器进行级联更新。
MongoDB作为非关系型数据库，数据更新效率不如PostgreSQL。
插入方面：MongoDB会直接将插入数据放在集合（相当于关系型数据库中的表）的末尾，不会去集合的中间部分添加一条数据。MongoDB的插入与更新和删除一样，在建立索引后进行数据的插入有可能反而使耗费的时间增加，因为需要对新增的数据建立索引。但是，建立索引后耗时更多的原因是更新数据时需要将数据对应的索引也更新，而且需要更新的数据越多，代价就越高。
删除方面：建立索引前，MongoDB要找到一条数据需要遍历集合，因此删除的速度与被删除数据在集合中所处的位置有关；建立索引后，MongoDB可以根据索引快速找到需要删除的数据，但也会增加删除索引的代价。因此在某些情况下也可能出现建立索引前删除比建立索引后删除更快的情况。

4.实验结果及分析
4.1 测试方案
MongoDB与ElasticSearch的同步
通过实验，我们发现ElasticSearch在数据查询方面拥有postgreSQL和MongoDB望尘莫及的优势，但ElasticSearch的增删改操作却相当复杂，因此我们想要将ElasticSearch作为一个专门的搜索引擎，而对数据的增删改使用另外两个数据库。因为postgreSQL是一个关系型数据库，数据的组织形式和ElasticSearch不一样，因此最后我们决定实现MongoDB和ElasticSearch的同步。
同步使用的工具是mongo-connector。mongo-connector是基于python开发的实时同步服务工具，该工具会创建一个从MongoDB簇到ElasticSearch系统的管道，在MongoDB和ElasticSearch之间同步数据，并跟踪MongoDB的操作日志，保持操作与MongoDB的实时同步。
ElasticSearch+Kibana+Logstash ：皆基于Docker，版本号皆为6.5.3
PostgreSQL12.1.3
admin: 作为Master Node协调分片的分发与路由，同时作为Data Node,存储分片Shared和Segment。
node1: 作为Data Node，存储分片Shared和Segment。
node2: 作为Data Node，存储分片Shared和Segment。
与单节点查询效率比较，理论上DataNode和MasterNode的分离能减轻单个datanode的分片存储与检索压力。

4.2 结果比较
存储开销
将全部数据集存入三个数据库中，用各自的存储查询函数，得到结果如下
PostgreSQL：2967MB
MongoDB：3.37GB
ElasticSearch：3.3GB
查询性能比较
PostgreSQL： 1555067条记录  索引前：24628.865ms  索引后：2162.835ms  
MongoDB：1548390条记录 索引前：11332ms 索引后：3604ms
ElasticSearch：1548390条记录 47ms 
更新性能比较:
PostgreSQL：3.764ms 46条记录
MongoDB：46664ms 724396条记录 添加索引后60894ms 724396条记录
ElasticSearch：/
图片: https://uploader.shimo.im/f/JZXv9enP4XAl7VKO.png
追加、删除性能比较：PostgreSQL稳定在10ms左右，性能非常稳定，MongoDB在数千ms，性能不稳定
图片: https://uploader.shimo.im/f/sZJ5BdzwADsPb0Fy.png


5.实例展现
5.1 描述性数据分析
	数据的分析和可视化使用Kibana。Kibana是一个数据分析与可视化平台，拥有各种维度的查询和分析，并可以在与ElasticSearch连接后使用图形化的界面展示存放在ElasticSearch中的数据。Kibana平台通过浏览器访问，其基本界面如图5.1.1所示。
图片: https://uploader.shimo.im/f/ya6ZvRJyJH4OvjGL.png
图5.1.1 kibana界面
5.1.1. 全市犯罪数及犯罪类型分析
图片: https://uploader.shimo.im/f/8TB2J36bwQ0MprIc.png
（图5.1.1.1：全市犯罪数随年份的变化）
       图5.1.1.1显示了芝加哥市从2001年到2018年犯罪数的变化。分析可知全市犯罪数从2001年开始呈下降趋势，至2018年犯罪数接近2001年的一半，该市的治安环境在逐步改善。但从2016年开始犯罪数即保持均势，且2016年相比2015年犯罪数还有些许回升。结合市议会、市长等行政机构在2016年没有大的变动，但现任芝加哥警察局局长埃迪·约翰逊于2016年4月就职的情况[2]，我们有理由认为现任警察局局长在整顿治安环境方面失职。
图片: https://uploader.shimo.im/f/mPsmG7urKeIv1TGm.png
（图5.1.1.2：全市各类型犯罪占比）
图片: https://uploader.shimo.im/f/tUncQs7NiQMVWCEO.png
（图5.1.1.3：前十大类型犯罪数随年份的变化）
       图5.1.1.2和图5.1.1.3展示了芝加哥市各类犯罪的百分比和变化情况。综合数据前五大犯罪类型依次为盗窃、殴打、刑事毁坏、致幻药品和言语人身攻击，分别占21.11%，18.28%，11.39%，10.36%和6.26%，但这些类型的犯罪都呈下降趋势，尤其是致幻药品，从2016年开始已掉出前五大犯罪类型。但以往的一些不多见的犯罪都有不同程度的增加，其中以欺诈最为显著，于2016年开始取代致幻药品进入前五大犯罪类型之列。从图六中还可以看到各个类型在2016年以后犯罪数几乎都有回升或保持原状，进一步证明了新任警察局长的不称职。
2.各区犯罪比较分析
图片: https://uploader.shimo.im/f/L7kmsL748HEp3oV4.png
（图5.1.1.4：各区犯罪数词云、随年份变化及分布热力图）
       图5.1.1.4是整理了四张图表的仪表板，其中左上角为犯罪总数按区域划分的词云（前15），右上为各年犯罪数后五名的区域统计，左下为各年犯罪数前五名的区域统计，右下为犯罪数在全市分布的热力图。结合仪表板各图分析可知：1.犯罪主要集中在芝加哥市南部、中部和西部，北部犯罪较少；犯罪总数多的区域为8区、7区、6区、11区和25区；犯罪总数少的区域为20区、4区、24区、17区和22区；各区犯罪数均呈下降趋势。
图片: https://uploader.shimo.im/f/ez1p52v0rZQNN3Vo.jpg
图5.1.1.5 区域分布图
	再结合图5.1.1.5的区域分布图，可以发现犯罪多发的区域大多处在南部和西部，而犯罪总数最少的几个区主要集中在东北部密歇根湖畔。资料显示，东北部主要为白人和华裔的聚集地，而南部旧市中心黑人占比较高，西部则以西裔为主。白人和华裔的收入水平较高，受教育程度也因此提高，东北部的公共设施覆盖完善，因此治安条件好；而黑人和西裔普遍存在低收入、低教育水平的特点，民众缺乏稳定的收入来源，自身也缺乏改变现状的知识和能力，加之旧区设施陈旧老化、人员混杂，因此民众有更大几率从事盗窃、抢劫、贩毒等违 法活动。4区、5区等作为城市偏远郊区，人口很少，因此虽然处于南部，犯罪数仍然较少。
3.“特朗普”分析
       2019年10月28日，特朗普在芝加哥对警察群体发表谈话，并在谈话中提到：“去年一年，芝加哥共有565人被谋杀；约翰逊上台以来，谋杀致死人数高达1500人，枪击案受伤者更是高达13067人。”特朗普不仅公开羞辱约翰逊，还引用犯罪率数据，对整个芝加哥市开“地图炮”，认为“芝加哥是美国最差劲的庇护城市”，“芝加哥比阿富汗死于枪战的人更多”[3]。我们可以通过分析，验证特朗普所说是否正确。
       首先，我们验证约翰逊2016年上台以后杀人案（Homicide）的犯罪数是否上升。我们筛选犯罪类型为HOMICIDE的数据，查看其按年份的变化，如5.1.1.6所示。
图片: https://uploader.shimo.im/f/A14Wvseh228klF9R.png
（图5.1.1.6：芝加哥市杀人案数量随年份的变化）
	通过图5.1.1.6可以发现，约翰逊上任的2016年开始杀人罪的发生次数的确高于之前，尤其是2016年，被害人数高达788人，为近20年来最高；尽管在2017年和2018年被害人数有所下降，但也保持着多年来的高峰。2016年至2018年被杀害人数总数为2053人，高于特朗普所说的1500人，是因为杀人罪的统计包括谋杀和过失杀人等。
	其次，我们统计枪击案的发生情况。如图5.1.1.7所示，从2016年开始枪击案的发生次数有了显著的升高，并于2017年和2018年两次打破近20年枪击案次数的记录。
	图片: https://uploader.shimo.im/f/Ct3i5eSq3EUixTAB.png
（图5.1.1.7：枪击案发生次数随年份的变化）
	上述两次对杀人案和枪击案的分析，证明了特朗普所言并非无的放矢，芝加哥市的治安环境相比之前有所恶化，特朗普对现任警察局长约翰逊的指责是合理的。芝加哥市需要重新考虑约翰逊提出的相关政策的可行性和有效性。 
4.校园枪击分析
       我们知道，美国的校园枪击事件非常严重，每年都会发生枪手在校园内实施暴力导致多人伤亡的惨剧。芝加哥的枪击发生次数在全美排名前列，对芝加哥校园枪击的研究具有代表性[4]。我们将通过数据验证芝加哥的校园枪击是否真的如报道的那样严重。
       首先，我们对全市范围内的枪支暴力案件数目进行统计，结果显示在图5.1.1.8，颜色从浅到深代表相应区域的枪支暴力事件发生次数越多。由图可知枪击案发生的地点集中在西北部和南部，且与犯罪总数分布一致，在黑人和西裔聚集区内的发生次数更多。
图片: https://uploader.shimo.im/f/2W70itgAcdEQlONT.png
（图5.1.1.8：芝加哥市枪支暴力分布）
       随后，我们放大几个发生次数最多的三个区域，展示在图5.1.1.9~图5.1.1.11中。我们发现这三个区域全部都是学院区，是各类学校集中的地方，因此验证了校园枪击案的确非常严重，政府需要加强对于学生的枪支理性的教育，尤其是治安混乱区域内的学生；警方也需要在高发区域内加强巡逻和管理，保护学生们的生命财产安全。
图片: https://uploader.shimo.im/f/HddC26kDRggLWMm7.png
（图5.1.1.9：枪击集中区域——西北）
图片: https://uploader.shimo.im/f/2bKaxZ0gFRsBgj83.png（图5.1.1.10：枪击集中区域——南）
图片: https://uploader.shimo.im/f/bkFXnYpzqvk1ZoKV.png
（图5.1.1.11：枪击集中区域——东南）
5.家庭暴力行为关联分析
       家庭暴力一直以来都是引发全社会关注的一个问题，如何有效地制止家暴，对家暴实施者应该采取什么样的处置措施等话题常常会在社会上引起激烈的讨论。数据集中给出了“domestic”字段，用以标记该行记录是否属于家庭暴力的范畴，我们通过该字段与其它字段的关联，对家暴的地点、类型等属性进行分析。
       家庭暴力全部事件占总犯罪记录的13.24%，共925626条记录。图5.1.1.12展示了家庭暴力的发生地点的占比，其中发生在独立住所内（residence）的最多，共353641次，占39.85%；其次是公寓内（apartment），共280811次，占31.64%；接下来多发生在街道上和人行道边，分别占比12.71%和6.61%；剩下的地点分布较为平均，且占比都不超过2%。独立居所即独栋平房或别墅，在其中实施家庭暴力几乎不会被非家庭成员所知，往往都是被施暴者主动报警；而在公寓内实施家暴的动静很有可能被邻居知晓。我们将“在某地实施家庭暴力被他人发现的难易程度”定义为地点的隔离性，则地点的隔离性排名为独立居所>公寓>公共场合，可见隔离性与家暴案件数正相关。
图片: https://uploader.shimo.im/f/PnwchQibdMIBJ36m.png
（图5.1.1.12：家庭暴力的发生地点占比）
       图5.1.1.13展示了家庭暴力的常见类型占比，其中最为常见的是殴打，占全部家暴事件的59.9%，远超其它类型的家庭暴力。接下来是其它侵害、言语人身攻击、刑事毁坏和盗窃。这里注意美国与我国的国情差异：我国将家庭内的盗窃案件按照普通的刑事盗窃或者民事事件处理，而美国则将其列入domesitc之内。图表说明了家庭暴力的主要行为是殴打，与我们通常对家庭暴力的理解相同，但家庭暴力也包含了大量其他类型的行为。
图片: https://uploader.shimo.im/f/5GGHxhRocqEPRsr1.png
（图5.1.1.13：家暴的常见类型占比）

5.2预测性数据分析
当数据量比较大，数据分析场景更加开放，需要进行更进一步的数据分析及预测的时候，可以通过学习数据库知识来完成数据分析任务。python有一些库同样提供了可视化的功能，并且可以通过机器学习的方式进行数据分析。
首先，应该考虑影响犯罪的因素，以抽取相应的属性作为特征学习。
考虑下面几个因素：
1）星期
某些类型的犯罪在特定星期发生的概率较高。
周末的犯罪率较高，如BATTERY,HOMICIDE明显在周末发生的频率高于平时。
图片: https://uploader.shimo.im/f/I5krnhsCYTYNrZGi.png
2）小时
某些类型的犯罪在特定小时发生的概率较高；夜晚犯罪率高于白天。
集中发生于夜晚22-0点的犯罪类型有：
刑事毁坏，嫖妓，枪支犯罪，抢劫，非法赌博，摩托车盗窃，扰乱公共秩序...
集中发生于凌晨深夜的犯罪类型：
摩托车盗窃，纵火，人口贩卖，性犯罪和自杀...
集中发生于光天化日之下的犯罪类型：
欺诈，盗窃，绑架...
图片: https://uploader.shimo.im/f/pWRFuvRiThgtfw4h.png
3）月份
犯罪率随月份呈周期性变化。
图片: https://uploader.shimo.im/f/QLgGDT6TBDgSiWBw.png
但是，反映到具体的犯罪类型上，规律性没有那么明显。
图片: https://uploader.shimo.im/f/XHBl8na10XA3n55G.png
因此，在后面训练模型的时候，不把月份作为特征。经过尝试，将月份作为特征后，模型的准确率反而降低。
4）地点类型
某些类型的犯罪在特定地点发生的概率较高，如sex offense多发生在residence和apartment，theft和robbery多发生在street。
图片: https://uploader.shimo.im/f/aCTj6U24g5A5qatt.png
5）经纬度
利用kibana适合地理信息可视化的特点，查看犯罪分布，可以看出：某些类型的犯罪在特定district发生的概率较高，相比经纬度，可以提取district为特征。

综上，我们确定了训练模型需要的特征：星期，小时，地点类型和区号。
第一个场合：给定星期，小时，犯罪地点，区域，预测犯罪类型
这个场合适用于警察根据部分信息对可能发生的犯罪类型进行初步判断，从而制止犯罪。使用朴素贝叶斯模型，得到的准确率为0.31104516591238507。实验结果表明，在芝加哥，给定了星期，小时，地点类型以后，我们预测它犯罪类型的准确率只有31%左右。
第二个场合：给定星期，小时，犯罪类型，预测犯罪地点
这个场合适用于警察执法之前根据部分信息对模糊的犯罪地点进行判断，便于准备合适的工具。同样使用朴素贝叶斯模型，得到的准确率为0.26053700576626293。实验结果表明，在芝加哥，给定了星期，小时，犯罪类型以后，我们预测它发生的地点类型的准确率只有26%左右
两种情况，预测的准确率都不高，原因可能有以下几点：
首先，犯罪预测对于大数据的要求非常高，而我们的数据质量并不是很好。尤其是时间方面的信息不够精准，这也和无法实时更新犯罪记录有关。
其次，我们的特征提取远远不够。犯罪行为与很多因素有关，如之前分析到的，一个市换了市长都会影响枪击案数量的上升，不能简单地把影响犯罪的特征归结为以上几点。
在这个层面上，其实模型的选择不再具有太大的影响力，重要的是数据质量和其他的一些因素。在预测中，我还使用了逻辑回归模型，得到的效果也并不是很好（准确率也只有30%左右），验证了这一点。由此得出：首先，通过大数据的犯罪预测不能直接判断因果关系，如果要寻找因果关系，仍然需要大量的人力来进行分析。其次，基于大数据的犯罪预测，涉及到安全和隐私的问题，这需要在数据来源和数据保护上多做努力。最后，在大数据的犯罪预测研究中，非常容易出现“受限于研究结果”，“执迷数据”的 倾向，有一些信息是不容易被量化的，不能为了数据而数据，而是要以犯罪预测理论为依托， 将大数据进行合理的加工利用，这样才能使大数据变成强大的武器。

6.总结和不足
思考：数据库底层实现对应用实例的影响
·搜索性能
对ElasticSearch进行调优以后，搭建三节点集群，减轻单个节点分片存储与检索压力。在分片上进行分布式的、并行的操作可以提高性能和吞吐量。搭建集群提高了对数据库基本操作的性能，而数据分析是建立在对数据库的基本操作之上的，如统计左上角(-88,41.8)，右下角(-87.5,41.75)的矩形内的犯罪情况，是通过复杂查询实现。因此，也一定程度上有助于数据分析。
·实时性
文档从Index请求到对外可见能够被搜到，最少要1秒钟，这么做是Lucene为了提高写操作的吞吐量而做出的延迟牺牲。因此，在我们的数据操作层面，如果往数据库里追加了一条犯罪信息，此时，在内存缓冲区中包含了新犯罪记录的 Lucene 索引，然后，缓冲区的内容已经被写入一个可被搜索的段中，但还没有进行提交，只有当分片刷新时才会提交，让更新对搜索可见。分片每秒刷新一次，也就是说，需要至少1s，才能在对应的返回结果中得到这条犯罪记录。因此，ElasticSearch不是用于实时查询的最佳选项。不过，在我们的应用目标中，并不需要实时检索，而是对历史犯罪记录进行统计分析，问题不大。
·可靠性
为了提高性能，Lucene会将同一个term重复地index到各种不同的数据结构中，以支持不同目的的搜索，最终index可能数倍于原本的数据大小；ES的排序和聚合操作会把几乎所有相关不相关的文档都加载到内存中；大量的增量写操作会导致大量的后台Merge，CPU和硬盘读写都会很容易达到瓶颈。这些都可能会导致OutOfMemory,集群中的节点逐个崩溃。我们在做数据分析的时候就遇到过状态变为红色的情况。
·分布一致性
Elasticsearch允许创建分片的一份或多份拷贝，这些拷贝叫做复制分片，或者直接叫复制。这个机制在分片/节点失败的情况下，提供了高可用性。同时，扩展了吞吐量，因为搜索可以在所有的复制上并行运行。但是，在分布式环境下，多个数据副本不一定能保证一致。比如说，在修改了犯罪信息之后再执行查询，如果多个数据副本的信息不一致，那么搜索在所有复制上并行运行，返回的结果可能也就不准确了。



7.参考文献
（不少于20篇，并且包含近三年的）
[1]李敏波,许鑫星,韩乐.基于JSON文档结构的工业大数据多维分析方法[J/OL].中国机械工程:1-9[2019-12-31].http://kns.cnki.net/kcms/detail/42.1294.th.20191223.1201.023.html. 
[2]俞志宏,栗国保,李少白.基于Elasticsearch的时空大数据存储与分析方法[J].电子技术与软件工程,2019(22):152-154. 
[3]鲜征征,叶嘉祥.一种改进的ELK日志采集与分析系统[J].软件导刊,2019,18(08):105-110. 
[4]李钦,杨程.基于ELK的日志分析平台搭建与优化[J].现代信息科技,2019,3(15):193-194. 
[5]李传根. Elasticsearch数据存储策略研究[D].重庆邮电大学,2019. 
[6]王章龙. Elasticsearch索引分片策略研究[D].重庆邮电大学,2019. 
[7]梁文楷.基于Elasticsearch全文检索系统的实现[J].电脑编程技巧与维护,2019(06):116-119. 
[8]徐伟杰,王挺,薛婉婷.基于ElasticSearch的搜索引擎设计与实现[J].智库时代,2019(23):228+240. 
[9]Zhanglong Wang. An Optimization Strategy of Shard on Elasticsearch[C]. Institute of Management Science and Industrial Engineering.Proceedings of 2019 4th International Conference on Automatic Control and Mechatronic Engineering(ACME 2019).Institute of Management Science and Industrial Engineering:计算机科学与电子技术国际学会(Computer Science and Electronic Technology International Society),2019:20-28. 
[10]Zachary Parker,Scott Poe,Susan V. Vrbsky.Comparing NoSQL MongoDB to an SQL DB.The University of Alabama Center for Advanced Public Safety Tuscaloosa, AL,2013.
[11]Pavel Seda,Jiri Hosek, Pavel Masek, Jiri Pokorny.Performance Testing of NoSQL and RDBMS for Storing Big Data in e-Applications.Department of Telecommunications, Brno University of Technology, Brno, Czech Republic Peoples’ Friendship University of Russia (RUDN University),2018.
[12]胡素梦.大数据云计算背景下的犯罪预测研究.黑龙江大学法学院,2018
[13]Barghouti, N.S. and Kaiser, G.E. (1991). Concurrency control in advanced database applications. ACM Computing Surveys, Vol. 23, No. 3, pp. 269-318.
[14]R. Agrawal, M. J. Carey, and M. Livny, "Concurrency control performance modelling: Alternatives and implications," ACM Trans. Database Syst., vol. 12, no. 4, Dec. 1987.
[15]Bruce Momjian. 2001. PostgreSQL performance tuning. Linux J. 2001, 88 (August 2001), 3.
[16]Dennis Butterstein and Torsten Grust. 2016. Precision performance surgery for CostgreSQL: LLVM---based Expression Compilation, Just in Time. Proc. VLDB Endow. 9, 13 (September 2016), 1517–1520. 
[17]Christian Riegger, Tobias Vinçon, and Ilia Petrov. 2019. Indexing large updatable datasets in multi-version database management systems. In Proceedings of the 23rd International Database Applications & Engineering Symposium (IDEAS ’19). Association for Computing Machinery, New York, NY, USA, Article 36, 1–5.
[18]Wentao Wu, Jeffrey F. Naughton, and Harneet Singh. 2016. Sampling-Based Query Re-Optimization. In Proceedings of the 2016 International Conference on Management of Data (SIGMOD ’16). Association for Computing Machinery, New York, NY, USA, 1721–1736. 
[19] Lucantonio Ghionna, Gianluigi Greco, and Francesco Scarcello. 2011. H-DB: a hybrid quantitative-structural sql optimizer. In Proceedings of the 20th ACM international conference on Information and knowledge management (CIKM ’11). Association for Computing Machinery, New York, NY, USA, 2573–2576. 
[20] Meduri Venkata Vamsikrishna and Kian-Lee Tan. 2011. Subquery plan reuse based query optimization. In Proceedings of the 17th International Conference on Management of Data (COMAD ’11). Computer Society of India, Mumbai, Maharashtra, IND, Article 11, 1–12.
[21] Tudor-Ioan Salomie, Ionut Emanuel Subasu, Jana Giceva, and Gustavo Alonso. 2011. Database engines on multicores, why parallelize when you can distribute? In Proceedings of the sixth conference on Computer systems (EuroSys ’11). Association for Computing Machinery, New York, NY, USA, 17–30.
[22] Christan Earl Grant, Joir-dan Gumbs, Kun Li, Daisy Zhe Wang, and George Chitouras. 2012. MADden: query-driven statistical text analytics. In Proceedings of the 21st ACM international conference on Information and knowledge management (CIKM ’12). Association for Computing Machinery, New York, NY, USA, 2740–2742.
[23]  George Candea, Neoklis Polyzotis, and Radek Vingralek. 2011. Predictable performance and high query concurrency for data analytics. The VLDB Journal 20, 2 (April 2011), 227–248.
[24]Hadjigeorgiou. Rdbms vs nosql: Performance and scaling comparison[C]. Master’s thesis, The University of Edinburgh, 2013.
附录1：https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2

8.小组分工
刘婧漪：PostgreSQL部分，参与数据预处理，转换为关系模式；配置PostgreSQL环境并编写脚本将.csv文件拆分处理，导入；分析测试PostgreSQL性能；预测性数据分析；海报制作；论文撰写。
王泽宇：收集获取源数据集；PostgreSQL部分，参与数据预处理，转换为关系模式；编写建库建表脚本和测试脚本；完成PostgreSQL原理及架构解读，源码阅读分析和性能比较分析；demo目标和挖掘技术制定以及论文撰写。
梁东宸：MongoDB部分，MongoDB的环境配置、数据处理、导入、增删改查的代码编写和结果分析，MongoDB与ElasticSearch的同步，建立索引及数据比较，描述性数据分析，论文撰写
赵海凯：ElasticSearch部分（包括论文）+ Python数据可视化（源码：https://github.com/AlexanderChiuluvB/ElasticSearch-WordCloud）
