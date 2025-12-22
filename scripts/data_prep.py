import pandas as pd
import numpy as np
import json
from itertools import combinations
from collections import Counter
import os

# Ensure directories exist
os.makedirs('data/processed', exist_ok=True)

# LOAD DATA
# Make sure your raw files are in 'data/raw/' or adjust the path below
try:
    credits_df = pd.read_csv('data/raw/tmdb_5000_credits.csv')
    movies_df = pd.read_csv('data/raw/tmdb_5000_movies.csv')
except FileNotFoundError:
    print("Error: Could not find raw files. Please check paths 'data/raw/tmdb_5000_credits.csv'")
    # Fallback for flat structure
    credits_df = pd.read_csv('tmdb_5000_credits.csv')
    movies_df = pd.read_csv('tmdb_5000_movies.csv')

# MERGE DATASETS
movies_df = movies_df.rename(columns={'id': 'movie_id'})
credits_df_clean = credits_df.drop(columns=['title'])
merged_df = movies_df.merge(credits_df_clean, on='movie_id')

# PARSE JSON COLUMNS
def parse_json_col(df, col_name, key_name='name'):
    try:
        return df[col_name].apply(lambda x: [i[key_name] for i in json.loads(x)] if isinstance(x, str) else [])
    except Exception as e:
        return df[col_name]

json_cols = ['genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages']
for col in json_cols:
    merged_df[col] = parse_json_col(merged_df, col)

# PARSE CREW (Director) & CAST
def get_director(x):
    if isinstance(x, str):
        x = json.loads(x)
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_top_3_cast(x):
    if isinstance(x, str):
        x = json.loads(x)
    if isinstance(x, list):
        names = [i['name'] for i in x]
        return names[:3]
    return []

merged_df['director'] = merged_df['crew'].apply(get_director)
merged_df['top_cast'] = merged_df['cast'].apply(get_top_3_cast)

# DATES
merged_df['release_date'] = pd.to_datetime(merged_df['release_date'])
merged_df['release_year'] = merged_df['release_date'].dt.year

# ---------------------------------------------------------
# GENERATE OUTPUT TABLES
# ---------------------------------------------------------

# 1. Main Movie Table
main_df = merged_df.dropna(subset=['release_date']).copy()
main_df['is_financial_valid'] = ((main_df['budget'] > 1000) & (main_df['revenue'] > 1000)).astype(int)

main_cols = ['movie_id', 'title', 'budget', 'revenue', 'popularity', 'vote_average', 'vote_count', 
             'runtime', 'release_date', 'release_year', 'director', 'original_language', 'is_financial_valid']
cleaned_movies = main_df[main_cols]

# 2. Movie Genres (One-to-Many)
movie_genres = merged_df[['movie_id', 'genres']].explode('genres').rename(columns={'genres': 'genre'}).dropna()
movie_genres = movie_genres[movie_genres['movie_id'].isin(cleaned_movies['movie_id'])]

# 3. Movie Countries (One-to-Many)
movie_countries = merged_df[['movie_id', 'production_countries']].explode('production_countries').rename(columns={'production_countries': 'country'}).dropna()
movie_countries = movie_countries[movie_countries['movie_id'].isin(cleaned_movies['movie_id'])]

# 4. Movie Cast (Top 3)
movie_cast = merged_df[['movie_id', 'top_cast']].explode('top_cast').rename(columns={'top_cast': 'actor'}).dropna()
movie_cast = movie_cast[movie_cast['movie_id'].isin(cleaned_movies['movie_id'])]

# 5. Actor Network (Graph Nodes/Edges)
top_actors = movie_cast['actor'].value_counts().head(100).index.tolist()
filtered_cast = movie_cast[movie_cast['actor'].isin(top_actors)]

actor_pairs = []
for movie, group in filtered_cast.groupby('movie_id'):
    actors = sorted(group['actor'].unique())
    if len(actors) > 1:
        actor_pairs.extend(combinations(actors, 2))

pair_counts = Counter(actor_pairs)
network_df = pd.DataFrame(pair_counts.items(), columns=['pair', 'weight'])
if not network_df.empty:
    network_df[['source', 'target']] = pd.DataFrame(network_df['pair'].tolist(), index=network_df.index)
    network_df = network_df.drop(columns=['pair'])
else:
    network_df = pd.DataFrame(columns=['source', 'target', 'weight'])

# 6. Correlation Matrix (Heatmap)
corr_cols = ['budget', 'revenue', 'popularity', 'vote_average', 'vote_count', 'runtime']
corr_matrix = cleaned_movies[corr_cols].corr()
corr_melted = corr_matrix.reset_index().melt(id_vars='index', var_name='variable_2', value_name='correlation').rename(columns={'index': 'variable_1'})

# ---------------------------------------------------------
# SAVE FILES
# ---------------------------------------------------------
output_path = 'data/processed/'

cleaned_movies.to_csv(f'{output_path}cleaned_movies.csv', index=False)
movie_genres.to_csv(f'{output_path}movie_genres.csv', index=False)
movie_countries.to_csv(f'{output_path}movie_countries.csv', index=False)
movie_cast.to_csv(f'{output_path}movie_cast.csv', index=False)
network_df.to_csv(f'{output_path}actor_network.csv', index=False)
corr_melted.to_csv(f'{output_path}correlation_matrix.csv', index=False)

print("SUCCESS: 6 CSV files generated in 'data/processed/'")