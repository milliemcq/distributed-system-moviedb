import Pyro4
import sys

with Pyro4.locateNS() as name_server:
    server_dict = name_server.list(prefix="ratings.database.")

num_servers = len(server_dict.keys())

servers = server_dict.values()
server_list = []

for item in server_dict.values():
    server = Pyro4.Proxy(item)
    server_list.append(server)

print(server_list)

@Pyro4.behavior(instance_mode = "single")
@Pyro4.expose
class NameServer:
    print("Looking in Name server")
    def choose_server(self):
        for item in server_list:
            print(item.get_status())
            if item.get_status() == 'online':
                return item
        print("no server online")
        raise ValueError('No server currently online')



daemon = Pyro4.Daemon()
uri = daemon.register(NameServer)
with Pyro4.locateNS() as name_server:
    name_server.register("nameServer", uri, safe=True)

print("FE Server Ready")
sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()