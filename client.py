import Pyro4

artist_name = input("Please give me the name of a movie: ")
    while artist_name == "":
        print("Cannot input empty string")
        artist_name = input("Please give me the name of an artist: ")
    artist_name = artist_name.lower()



