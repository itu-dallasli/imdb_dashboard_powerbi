# Manual IMDB Styling Guide for PowerBI

Since PowerBI theme files have limitations, use this guide to manually apply IMDB styling to your visuals.

## 🎨 Color Palette (Copy-Paste)

- **Primary Yellow**: `#F5C518`
- **Black**: `#000000`
- **White**: `#FFFFFF`
- **Dark Gray**: `#1A1A1A`
- **Light Gray**: `#F5F5F5`
- **Accent Yellow**: `#FFD700`

## 📐 Step-by-Step Manual Styling

### 1. Apply Basic Theme
1. **View** → **Themes** → **Browse for themes**
2. Import `IMDB_Theme.json` (simplified version)
3. This sets basic colors

### 2. Format KPI Cards

For each KPI Card:
1. Select the card
2. **Format visual** (paint roller icon)
3. **General**:
   - **Background**: `#F5C518` (Yellow)
   - **Border**: `#000000`, Width: 3pt
4. **Callout value**:
   - **Font**: Impact
   - **Size**: 36pt
   - **Color**: `#000000` (Black)
   - **Style**: Bold
5. **Category label**:
   - **Font**: Arial Black
   - **Size**: 14pt
   - **Color**: `#000000` (Black)

### 3. Format Charts

#### Column/Bar Charts:
1. Select chart
2. **Format visual** → **General**:
   - **Background**: `#000000` or `#1A1A1A`
   - **Border**: `#F5C518`, Width: 2pt
3. **Data colors**:
   - **Show all**: ON
   - **Color 1**: `#F5C518` (Yellow)
   - **Color 2**: `#FFD700` (Gold)
4. **Title**:
   - **Font**: Impact
   - **Size**: 18pt
   - **Color**: `#F5C518`
5. **X-axis**:
   - **Font**: Arial
   - **Size**: 11pt
   - **Color**: `#FFFFFF`
6. **Y-axis**:
   - **Font**: Arial
   - **Size**: 11pt
   - **Color**: `#FFFFFF`
7. **Gridlines**:
   - **Color**: `#666666`
   - **Style**: Solid, Width: 1pt

#### Line Charts:
1. Same as Column/Bar Charts
2. **Lines**:
   - **Color**: `#F5C518`
   - **Width**: 3pt
3. **Markers**:
   - **Show**: ON
   - **Color**: `#F5C518`
   - **Size**: 8pt

#### Scatter Charts:
1. Same background and title settings
2. **Data colors**: `#F5C518`
3. **X-axis**: White text
4. **Y-axis**: White text

### 4. Format Tables

1. Select table
2. **Format visual** → **General**:
   - **Background**: `#000000`
3. **Column headers**:
   - **Background**: `#000000`
   - **Font**: Impact
   - **Size**: 12pt
   - **Color**: `#F5C518`
   - **Style**: Bold
4. **Values**:
   - **Font**: Arial
   - **Size**: 11pt
   - **Color**: `#FFFFFF`
5. **Grid**:
   - **Vertical grid**: `#333333`
   - **Horizontal grid**: `#333333`
6. **Row headers** (if applicable):
   - **Background**: `#1A1A1A`
   - **Font**: Arial
   - **Color**: `#FFFFFF`

### 5. Format Matrix

1. Select matrix
2. **Format visual** → **General**:
   - **Background**: `#000000`
3. **Column headers**:
   - **Background**: `#000000`
   - **Font**: Impact
   - **Size**: 12pt
   - **Color**: `#F5C518`
4. **Row headers**:
   - **Background**: `#1A1A1A`
   - **Font**: Arial
   - **Color**: `#FFFFFF`
5. **Values**:
   - **Font**: Arial
   - **Size**: 11pt
   - **Color**: `#FFFFFF`
6. **Grid**:
   - **Color**: `#333333`

### 6. Format Slicers

1. Select slicer
2. **Format visual** → **General**:
   - **Background**: `#000000`
3. **Header**:
   - **Background**: `#000000`
   - **Font**: Impact
   - **Size**: 14pt
   - **Color**: `#F5C518`
4. **Items**:
   - **Background**: `#1A1A1A`
   - **Font**: Arial
   - **Size**: 11pt
   - **Color**: `#FFFFFF`
5. **Selected items**:
   - **Background**: `#F5C518`
   - **Color**: `#000000`
   - **Font**: Arial Black

### 7. Format Page Background

1. Click on empty area of page
2. **Format** → **Page background**
3. **Color**: `#000000` (Black)
4. **Transparency**: 0%

### 8. Create IMDB-Style Header

1. **Insert** → **Text box**
2. Type: "MOVIE ANALYTICS DASHBOARD"
3. **Format text box**:
   - **Background**: `#000000`
   - **Font**: Impact
   - **Size**: 32pt
   - **Color**: `#F5C518`
   - **Style**: Bold
   - **Alignment**: Center
4. Add subtitle text box below:
   - "Comprehensive Movie Performance Analysis"
   - **Font**: Arial
   - **Size**: 14pt
   - **Color**: `#FFFFFF`

## 🎯 Quick Formatting Checklist

### For Each Visual:
- [ ] Background: Black or Dark Gray
- [ ] Title: Impact font, Yellow, 18pt
- [ ] Data colors: Yellow (#F5C518)
- [ ] Axis labels: Arial, White, 11pt
- [ ] Border: Yellow, 2pt (optional)

### For KPI Cards:
- [ ] Background: Yellow (#F5C518)
- [ ] Value: Impact, 36pt, Black
- [ ] Label: Arial Black, 14pt, Black
- [ ] Border: Black, 3pt

### For Tables:
- [ ] Header: Black bg, Yellow text, Impact font
- [ ] Rows: Dark Gray bg, White text, Arial font
- [ ] Grid: Gray lines

## 💡 Pro Tips

1. **Use Format Painter**: Format one visual, then use Format Painter to copy to others
2. **Create Visual Templates**: Format one of each type, duplicate for consistency
3. **Use Themes**: Apply the basic theme first, then customize individual visuals
4. **Save as Template**: Save your formatted page as a template for other pages

## 🔄 Alternative: Create Custom Theme

If you want to create a more complete theme:

1. **View** → **Themes** → **Customize current theme**
2. Set:
   - **Primary color**: `#F5C518`
   - **Background**: `#000000`
   - **Foreground**: `#F5C518`
3. **Save theme** as `IMDB_Custom.json`

Then manually format visuals as described above.

---

**Note**: The simplified `IMDB_Theme.json` will set basic colors. Use this manual guide for complete IMDB styling.

