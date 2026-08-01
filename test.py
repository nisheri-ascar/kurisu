from mcstatus import JavaServer
import sys

IP_ADDR = "mc.hypixel.ne"

try:
	server = JavaServer.lookup(IP_ADDR)
	status = server.status()
except:
	print("error!")
	sys.exit(1)

print(status.players.online)

if status.players.online > 0:
	print("server is up!")
else: 
	print("error!")
