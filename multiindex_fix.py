"""
Solution for MultiIndex Reindexing Error

The error "cannot handle a non-unique multi-index!" occurs when your DataFrame 
has duplicate index values. This script demonstrates the problem and provides 
multiple solutions.
"""

import pandas as pd
import numpy as np

def demonstrate_multiindex_error():
    print("=== MULTIINDEX REINDEXING ERROR DEMONSTRATION ===\n")
    
    # Create sample data with duplicate indices
    locations = ['A', 'B', 'C']
    times = [1, 2, 3]
    
    # Create some sample data with duplicates
    np.random.seed(42)
    sample_data = []
    for loc in locations:
        for time in times:
            # Add multiple entries for some combinations (creating duplicates)
            for _ in range(np.random.choice([1, 2])):  # 1 or 2 entries per combination
                sample_data.append({
                    'location': loc,
                    'time': time,
                    'value': np.random.randn()
                })
    
    # Create DataFrame with MultiIndex
    data_df = pd.DataFrame(sample_data).set_index(['location', 'time'])
    print("Sample data with duplicates:")
    print(data_df)
    print(f"Has duplicates: {data_df.index.duplicated().any()}")
    print(f"Number of duplicates: {data_df.index.duplicated().sum()}")
    print()
    
    # Create the full index we want to reindex to
    full_index = pd.MultiIndex.from_product(
        [locations, times],
        names=['location', 'time']
    )
    print("Full index we want to reindex to:")
    print(full_index)
    print()
    
    # Try the original approach (this will fail)
    try:
        result = data_df.reindex(full_index)
        print("✅ Original reindex succeeded")
    except ValueError as e:
        print(f"❌ Original reindex failed: {e}")
    print()
    
    return data_df, full_index

def solution_1_remove_duplicates(data_df, full_index):
    """Solution 1: Remove duplicate indices before reindexing"""
    print("=== SOLUTION 1: Remove duplicates (keep first) ===")
    
    # Remove duplicates, keeping the first occurrence
    data_df_clean = data_df[~data_df.index.duplicated(keep='first')]
    print(f"After removing duplicates: {data_df_clean.shape[0]} rows")
    
    # Now reindex
    result = data_df_clean.reindex(full_index)
    print("✅ Success! Result shape:", result.shape)
    print("Result:")
    print(result)
    print()
    return result

def solution_2_aggregate_duplicates(data_df, full_index):
    """Solution 2: Aggregate duplicate indices"""
    print("=== SOLUTION 2: Aggregate duplicates using mean ===")
    
    # Group by index and aggregate (using mean)
    data_df_agg = data_df.groupby(level=[0, 1]).mean()
    print(f"After aggregating: {data_df_agg.shape[0]} rows")
    
    # Now reindex
    result = data_df_agg.reindex(full_index)
    print("✅ Success! Result shape:", result.shape)
    print("Result:")
    print(result)
    print()
    return result

def solution_3_aggregate_other_methods(data_df, full_index):
    """Solution 3: Other aggregation methods"""
    print("=== SOLUTION 3: Other aggregation methods ===")
    
    # You can use different aggregation methods:
    methods = ['first', 'last', 'sum', 'max', 'min']
    
    for method in methods:
        try:
            if method in ['first', 'last']:
                data_df_agg = getattr(data_df.groupby(level=[0, 1]), method)()
            else:
                data_df_agg = getattr(data_df.groupby(level=[0, 1]), method)()
            
            result = data_df_agg.reindex(full_index)
            print(f"✅ {method.upper()} method - Success! Shape: {result.shape}")
        except Exception as e:
            print(f"❌ {method.upper()} method failed: {e}")
    print()

def solution_4_merge_approach(data_df, full_index):
    """Solution 4: Use merge instead of reindex"""
    print("=== SOLUTION 4: Using merge instead of reindex ===")
    
    # First remove duplicates (or aggregate them)
    data_df_clean = data_df[~data_df.index.duplicated(keep='first')]
    
    # Reset index to columns
    data_df_reset = data_df_clean.reset_index()
    
    # Create full index as DataFrame
    full_df = pd.DataFrame(index=full_index).reset_index()
    
    # Merge to get all combinations
    result = full_df.merge(data_df_reset, on=['location', 'time'], how='left').set_index(['location', 'time'])
    
    print("✅ Success! Result shape:", result.shape)
    print("Result:")
    print(result)
    print()
    return result

def diagnostic_functions(data_df):
    """Diagnostic functions to understand your data"""
    print("=== DIAGNOSTIC FUNCTIONS ===")
    
    print("1. Check for duplicates:")
    print(f"   Has duplicate indices: {data_df.index.duplicated().any()}")
    print(f"   Number of duplicates: {data_df.index.duplicated().sum()}")
    
    if data_df.index.duplicated().any():
        print("   Duplicate indices:")
        duplicate_indices = data_df.index[data_df.index.duplicated()]
        for idx in duplicate_indices.unique():
            print(f"     {idx}")
            
    print("\n2. Index information:")
    print(f"   Index type: {type(data_df.index)}")
    print(f"   Index names: {data_df.index.names}")
    print(f"   Index levels: {data_df.index.nlevels}")
    
    print("\n3. Data at duplicate indices:")
    if data_df.index.duplicated().any():
        for idx in data_df.index[data_df.index.duplicated()].unique():
            print(f"   Data at {idx}:")
            print(data_df.loc[idx])
    print()

if __name__ == "__main__":
    # Demonstrate the problem and solutions
    data_df, full_index = demonstrate_multiindex_error()
    
    # Show diagnostic information
    diagnostic_functions(data_df)
    
    # Apply all solutions
    result1 = solution_1_remove_duplicates(data_df, full_index)
    result2 = solution_2_aggregate_duplicates(data_df, full_index)
    solution_3_aggregate_other_methods(data_df, full_index)
    result4 = solution_4_merge_approach(data_df, full_index)
    
    print("=== SUMMARY ===")
    print("Choose the solution that best fits your use case:")
    print("1. Remove duplicates if you only want one value per index combination")
    print("2. Aggregate if you want to combine duplicate values (mean, sum, etc.)")
    print("3. Use merge if you need more control over the process")
    print("\nFor your specific error, replace your problematic code:")
    print("# data_df = data_df.reindex(full_index)  # This fails")
    print("# With one of these:")
    print("data_df = data_df[~data_df.index.duplicated(keep='first')].reindex(full_index)")
    print("# OR")
    print("data_df = data_df.groupby(level=[0, 1]).first().reindex(full_index)")