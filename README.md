# TMDB 5000 Movies - PowerBI Dashboard Project

## 📋 Project Overview
This project preprocesses TMDB movie datasets and prepares them for creating a comprehensive PowerBI dashboard.

## 📁 Files

### Source Data
- `tmdb_5000_movies.csv` - Original movies dataset
- `tmdb_5000_credits.csv` - Original credits dataset

### Preprocessed Data (Ready for PowerBI)
- `movies_cleaned.csv` - Main fact table with 4,803 movies
- `genres_dimension.csv` - Genre breakdown (12,160 rows)
- `keywords_dimension.csv` - Keywords/tags (36,194 rows)
- `production_companies_dimension.csv` - Production companies (13,677 rows)
- `cast_dimension.csv` - Cast members (44,927 rows)
- `crew_dimension.csv` - Crew members (32,061 rows)

### Scripts & Documentation
- `preprocess.py` - Data preprocessing script
- `POWERBI_DASHBOARD_GUIDE.md` - Complete PowerBI dashboard guide
- `README.md` - This file

## 🚀 Quick Start

### 1. Run Preprocessing (Already Done!)
```bash
python preprocess.py
```

### 2. Open PowerBI Desktop
1. Launch PowerBI Desktop
2. Click **Get Data** → **Text/CSV**
3. Import all 6 CSV files from the preprocessed data section above

### 3. Follow the Dashboard Guide
Open `POWERBI_DASHBOARD_GUIDE.md` for:
- Step-by-step setup instructions
- Relationship creation
- Calculated measures (DAX formulas)
- Visualization recommendations
- Design best practices

## 📊 Dataset Summary

- **Total Movies**: 4,803
- **Date Range**: 1916 - 2017
- **Total Budget**: $139.50B
- **Total Revenue**: $395.10B
- **Total Profit**: $251.99B
- **Profitable Movies**: 50.8%
- **Average Rating**: 6.09/10

## 🎯 Key Features

### Data Preprocessing
- ✅ Merged movies and credits datasets
- ✅ Parsed JSON columns (genres, keywords, cast, crew)
- ✅ Calculated derived metrics (profit, ROI)
- ✅ Created normalized dimension tables
- ✅ Added categorical fields for analysis

### PowerBI Ready
- ✅ Clean, structured data
- ✅ Proper relationships between tables
- ✅ Calculated measures ready to use
- ✅ Comprehensive dashboard design guide

## 📖 Next Steps

1. **Import Data**: Load all CSV files into PowerBI
2. **Apply Theme**: Import `IMDB_Theme.json` for IMDB-style colors
3. **Create Relationships**: Link tables via `movie_id`
4. **Build Measures**: Use advanced DAX formulas from the guide
5. **Design Dashboard**: Follow advanced visualization recommendations
6. **Customize**: Apply IMDB branding (Yellow & Black theme)

## 📚 Documentation

For detailed instructions, see:
- **POWERBI_DASHBOARD_GUIDE_ADVANCED.md** - ⭐ **MAIN GUIDE** - Advanced IMDB-style dashboard guide
- **QUICK_REFERENCE.md** - Quick reference for colors, fonts, and checklists
- **IMDB_Theme.json** - PowerBI theme file (Yellow & Black IMDB style)
- **POWERBI_DASHBOARD_GUIDE.md** - Basic dashboard guide (reference)

## 💡 Tips

- Start with the Executive Summary page
- Use slicers for interactivity
- Apply consistent color schemes
- Test cross-filtering between visuals
- Export to PDF for presentations

---

**Ready to create your dashboard!** 🎬📊

