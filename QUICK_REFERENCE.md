# Quick Reference - IMDB Style PowerBI Dashboard

## 🎨 Color Codes (Copy-Paste Ready)

- **Primary Yellow**: `#F5C518`
- **Black**: `#000000`
- **White**: `#FFFFFF`
- **Dark Gray**: `#1A1A1A`
- **Light Gray**: `#F5F5F5`
- **Accent Yellow**: `#FFD700`

## 🔤 Font Settings

- **Headings**: Impact, 24-32pt, Yellow (#F5C518)
- **Subheadings**: Arial Black, 16-20pt, Yellow/White
- **Body Text**: Arial, 11-14pt, White
- **KPI Numbers**: Impact, 36pt, Black (on Yellow background)

## 📊 Key Visualizations Checklist

### Page 1: Executive Overview
- [ ] IMDB-style header (Black bg, Yellow text, Impact font)
- [ ] 4 KPI Cards (Yellow background, Black text)
- [ ] Revenue/Budget Trend (Area chart, Yellow/Dark Gray)
- [ ] Top 10 Genres Bar Chart (Yellow bars)
- [ ] Profitability Matrix (Heatmap)
- [ ] Top 20 Movies Table (IMDB style)

### Page 2: Genre Analysis
- [ ] Genre Revenue Treemap
- [ ] Genre Rating Comparison
- [ ] Genre Trends Over Time

### Page 3: Director & Cast
- [ ] Director Leaderboard
- [ ] Actor Performance Matrix
- [ ] Director-Actor Collaborations

### Page 4: Financial Analytics
- [ ] ROI Distribution Histogram
- [ ] Budget vs Revenue Scatter
- [ ] Profitability Funnel
- [ ] Financial Performance by Decade

### Page 5: Time Series
- [ ] Movies Timeline
- [ ] Rating Trends
- [ ] Seasonal Release Analysis

### Page 6: Drill-Through
- [ ] Movie Details Page
- [ ] Genre Analysis Page
- [ ] Director Profile Page

## 🎯 Advanced Features Checklist

- [ ] Apply IMDB_Theme.json
- [ ] Create all DAX measures
- [ ] Set up relationships (movie_id)
- [ ] Create bookmarks (5+ views)
- [ ] Set up drill-through pages
- [ ] Configure custom tooltips
- [ ] Add slicers (Year, Genre, Budget, Rating)
- [ ] Enable cross-filtering
- [ ] Apply conditional formatting
- [ ] Test all interactions

## 📐 DAX Measures Quick Copy

### Essential Measures
```DAX
Total Revenue = FORMAT(SUM(movies_cleaned[revenue]), "$#,##0.0,,B")
Total Budget = FORMAT(SUM(movies_cleaned[budget]), "$#,##0.0,,B")
Total Profit = FORMAT(SUM(movies_cleaned[profit]), "$#,##0.0,,B")
Average Rating = ROUND(AVERAGE(movies_cleaned[vote_average]), 2)
Movies Count = COUNTROWS(movies_cleaned)
Profitable Movies = CALCULATE([Movies Count], movies_cleaned[is_profitable] = TRUE())
Profitability Rate = DIVIDE([Profitable Movies], [Movies Count], 0) * 100
```

## 🎬 IMDB Style Elements

### Header Design
- Background: Black (#000000)
- Text: "MOVIE ANALYTICS DASHBOARD"
- Font: Impact, 32pt, Yellow (#F5C518)
- Subtitle: Arial, 14pt, White

### KPI Cards
- Background: Yellow (#F5C518)
- Value: Impact, 36pt, Black, Bold
- Label: Arial Black, 14pt, Black
- Border: Black, 3pt

### Charts
- Background: Black or Dark Gray (#1A1A1A)
- Data Colors: Yellow (#F5C518)
- Title: Impact, 18pt, Yellow
- Axis: Arial, 11pt, White

## 🔧 PowerBI Settings

1. **View → Themes → Browse** → Import `IMDB_Theme.json`
2. **View → Model** → Create relationships
3. **View → Data** → Create measures
4. **Format** → Apply IMDB colors manually if needed

## 📱 Slicer Configuration

- **Year Range**: Between, Black bg, Yellow selected
- **Genre**: Chiclet Slicer (custom visual), Yellow tags
- **Budget Category**: Dropdown, Black bg
- **Rating**: Between (0-10), Yellow/Black

## 🎯 Presentation Tips

1. Start with Executive Overview
2. Use bookmarks for smooth navigation
3. Highlight key insights in Yellow
4. Show interactivity (filtering, drill-through)
5. Explain methodology and preprocessing

---

**Good luck with your term project! 🎬**

