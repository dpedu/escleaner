#!/usr/bin/env python3

import requests
import re
from datetime import datetime,timedelta

def get_indices():
    req = requests.get("{}/_cat/indices".format(es_url))
    data = req.text.strip().split("\n")
    
    data = [row.split(" ")[2] for row in data]
    
    data = [item for item in filter(lambda x: logstash_pattern.match(x), data)]
    
    return sorted(data)


def delete_index(index):
    if index:
        print("deleting {}".format(index))
        #print("curl -XDELETE {}{} &&".format(es_url, index))
        del_url = "{}{}".format(es_url, index)
        print(requests.delete(del_url).text)


def main(url, index, days):
    global es_url
    global logstash_pattern
    es_url = url
    logstash_pattern = re.compile(r'%s\-(([0-9]{4})\.([0-9]{2})\.([0-9]{2}))'%index)
    
    deleteBefore = datetime.now() - timedelta(days=days)
    
    indexes = get_indices()
    
    for index in indexes:
        datematch = logstash_pattern.match(index)
        year =  int(datematch.group(2))
        month = int(datematch.group(3))
        day =   int(datematch.group(4))
        
        indexDate = datetime(year=year, month=month, day=day)
        
        if indexDate < deleteBefore:
            delete_index(index)

def shell():
    import argparse
    
    parser = argparse.ArgumentParser(description='Delete logstash indexes by age')
    parser.add_argument('-u', '--url',   action='store', required=True,      help='Elasticsearch url')
    parser.add_argument('-d', '--days',  action='store', default=31,         help='Maximum index age that will be kept', type=int)
    parser.add_argument('-i', '--index', action='store', default="logstash", help='Index name to inspect. (Used as so: "%%s-YYYY.MM.DD")')
    
    args = parser.parse_args()
    
    main(args.url, args.index, args.days)


if __name__ == '__main__':
    shell()
