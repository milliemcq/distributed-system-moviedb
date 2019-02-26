import Pyro4
import read_update_csv as data
import sys

status = "online"

rating_dict = data.movie_rating_dict
id_dict = data.movie_id_dict

# retrieve, submit and update movie ratings
@Pyro4.behavior(instance_mode = "single")
@Pyro4.expose
class Database:
    ratings = rating_dict

    def update_movie_rating(self, movie, id, user_id):
        #TODO updates movie rating
        return

    def get_movie_rating(self, movie):
        #TODO return movie rating for given film
        return

    def get_my_movie_rating(self, movie, user_id):
        pass

    def go_offline(self):
        Database.status = "offline"

    def overload(self):
        Database.status = "overload"

    def online(self):
        Database.status = "online"

    def increment_counter(self):
        Database.counter += 1

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

    def get_rating_dict(self):
        return rating_dict


def update_status(self):

        pass


daemon = Pyro4.Daemon()
uri = daemon.register(Database)

with Pyro4.locateNS() as name_server:
    name_server.register("ratings.database." + str(uri), uri, safe=True)


print("Server Ready: Object URI = " + str(uri))
sys.excepthook = Pyro4.util.excepthook
daemon.requestLoop()


