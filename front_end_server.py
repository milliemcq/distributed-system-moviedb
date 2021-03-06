import Pyro4
import sys




@Pyro4.behavior(instance_mode = "single")
@Pyro4.expose
class NameServer:
    fe_timestamp_vector = [0, 0, 0]
    update_id = 0
    print("Looking in Name server")

    #chooses the first available online server, returns a list [0] = Server number [1] = server
    def choose_server(self, curr_server):
        with Pyro4.locateNS() as name_server:
            server_dict = name_server.list(prefix="ratings.database.")

        num_servers = len(server_dict.keys())

        servers = server_dict.values()
        server_list = []

        for item in server_dict.values():
            server = Pyro4.Proxy(item)
            server_list.append(server)

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
        replica_value_timestamp = server.new_update(self.fe_timestamp_vector, self.update_id, movie_name, user_id, rating, False, None)
        self.update_id += 1
        print(replica_value_timestamp)
        self.fe_timestamp_vector = replica_value_timestamp



    #iterate over servers until one has the highest timestamp, and collect the results from this server.
    def average_rating(self, movie_name):
        print("FRONT END TIMESTAMP = " + str(self.fe_timestamp_vector))
        chosen_server = self.choose_server(0)
        if chosen_server == 1:
            return "No current server available, Try again in a few seconds"
        server = chosen_server[0]
        #TODO - iterate over servers till found one up to date
        response = server.new_query(self.fe_timestamp_vector, movie_name)
        print("Average Response: " + str(response))
        return response


    def get_user_rating(self, user_id, movie_name):
        print(user_id)
        print(movie_name)
        print("FRONT END TIMESTAMP = " + str(self.fe_timestamp_vector))
        chosen_server = self.choose_server(0)
        if chosen_server == 1:
            return "No current server available, Try again in a few seconds"
        server = chosen_server[0]
        # TODO - iterate over servers till found one up to date
        response = server.get_user_rating(self.fe_timestamp_vector, user_id ,movie_name)
        print(response)
        return response







daemon = Pyro4.Daemon()
uri = daemon.register(NameServer)
with Pyro4.locateNS() as name_server:
    name_server.register("frontEnd", uri, safe=True)

print("FE Server Ready")
sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()