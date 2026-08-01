from mcstatus import JavaServer
import sys

IP_ADDR = "white-navigate.gl.at.ply.gg"

try:
	server = JavaServer.lookup(IP_ADDR)
	status = server.status()
	print(status)
	if status.players.max > 0:
		print("server is up!")
		print(status.players.max)
except:
	print("error!")



