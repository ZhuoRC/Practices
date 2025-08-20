# E-commerce Business Analytics Framework

A comprehensive, modular framework for analyzing e-commerce performance metrics with configurable parameters and professional visualizations.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Jupyter Notebook
- CSV datasets in `ecommerce_data/` directory

### Installation
```bash
# Clone or download the project
# Navigate to project directory

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter and open the main notebook
jupyter notebook EDA_refactored.ipynb
```

## 📊 What's Included

### Core Analysis Features
- **Revenue Performance**: YoY growth, monthly trends, seasonality analysis
- **Product Analytics**: Category performance, market share, top performers
- **Geographic Insights**: State-level revenue distribution and customer analysis
- **Customer Experience**: Delivery performance, satisfaction correlation, operational metrics
- **Executive Reporting**: Automated insights and strategic recommendations

### Key Files
- `EDA_refactored.ipynb` - Main analysis notebook with comprehensive business insights
- `data_loader.py` - Modular data loading and preprocessing
- `business_metrics.py` - Reusable business metric calculations
- `config.yaml` - Configuration file for analysis parameters
- `requirements.txt` - Python dependencies

## ⚙️ Configuration

### Basic Configuration (config.yaml)
```yaml
analysis:
  current_year: 2023        # Primary analysis year
  comparison_year: 2022     # Comparison year (null to disable)
  
data:
  data_directory: \"ecommerce_data\"
  delivered_only: true      # Filter for delivered orders only
  include_product_info: true
  include_customer_info: true
  include_review_scores: true
```

### Advanced Options
- **Date Ranges**: Specify custom start/end dates instead of full years
- **Metrics Selection**: Choose which business metrics to calculate
- **Visualization**: Customize colors, chart types, and styling
- **Export Settings**: Configure output formats and directories

## 📈 Analysis Workflow

### 1. Data Loading & Validation
```python
from data_loader import load_and_prepare_data

# Load data with configuration
sales_data = load_and_prepare_data(
    data_dir=\"ecommerce_data\",
    years=[2023, 2022],
    delivered_only=True
)
```

### 2. Business Metrics Calculation
```python
from business_metrics import calculate_comprehensive_metrics

# Calculate all business metrics
metrics = calculate_comprehensive_metrics(
    data=sales_data,
    current_year=2023,
    comparison_year=2022
)
```

### 3. Visualization & Reporting
The notebook automatically generates:
- Interactive revenue trend charts
- Product category performance bars
- Geographic revenue choropleth maps
- Customer satisfaction dashboards
- Executive summary with recommendations

## 🛠️ Customization Examples

### Analyze Different Time Period
```yaml
# In config.yaml
analysis:
  current_year: 2024
  comparison_year: 2023
  # Or use date ranges:
  # date_range:
  #   start_date: \"2024-01-01\"
  #   end_date: \"2024-06-30\"
```

### Add New Business Metrics
```python
# In business_metrics.py
def calculate_customer_lifetime_value(self, year: int) -> Dict:
    \"\"\"Calculate CLV metrics.\"\"\"
    # Implementation here
    pass

# In notebook
clv_metrics = calculator.calculate_customer_lifetime_value(2023)
```

### Modify Data Processing
```python
# In data_loader.py  
def add_seasonal_indicators(self, sales_df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Add seasonal business indicators.\"\"\"
    # Implementation here
    pass
```

## 📋 Business Metrics Reference

### Revenue Metrics
- Total revenue by period
- Year-over-year growth percentages
- Month-over-month trends
- Quarterly performance
- Revenue forecasting indicators

### Order Metrics  
- Total order count and growth
- Average order value (AOV)
- Items per order
- Order status distribution
- Customer acquisition rates

### Product Performance
- Revenue by product category
- Category market share
- Top performing products
- Category growth rates
- Cross-selling opportunities

### Geographic Analysis
- Revenue by state/region
- Customer distribution
- Market penetration rates
- Geographic growth opportunities
- Shipping cost analysis

