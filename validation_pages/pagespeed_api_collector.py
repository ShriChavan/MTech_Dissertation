"""
PageSpeed API Metrics Collector for Real-World Validation

This script collects web performance metrics from Google PageSpeed Insights API
for use in validating the Phase 2 prescriptive optimization model.

Requirements:
    pip install requests pandas

Usage:
    python pagespeed_api_collector.py --url "https://your-page-url.com" --output metrics.json
    
    # With API key (recommended for production):
    python pagespeed_api_collector.py --url "https://your-page-url.com" --api-key "YOUR_API_KEY"

Output:
    JSON file with metrics compatible with the Phase 2 model features:
    - fcp, lcp, tti, tbt, cls, speed_index
    - total_byte_weight, num_requests
    - performance_score
    - And more...

API Documentation:
    https://developers.google.com/speed/docs/insights/v5/get-started
"""

import requests
import json
import pandas as pd
import argparse
from datetime import datetime
import time
import sys


class PageSpeedCollector:
    """
    Collects web performance metrics from Google PageSpeed Insights API.
    """
    
    BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    # Map PageSpeed metrics to model features
    METRIC_MAPPING = {
        'first-contentful-paint': 'fcp',
        'largest-contentful-paint': 'lcp',
        'interactive': 'tti',
        'total-blocking-time': 'tbt',
        'cumulative-layout-shift': 'cls',
        'speed-index': 'speed_index',
    }
    
    def __init__(self, api_key=None):
        """
        Initialize the collector.
        
        Parameters:
        -----------
        api_key : str, optional
            Google PageSpeed Insights API key.
            Get one at: https://developers.google.com/speed/docs/insights/v5/get-started
        """
        self.api_key = api_key
        
    def collect_metrics(self, url, strategy='mobile'):
        """
        Collect metrics for a URL from PageSpeed Insights API.
        
        Parameters:
        -----------
        url : str
            The URL to analyze
        strategy : str
            'mobile' or 'desktop'
            
        Returns:
        --------
        dict
            Metrics dictionary compatible with Phase 2 model
        """
        print(f"\n{'='*60}")
        print(f"COLLECTING PAGESPEED METRICS")
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"Strategy: {strategy}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Build API request
        params = {
            'url': url,
            'strategy': strategy,
            'category': 'performance',
        }
        
        if self.api_key:
            params['key'] = self.api_key
            print("API Key: Provided ✓")
        else:
            print("API Key: Not provided (rate limits may apply)")
        
        print(f"\nSending request to PageSpeed API...")
        start_time = time.time()
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=120)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None
        
        elapsed = time.time() - start_time
        print(f"Response received in {elapsed:.2f} seconds")
        
        # Parse response
        data = response.json()
        
        if 'error' in data:
            print(f"❌ API Error: {data['error']['message']}")
            return None
        
        # Extract metrics
        metrics = self._extract_metrics(data)
        
        # Print summary
        self._print_metrics_summary(metrics)
        
        return metrics
    
    def _extract_metrics(self, data):
        """Extract relevant metrics from API response."""
        metrics = {
            'url': data.get('id', ''),
            'timestamp': datetime.now().isoformat(),
            'strategy': data.get('lighthouseResult', {}).get('configSettings', {}).get('emulatedFormFactor', 'unknown'),
        }
        
        lighthouse = data.get('lighthouseResult', {})
        
        # Performance score
        categories = lighthouse.get('categories', {})
        if 'performance' in categories:
            metrics['performance_score'] = categories['performance'].get('score', 0) * 100
        
        # Core Web Vitals and timing metrics
        audits = lighthouse.get('audits', {})
        
        # Map Lighthouse audits to model features
        for audit_key, feature_name in self.METRIC_MAPPING.items():
            if audit_key in audits:
                audit = audits[audit_key]
                # Get numeric value (in milliseconds for timing, unitless for CLS)
                metrics[feature_name] = audit.get('numericValue', 0)
        
        # Total byte weight
        if 'total-byte-weight' in audits:
            metrics['total_byte_weight'] = audits['total-byte-weight'].get('numericValue', 0)
        
        # Number of requests
        if 'network-requests' in audits:
            network_items = audits['network-requests'].get('details', {}).get('items', [])
            metrics['num_requests'] = len(network_items)
        
        # DOM size
        if 'dom-size' in audits:
            metrics['dom_size'] = audits['dom-size'].get('numericValue', 0)
        
        # Unused JavaScript
        if 'unused-javascript' in audits:
            unused_js_details = audits['unused-javascript'].get('details', {})
            items = unused_js_details.get('items', [])
            total_unused = sum(item.get('wastedBytes', 0) for item in items)
            metrics['unused_js'] = total_unused
        
        # Server response time (TTFB)
        if 'server-response-time' in audits:
            metrics['Response Time(s)'] = audits['server-response-time'].get('numericValue', 0) / 1000  # Convert to seconds
        
        # Calculate Page Size (KB) from total byte weight
        if 'total_byte_weight' in metrics:
            metrics['Page Size (KB)'] = metrics['total_byte_weight'] / 1024
        
        # Estimate Load Time (from LCP as proxy)
        if 'lcp' in metrics:
            metrics['Load Time(s)'] = metrics['lcp'] / 1000  # Convert to seconds
        
        # Throughput estimation (bytes / time)
        if 'total_byte_weight' in metrics and 'Load Time(s)' in metrics and metrics['Load Time(s)'] > 0:
            metrics['Throughput'] = metrics['total_byte_weight'] / metrics['Load Time(s)']
        
        # Additional diagnostic audits
        for audit_key in ['render-blocking-resources', 'uses-text-compression', 'modern-image-formats']:
            if audit_key in audits:
                audit = audits[audit_key]
                metrics[audit_key.replace('-', '_')] = audit.get('score', 0)
        
        # Raw Lighthouse data for reference
        metrics['_raw_lighthouse'] = {
            'fetchTime': lighthouse.get('fetchTime', ''),
            'finalUrl': lighthouse.get('finalUrl', ''),
            'lighthouseVersion': lighthouse.get('lighthouseVersion', ''),
        }
        
        return metrics
    
    def _print_metrics_summary(self, metrics):
        """Print a summary of collected metrics."""
        print(f"\n{'='*60}")
        print("COLLECTED METRICS SUMMARY")
        print(f"{'='*60}")
        
        # Performance score
        score = metrics.get('performance_score', 0)
        if score < 50:
            score_emoji = "🔴"
            score_label = "POOR"
        elif score < 90:
            score_emoji = "🟡"
            score_label = "NEEDS IMPROVEMENT"
        else:
            score_emoji = "🟢"
            score_label = "GOOD"
        
        print(f"\n{score_emoji} Performance Score: {score:.0f}/100 ({score_label})")
        
        print(f"\n📊 Core Web Vitals:")
        print(f"   FCP (First Contentful Paint):    {metrics.get('fcp', 0):,.0f} ms")
        print(f"   LCP (Largest Contentful Paint):  {metrics.get('lcp', 0):,.0f} ms")
        print(f"   TTI (Time to Interactive):       {metrics.get('tti', 0):,.0f} ms")
        print(f"   TBT (Total Blocking Time):       {metrics.get('tbt', 0):,.0f} ms")
        print(f"   CLS (Cumulative Layout Shift):   {metrics.get('cls', 0):.4f}")
        print(f"   Speed Index:                     {metrics.get('speed_index', 0):,.0f} ms")
        
        print(f"\n📦 Size Metrics:")
        print(f"   Total Byte Weight:               {metrics.get('total_byte_weight', 0):,.0f} bytes")
        print(f"   Page Size:                       {metrics.get('Page Size (KB)', 0):,.2f} KB")
        print(f"   Number of Requests:              {metrics.get('num_requests', 0)}")
        print(f"   DOM Size:                        {metrics.get('dom_size', 0):,.0f} elements")
        print(f"   Unused JavaScript:               {metrics.get('unused_js', 0):,.0f} bytes")
        
        print(f"\n⏱️ Timing Metrics:")
        print(f"   Response Time (TTFB):            {metrics.get('Response Time(s)', 0):.3f} s")
        print(f"   Load Time (estimated):           {metrics.get('Load Time(s)', 0):.3f} s")
        print(f"   Throughput:                      {metrics.get('Throughput', 0):,.0f} bytes/s")
        
        # Expected classification
        print(f"\n🎯 EXPECTED MODEL CLASSIFICATION:")
        if score < 50:
            print(f"   Based on performance score {score:.0f}, expected class: SLOW")
        elif score < 90:
            print(f"   Based on performance score {score:.0f}, expected class: MEDIUM")
        else:
            print(f"   Based on performance score {score:.0f}, expected class: FAST")
        
        print(f"\n{'='*60}")
    
    def save_metrics(self, metrics, output_path):
        """Save metrics to JSON file."""
        # Remove raw lighthouse data for cleaner output
        metrics_clean = {k: v for k, v in metrics.items() if not k.startswith('_')}
        
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"\n✓ Metrics saved to: {output_path}")
        
        return output_path
    
    def to_model_features(self, metrics):
        """
        Convert collected metrics to format expected by Phase 2 model.
        
        Returns a dictionary with feature names matching the model's expected input.
        """
        # Features expected by the XGBoost model (from IMPLEMENTATION_SUMMARY.md)
        model_features = {
            'fcp': metrics.get('fcp', 0),
            'lcp': metrics.get('lcp', 0),
            'tti': metrics.get('tti', 0),
            'tbt': metrics.get('tbt', 0),
            'cls': metrics.get('cls', 0),
            'speed_index': metrics.get('speed_index', 0),
            'Response Time(s)': metrics.get('Response Time(s)', 0),
            'Load Time(s)': metrics.get('Load Time(s)', 0),
            'performance_score': metrics.get('performance_score', 0),
            'Page Size (KB)': metrics.get('Page Size (KB)', 0),
            'total_byte_weight': metrics.get('total_byte_weight', 0),
            'num_requests': metrics.get('num_requests', 0),
            'Throughput': metrics.get('Throughput', 0),
            'unused_js': metrics.get('unused_js', 0),
            'Category': 'Test',  # Placeholder
        }
        
        return model_features


