import Pyro4
import read_update_csv as data
import sys
import random


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
    replica_timestamp = [0, 0, 0]
    value_timestamp = [0, 0, 0]
    all_updates = []

    timestamp_table = [[],[],[]]

    def get_status(self):
        if len(Database.update_list) > 10:
            return "overloaded"
        num = random.uniform(0, 1)
        if num < 0.9:
            return "online"
        return "offline"

    def add_rating(self, movie_title, user_id, rating):
        if movie_title in rating_dict:
            rating_dict[movie_title][user_id] = rating
        else:
            return "Could not find Movie with that title"

    def average_rating(self, movie_title):
        print("Inside average rating")
        if movie_title in Database.ratings:
            total = 0
            number_ratings = 0
            print(rating_dict[movie_title])
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

    def new_update(self, timestamp, update_type, movie_name, user_id, rating, gossip=False, server=None):
        print(str(Database.average_rating(self, movie_name)))
        if gossip:


            #Add processed update to timestamp table - if every server has seen update, delete from update_list
            timestamp_table[server].append(timestamp)
            found = True
            for used_timestamp_list in timestamp_table:
                if timestamp in used_timestamp_list:
                    continue
                found = False

            for item in Database.all_updates:
                if item[0] == timestamp:
                    if found:
                        Database.update_list.remove(item)
                    return "Update already processed"
            Database.update_list.append((timestamp, update_type, movie_name, user_id, rating))
            Database.replica_timestamp[this_server_num] += 1
            return Database.value_timestamp
        else:
            for item in Database.all_updates:
                if item[0] == timestamp:
                    return "Update already processed"

            Database.replica_timestamp[this_server_num] += 1
            timestamp[this_server_num] = Database.replica_timestamp[this_server_num]

            print("Timestamp Adding: " + str(timestamp))
            Database.update_list.append((timestamp, update_type, movie_name, user_id, rating))
            Database.gossip()
            return Database.value_timestamp


    def new_query(self, timestamp, movie_name):
        print(timestamp)
        print(movie_name)
        greatest_time = Database.compare_timestamp(self, timestamp)
        print(this_server_num)
        if greatest_time <= Database.value_timestamp[this_server_num]:
            return Database.average_rating(self, movie_name)
        return 0


    def compare_timestamp(self, timestamp):
        num = 0
        print(timestamp)
        for item in timestamp:
            if item > num:
                num = item
        return num



    def gossip():
        print(Database.update_list)
        print("Gossip Called")
        Database.update_list = sorted(Database.update_list, key=sort_tuple)
        print(Database.update_list)
        for item in Database.update_list:
            if item[0][this_server_num] == Database.value_timestamp[this_server_num] + 1:
                print(item[2])
                print(item[3])
                print(item[4])
                Database.add_rating(0, item[2], item[3], item[4])
                Database.all_updates.append((item[0], item[1], item[2], item[3], item[4]))
                Database.value_timestamp[this_server_num] += 1

                print("New Gossip Update")


        print("Updating other servers")
        for item in Database.update_list:
            print("Looping through update list")
            server_list = get_server_list()
            print(server_list)
            for other_server in server_list:
                print("Sending to other server")
                other_timestamp = other_server.new_update(item[0], item[1], item[2], item[3], item[4], True, this_server_num)

        # print("Should be different + " + str(Database.average_rating("Horns")))
        print("Returning from Gossip")



def sort_tuple(item):
    print("Sorting Tuple")
    return item[0][this_server_num]

def get_server_list():
    server_dict = name_server.list(prefix="ratings.database.")
    server_list = []
    for item in server_dict.values():
        if item != uri:
            print("Server found not this one")

            server = Pyro4.Proxy(item)
            print(server.get_status())
            if server.get_status() == "online":
                print("Adding server")
                server_list.append(server)
    print("Server List = " + str(server_list))
    return server_list


with Pyro4.locateNS() as name_server:
    server_dict = name_server.list(prefix="ratings.database.")

daemon = Pyro4.Daemon()
uri = daemon.register(Database)

num_servers = len(server_dict.keys()) - 1
#print(num_servers)

this_server_num = num_servers + 1



timestamp_table = [[] for _ in range(num_servers)]


with Pyro4.locateNS() as name_server:
    name_server.register("ratings.database." + str(num_servers + 1), uri, safe=True)



print("Server Ready: Object URI = " + str(num_servers + 1))

sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()


print("Loop Stopped")


"""
Giving other servers access to one another

Update log greater than size 10, can't accept anything - call - overloaded -

"""
