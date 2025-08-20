"""
Business Metrics Module for E-commerce Analysis

This module contains functions to calculate key business metrics including:
- Revenue and growth analysis
- Order volume and value metrics  
- Product performance analysis
- Geographic revenue analysis
- Customer experience metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BusinessMetricsCalculator:
    """Calculates various business metrics for e-commerce analysis."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize calculator with prepared sales data.
        
        Args:
            data (pd.DataFrame): Prepared sales dataset with all required columns
        """
        self.data = data
        self.validate_data()
    
    def validate_data(self):
        """Validate that required columns exist in the dataset."""
        required_columns = [
            'order_id', 'price', 'order_purchase_timestamp', 
            'year', 'month', 'order_status'
        ]
        
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def calculate_revenue_metrics(self, 
                                current_year: int, 
                                comparison_year: Optional[int] = None) -> Dict:
        """
        Calculate revenue metrics for specified years.
        
        Args:
            current_year (int): Year to analyze
            comparison_year (int, optional): Year to compare against
            
        Returns:
            Dict: Revenue metrics including totals, growth rates, and trends
        """
        current_data = self.data[self.data['year'] == current_year]
        current_revenue = current_data['price'].sum()
        
        metrics = {
            'current_year': current_year,
            'total_revenue': current_revenue,
            'monthly_revenue': current_data.groupby('month')['price'].sum().to_dict(),
            'quarterly_revenue': current_data.groupby('quarter')['price'].sum().to_dict()
        }
        
        # Calculate growth metrics if comparison year provided
        if comparison_year:
            comparison_data = self.data[self.data['year'] == comparison_year]
            comparison_revenue = comparison_data['price'].sum()
            
            if comparison_revenue > 0:
                yoy_growth = ((current_revenue - comparison_revenue) / comparison_revenue) * 100
                metrics.update({
                    'comparison_year': comparison_year,
                    'comparison_revenue': comparison_revenue,
                    'yoy_growth_percent': yoy_growth
                })
        
        # Monthly growth trend within current year
        monthly_data = current_data.groupby('month')['price'].sum()
        if len(monthly_data) > 1:
            monthly_growth = monthly_data.pct_change().dropna()
            metrics['monthly_growth_trend'] = {
                'average_mom_growth': monthly_growth.mean() * 100,
                'monthly_growth_rates': monthly_growth.to_dict()
            }
        
        logger.info(f"Revenue metrics calculated for {current_year}")
        return metrics
    
    def calculate_order_metrics(self, 
                              current_year: int,
                              comparison_year: Optional[int] = None) -> Dict:
        """
        Calculate order volume and value metrics.
        
        Args:
            current_year (int): Year to analyze
            comparison_year (int, optional): Year to compare against
            
        Returns:
            Dict: Order metrics including counts, AOV, and distributions
        """
        current_data = self.data[self.data['year'] == current_year]
        
        # Order level aggregations
        order_summary = current_data.groupby('order_id').agg({
            'price': 'sum',
            'order_item_id': 'count'
        }).rename(columns={'order_item_id': 'items_per_order'})
        
        metrics = {
            'current_year': current_year,
            'total_orders': len(order_summary),
            'total_items': current_data['order_item_id'].count(),
            'average_order_value': order_summary['price'].mean(),
            'median_order_value': order_summary['price'].median(),
            'average_items_per_order': order_summary['items_per_order'].mean(),
            'order_status_distribution': current_data['order_status'].value_counts(normalize=True).to_dict()
        }
        
        # Comparison metrics
        if comparison_year:
            comparison_data = self.data[self.data['year'] == comparison_year]
            comparison_orders = comparison_data['order_id'].nunique()
            comparison_aov = comparison_data.groupby('order_id')['price'].sum().mean()
            
            if comparison_orders > 0:
                order_growth = ((metrics['total_orders'] - comparison_orders) / comparison_orders) * 100
                aov_growth = ((metrics['average_order_value'] - comparison_aov) / comparison_aov) * 100
                
                metrics.update({
                    'comparison_year': comparison_year,
                    'comparison_orders': comparison_orders,
                    'comparison_aov': comparison_aov,
                    'order_growth_percent': order_growth,
                    'aov_growth_percent': aov_growth
                })
        
        logger.info(f"Order metrics calculated for {current_year}")
        return metrics
    
    def calculate_product_performance(self, year: int) -> Dict:
        """
        Calculate product category performance metrics.
        
        Args:
            year (int): Year to analyze
            
        Returns:
            Dict: Product performance metrics by category
        """
        if 'product_category_name' not in self.data.columns:
            logger.warning("Product category data not available")
            return {}
        
        year_data = self.data[self.data['year'] == year]
        
        category_metrics = year_data.groupby('product_category_name').agg({
            'price': ['sum', 'mean', 'count'],
            'order_id': 'nunique'
        }).round(2)
        
        # Flatten column names
        category_metrics.columns = ['total_revenue', 'avg_item_price', 'total_items', 'unique_orders']
        category_metrics = category_metrics.sort_values('total_revenue', ascending=False)
        
        # Calculate market share
        total_revenue = category_metrics['total_revenue'].sum()
        category_metrics['revenue_share_percent'] = (
            category_metrics['total_revenue'] / total_revenue * 100
        ).round(2)
        
        metrics = {
            'year': year,
            'category_performance': category_metrics.to_dict('index'),
            'top_categories': category_metrics.head(5)['total_revenue'].to_dict(),
            'category_count': len(category_metrics)
        }
        
        logger.info(f"Product performance calculated for {year}")
        return metrics
    
    def calculate_geographic_metrics(self, year: int) -> Dict:
        """
        Calculate revenue metrics by geographic region.
        
        Args:
            year (int): Year to analyze
            
        Returns:
            Dict: Geographic performance metrics
        """
        if 'customer_state' not in self.data.columns:
            logger.warning("Customer geographic data not available")
            return {}
        
        year_data = self.data[self.data['year'] == year]
        
        state_metrics = year_data.groupby('customer_state').agg({
            'price': ['sum', 'mean'],
            'order_id': 'nunique',
            'customer_id': 'nunique'
        }).round(2)
        
        # Flatten column names
        state_metrics.columns = ['total_revenue', 'avg_order_value', 'total_orders', 'unique_customers']
        state_metrics = state_metrics.sort_values('total_revenue', ascending=False)
        
        # Calculate metrics
        total_revenue = state_metrics['total_revenue'].sum()
        state_metrics['revenue_share_percent'] = (
            state_metrics['total_revenue'] / total_revenue * 100
        ).round(2)
        
        metrics = {
            'year': year,
            'state_performance': state_metrics.to_dict('index'),
            'top_states': state_metrics.head(10)['total_revenue'].to_dict(),
            'state_count': len(state_metrics)
        }
        
        logger.info(f"Geographic metrics calculated for {year}")
        return metrics
    
    def calculate_customer_experience_metrics(self, year: int) -> Dict:
        """
        Calculate customer experience and satisfaction metrics.
        
        Args:
            year (int): Year to analyze
            
        Returns:
            Dict: Customer experience metrics
        """
        year_data = self.data[self.data['year'] == year]
        
        metrics = {
            'year': year
        }
        
        # Delivery performance
        if 'delivery_days' in year_data.columns:
            delivery_data = year_data.dropna(subset=['delivery_days'])
            
            metrics['delivery_performance'] = {
                'average_delivery_days': delivery_data['delivery_days'].mean(),
                'median_delivery_days': delivery_data['delivery_days'].median(),
                'delivery_percentiles': {
                    '25th': delivery_data['delivery_days'].quantile(0.25),
                    '75th': delivery_data['delivery_days'].quantile(0.75),
                    '95th': delivery_data['delivery_days'].quantile(0.95)
                }
            }
            
            # Categorize delivery speed
            def categorize_delivery_speed(days):
                if pd.isna(days):
                    return 'Unknown'
                elif days <= 3:
                    return '1-3 days'
                elif days <= 7:
                    return '4-7 days'
                else:
                    return '8+ days'
            
            delivery_data = delivery_data.copy()
            delivery_data['delivery_category'] = delivery_data['delivery_days'].apply(categorize_delivery_speed)
            metrics['delivery_speed_distribution'] = delivery_data['delivery_category'].value_counts(normalize=True).to_dict()
        
        # Review scores analysis
        if 'review_score' in year_data.columns:
            review_data = year_data.dropna(subset=['review_score'])
            
            metrics['review_performance'] = {
                'average_review_score': review_data['review_score'].mean(),
                'review_distribution': review_data['review_score'].value_counts(normalize=True).sort_index().to_dict(),
                'total_reviews': len(review_data)
            }
            
            # Review score by delivery speed (if both available)
            if 'delivery_days' in review_data.columns:
                review_data = review_data.dropna(subset=['delivery_days'])
                review_data['delivery_category'] = review_data['delivery_days'].apply(categorize_delivery_speed)
                
                delivery_satisfaction = review_data.groupby('delivery_category')['review_score'].mean().to_dict()
                metrics['delivery_satisfaction_correlation'] = delivery_satisfaction
        
        logger.info(f"Customer experience metrics calculated for {year}")
        return metrics
    
    def generate_time_series_data(self, 
                                years: List[int], 
                                metric: str = 'revenue',
                                frequency: str = 'monthly') -> pd.DataFrame:
        """
        Generate time series data for trend analysis.
        
        Args:
            years (List[int]): Years to include in analysis
            metric (str): Metric to calculate ('revenue', 'orders', 'aov')
            frequency (str): Time frequency ('monthly', 'quarterly')
            
        Returns:
            pd.DataFrame: Time series data
        """
        data_subset = self.data[self.data['year'].isin(years)]
        
        if frequency == 'monthly':
            group_cols = ['year', 'month']
        elif frequency == 'quarterly':
            group_cols = ['year', 'quarter']
        else:
            raise ValueError("Frequency must be 'monthly' or 'quarterly'")
        
        if metric == 'revenue':
            ts_data = data_subset.groupby(group_cols)['price'].sum().reset_index()
            ts_data.rename(columns={'price': 'value'}, inplace=True)
        elif metric == 'orders':
            ts_data = data_subset.groupby(group_cols)['order_id'].nunique().reset_index()
            ts_data.rename(columns={'order_id': 'value'}, inplace=True)
        elif metric == 'aov':
            order_values = data_subset.groupby(group_cols + ['order_id'])['price'].sum().reset_index()
            ts_data = order_values.groupby(group_cols)['price'].mean().reset_index()
            ts_data.rename(columns={'price': 'value'}, inplace=True)
        else:
            raise ValueError("Metric must be 'revenue', 'orders', or 'aov'")
        
        # Create date column for plotting
        if frequency == 'monthly':
            ts_data['date'] = pd.to_datetime(
                ts_data[['year', 'month']].assign(day=1)
            )
        else:  # quarterly
            ts_data['date'] = pd.to_datetime(
                ts_data['year'].astype(str) + '-' + 
                (ts_data['quarter'] * 3 - 2).astype(str) + '-01'
            )
        
        ts_data['metric'] = metric
        ts_data['frequency'] = frequency
        
        logger.info(f"Generated {frequency} {metric} time series for years {years}")
        return ts_data[['date', 'year', 'month' if frequency == 'monthly' else 'quarter', 'value', 'metric', 'frequency']]


def calculate_comprehensive_metrics(data: pd.DataFrame, 
                                  current_year: int,
                                  comparison_year: Optional[int] = None) -> Dict:
    """
    Calculate comprehensive business metrics for e-commerce analysis.
    
    Args:
        data (pd.DataFrame): Prepared sales dataset
        current_year (int): Year to analyze  
        comparison_year (int, optional): Year to compare against
        
    Returns:
        Dict: Comprehensive metrics dictionary
    """
    calculator = BusinessMetricsCalculator(data)
    
    metrics = {
        'revenue_metrics': calculator.calculate_revenue_metrics(current_year, comparison_year),
        'order_metrics': calculator.calculate_order_metrics(current_year, comparison_year),
        'product_performance': calculator.calculate_product_performance(current_year),
        'geographic_metrics': calculator.calculate_geographic_metrics(current_year),
        'customer_experience': calculator.calculate_customer_experience_metrics(current_year)
    }
    
    # Add time series data
    years_to_analyze = [current_year]
    if comparison_year:
        years_to_analyze.append(comparison_year)
        
    metrics['time_series'] = {
        'monthly_revenue': calculator.generate_time_series_data(years_to_analyze, 'revenue', 'monthly'),
        'monthly_orders': calculator.generate_time_series_data(years_to_analyze, 'orders', 'monthly'),
        'monthly_aov': calculator.generate_time_series_data(years_to_analyze, 'aov', 'monthly')
    }
    
    logger.info(f"Comprehensive metrics calculated for {current_year}")
    return metrics