def main():
    parser = argparse.ArgumentParser(
        description='Collect PageSpeed Insights metrics for model validation'
    )
    parser.add_argument('--url', required=True, help='URL to analyze')
    parser.add_argument('--api-key', default=None, help='Google PageSpeed API key')
    parser.add_argument('--output', default='pagespeed_metrics.json', help='Output JSON file')
    parser.add_argument('--strategy', default='mobile', choices=['mobile', 'desktop'], 
                       help='Test strategy')
    parser.add_argument('--both', action='store_true', 
                       help='Collect both mobile and desktop metrics')
    
    args = parser.parse_args()
    
    collector = PageSpeedCollector(api_key=args.api_key)
    
    if args.both:
        # Collect both mobile and desktop
        print("\n" + "="*60)
        print("COLLECTING MOBILE METRICS")
        print("="*60)
        mobile_metrics = collector.collect_metrics(args.url, strategy='mobile')
        
        print("\n" + "="*60)
        print("COLLECTING DESKTOP METRICS")
        print("="*60)
        desktop_metrics = collector.collect_metrics(args.url, strategy='desktop')
        
        # Save both
        output_base = args.output.rsplit('.', 1)[0]
        if mobile_metrics:
            collector.save_metrics(mobile_metrics, f"{output_base}_mobile.json")
        if desktop_metrics:
            collector.save_metrics(desktop_metrics, f"{output_base}_desktop.json")
    else:
        metrics = collector.collect_metrics(args.url, strategy=args.strategy)
        if metrics:
            collector.save_metrics(metrics, args.output)
            
            # Also save model-ready features
            model_features = collector.to_model_features(metrics)
            model_output = args.output.rsplit('.', 1)[0] + '_model_features.json'
            with open(model_output, 'w') as f:
                json.dump(model_features, f, indent=2)
            print(f"✓ Model-ready features saved to: {model_output}")


if __name__ == "__main__":
    main()
