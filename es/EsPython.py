from elasticsearch import Elasticsearch

host = '3.15.141.41'
port = 9200
es = Elasticsearch([{'host': host, 'port': port}])

body = {
  "query": {
    "match": {
      "primary_type": {
        "query": "THEFT",
        "type": "phrase"
      }
    }
  }
}

def search(index,query):
    """
    https://www.cnblogs.com/xing901022/p/4974977.html
    query 为lucene语法表达式
    :param index:
    :param query:
    :return:
    """
    result = es.search(index=index, q=query)
    print(result)

def searchByJson(index,body,scroll,size):
    """
    返回全量数据
    :param index:
    :param body:
    :param scroll:
    :param size:
    :return: mdata
    """
    try:
        queryData = es.search(index=index, body=body,scroll=scroll,size=size)
        mdata = queryData.get('hits').get('hits')
        scroll_id = queryData["_scroll_id"]
        scroll_size = len(mdata)
        if not mdata:
            print('empty')
            return None
        while scroll_size > 0:
            res = es.scroll(scroll_id=scroll_id, scroll=scroll)
            scroll_id = res["_scroll_id"]
            scroll_size = len(res.get('hits').get('hits'))
            mdata += res.get("hits").get("hits")
            # Process
    except Exception as e:
        print(e)
    finally:
        print(len(mdata))
    return mdata


if __name__ == "__main__":
    # search("chicago*","year:2019 AND primary_type:THEFT")
    searchByJson(index="chicago*",body=body,scroll="25m",size=10000)




