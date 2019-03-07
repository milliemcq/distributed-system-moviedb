import Pyro4




print("Welcome to the Gossip Architecture movie rating system!")



#Get the user ID and return as lowercase
user_id = input("Please enter your user ID: ")
while user_id == "":
    print("Cannot input empty string")
    user_id = input("Please enter your user ID: ")

user_id = user_id.strip()


#Connecting to the front end server
with Pyro4.locateNS() as name_server:
    uri = name_server.lookup("frontEnd")

front_end_server = Pyro4.Proxy(uri)


#print("Rating: " + str(front_end_server.get_user_rating('1', "Horns")))



def run_instruction(instruction):
    #return the average rating for a given film in server
    if instruction == "average":
        average_rating = str(str((front_end_server.average_rating(movie_name))))
        print("Average rating for " + movie_name + " is: " + average_rating)

    #add a rating to a movie in the database
    elif instruction == "add" or instruction == "update":
        while True:
            try:
                user_rating = float(input('Please enter a rating for the movie ' + movie_name + ': '))
                if user_rating < 0 or user_rating > 10:
                    raise ValueError
                break
            except ValueError:
                print("Invalid rating. The rating must be in the range 0-10.")
        front_end_server.add_movie_rating(movie_name, user_id, user_rating)
    else:
        print("No Valid input entered")


instruction = ""
while instruction != "quit":
    movie_name = ""
    instruction = ""
    movie_name = input("What movie would you like to open?: ")
    while movie_name == "":
        print("Cannot input empty string")
        movie_name = input("What movie would you like to open?: ")

    movie_name.strip()

    current_rating = front_end_server.get_user_rating(user_id, movie_name)
    if current_rating == "No Rating":
        print("You have not yet entered a rating for this movie.")
    elif current_rating == "Behind":
        print("No Current Server available to check current rating")
    else:
        print("Your current rating for this movie is: " + str(current_rating))


    instruction = input("Would you like to add/update a rating (add/update) or view the average rating for this movie? (average)? ")
    instruction = instruction.lower()
    while instruction == "":
        instruction = input(
            "Would you like to update your rating (update) or view the average rating for this movie? (average)? ")
        instruction = instruction.lower()

    instruction.strip()

    run_instruction(instruction)




