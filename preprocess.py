"""
Preprocessing script for TMDB 5000 Movies and Credits datasets
Prepares data for PowerBI dashboard visualization
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime

def parse_json_column(df, column_name):
    """Parse JSON string column and return list of values"""
    def extract_values(json_str):
        if pd.isna(json_str) or json_str == '':
            return []
        try:
            data = json.loads(json_str)
            if isinstance(data, list):
                return [item.get('name', '') for item in data if isinstance(item, dict)]
            return []
        except:
            return []
    return df[column_name].apply(extract_values)

def extract_director(crew_json):
    """Extract director name from crew JSON"""
    if pd.isna(crew_json) or crew_json == '':
        return None
    try:
        crew = json.loads(crew_json)
        for person in crew:
            if person.get('job') == 'Director':
                return person.get('name')
    except:
        pass
    return None

def extract_top_cast(cast_json, top_n=3):
    """Extract top N cast members from cast JSON"""
    if pd.isna(cast_json) or cast_json == '':
        return []
    try:
        cast = json.loads(cast_json)
        # Sort by order (main cast first)
        cast_sorted = sorted(cast, key=lambda x: x.get('order', 999))[:top_n]
        return [actor.get('name') for actor in cast_sorted]
    except:
        return []

def calculate_profit(row):
    """Calculate profit (revenue - budget)"""
    if pd.notna(row['revenue']) and pd.notna(row['budget']) and row['budget'] > 0:
        return row['revenue'] - row['budget']
    return None

def calculate_roi(row):
    """Calculate Return on Investment percentage"""
    if pd.notna(row['revenue']) and pd.notna(row['budget']) and row['budget'] > 0:
        return ((row['revenue'] - row['budget']) / row['budget']) * 100
    return None

def main():
    print("Loading datasets...")
    # Load datasets
    movies_df = pd.read_csv('tmdb_5000_movies.csv')
    credits_df = pd.read_csv('tmdb_5000_credits.csv')
    
    print(f"Movies dataset: {len(movies_df)} rows")
    print(f"Credits dataset: {len(credits_df)} rows")
    
    # Merge datasets on movie_id/id
    print("\nMerging datasets...")
    movies_df = movies_df.rename(columns={'id': 'movie_id'})
    # Drop title from credits to avoid conflict (use title from movies)
    credits_df_clean = credits_df.drop(columns=['title'], errors='ignore')
    merged_df = movies_df.merge(credits_df_clean, on='movie_id', how='left')
    
    print(f"Merged dataset: {len(merged_df)} rows")
    
    # Data cleaning and transformation
    print("\nCleaning and transforming data...")
    
    # Convert release_date to datetime
    merged_df['release_date'] = pd.to_datetime(merged_df['release_date'], errors='coerce')
    merged_df['release_year'] = merged_df['release_date'].dt.year
    merged_df['release_month'] = merged_df['release_date'].dt.month
    merged_df['release_month_name'] = merged_df['release_date'].dt.strftime('%B')
    
    # Extract director
    merged_df['director'] = merged_df['crew'].apply(extract_director)
    
    # Extract top 3 cast members
    merged_df['top_cast'] = merged_df['cast'].apply(lambda x: extract_top_cast(x, 3))
    merged_df['lead_actor'] = merged_df['top_cast'].apply(lambda x: x[0] if len(x) > 0 else None)
    merged_df['supporting_actors'] = merged_df['top_cast'].apply(lambda x: ', '.join(x[1:]) if len(x) > 1 else None)
    
    # Parse genres
    merged_df['genres_list'] = parse_json_column(merged_df, 'genres')
    merged_df['primary_genre'] = merged_df['genres_list'].apply(lambda x: x[0] if len(x) > 0 else None)
    merged_df['all_genres'] = merged_df['genres_list'].apply(lambda x: ', '.join(x) if x else None)
    
    # Parse keywords
    merged_df['keywords_list'] = parse_json_column(merged_df, 'keywords')
    
    # Parse production companies
    merged_df['production_companies_list'] = parse_json_column(merged_df, 'production_companies')
    merged_df['primary_production_company'] = merged_df['production_companies_list'].apply(lambda x: x[0] if len(x) > 0 else None)
    
    # Parse production countries
    merged_df['production_countries_list'] = parse_json_column(merged_df, 'production_countries')
    merged_df['primary_production_country'] = merged_df['production_countries_list'].apply(lambda x: x[0] if len(x) > 0 else None)
    
    # Parse spoken languages
    merged_df['spoken_languages_list'] = parse_json_column(merged_df, 'spoken_languages')
    
    # Calculate derived metrics
    print("\nCalculating derived metrics...")
    merged_df['profit'] = merged_df.apply(calculate_profit, axis=1)
    merged_df['roi_percentage'] = merged_df.apply(calculate_roi, axis=1)
    
    # Create budget and revenue categories
    merged_df['budget_category'] = pd.cut(
        merged_df['budget'],
        bins=[0, 1000000, 10000000, 50000000, float('inf')],
        labels=['Low (<$1M)', 'Medium ($1M-$10M)', 'High ($10M-$50M)', 'Very High (>$50M)']
    )
    
    merged_df['revenue_category'] = pd.cut(
        merged_df['revenue'],
        bins=[0, 1000000, 10000000, 100000000, 1000000000, float('inf')],
        labels=['Low (<$1M)', 'Medium ($1M-$10M)', 'High ($10M-$100M)', 'Very High ($100M-$1B)', 'Blockbuster (>$1B)']
    )
    
    # Create success indicator
    merged_df['is_profitable'] = merged_df['profit'] > 0
    merged_df['is_high_rated'] = merged_df['vote_average'] >= 7.0
    merged_df['is_popular'] = merged_df['popularity'] >= merged_df['popularity'].median()
    
    # Create decade field (handle nulls properly)
    merged_df['decade'] = merged_df['release_year'].apply(
        lambda x: (int(x) // 10) * 10 if pd.notna(x) and not pd.isna(x) and x > 0 else 0
    )
    merged_df['decade_label'] = merged_df['decade'].apply(
        lambda x: f"{int(x)}s" if x > 0 else 'Unknown'
    )
    
    # Create rating categories
    def categorize_rating(rating):
        if pd.isna(rating):
            return 'Not Rated'
        elif rating >= 8.0:
            return 'Excellent (8.0+)'
        elif rating >= 7.0:
            return 'Good (7.0-7.9)'
        elif rating >= 6.0:
            return 'Average (6.0-6.9)'
        elif rating >= 5.0:
            return 'Below Average (5.0-5.9)'
        else:
            return 'Poor (<5.0)'
    
    merged_df['rating_category'] = merged_df['vote_average'].apply(categorize_rating)
    
    # Create blockbuster indicator
    merged_df['is_blockbuster'] = merged_df['revenue'] >= 1000000000
    
    # Calculate budget efficiency (revenue per dollar of budget)
    merged_df['budget_efficiency'] = merged_df.apply(
        lambda row: row['revenue'] / row['budget'] if pd.notna(row['budget']) and row['budget'] > 0 else None,
        axis=1
    )
    
    # Create success score (composite metric)
    # Normalize rating (0-10 scale), profitability, and popularity
    max_rating = merged_df['vote_average'].max()
    max_popularity = merged_df['popularity'].max()
    max_profit = merged_df['profit'].max()
    
    def calculate_success_score(row):
        score = 0
        # Rating component (40% weight)
        if pd.notna(row['vote_average']):
            score += (row['vote_average'] / 10) * 40
        
        # Profitability component (40% weight)
        if pd.notna(row['profit']) and max_profit > 0:
            normalized_profit = max(0, row['profit'] / max_profit)
            score += normalized_profit * 40
        
        # Popularity component (20% weight)
        if pd.notna(row['popularity']) and max_popularity > 0:
            normalized_pop = row['popularity'] / max_popularity
            score += normalized_pop * 20
        
        return round(score, 2)
    
    merged_df['success_score'] = merged_df.apply(calculate_success_score, axis=1)
    
    # Create success tier
    def categorize_success(score):
        if pd.isna(score):
            return 'Unknown'
        elif score >= 70:
            return 'Blockbuster'
        elif score >= 50:
            return 'Successful'
        elif score >= 30:
            return 'Moderate'
        else:
            return 'Underperforming'
    
    merged_df['success_tier'] = merged_df['success_score'].apply(categorize_success)
    
    # Create revenue per vote (engagement metric)
    merged_df['revenue_per_vote'] = merged_df.apply(
        lambda row: row['revenue'] / row['vote_count'] if pd.notna(row['vote_count']) and row['vote_count'] > 0 else None,
        axis=1
    )
    
    # Select and order columns for main movies table
    movies_columns = [
        'movie_id', 'title', 'release_date', 'release_year', 'release_month', 'release_month_name',
        'decade', 'decade_label',
        'director', 'lead_actor', 'supporting_actors',
        'primary_genre', 'all_genres', 'primary_production_company', 'primary_production_country',
        'budget', 'revenue', 'profit', 'roi_percentage', 'budget_efficiency', 'revenue_per_vote',
        'budget_category', 'revenue_category',
        'runtime', 'popularity', 'vote_average', 'vote_count', 'rating_category',
        'is_profitable', 'is_high_rated', 'is_popular', 'is_blockbuster',
        'success_score', 'success_tier',
        'status', 'tagline', 'overview'
    ]
    
    movies_table = merged_df[movies_columns].copy()
    
    # Comprehensive null handling for PowerBI compatibility
    print("\nHandling null values for PowerBI compatibility...")
    
    # Handle date-related nulls
    movies_table['release_year'] = movies_table['release_year'].fillna(0).astype(int)
    movies_table['release_month'] = movies_table['release_month'].fillna(0).astype(int)
    movies_table['release_month_name'] = movies_table['release_month_name'].fillna('Unknown')
    
    # Handle decade nulls
    movies_table['decade'] = movies_table['decade'].fillna(0).astype(int)
    # Fix decade_label - if decade is 0, set to Unknown
    movies_table['decade_label'] = movies_table.apply(
        lambda row: 'Unknown' if row['decade'] == 0 else f"{int(row['decade'])}s",
        axis=1
    )
    
    # Handle string nulls - replace None with empty string or "Unknown"
    string_columns = ['director', 'lead_actor', 'supporting_actors', 'primary_genre', 
                      'all_genres', 'primary_production_company', 'primary_production_country',
                      'status', 'tagline', 'overview', 'rating_category', 'success_tier']
    for col in string_columns:
        if col in movies_table.columns:
            movies_table[col] = movies_table[col].fillna('Unknown' if col in ['director', 'primary_genre', 'primary_production_company', 'primary_production_country', 'status', 'rating_category', 'success_tier'] else '')
    
    # Handle categorical nulls from pd.cut
    movies_table['budget_category'] = movies_table['budget_category'].cat.add_categories(['Unknown']).fillna('Unknown')
    movies_table['revenue_category'] = movies_table['revenue_category'].cat.add_categories(['Unknown']).fillna('Unknown')
    
    # Handle boolean nulls - convert to False
    boolean_columns = ['is_profitable', 'is_high_rated', 'is_popular', 'is_blockbuster']
    for col in boolean_columns:
        if col in movies_table.columns:
            movies_table[col] = movies_table[col].fillna(False).astype(bool)
    
    # Handle numeric nulls - fill with 0 for financial metrics, NaN for others
    numeric_fill_zero = ['budget', 'revenue', 'profit', 'runtime', 'popularity', 'vote_count']
    for col in numeric_fill_zero:
        if col in movies_table.columns:
            movies_table[col] = movies_table[col].fillna(0).astype(float)
    
    # Handle percentage/ratio nulls - fill with 0
    ratio_columns = ['roi_percentage', 'budget_efficiency', 'revenue_per_vote', 'vote_average', 'success_score']
    for col in ratio_columns:
        if col in movies_table.columns:
            movies_table[col] = movies_table[col].fillna(0.0).astype(float)
    
    # Ensure movie_id and title are never null
    movies_table['movie_id'] = movies_table['movie_id'].fillna(0).astype(int)
    movies_table['title'] = movies_table['title'].fillna('Unknown Movie')
    
    # Handle release_date - keep as datetime but fill NaT with a default date
    if 'release_date' in movies_table.columns:
        movies_table['release_date'] = pd.to_datetime(movies_table['release_date'], errors='coerce')
        # Fill NaT with a default date (1900-01-01) for PowerBI compatibility
        movies_table['release_date'] = movies_table['release_date'].fillna(pd.Timestamp('1900-01-01'))
    
    print(f"  - Fixed {movies_table.isnull().sum().sum()} null values")
    
    # Create genres dimension table
    print("\nCreating genres dimension table...")
    genres_data = []
    for idx, row in merged_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        for genre in row['genres_list']:
            genres_data.append({
                'movie_id': movie_id,
                'title': title,
                'genre': genre
            })
    genres_table = pd.DataFrame(genres_data)
    # Handle nulls in genres table
    if len(genres_table) > 0:
        genres_table['movie_id'] = genres_table['movie_id'].fillna(0).astype(int)
        genres_table['title'] = genres_table['title'].fillna('Unknown Movie')
        genres_table['genre'] = genres_table['genre'].fillna('Unknown')
        # Remove empty genres
        genres_table = genres_table[genres_table['genre'] != '']
    
    # Create keywords dimension table
    print("Creating keywords dimension table...")
    keywords_data = []
    for idx, row in merged_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        for keyword in row['keywords_list']:
            keywords_data.append({
                'movie_id': movie_id,
                'title': title,
                'keyword': keyword
            })
    keywords_table = pd.DataFrame(keywords_data)
    # Handle nulls in keywords table
    if len(keywords_table) > 0:
        keywords_table['movie_id'] = keywords_table['movie_id'].fillna(0).astype(int)
        keywords_table['title'] = keywords_table['title'].fillna('Unknown Movie')
        keywords_table['keyword'] = keywords_table['keyword'].fillna('Unknown')
        # Remove empty keywords
        keywords_table = keywords_table[keywords_table['keyword'] != '']
    
    # Create production companies dimension table
    print("Creating production companies dimension table...")
    companies_data = []
    for idx, row in merged_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        for company in row['production_companies_list']:
            companies_data.append({
                'movie_id': movie_id,
                'title': title,
                'production_company': company
            })
    companies_table = pd.DataFrame(companies_data)
    # Handle nulls in companies table
    if len(companies_table) > 0:
        companies_table['movie_id'] = companies_table['movie_id'].fillna(0).astype(int)
        companies_table['title'] = companies_table['title'].fillna('Unknown Movie')
        companies_table['production_company'] = companies_table['production_company'].fillna('Unknown')
        # Remove empty companies
        companies_table = companies_table[companies_table['production_company'] != '']
    
    # Create cast dimension table (top 10 cast per movie)
    print("Creating cast dimension table...")
    cast_data = []
    for idx, row in merged_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        if pd.notna(row['cast']) and row['cast'] != '':
            try:
                cast = json.loads(row['cast'])
                cast_sorted = sorted(cast, key=lambda x: x.get('order', 999))[:10]
                for actor in cast_sorted:
                    cast_data.append({
                        'movie_id': movie_id,
                        'title': title,
                        'actor_name': actor.get('name'),
                        'character': actor.get('character'),
                        'cast_order': actor.get('order'),
                        'gender': actor.get('gender')
                    })
            except:
                pass
    cast_table = pd.DataFrame(cast_data)
    # Handle nulls in cast table
    if len(cast_table) > 0:
        cast_table['movie_id'] = cast_table['movie_id'].fillna(0).astype(int)
        cast_table['title'] = cast_table['title'].fillna('Unknown Movie')
        cast_table['actor_name'] = cast_table['actor_name'].fillna('Unknown Actor')
        cast_table['character'] = cast_table['character'].fillna('Unknown Character')
        cast_table['cast_order'] = cast_table['cast_order'].fillna(999).astype(int)
        cast_table['gender'] = cast_table['gender'].fillna(0).astype(int)
        # Remove rows with unknown actors
        cast_table = cast_table[cast_table['actor_name'] != 'Unknown Actor']
    
    # Create crew dimension table (directors, producers, writers)
    print("Creating crew dimension table...")
    crew_data = []
    for idx, row in merged_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        if pd.notna(row['crew']) and row['crew'] != '':
            try:
                crew = json.loads(row['crew'])
                important_jobs = ['Director', 'Producer', 'Executive Producer', 'Writer', 'Screenplay', 'Original Music Composer']
                for person in crew:
                    if person.get('job') in important_jobs:
                        crew_data.append({
                            'movie_id': movie_id,
                            'title': title,
                            'crew_name': person.get('name'),
                            'job': person.get('job'),
                            'department': person.get('department')
                        })
            except:
                pass
    crew_table = pd.DataFrame(crew_data)
    # Handle nulls in crew table
    if len(crew_table) > 0:
        crew_table['movie_id'] = crew_table['movie_id'].fillna(0).astype(int)
        crew_table['title'] = crew_table['title'].fillna('Unknown Movie')
        crew_table['crew_name'] = crew_table['crew_name'].fillna('Unknown')
        crew_table['job'] = crew_table['job'].fillna('Unknown')
        crew_table['department'] = crew_table['department'].fillna('Unknown')
        # Remove rows with unknown crew
        crew_table = crew_table[crew_table['crew_name'] != 'Unknown']
    
    # Save to CSV files with proper null handling
    print("\nSaving preprocessed data...")
    # Use na_rep='' for empty strings instead of 'nan' or 'None'
    movies_table.to_csv('movies_cleaned.csv', index=False, encoding='utf-8-sig', na_rep='')
    print(f"[OK] Saved movies_cleaned.csv ({len(movies_table)} rows)")
    
    if len(genres_table) > 0:
        genres_table.to_csv('genres_dimension.csv', index=False, encoding='utf-8-sig', na_rep='')
        print(f"[OK] Saved genres_dimension.csv ({len(genres_table)} rows)")
    
    if len(keywords_table) > 0:
        keywords_table.to_csv('keywords_dimension.csv', index=False, encoding='utf-8-sig', na_rep='')
        print(f"[OK] Saved keywords_dimension.csv ({len(keywords_table)} rows)")
    
    if len(companies_table) > 0:
        companies_table.to_csv('production_companies_dimension.csv', index=False, encoding='utf-8-sig', na_rep='')
        print(f"[OK] Saved production_companies_dimension.csv ({len(companies_table)} rows)")
    
    if len(cast_table) > 0:
        cast_table.to_csv('cast_dimension.csv', index=False, encoding='utf-8-sig', na_rep='')
        print(f"[OK] Saved cast_dimension.csv ({len(cast_table)} rows)")
    
    if len(crew_table) > 0:
        crew_table.to_csv('crew_dimension.csv', index=False, encoding='utf-8-sig', na_rep='')
        print(f"[OK] Saved crew_dimension.csv ({len(crew_table)} rows)")
    
    # Create summary statistics
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"\nTotal Movies: {len(movies_table)}")
    
    # Safe date range calculation
    valid_years = movies_table[movies_table['release_year'] > 0]['release_year']
    if len(valid_years) > 0:
        print(f"Date Range: {valid_years.min():.0f} - {valid_years.max():.0f}")
    else:
        print("Date Range: Unknown")
    
    print(f"\nFinancial Metrics:")
    print(f"  Total Budget: ${movies_table['budget'].sum()/1e9:.2f}B")
    print(f"  Total Revenue: ${movies_table['revenue'].sum()/1e9:.2f}B")
    print(f"  Total Profit: ${movies_table['profit'].sum()/1e9:.2f}B")
    
    # Safe ROI calculation
    valid_roi = movies_table[movies_table['roi_percentage'] != 0]['roi_percentage']
    if len(valid_roi) > 0:
        print(f"  Average ROI: {valid_roi.mean():.1f}%")
    else:
        print(f"  Average ROI: 0.0%")
    
    print(f"  Profitable Movies: {movies_table['is_profitable'].sum()} ({movies_table['is_profitable'].sum()/len(movies_table)*100:.1f}%)")
    print(f"\nRating Metrics:")
    
    # Safe rating calculation
    valid_ratings = movies_table[movies_table['vote_average'] > 0]['vote_average']
    if len(valid_ratings) > 0:
        print(f"  Average Rating: {valid_ratings.mean():.2f}")
    else:
        print(f"  Average Rating: 0.00")
    
    print(f"  High Rated Movies (>=7.0): {movies_table['is_high_rated'].sum()} ({movies_table['is_high_rated'].sum()/len(movies_table)*100:.1f}%)")
    
    if len(genres_table) > 0:
        print(f"\nTop Genres:")
        top_genres = genres_table['genre'].value_counts().head(10)
        for genre, count in top_genres.items():
            print(f"  {genre}: {count}")
    
    print("\n" + "="*60)
    print("Preprocessing complete! Files ready for PowerBI import.")
    print("="*60)
    print("\nRecommended PowerBI Setup:")
    print("1. Import movies_cleaned.csv as the main fact table")
    print("2. Import dimension tables (genres, keywords, companies, cast, crew)")
    print("3. Create relationships: movie_id -> movie_id")
    print("4. Build visualizations using:")
    print("   - Revenue/Budget trends over time")
    print("   - Genre performance analysis")
    print("   - Director/actor performance")
    print("   - ROI and profitability metrics")
    print("   - Rating vs Revenue analysis")

if __name__ == "__main__":
    main()

