# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a refactored e-commerce data analysis project with modular architecture:
- **EDA_refactored.ipynb**: Main analysis notebook with comprehensive business insights
- **data_loader.py**: Data loading and preprocessing module
- **business_metrics.py**: Business metrics calculation module  
- **config.yaml**: Configuration file for analysis parameters
- **ecommerce_data/**: Directory containing CSV datasets

## Analysis Framework

The project uses a configurable analysis framework that supports:
- **Flexible Time Periods**: Analyze any year or date range via config.yaml
- **Modular Calculations**: Reusable functions for revenue, product, geographic, and customer metrics
- **Professional Visualizations**: Interactive charts with business-appropriate styling
- **Executive Reporting**: Automated summary generation and strategic recommendations

## Key Commands

### Setup and Installation
```bash
pip install -r requirements.txt
```

### Running the Analysis
```bash
jupyter notebook EDA_refactored.ipynb
```

### Customizing Analysis Parameters
Edit `config.yaml` to modify:
- Analysis years (current_year, comparison_year)
- Data filters (delivered_only, date ranges)
- Metrics to calculate
- Visualization preferences

## Dataset Structure

The project analyzes e-commerce data with these datasets:
- `orders_dataset.csv` - Order information with timestamps and status
- `order_items_dataset.csv` - Individual items within orders with pricing  
- `customers_dataset.csv` - Customer demographics and location data
- `products_dataset.csv` - Product catalog with categories and dimensions
- `order_reviews_dataset.csv` - Customer reviews and ratings
- `order_payments_dataset.csv` - Payment information

## Module Architecture

### data_loader.py
- `DataLoader` class for loading and validating data
- `load_and_prepare_data()` - Main function to create analysis-ready dataset
- Functions for filtering by date, enriching with product/customer data
- Built-in data quality validation

### business_metrics.py  
- `BusinessMetricsCalculator` class for all metric calculations
- Revenue metrics: YoY growth, monthly trends, seasonality
- Product performance: category analysis, market share
- Geographic metrics: state-level revenue distribution
- Customer experience: delivery performance, satisfaction correlation
- `calculate_comprehensive_metrics()` - Main function for full analysis

### Configuration (config.yaml)
- Analysis period configuration (years, date ranges)
- Data processing options (filters, enrichment)
- Metrics to calculate
- Visualization settings
- Export preferences

## Common Development Tasks

### Adding New Metrics
1. Add calculation function to `business_metrics.py` 
2. Update `calculate_comprehensive_metrics()` to include new metric
3. Add visualization code to notebook if needed
4. Update config.yaml to make metric optional

### Changing Analysis Period
1. Modify `current_year` and `comparison_year` in config.yaml
2. Or specify `date_range` with start_date/end_date
3. Re-run notebook - all calculations will automatically adjust

### Adding New Data Sources
1. Add loading logic to `DataLoader.load_all_datasets()`
2. Create enrichment function (e.g., `add_new_data_info()`)
3. Update `load_and_prepare_data()` to include new enrichment
4. Add config options for the new data source

## Data Processing Patterns

The refactored version uses these patterns:
- **Class-based architecture** for maintainable data processing
- **Configuration-driven analysis** via YAML files
- **Comprehensive error handling** and data validation
- **Modular metric calculations** with reusable functions
- **Professional visualization** with consistent styling