# Advanced PowerBI Dashboard Guide - IMDB Style Theme
## Data Visualization Term Project - TMDB Movies Dataset

## 🎬 Overview
This guide will help you create a **professionally advanced** and **visually stunning** PowerBI dashboard with an IMDB-inspired theme (Yellow & Black) for your Data Visualization term project.

---

## 📁 Data Files Generated

1. **movies_cleaned.csv** - Main fact table (4,803 movies)
2. **genres_dimension.csv** - Genre breakdown (12,160 rows)
3. **keywords_dimension.csv** - Keywords/tags (36,194 rows)
4. **production_companies_dimension.csv** - Production companies (13,677 rows)
5. **cast_dimension.csv** - Cast members (44,927 rows)
6. **crew_dimension.csv** - Crew members (32,061 rows)

---

## 🎨 IMDB Color Scheme & Typography

### Color Palette
- **Primary Yellow**: `#F5C518` (IMDB Yellow)
- **Black**: `#000000` (Text, borders)
- **White**: `#FFFFFF` (Backgrounds)
- **Dark Gray**: `#1A1A1A` (Alternate backgrounds)
- **Light Gray**: `#F5F5F5` (Card backgrounds)
- **Accent Yellow**: `#FFD700` (Highlights)

### Typography
- **Headings**: **Impact** (Bold, 24-32pt) - IMDB logo style
- **Subheadings**: **Arial Black** (Bold, 16-20pt)
- **Body Text**: **Arial** (Regular, 11-14pt)
- **KPI Numbers**: **Impact** (Bold, 28-36pt)

---

## 🚀 Step 1: Import Data & Apply Theme

### Import Data
1. Open PowerBI Desktop
2. Click **Get Data** → **Text/CSV**
3. Import all 6 CSV files
4. For each file:
   - **Delimiter**: Comma
   - **Data Type Detection**: Based on first 200 rows
   - Click **Load**

### Apply IMDB Theme
1. Go to **View** → **Themes** → **Browse for themes**
2. Import `IMDB_Theme.json` (simplified version - sets basic colors)
3. **Note**: The theme file sets basic colors. For complete IMDB styling, see **MANUAL_STYLING_GUIDE.md** for detailed formatting instructions.
4. Or manually set:
   - **View** → **Themes** → **Customize current theme**
   - Set colors as specified above

---

## 🔗 Step 2: Create Relationships

1. Go to **Model** view
2. Create relationships (One-to-Many):
   - `movies_cleaned[movie_id]` → `genres_dimension[movie_id]`
   - `movies_cleaned[movie_id]` → `keywords_dimension[movie_id]`
   - `movies_cleaned[movie_id]` → `production_companies_dimension[movie_id]`
   - `movies_cleaned[movie_id]` → `cast_dimension[movie_id]`
   - `movies_cleaned[movie_id]` → `crew_dimension[movie_id]`

3. Set **Cross filter direction** to **Both** for all relationships
4. Enable **Make this relationship active**

---

## 📐 Step 3: Advanced Calculated Measures (DAX)

Create these measures in the `movies_cleaned` table:

### Financial Measures
```DAX
Total Revenue = 
FORMAT(SUM(movies_cleaned[revenue]), "$#,##0.0,,B")

Total Budget = 
FORMAT(SUM(movies_cleaned[budget]), "$#,##0.0,,B")

Total Profit = 
FORMAT(SUM(movies_cleaned[profit]), "$#,##0.0,,B")

Average ROI = 
AVERAGE(movies_cleaned[roi_percentage])

Profit Margin % = 
DIVIDE(SUM(movies_cleaned[profit]), SUM(movies_cleaned[revenue]), 0) * 100

Budget Efficiency = 
DIVIDE(SUM(movies_cleaned[revenue]), SUM(movies_cleaned[budget]), 0)

Average Budget = 
AVERAGE(movies_cleaned[budget])

Average Revenue = 
AVERAGE(movies_cleaned[revenue])

Median ROI = 
MEDIAN(movies_cleaned[roi_percentage])

Top 10% Revenue = 
PERCENTILE.INC(movies_cleaned[revenue], 0.9)
```

