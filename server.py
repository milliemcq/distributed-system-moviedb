import Pyro4
import read_update_csv as data
import sys


status = "online"
other_servers = []

rating_dict = data.movie_rating_dict
update_log = {}
timestamp_vector = []

# retrieve, submit and update movie ratings
@Pyro4.behavior(instance_mode = "single")
@Pyro4.expose
class Database:
    ratings = rating_dict
    update_list = []
    hold_back_queue = []
    replica_timestamp = []
    value_timestamp = []
    all_updates = []

    timestamp_table = []

    def go_offline(self):
        Database.status = "offline"

    def overload(self):
        Database.status = "overload"

    def online(self):
        Database.status = "online"

    def get_status(self):
        return status

    def add_rating(self, movie_title, user_id, rating):
        if movie_title in rating_dict:
            rating_dict[movie_title][user_id] = rating
        else:
            return "Could not find Movie with that title"

    def average_rating(self, movie_title):
        if movie_title in rating_dict:
            total = 0
            number_ratings = 0
            for item in rating_dict[movie_title].keys():
                total += rating_dict[movie_title][item]
                number_ratings += 1
            return total / number_ratings

        return "Could not find movie with that title"

    def find_movie(self, movie_title):
        if movie_title in rating_dict:
            return rating_dict[movie_title]
        else:
            return "No movie found"

    def get_user_rating(self, movie, user_id):
        return rating_dict[movie][user_id]

    def get_rating_dict(self):
        return rating_dict

    def new_update(self, timestamp, update_type, movie_name, user_id, rating, gossip=False):
        if gossip:
            #timestamp_table.append(timestamp) - find out what server this is coming from ^^ pass form above
            for item in Database.all_updates:
                if item[0] == timestamp:
                    return "Update already processed"
            Database.update_list.append((timestamp, update_type, movie_name, user_id, rating))
            Database.replica_timestamp[this_server_num] += 1
            return Database.value_timestamp
        else:
            for item in Database.all_updates:
                if item[0] == timestamp:
                    return "Update already processed"

            Database.update_list.append((timestamp, update_type, movie_name, user_id, rating))

            Database.replica_timestamp[this_server_num] += 1

            return Database.value_timestamp


    def new_query(self, timestamp, movie_name):
        greatest_time = compare_timestamp(timestamp)
        if greatest_time <= Database.value_timestamp[this_server_num]:
            return Database.average_rating(movie_name)
        return 0


    def compare_timestamp(self, timestamps):
        num = 0
        for item in timestamps:
            if item > num:
                num = item
        return num

def sort_tuple(item):
    return item[0][this_server_num]


def gossip():
    Database.update_list = sorted(Database.update_list, key=sort_tuple)
    for item in Database.update_list:
        if item[0][this_server_num] == Database.value_timestamp[this_server_num] + 1:
            Database.add_rating(item[2], item[3], item[4])
            Database.all_updates.append((item[0], item[1], item[2], item[3], item[4]))
            Database.value_timestamp[this_server_num] += 1

    for item in Database.hold_back_queue:
        #ANSWER queries and send back to the right client
        pass

    for item in Database.update_list:
        for other_server in server_list:
            other_server.new_update(item[0], item[1], item[2], item[3], item[4])


with Pyro4.locateNS() as name_server:
    server_dict = name_server.list(prefix="ratings.database.")

daemon = Pyro4.Daemon()
uri = daemon.register(Database)

num_servers = len(server_dict.keys()) - 1

this_server_num = num_servers + 1

server_list = []

for item in server_dict.values():
    if item != uri:
        server = Pyro4.Proxy(item)
        if server.get_status == "online":
            server_list.append(server)

timestamp_table = [[] for _ in range(num_servers)]




with Pyro4.locateNS() as name_server:
    name_server.register("ratings.database." + str(num_servers + 1), uri, safe=True)

print("Server Ready: Object URI = " + str(num_servers + 1))

sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop(gossip)





"""
Giving other servers access to one another

Update log greater than size 10, can't accept anything - call - overloaded -

"""
