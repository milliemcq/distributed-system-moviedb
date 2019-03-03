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
    timestamp_vector = [0, 0, 0]
    print("Looking in Name server")

    #chooses the first available online server, returns a list [0] = Server number [1] = server
    def choose_server(self, curr_server):
        for i in range(curr_server, len(server_list)):
            #print(server_list[i].get_status())
            if server_list[i].get_status() == 'online':
                return [server_list[i], i]
        print("no server online")
        return 1


    #Movie rating is added and current highest timestamp for that server returned
    def add_movie_rating(self, movie_name, user_id, rating):
        chosen_server = self.choose_server(0)
        if chosen_server == 1:
            return "No current server available"
        server = chosen_server[0]
        #TODO Return timestamp vector here and update 'global' timestamp
        replica_value_timestamp = self.server.new_update(movie_name, user_id, rating)



    #iterate over servers until one has the highest timestamp, and collect the results from this server.
    def average_rating(self, movie_name):
        chosen_server = self.choose_server(0)
        if chosen_server == 1:
            return "No current server available"
        server = chosen_server[0]
        response = server.new_query(self.timestamp_vector, movie_name)
        print("Average Response: " + str(response))
        return response
        """
        while response == 0:
            new_server = self.choose_server(server[1])
            response = new_server.new_query(self.timestamp_vector, movie_name)
        return response"""




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