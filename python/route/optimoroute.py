import requests
import json

AUTH_KEY = "fcc77ded6481a3935dc34bd3568afe4f8bGiGpnujDc"

class Order:
	def __init__(self, orderNo, date, address, name, duration, weight, volume):
		self.orderNo = orderNo
		self.date = date
		self.address = address
		self.name = name
		self.duration = duration
		self.weight = weight
		self.volume = volume

def jprint(obj):
	# create a formatted string of the Python JSON object
	text = json.dumps(obj, sort_keys=True, indent=4)
	print(text)

def get_routes(date):
	parameters = {
		"key": AUTH_KEY,
		"date": date
	}

	response = requests.get("https://api.optimoroute.com/v1/get_routes", params=parameters)
	return (json.dumps(response.json(), sort_keys=True, indent=4))
	jprint(response.json())

def create_order(order):
	parameters = {
		"key": AUTH_KEY
	}

	data = json.dumps({
		"operation": "CREATE",
		"orderNo": order.orderNo,
		"type": "D",
		"date": order.date,
		"location": {
			"address": order.address,
			"locationName": order.name,
			"acceptPartialMatch": True
		},
		"duration": order.duration,
		"load1": order.weight,
		"load2": order.volume
	})

	response = requests.post("https://api.optimoroute.com/v1/create_order", params=parameters, data=data)
	jprint(response.json())

def get_order(orderNo):
	parameters = {
		"key": AUTH_KEY,
		"orderNo": orderNo
	}

	response = requests.get("https://api.optimoroute.com/v1/get_orders", params=parameters)
	text = json.dumps(response.json(), sort_keys=True, indent=4)

	jprint(response.json())

def delete_order(orderNo):
	parameters = {
		"key": AUTH_KEY
	}

	data = json.dumps({
		"orderNo": orderNo
	})

	response = requests.post("https://api.optimoroute.com/v1/delete_order", params=parameters, data=data)
	jprint(response.json())

def start_planning(date):
	parameters = {
		"key": AUTH_KEY
	}

	data = json.dumps({
		"date": date
	})

	response = requests.post("https://api.optimoroute.com/v1/start_planning", params=parameters, data=data)
	jprint(response.json())
	
	
	
	