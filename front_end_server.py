import Pyro4

with Pyro4.locateNS() as name_server:
    server_dict = name_server.list(prefix="ratings.database.")

num_servers = len(server_dict.keys())

servers = server_dict.values()
server_list = []

for item in server_dict.values():
    server = Pyro4.Proxy(item)
    server_list.append(server)

@Pyro4.behavior(instance_mode = "single")
class NameServer:




    def choose_server(self):
        for item in server_list:


    def choose_server():
        pass



daemon = Pyro4.Daemon()
uri = daemon.register(NameServer)
with Pyro4.locateNS() as name_server:
    name_server.register("nameServer." + str(uri), uri, safe=True)


# self.server.look_up