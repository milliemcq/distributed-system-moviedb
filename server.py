import Pyro4
import read_update_csv as data
import sys
import random
import threading


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
    executed_updates = []

    timestamp_table = [[], [], []]

    def get_status(self):
        if len(Database.update_list) > 10:
            print("Returning Overloaded")
            return "overloaded"
        num = random.uniform(0, 1)
        if num < 0.9:
            return "online"
        print("Returning Offline")
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

    def new_update(self, timestamp, update_id, movie_name, user_id, rating, gossip, server):
        print("Average rating within new_update: " + str(Database.average_rating(self, movie_name)))
        #print(Database.timestamp_table)
        if gossip:

            print("Timestamp table, within gossip new_update: " + str(Database.timestamp_table))
            print("server num: " + str(server))
            print("Timestamp: " + str(timestamp))
            #Add processed update to timestamp table - if every server has seen update, delete from update_list
            if timestamp not in Database.timestamp_table[server]:
                Database.timestamp_table[server].append(timestamp)


            if Database.check_timestamp_table(self, timestamp, update_id):
                print("Update already processed within gossip")
                return "Update already processed"

            if update_id not in Database.executed_updates:
                Database.replica_timestamp[this_server_num] += 1
                #timestamp[this_server_num] = Database.replica_timestamp[this_server_num]
                print("APPENDING BECAUSE GOSSIP SAYS SO")
                Database.update_list.append((timestamp, update_id, movie_name, user_id, rating))

            return timestamp
        else:

            if update_id in Database.executed_updates:
                return timestamp

            Database.replica_timestamp[this_server_num] += 1
            timestamp[this_server_num] = Database.replica_timestamp[this_server_num]

            print("Timestamp Adding: " + str(timestamp))
            print("APPENDING BECAUSE FRONT END SAYS SO")
            Database.update_list.append((timestamp, update_id, movie_name, user_id, rating))
            #Database.gossip()
            return timestamp


    def check_timestamp_table(self, timestamp, update_id):
        print("Update id: " + str(update_id))
        found = True
        for used_timestamp_list in Database.timestamp_table:
            if timestamp in used_timestamp_list:
                print("FOUND!")
                continue
            print("Making found False")
            found = False

        print(found)
        if found:
            print(Database.update_list)
            # find timestamp and remove on index
            for i in range(len(Database.update_list)):
                if Database.update_list[i][1] == update_id:
                    print("Should be more: " + str(Database.update_list))
                    del Database.update_list[i]
                    print("Should be less: " + str(Database.update_list))
                    return found
        return found


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


    @staticmethod
    def gossip():
        print(Database.update_list)
        print("Gossip Called")
        Database.update_list = sorted(Database.update_list, key=sort_tuple)
        print(Database.update_list)
        for item in Database.update_list:
            if item[1] not in Database.executed_updates:
            #if item[0][this_server_num] == Database.value_timestamp[this_server_num] + 1:
                Database.add_rating(0, item[2], item[3], item[4])
                Database.executed_updates.append(item[1])
                Database.all_updates.append((item[0], item[1], item[2], item[3], item[4]))
                print(Database.timestamp_table)
                Database.timestamp_table[this_server_num].append(item[0])
                #Database.check_timestamp_table(0, item[0], item[1])
                print(Database.timestamp_table)
                Database.value_timestamp[this_server_num] += 1

        print("New Gossip Update")


        for item in Database.update_list:
            server_list = get_server_list()
            print(server_list)
            for other_server in server_list:
                print("Sending to other server")
                print("this server num: " + str(this_server_num))
                other_timestamp = other_server.new_update(item[0], item[1], item[2], item[3], item[4], True, this_server_num)

        for item in Database.update_list:
            Database.check_timestamp_table(0, item[0], item[1])
        # print("Should be different + " + str(Database.average_rating("Horns")))
        threading.Timer(5, Database.gossip).start()
        print("Returning from Gossip")



def sort_tuple(item):
    #print("Sorting Tuple")
    return item[0][this_server_num]

def get_server_list():
    server_dict = name_server.list(prefix="ratings.database.")
    server_list = []
    for item in server_dict.values():
        if str(item) != str(uri):
            server = Pyro4.Proxy(item)
            if server.get_status() == "online":
                #print("Adding server")
                server_list.append(server)
    #print("Server List = " + str(server_list))
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



threading.Timer(5, Database.gossip).start()
daemon.requestLoop()


print("Loop Stopped")


"""
Giving other servers access to one another

Update log greater than size 10, can't accept anything - call - overloaded -

"""