### Rating & Quality Measures
```DAX


Weighted Average Rating = 
DIVIDE(
    SUMX(movies_cleaned, movies_cleaned[vote_average] * movies_cleaned[vote_count]),
    SUM(movies_cleaned[vote_count]),
    0
)

Total Votes = 
SUM(movies_cleaned[vote_count])

Movies Count = 
COUNTROWS(movies_cleaned)

High Rated Movies = 
CALCULATE(
    [Movies Count],
    movies_cleaned[vote_average] >= 7.0
)

Top Rated Movies = 
CALCULATE(
    [Movies Count],
    movies_cleaned[vote_average] >= 8.0
)

Rating Distribution = 
VAR AvgRating = [Average Rating]
RETURN
    SWITCH(
        TRUE(),
        AvgRating >= 8.0, "Excellent",
        AvgRating >= 7.0, "Good",
        AvgRating >= 6.0, "Average",
        "Below Average"
    )
```

### Performance Metrics
```DAX
Profitable Movies = 
CALCULATE(
    [Movies Count],
    movies_cleaned[is_profitable] = TRUE()
)

Profitability Rate = 
DIVIDE([Profitable Movies], [Movies Count], 0) * 100

High ROI Movies = 
CALCULATE(
    [Movies Count],
    movies_cleaned[roi_percentage] > 100
)

Blockbuster Movies = 
CALCULATE(
    [Movies Count],
    movies_cleaned[revenue] >= 1000000000
)

Success Score = 
([Average Rating] * 10) + 
([Profitability Rate] / 10) + 
(LOG([Average Revenue], 10) * 10)
```

### Time-Based Measures
```DAX
Movies This Year = 
CALCULATE(
    [Movies Count],
    YEAR(movies_cleaned[release_date]) = YEAR(TODAY())
)

Revenue YoY Growth = 
VAR CurrentYear = YEAR(TODAY())
VAR PreviousYear = CurrentYear - 1
VAR CurrentRevenue = 
    CALCULATE(
        SUM(movies_cleaned[revenue]),
        YEAR(movies_cleaned[release_date]) = CurrentYear
    )
VAR PreviousRevenue = 
    CALCULATE(
        SUM(movies_cleaned[revenue]),
        YEAR(movies_cleaned[release_date]) = PreviousYear
    )
RETURN
    DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0) * 100

Decade Average Revenue = 
AVERAGEX(
    VALUES(movies_cleaned[release_year]),
    CALCULATE(SUM(movies_cleaned[revenue]))
)
```

### Genre Performance Measures
```DAX
Top Genre by Revenue = 
VAR GenreRevenue = 
    ADDCOLUMNS(
        VALUES(genres_dimension[genre]),
        "Revenue", CALCULATE(SUM(movies_cleaned[revenue]))
    )
VAR MaxRevenue = MAXX(GenreRevenue, [Revenue])
VAR TopGenre = 
    FILTER(GenreRevenue, [Revenue] = MaxRevenue)
RETURN
    MAXX(TopGenre, genres_dimension[genre])

Genre Revenue Share = 
DIVIDE(
    SUM(movies_cleaned[revenue]),
    CALCULATE(
        SUM(movies_cleaned[revenue]),
        ALL(genres_dimension[genre])
    ),
    0
) * 100
```

### Director/Actor Performance
```DAX
Director Average Revenue = 
CALCULATE(
    AVERAGE(movies_cleaned[revenue]),
    ALLEXCEPT(movies_cleaned, movies_cleaned[director])
)

Top Director = 
VAR DirectorStats = 
    ADDCOLUMNS(
        VALUES(movies_cleaned[director]),
        "AvgRevenue", [Director Average Revenue],
        "MovieCount", CALCULATE([Movies Count])
    )
VAR TopDirector = 
    TOPN(1, DirectorStats, [AvgRevenue], DESC)
RETURN
    MAXX(TopDirector, movies_cleaned[director])
```

---

## 🎬 Step 4: Advanced Dashboard Design

### Page 1: Executive Overview (IMDB Style Header)

#### Header Design
```
┌─────────────────────────────────────────────────────────────┐
│  [IMDB LOGO STYLE]  MOVIE ANALYTICS DASHBOARD                │
│  Background: Black (#000000)                                 │
│  Text: Yellow (#F5C518), Font: Impact, 32pt                 │
│  Subtitle: "Comprehensive Movie Performance Analysis"         │
│  Font: Arial, 14pt, White                                   │
└─────────────────────────────────────────────────────────────┘
```

