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
class NameServer:

    def choose_server(self):
        for item in server_list:
            if item.status == 'Online':
                return item





daemon = Pyro4.Daemon()
with Pyro4.locateNS() as name_server:
    name_server.register("nameServer")

print("Front end server Ready")
sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()