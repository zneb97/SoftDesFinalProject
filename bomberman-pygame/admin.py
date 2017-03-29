import os, sys, random
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *

client = TCPClient()
# client.connect("localhost", 6317)
# server_name = sys.argv[1]
# server_address = (server_name, 6317)
# print >>sys.stderr, 'starting up on %s port %s' % server_address
client.connect('gsteelman-Latitude-E5470', 6317)

def main():
	#client.send_data(["update",None])
	print("1) Clear Data")
	print("2) Reset Users")
	print("3) Add User")
	print("8) Start Game")
	print("9) Exit")

	input = 0
	while input != "4":
		input = input("$: ")

		if input == "1":
			client.send_data(["update","clear all"])
		elif input == "2":
			client.send_data(["update","reset ids"])
		elif input == "3":
			client.send_data(["update","user joined",random.randint(0,10000000)])
		elif input == "8":
			client.send_data(["update", "start game"])
		elif input == "9":
			sys.exit()

if __name__ == '__main__':
	main()
