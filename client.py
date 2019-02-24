import Pyro4





with Pyro4.locateNS() as name_server:
    uri = name_server.lookup("nameServer")

front_end_server = Pyro4.Proxy(uri)
try:
    server = front_end_server.choose_server()
except:
    print("Couldn't Choose Server")







user_id = input("Please enter your user ID: ")
while user_id == "":
    print("Cannot input empty string")
    user_id = input("Please enter your user ID: ")
user_id = user_id.lower()


#update a movie
movie_name = input("What movie would you like to open?: ")
while movie_name == "":
    print("Cannot input empty string")
    movie_name = input("What movie would you like to open?: ")
movie_name = movie_name.lower()

already_rated = True

if already_rated:
    instruction = input("Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "" or instruction != "update" or instruction != "average":
        instruction = input("Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()


if already_rated:
    instruction = input("Would you like to add a rating (update) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "" or instruction != "add" or instruction != "average":
        instruction = input("Would you like to add a rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()







