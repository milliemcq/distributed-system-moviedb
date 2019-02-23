import csv


movie_id_dict = {}
movie_rating_dict = {}


#parse the ID/Title file so we can see which movie has which ID
with open('movies.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_row = True
    for row in csv_reader:
        #print(row)
        if first_row:
            first_row = False
        else:
            if row[0] not in movie_id_dict:
                movie_id_dict[row[0]] = row[1][:-7]


"""userId,movieId,rating,timestamp"""

with open('ratings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_row = True
    for row in csv_reader:
        if first_row:
            first_row = False
        else:
            movie_title = movie_id_dict[row[1]]
            if movie_title not in movie_rating_dict:
                ratings_user_dict = {row[0]: float(row[2])}
                movie_rating_dict[movie_title] = ratings_user_dict
            else:
                movie_rating_dict[movie_title][row[0]] = float(row[2])


def add_rating(movie_title, rating):
    if movie_title in movie_rating_dict:
        movie_rating_dict[movie_title].append(rating)
    else:
        return "Could not find Movie with that title"

def average_rating(movie_title):
    if movie_title in movie_rating_dict:
        total = 0
        number_ratings = 0
        for item in movie_rating_dict[movie_title]:
            total += item
            number_ratings += 1
        return total/number_ratings

    return "Could not find movie with that title"


print(movie_id_dict)
print(movie_rating_dict)