import Pyro4



user_id = input("Please enter your user ID: ")
while user_id == "":
    print("Cannot input empty string")
    user_id = input("Please enter your user ID: ")
user_id = user_id.lower()


#TODO when to connect to server?
with Pyro4.locateNS() as name_server:
    uri = name_server.lookup("nameServer")

front_end_server = Pyro4.Proxy(uri)
try:
    server = front_end_server.choose_server()

except:
    print("Couldn't find a server online")

#TODO - Delete this at the end
rating_horns = server.find_movie("Horns")
print(rating_horns)

already_rated = False
current_rating = None

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
            current_rating = server.get_user_rating(movie_name, user_id)
            already_rated = True
            break
        else:
            break




def run_instruction(instruction, current_rating):

    #update a users rating in server database
    if instruction == "update":
        print("Current rating is currently" + str(current_rating))
        while True:
            try:
                user_rating = float(input('Please enter an updating rating for the movie ' + movie_name
                                          + ', your current rating is ' + str(current_rating) + ': '))
                if user_rating < 0 or user_rating > 10:
                    raise ValueError
                break
            except ValueError:
                print("Invalid rating. The rating must be in the range 0-10.")
        server.add_rating(movie_name, user_id, user_rating)

    #return the average rating for a given film in server
    elif instruction == "average":
        print(server.average_rating(movie_name))

    #add a rating to a movie in the database
    elif instruction == "add":
        while True:
            try:
                user_rating = float(input('Please enter a rating for the movie ' + movie_name + ': '))
                if user_rating < 0 or user_rating > 10:
                    raise ValueError
                break
            except ValueError:
                print("Invalid rating. The rating must be in the range 0-10.")
        server.add_rating(movie_name, user_id, user_rating)
    else:
        print("No Valid input entered")




if already_rated:
    instruction = input("Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "":
        instruction = input(
            "Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()
    print(current_rating)
    run_instruction(instruction, current_rating)
else:
    instruction = input("Would you like to add a rating (add) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "":
        instruction = input("Would you like to add a rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()
    run_instruction(instruction, current_rating)






