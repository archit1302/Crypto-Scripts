'''
	author : Archit Mittal
	Python Version : 3.8.2
	Websocket Version : 1.2.3

'''

import websocket,json
import requests
import time
from datetime import datetime
from prettytable import PrettyTable

socket = 'wss://fstream.binance.com/ws/btcusdt@depth10@500ms'
link = 'https://fapi.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10'

def logging(data):
	file = open("logs.txt", "a")
	file.write(str(data))
	file.write("\n")
	file.close()

def printTable(bids,asks):
	myTable = PrettyTable(["S.No.","Bid Price", "Bid Qty", "Ask Price", "Ask Qty"])
	for i in range(10) :
		myTable.add_row([i+1,bids[i][0],bids[i][1],asks[i][0],asks[i][1]])
	print(myTable)
#	logging(myTable)	

def printTime():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Current Time =", current_time)
	logging(current_time)	

def getSnapshot():
	data = requests.get(link)
	convertData = data.json()
	bids = convertData['bids']
	asks = convertData['asks']
	printTime()
	printTable(bids,asks)

def on_message(ws, message):
	global start 
	end = time.time()
	timeDifference = end-start   
	if timeDifference >= 1:	# time difference should be 15 seconds
		getSnapshot()
		start = time.time()     # start time reset to current time
	
def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("Connection killed manually")

if __name__ == "__main__":
	ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
	getSnapshot()
	start = time.time()
	ws.run_forever()			# run_forever ensures to reconnect if the system is not killed manually
