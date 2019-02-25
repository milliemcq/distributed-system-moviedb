import Pyro4



user_id = input("Please enter your user ID: ")
while user_id == "":
    print("Cannot input empty string")
    user_id = input("Please enter your user ID: ")
user_id = user_id.lower()


with Pyro4.locateNS() as name_server:
    uri = name_server.lookup("nameServer")

front_end_server = Pyro4.Proxy(uri)
try:
    server = front_end_server.choose_server()

except:
    print("Couldn't Choose Server")




ratings = server.get_rating_dict()

print(ratings)

already_rated = False

while True:
    movie_name = input("What movie would you like to open?: ")
    while movie_name == "":
        print("Cannot input empty string")
        movie_name = input("What movie would you like to open?: ")

    movie_dict = server.find_movie(movie_name)
    if movie_dict == "No movie found":
        print("That movie couldn't be found in our Database")
        #TODO would you like to add it?
        continue
    else:
        if user_id in movie_dict:
            print("Making Already Rated True")
            already_rated = True
            break
        else:
            break



if already_rated:
    instruction = input("Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "" or instruction != "update" or instruction != "average":
        instruction = input(
            "Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()
else:
    instruction = input("Would you like to add a rating (add) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "" or instruction != "add" or instruction != "average":
        instruction = input("Would you like to add a rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()



#update a movie
def update_movie(movie_title):











