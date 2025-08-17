# Vahan Vehicle Registration Dashboard

## **Project Overview**
This project is a **Streamlit-based interactive dashboard** that visualizes vehicle registration data across India.  
The dashboard is designed for **investors and decision-makers** to explore trends in vehicle registrations, including YoY (Year-over-Year) and QoQ (Quarter-over-Quarter) growth, top manufacturers, and vehicle categories.  

The dashboard uses **SQLite** as the backend database and **Plotly** for interactive visualizations.  

---

## **Features**

### **Filters**
- **Date Range**: Select start and end dates for analysis.  
- **State**: Filter data by one or more states.  
- **Manufacturer**: Filter by vehicle manufacturers.  
- **Vehicle Category**: Filter by 2W, 3W, 4W, or Others.  

### **Key Metrics (KPIs)**
- Total registrations  
- YoY growth (%)  
- QoQ growth (%)  

### **Visualizations**
1. **YoY Trends**: Animated bar chart showing yearly registrations for each vehicle category.  
2. **QoQ Trends**: Smooth line chart showing quarter-over-quarter registrations.  
3. **Manufacturers**: Horizontal stacked bar chart showing top manufacturers by category.  
4. **Vehicle Categories**: Pie chart showing distribution of registrations across categories.  
5. **Raw Data**: Interactive table with download option.  

### **Animations**
- Lottie animations enhance the user experience with interactive visuals for cars and growth metrics.  

---

## **Code Structure**

### **1. `build_db.py`**
- Loads CSV (`vahan-manufacturer-vehicle-category.csv`) and normalizes columns.  
- Maps vehicle types to simplified categories (`2W`, `3W`, `4W`, `OTHERS`).  
- Creates an SQLite database `vahan.db` with table `vahan_data`.  
- Columns in DB: `id`, `date`, `manufacturer`, `vehicle_category`, `registrations`.  

**Usage**:  
```bash
python build_db.py

```

### `app.py`
- Loads data from `vahan.db`  
- Applies filters and computes KPIs  
- Displays visualizations in tabs  
- Uses Plotly for charts and Streamlit-Lottie for animations  

**Run:**
```bash
streamlit run app.py
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd vahan-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Build the database**
```bash
python build_db.py
```

4. **Launch the dashboard**
```bash
streamlit run app.py
```

5. **Open in browser**
```
http://localhost:8501
```

---

## 📁 Data Assumptions

- CSV columns: `date`, `state_name`, `manufacturer`, `vehicle_type_simplified`, `registrations`  
- Missing values for `state_name` or `manufacturer` are filled as `Unknown`  
- Vehicle types mapped to: `2W`, `3W`, `4W`, `OTHERS`  
- `registrations` is numeric (int or float)

---

## 🚀 Feature Roadmap

- 📅 Monthly trend analysis  
- 🗺️ State-level map visualizations  
- 🔮 Predictive analytics for future registrations  
- 🔐 Investor login for restricted access  
- 📄 Downloadable reports (PDF/Excel)

---

## 🎥 Video Walkthrough

Record a short demo (max 5 minutes) showing:
1. Dashboard overview  
2. Filters in action  
3. Key insights for investors  

Upload to **YouTube (unlisted)** or **Google Drive** and paste the link below:

```
https://drive.google.com/file/d/1AnUfHH-Q3ffeUKf20SjIx46BJgWnEgpL/view?usp=sharing
```

---

## 📦 Dependencies

- Python 3.10+  
- Streamlit  
- Pandas  
- Plotly  
- Streamlit-Lottie  
- Requests  
- SQLite3  

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

---

## 📬 Contact

For questions or feedback, feel free to open an issue or reach out via [GitHub Discussions](https://github.com/).

```

---

Would you like help generating a sample CSV or adding a badge section for GitHub stars, license, or deployment status?