### Customer Experience
- Average delivery times
- Delivery speed distribution
- Customer satisfaction scores
- Satisfaction correlation with delivery
- Operational efficiency metrics

## 🎯 Strategic Recommendations Engine

The framework automatically generates strategic recommendations based on:
- Performance thresholds and benchmarks
- Industry best practices
- Trend analysis and anomaly detection
- Correlation insights between metrics

Example recommendations:
- Revenue recovery strategies for negative growth
- Delivery optimization for customer satisfaction
- Category focus areas for marketing spend
- Geographic expansion opportunities

## 📊 Sample Output

### Executive Summary
```
💰 FINANCIAL PERFORMANCE
   • Total Revenue: $3,360,294.74
   • Total Orders: 4,635
   • Average Order Value: $724.98
   • YoY Decline: -2.46%

🛍️ PRODUCT PERFORMANCE  
   • Top Category: Electronics
   • Categories Analyzed: 13

🌎 GEOGRAPHIC PERFORMANCE
   • Top State: CA
   • Active States: 50

📦 CUSTOMER EXPERIENCE
   • Average Delivery Time: 8.0 days
   • Average Customer Rating: 4.10/5.0
```

## 🔧 Technical Architecture

### Modular Design
- **Separation of Concerns**: Data loading, calculations, and visualization are separate
- **Reusable Components**: Functions can be imported and used independently
- **Configuration-Driven**: Analysis parameters controlled via YAML
- **Error Handling**: Comprehensive validation and error reporting

### Data Processing Pipeline
1. **Loading**: Multi-dataset CSV loading with validation
2. **Preprocessing**: Data cleaning, type conversion, enrichment
3. **Filtering**: Date ranges, order status, data quality filters
4. **Calculation**: Business metrics with configurable parameters
5. **Visualization**: Interactive charts with business styling
6. **Reporting**: Executive summaries and recommendations

### Performance Considerations
- Efficient pandas operations for large datasets
- Memory usage optimization
- Configurable data loading (only load what's needed)
- Caching for expensive calculations

## 🚀 Advanced Usage

### Batch Analysis
```python
# Analyze multiple years in batch
years_to_analyze = [2021, 2022, 2023]
results = {}

for year in years_to_analyze:
    data = load_and_prepare_data(years=[year])
    results[year] = calculate_comprehensive_metrics(data, year)
```

### Custom Visualizations
```python
# Create custom business charts
def create_custom_kpi_dashboard(metrics):
    # Custom visualization logic
    pass
```

### Export and Automation
```python
# Export results for business reporting
import json

with open('business_metrics_2023.json', 'w') as f:
    json.dump(metrics, f, indent=2, default=str)
```

## 📝 Data Requirements

### Required CSV Files (in ecommerce_data/)
- `orders_dataset.csv` - Order information
- `order_items_dataset.csv` - Line item details
- `customers_dataset.csv` - Customer data
- `products_dataset.csv` - Product catalog  
- `order_reviews_dataset.csv` - Customer reviews
- `order_payments_dataset.csv` - Payment data

### Column Requirements
The framework expects standard e-commerce data schemas. See `data_loader.py` for specific column requirements.

## 🔍 Troubleshooting

### Common Issues
1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **Data Files Not Found**: Ensure CSV files are in `ecommerce_data/` directory
3. **Memory Issues**: Reduce date ranges or filter data in config.yaml
4. **Visualization Issues**: Check that plotly is properly installed

### Performance Tips
- Use `delivered_only: true` to reduce dataset size
- Limit analysis to specific years/quarters
- Disable unused enrichments in config.yaml

## 🤝 Contributing

To extend the framework:
1. Add new metrics to `business_metrics.py`
2. Create new data loading functions in `data_loader.py`
3. Update configuration options in `config.yaml`
4. Add visualizations to the notebook

## 📄 License

This project is provided as-is for business analytics purposes.

---

**Ready to get started?** Open `EDA_refactored.ipynb` and run all cells to see your comprehensive e-commerce analysis! 🚀