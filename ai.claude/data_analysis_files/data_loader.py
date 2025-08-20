"""
Data Loading and Processing Module for E-commerce Analysis

This module handles loading, validation, and preprocessing of e-commerce datasets.
Provides functions to load data, validate integrity, and prepare analysis-ready datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
import logging
from pathlib import Path
import warnings

# Suppress pandas warnings
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading and preprocessing of e-commerce datasets."""
    
    def __init__(self, data_dir: str = "ecommerce_data"):
        """
        Initialize DataLoader with data directory path.
        
        Args:
            data_dir (str): Path to directory containing CSV files
        """
        self.data_dir = Path(data_dir)
        self.datasets = {}
        
    def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Load all e-commerce datasets from CSV files.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets
            
        Raises:
            FileNotFoundError: If any required CSV file is missing
        """
        dataset_files = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv', 
            'customers': 'customers_dataset.csv',
            'products': 'products_dataset.csv',
            'reviews': 'order_reviews_dataset.csv',
            'payments': 'order_payments_dataset.csv'
        }
        
        for name, filename in dataset_files.items():
            file_path = self.data_dir / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Required file {filename} not found in {self.data_dir}")
            
            try:
                self.datasets[name] = pd.read_csv(file_path)
                logger.info(f"Loaded {name}: {len(self.datasets[name])} rows")
            except Exception as e:
                logger.error(f"Error loading {filename}: {str(e)}")
                raise
                
        return self.datasets
    
    def validate_data(self) -> Dict[str, Dict]:
        """
        Validate data quality and return summary statistics.
        
        Returns:
            Dict[str, Dict]: Validation results for each dataset
        """
        validation_results = {}
        
        for name, df in self.datasets.items():
            validation_results[name] = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'missing_values': df.isnull().sum().to_dict(),
                'duplicate_rows': df.duplicated().sum(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
            }
            
        return validation_results
    
    def prepare_sales_data(self) -> pd.DataFrame:
        """
        Create analysis-ready sales dataset by joining relevant tables.
        
        Returns:
            pd.DataFrame: Merged dataset with order, item, and temporal information
        """
        if not self.datasets:
            self.load_all_datasets()
            
        # Start with order items as base
        sales_data = self.datasets['order_items'][
            ['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']
        ].copy()
        
        # Add order information
        order_cols = ['order_id', 'customer_id', 'order_status', 
                     'order_purchase_timestamp', 'order_delivered_customer_date']
        
        sales_data = sales_data.merge(
            self.datasets['orders'][order_cols], 
            on='order_id', 
            how='left'
        )
        
        # Convert timestamps
        sales_data['order_purchase_timestamp'] = pd.to_datetime(
            sales_data['order_purchase_timestamp']
        )
        sales_data['order_delivered_customer_date'] = pd.to_datetime(
            sales_data['order_delivered_customer_date']
        )
        
        # Add temporal columns
        sales_data['year'] = sales_data['order_purchase_timestamp'].dt.year
        sales_data['month'] = sales_data['order_purchase_timestamp'].dt.month
        sales_data['quarter'] = sales_data['order_purchase_timestamp'].dt.quarter
        sales_data['day_of_week'] = sales_data['order_purchase_timestamp'].dt.day_name()
        
        # Calculate delivery time in days
        sales_data['delivery_days'] = (
            sales_data['order_delivered_customer_date'] - 
            sales_data['order_purchase_timestamp']
        ).dt.days
        
        logger.info(f"Prepared sales data: {len(sales_data)} rows")
        return sales_data
    
    def filter_by_date_range(self, 
                           df: pd.DataFrame, 
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           years: Optional[List[int]] = None,
                           months: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Filter dataframe by specified date criteria.
        
        Args:
            df (pd.DataFrame): Input dataframe with order_purchase_timestamp
            start_date (str, optional): Start date in 'YYYY-MM-DD' format
            end_date (str, optional): End date in 'YYYY-MM-DD' format  
            years (List[int], optional): List of years to include
            months (List[int], optional): List of months to include (1-12)
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        filtered_df = df.copy()
        
        if start_date:
            filtered_df = filtered_df[
                filtered_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)
            ]
            
        if end_date:
            filtered_df = filtered_df[
                filtered_df['order_purchase_timestamp'] <= pd.to_datetime(end_date)
            ]
            
        if years:
            filtered_df = filtered_df[filtered_df['year'].isin(years)]
            
        if months:
            filtered_df = filtered_df[filtered_df['month'].isin(months)]
            
        logger.info(f"Filtered data: {len(filtered_df)} rows remaining")
        return filtered_df
    
    def get_delivered_orders(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter for successfully delivered orders only.
        
        Args:
            df (pd.DataFrame): Input sales dataframe
            
        Returns:
            pd.DataFrame: Filtered dataframe with delivered orders only
        """
        delivered = df[df['order_status'] == 'delivered'].copy()
        logger.info(f"Delivered orders: {len(delivered)} rows")
        return delivered
    
    def add_product_info(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich sales data with product category information.
        
        Args:
            sales_df (pd.DataFrame): Sales dataframe
            
        Returns:
            pd.DataFrame: Sales data enriched with product information
        """
        if 'products' not in self.datasets:
            raise ValueError("Products dataset not loaded")
            
        product_info = self.datasets['products'][
            ['product_id', 'product_category_name', 'product_weight_g']
        ]
        
        enriched = sales_df.merge(product_info, on='product_id', how='left')
        logger.info(f"Added product info: {len(enriched)} rows")
        return enriched
    
    def add_customer_info(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich sales data with customer geographic information.
        
        Args:
            sales_df (pd.DataFrame): Sales dataframe
            
        Returns:
            pd.DataFrame: Sales data enriched with customer information
        """
        if 'customers' not in self.datasets:
            raise ValueError("Customers dataset not loaded")
            
        customer_info = self.datasets['customers'][
            ['customer_id', 'customer_state', 'customer_city', 'customer_zip_code_prefix']
        ]
        
        enriched = sales_df.merge(customer_info, on='customer_id', how='left')
        logger.info(f"Added customer info: {len(enriched)} rows")
        return enriched
    
    def add_review_scores(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich sales data with review scores.
        
        Args:
            sales_df (pd.DataFrame): Sales dataframe
            
        Returns:
            pd.DataFrame: Sales data enriched with review scores
        """
        if 'reviews' not in self.datasets:
            raise ValueError("Reviews dataset not loaded")
            
        review_info = self.datasets['reviews'][
            ['order_id', 'review_score', 'review_creation_date']
        ]
        
        enriched = sales_df.merge(review_info, on='order_id', how='left')
        logger.info(f"Added review scores: {len(enriched)} rows")
        return enriched


def load_and_prepare_data(data_dir: str = "ecommerce_data", 
                         years: Optional[List[int]] = None,
                         include_product_info: bool = True,
                         include_customer_info: bool = True,
                         include_reviews: bool = True,
                         delivered_only: bool = True) -> pd.DataFrame:
    """
    Convenience function to load and prepare analysis-ready dataset.
    
    Args:
        data_dir (str): Directory containing CSV files
        years (List[int], optional): Years to include in analysis
        include_product_info (bool): Whether to include product categories
        include_customer_info (bool): Whether to include customer geography
        include_reviews (bool): Whether to include review scores
        delivered_only (bool): Whether to filter for delivered orders only
        
    Returns:
        pd.DataFrame: Analysis-ready dataset
    """
    loader = DataLoader(data_dir)
    loader.load_all_datasets()
    
    # Prepare base sales data
    sales_data = loader.prepare_sales_data()
    
    # Filter by years if specified
    if years:
        sales_data = loader.filter_by_date_range(sales_data, years=years)
    
    # Filter for delivered orders
    if delivered_only:
        sales_data = loader.get_delivered_orders(sales_data)
    
    # Add enrichment data as requested
    if include_product_info:
        sales_data = loader.add_product_info(sales_data)
        
    if include_customer_info:
        sales_data = loader.add_customer_info(sales_data)
        
    if include_reviews:
        sales_data = loader.add_review_scores(sales_data)
    
    return sales_data