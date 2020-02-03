import optimoroute
from optimoroute import Order
import time

#function for cleaning and sorting the input data from the Optimoroute api
def clean_data(data):
    input_data = data
    input_data = input_data.replace("null","'null'")
    input_data = input_data.replace("true","'true'")

    print(input_data)
    input_data = eval(input_data)
    result1 = []
    result2 = []
    data1 = input_data["routes"][0]["stops"]
    for i in data1:
        result1.append(i["distance"])
        result2.append((i["latitude"],i["longitude"]))
    print(result1)
    return result1, result2

#function for sending the received full bin location data to the optimoroute api and receiving optimal route data

def get_routes_from_txt(txt_name):
	my_file = open(txt_name,"r")
	lines = my_file.readlines()
	orderlist=[]

	for line in lines: 

		params = line.split(",,")
		optimoroute.delete_order(params[0])

		orderlist.append(Order(params[0],params[1],params[2],params[3],int(params[4]),int(params[5]),int(params[6])))
		
	for item in orderlist:
		optimoroute.create_order(item)
		


	plan = optimoroute.start_planning(params[1])
	time.sleep(2)

	my_routes = optimoroute.get_routes(params[1])		
	print(my_routes)
	my_routes= clean_data(my_routes)
	return(my_routes)
	
print(get_routes_from_txt("input.txt"))
