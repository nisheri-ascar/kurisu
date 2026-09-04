from mcstatus import JavaServer


def check_server_status():
    try:
        server = JavaServer.lookup(MC_IP_ADDR)
        status = server.status()
        return 0
    except:
        print("cannot access server!!")
        return 1