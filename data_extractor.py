import os
import pandas as pd
import uuid
import dataclasses
from dataclasses import dataclass
import json
import numpy as np


@dataclass
class Person:
    id: str
    name: str
    bio: str
    profile_pic: str


@dataclass
class Movie:
    id: str
    title: str
    cast: list
    crew: list
    banner_url: str
    votes: str
    runtime: str
    additional_data: dict


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


# Path for Input files.
data_path = os.path.join(os.path.dirname(__file__), 'data')
csv_file = os.path.join(data_path, 'media.csv')

# Path for Output Files.
cast_path = os.path.join(data_path, 'cast.json')
crew_path = os.path.join(data_path, 'crew.json')
movie_path = os.path.join(data_path, 'movies.json')
df = pd.read_csv(csv_file)

df = df.dropna(subset=['Actors (S)', 'Director (S)', 'Writer (S)', 'Title (S)'])
actor_set = set()
crew_set = set()
cast = list()
crew = list()
movies = list()
df = df.replace(np.nan, '', regex=True)
for index, row in df.iterrows():
    actor_id_list = list()
    crew_id_list = list()
    # Loop for cast
    for actor in row['Actors (S)'].split(", "):
        if actor not in actor_set:
            actor_id = str(uuid.uuid4())
            cast.append(Person(actor_id, actor, "", ""))
            actor_id_list.append(actor_id)
            actor_set.add(actor)

        else:
            continue
    # Loop for crew
    for director in row['Director (S)'].split(", "):
        if director not in crew_set:
            director_id = str(uuid.uuid4())
            crew.append(Person(director_id, director, "", ""))
            crew_id_list.append(director_id)
            crew_set.add(director)
        else:
            continue
    # Loop for Crew
    for writer in row['Writer (S)'].split(", "):
        if writer not in crew_set:
            writer_id = str(uuid.uuid4())
            crew.append(Person(writer_id, writer, "", ""))
            crew_id_list.append(writer_id)
            crew_set.add(writer)
        else:
            continue
    # Logic for the populating Master movie Json.
    additional_details = {'genre': row['Genre (S)'], 'language': row['Language (S)'], 'ratings': row['Ratings (L)']}
    movie = Movie(str(uuid.uuid4()), row['Title (S)'], actor_id_list, crew_id_list, row['Poster (S)'],
                  row['imdbVotes (S)'], row['Runtime (S)'], additional_details)
    movies.append(movie)

# Cast JSON
with open(cast_path, "w") as cast_file:
    json.dump({'cast': cast}, cast_file, indent=4, cls=EnhancedJSONEncoder)
# Crew JSON
with open(crew_path, "w") as crew_file:
    json.dump({'crew': crew}, crew_file, indent=4, cls=EnhancedJSONEncoder)

# Movie JSON
with open(movie_path, "w") as movie_file:
    json.dump(movies, movie_file, indent=4, cls=EnhancedJSONEncoder)