#### Layout Structure:
```
┌─────────────────────────────────────────────────────────────┐
│  [IMDB Header with Logo Style]                               │
└─────────────────────────────────────────────────────────────┘
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Movies │ Total Revenue│ Total Budget │ Total Profit │
│   (KPI Card) │   (KPI Card) │   (KPI Card) │   (KPI Card) │
│  Yellow bg   │  Yellow bg   │  Yellow bg   │  Yellow bg   │
└──────────────┴──────────────┴──────────────┴──────────────┘
┌─────────────────────────────────────────────────────────────┐
│  Revenue & Budget Trend (Area Chart with Gradient)           │
│  Background: Dark Gray (#1A1A1A)                             │
└─────────────────────────────────────────────────────────────┘
┌──────────────────────┬──────────────────────────────────────┐
│  Top 10 Genres by    │  Profitability Matrix                │
│  Revenue (Bar Chart) │  (Heatmap/Matrix)                    │
└──────────────────────┴──────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  Top 20 Movies by Revenue (Table with Conditional Formatting)│
└─────────────────────────────────────────────────────────────┘
```

#### Visualizations:

1. **IMDB-Style Header** (Text Box)
   - **Background**: Black (#000000)
   - **Text**: "MOVIE ANALYTICS DASHBOARD"
   - **Font**: Impact, 32pt, Yellow (#F5C518)
   - **Subtitle**: "Comprehensive Movie Performance Analysis"
   - **Font**: Arial, 14pt, White

2. **KPI Cards** (4 Cards - Top Row)
   - **Background**: Yellow (#F5C518)
   - **Text Color**: Black (#000000)
   - **Value Font**: Impact, 36pt, Bold
   - **Label Font**: Arial Black, 14pt
   - **Border**: Black, 2pt
   - **Values**:
     - Total Movies: `[Movies Count]`
     - Total Revenue: `[Total Revenue]`
     - Total Budget: `[Total Budget]`
     - Total Profit: `[Total Profit]`

3. **Revenue & Budget Trend** (Area Chart)
   - **Background**: Dark Gray (#1A1A1A)
   - **X-axis**: `release_year`
   - **Y-axis**: `[Total Revenue]` and `[Total Budget]`
   - **Colors**: 
     - Revenue: Yellow (#F5C518)
     - Budget: Dark Gray (#666666)
   - **Gradient Fill**: Enabled
   - **Title**: "Financial Performance Over Time"
   - **Title Font**: Impact, 18pt, Yellow
   - **Axis Font**: Arial, 11pt, White

4. **Top 10 Genres by Revenue** (Horizontal Bar Chart)
   - **Background**: Black (#000000)
   - **Axis**: `genre` (from genres_dimension)
   - **Values**: `[Total Revenue]`
   - **Color**: Yellow (#F5C518) with gradient
   - **Sort**: Descending
   - **Title**: "TOP PERFORMING GENRES"
   - **Title Font**: Impact, 16pt, Yellow

5. **Profitability Matrix** (Matrix Visual)
   - **Rows**: `primary_genre`
   - **Columns**: `budget_category`
   - **Values**: 
     - `[Movies Count]`
     - `[Average ROI]`
   - **Conditional Formatting**: 
     - Green for high ROI
     - Red for negative ROI
     - Yellow for medium ROI
   - **Background**: Dark Gray (#1A1A1A)

6. **Top 20 Movies Table** (Table)
   - **Columns**: 
     - `title` (Yellow highlight)
     - `release_year`
     - `director`
     - `primary_genre`
     - `revenue` (Currency)
     - `profit` (Currency)
     - `vote_average` (with star icon)
   - **Conditional Formatting**: 
     - Revenue: Yellow gradient
     - Rating: Star icons
   - **Background**: Black (#000000)
   - **Text**: White/Arial

### Page 2: Genre Deep Dive

#### Visualizations:

1. **Genre Performance Dashboard** (Multi-card Layout)
   - **Genre Revenue Treemap**
     - Background: Black
     - Colors: Yellow gradient
     - Shows: Revenue distribution
   
   - **Genre Rating Comparison** (Box Plot)
     - Shows: Rating distribution by genre
     - Colors: Yellow/Black
   
   - **Genre Profitability** (Funnel Chart)
     - Shows: Movies count by profitability
     - Colors: Yellow gradient

2. **Genre Revenue Matrix** (Matrix with Heatmap)
   - **Rows**: `genre`
   - **Values**: 
     - `[Total Revenue]`
     - `[Average ROI]`
     - `[Average Rating]`
     - `[Movies Count]`
   - **Conditional Formatting**: Heatmap
   - **Background**: Dark Gray

3. **Genre Trends Over Time** (Line Chart)
   - **X-axis**: `release_year`
   - **Y-axis**: `[Movies Count]`
   - **Legend**: `genre` (Top 5 genres)
   - **Colors**: Yellow variations
   - **Background**: Black

### Page 3: Director & Cast Analysis

#### Visualizations:

1. **Director Performance Leaderboard** (Ranking Visual)
   - **Custom Visual**: Chiclet Slicer or Ranking Chart
   - **Shows**: Top 20 Directors
   - **Metrics**: Revenue, Movie Count, Average Rating
   - **Style**: IMDB card style

2. **Director Network Analysis** (Network Visual - if available)
   - Shows: Director collaborations
   - Custom visual from AppSource

3. **Actor Performance Matrix** (Matrix)
   - **Rows**: `actor_name` (Top 30)
   - **Values**: 
     - `[Movies Count]`
     - `[Total Revenue]`
     - `[Average Rating]`
   - **Conditional Formatting**: Heatmap

4. **Director-Actor Collaborations** (Scatter Chart)
   - **X-axis**: Director Revenue
   - **Y-axis**: Actor Revenue
   - **Size**: Collaboration count
   - **Color**: Genre

### Page 4: Financial Analytics

#### Visualizations:

1. **ROI Distribution** (Histogram)
   - **Background**: Black
   - **Bars**: Yellow (#F5C518)
   - **Shows**: ROI distribution
   - **Title**: "RETURN ON INVESTMENT DISTRIBUTION"

2. **Budget vs Revenue Scatter** (Scatter Chart)
   - **X-axis**: `budget`
   - **Y-axis**: `revenue`
   - **Color**: `is_profitable` (Yellow/Red)
   - **Size**: `vote_count`
   - **Background**: Dark Gray
   - **Reference Lines**: Break-even line

3. **Profitability Funnel** (Funnel Chart)
   - **Stages**: Budget Categories
   - **Values**: Profit
   - **Colors**: Yellow gradient

4. **Financial Performance by Decade** (Waterfall Chart)
   - **Shows**: Revenue growth by decade
   - **Colors**: Yellow/Black

### Page 5: Time Series & Trends

#### Visualizations:

1. **Movies Released Timeline** (Timeline Visual)
   - **Shows**: Movie releases over time
   - **Color**: Yellow dots
   - **Background**: Black

2. **Rating Trends** (Line Chart with Confidence Bands)
   - **X-axis**: `release_year`
   - **Y-axis**: `[Average Rating]`
   - **Shows**: Trend with confidence interval
   - **Colors**: Yellow line, Gray band

3. **Seasonal Release Analysis** (Radar Chart)
   - **Shows**: Revenue by release month
   - **Colors**: Yellow
   - **Background**: Black

4. **Decade Comparison** (Multi-row Card)
   - **Shows**: Key metrics by decade
   - **Style**: IMDB card style

### Page 6: Interactive Drill-Through Page

#### Create Drill-Through Page:
1. **Right-click** on any movie title
2. **Select**: "Drill through" → "Movie Details"
3. **Create new page**: "Movie Details"

#### Movie Details Page Visualizations:

1. **Movie Header Card**
   - **Title**: `title` (Impact, 28pt, Yellow)
   - **Year**: `release_year`
   - **Genre**: `all_genres`
   - **Rating**: `vote_average` (with stars)

2. **Financial Metrics** (Cards)
   - Budget, Revenue, Profit, ROI

3. **Cast & Crew** (Tables)
   - Top Cast members
   - Director and key crew

4. **Similar Movies** (Table)
   - Based on genre and rating

---

## 🎨 Advanced Styling & Formatting

### Visual Formatting

#### All Charts:
- **Background**: Black (#000000) or Dark Gray (#1A1A1A)
- **Title**: Impact font, Yellow (#F5C518), 16-20pt
- **Axis Labels**: Arial, White, 11pt
- **Gridlines**: Gray (#666666), Thin
- **Border**: Yellow (#F5C518), 2pt

#### KPI Cards:
- **Background**: Yellow (#F5C518)
- **Value**: Impact, 36pt, Black, Bold
- **Label**: Arial Black, 14pt, Black
- **Border**: Black, 3pt
- **Shadow**: Enabled, Black

#### Tables:
- **Header**: Black background, Yellow text, Impact font
- **Rows**: Alternating Dark Gray/Black
- **Text**: Arial, White, 11pt
- **Hover**: Yellow highlight

### Slicers (IMDB Style)

1. **Year Range Slicer**
   - **Style**: Between
   - **Background**: Black
   - **Selected**: Yellow
   - **Font**: Arial, White

2. **Genre Slicer** (Chiclet Slicer - Custom Visual)
   - **Style**: IMDB tag style
   - **Colors**: Yellow/Black
   - **Font**: Arial Black

3. **Budget Category Slicer**
   - **Style**: Dropdown
   - **Background**: Black
   - **Selected**: Yellow

4. **Rating Slicer**
   - **Style**: Between
   - **Min/Max**: 0-10
   - **Colors**: Yellow/Black

### Tooltips (Advanced)

Create custom tooltips:
1. **Create Tooltip Page**
2. **Add visuals**:
   - Movie poster (if available)
   - Key metrics
   - Cast list
   - Financial summary
3. **Format**: IMDB style card
4. **Set as tooltip** for main visuals

---

## 🔧 Advanced Features

### Bookmarks

Create bookmarks for:
1. **Default View** - All data
2. **Top Performers** - Filtered to top 20%
3. **Recent Movies** - Last 5 years
4. **Blockbusters** - Revenue > $1B
5. **Award Winners** - High rated movies

### Drill-Through Pages

1. **Movie Details** - From any movie title
2. **Genre Analysis** - From genre selections
3. **Director Profile** - From director name
4. **Actor Profile** - From actor name

### Custom Visuals (AppSource)

Recommended custom visuals:
1. **Chiclet Slicer** - For genre filtering
2. **Infographic Designer** - For custom KPI cards
3. **Synoptic Panel** - For geographic data
4. **Timeline Storyteller** - For time-based narratives
5. **Enlighten Waterfall** - For financial flows

### Advanced Interactions

1. **Cross-filtering**: Enable between all visuals
2. **Edit interactions**: 
   - Some visuals filter others
   - Some visuals highlight others
3. **Drill-down**: Enable on hierarchical visuals

---

## 📊 Key Visualizations Summary

### Must-Have Visuals:
1. ✅ IMDB-style header with logo
2. ✅ KPI cards (Yellow/Black theme)
3. ✅ Revenue/Budget trend chart
4. ✅ Genre performance matrix
5. ✅ Top movies table
6. ✅ Director/Actor leaderboards
7. ✅ Financial scatter plots
8. ✅ Time series analysis
9. ✅ Drill-through pages
10. ✅ Interactive slicers

### Advanced Features:
- ✅ Custom tooltips
- ✅ Bookmarks
- ✅ Conditional formatting
- ✅ Custom visuals
- ✅ Advanced DAX measures
- ✅ Cross-filtering
- ✅ Drill-down capabilities

---

## 🎯 Presentation Tips

1. **Start with Overview**: Show executive summary first
2. **Use Bookmarks**: Navigate between views smoothly
3. **Highlight Insights**: Use yellow highlights for key findings
4. **Tell a Story**: Guide through data narrative
5. **Interactive Demo**: Show filtering and drill-through
6. **Explain Methodology**: Mention preprocessing and measures

---

## 📤 Export & Sharing

1. **Save** as `.pbix` file
2. **Publish** to PowerBI Service (optional)
3. **Export to PDF** for submission
4. **Create Presentation Mode**: Use bookmarks for slides

---

**Good luck with your Data Visualization term project! 🎬📊**

