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

@Pyro4.expose
class NameServer:
    timestamp_vector = []
    print("Looking in Name server")
    def choose_server(self):
        for item in server_list:
            print(item.get_status())
            if item.get_status() == 'online':
                return item
        print("no server online")
        raise ValueError('No server currently online')
    def add_movie_rating(self, movie_name, user_id, rating):
        try:
          self.server = self.choose_server()
        except:
            return "No online server found"
        self.server.new_update(movie_name, user_id, rating)

    def average_rating(self, movie_name):
        try:
          self.server = self.choose_server()
        except:
            return "No online server found"
        self.server.new_query(movie_name, user_id, rating)

    def get_user_rating(self):
        try:
          self.server = self.choose_server()
        except:
            return "No online server found"
        self.server.add_rating(movie_name, user_id, rating)





daemon = Pyro4.Daemon()
uri = daemon.register(NameServer)
with Pyro4.locateNS() as name_server:
    name_server.register("frontEnd", uri, safe=True)

print("FE Server Ready")
sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()