
import pandas as pd
from io import StringIO
import csv, json
import requests
import numpy as np
import os
#import ast
def crawl_stock(date):
    r=requests.get('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL')
    #! refine to use native csv lib
    list = []
    #! Please remove following for-loop and use native csv
    #  reader instead of pandas.
    for i in r.text.split('\n'):
	    if len(i.split('",')) == 17 and i[0] != '=':
		    i = i.strip(",\r\n")
		    list.append(i)
    df = pd.read_csv(StringIO("\n".join(list)))
    data = df.values.tolist()
    result = {}
    for row in data[1:]:
        result[row[0]] = {
            "Company_name": row[1],
            "Trade_Volume": row[2],
            "Transaction": row[3],
            "Trade_Value": row[4],
            "Opening_Price": row[5],
            "Highest_Price": row[6],
            "Lowest_Price": row[7],
            "Closing_Price": row[8],
            "Dir(+/-)": row[9],
            "Change": row[10],
            "Last_Best_Bid_Price": row[11],
            "Bid_Volume": row[12],
            "Last_Best_Ask_Price": row[13],
            "Ask_Volume": row[14],
            "P/E_Ratio": row[15]

        }
    with open('Out.json','w')as f:
        json.dump(result, f, ensure_ascii = False, indent = 4)

def get14days_feature(day, StockID, feature):
    #! remove not necessary comment.
    #date, stock, feature):
    path_init = "/home/db/stock_resource_center/resource/twse/json"
    path_list = os.listdir(path_init)
    #! No Chinese please.
    path_list = sorted(os.listdir(path_init), key = lambda x:x[:-5])  #對讀取的路徑進行排序
    for i in range(15):
        #! Please refer to Python official document about range
        #  function and remove following if-else
        if i==0 :
            path = path_init + '/' + day + '.json'
            index = path_list.index(day + '.json')
        else :
            index -= 1
            path = path_init + '/' + path_list[index]
        with open(path,'r') as g:
            cc = json.loads(g.read())
        print(cc[StockID][feature])
if __name__ == "__main__":
    date = input("Input the date you want: ")
    crawl_stock(date)
    day = input("Input the date you want: ")
    StockID = input("Input the SrockID you want: ")
    feature = input("Input the one feature you want to see( 1.adj_close 2.close 3.high 4.low 5.open 6.volume ): ")
    get14days_feature(day, StockID, feature)
