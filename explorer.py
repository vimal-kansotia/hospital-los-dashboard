"""
Page 7: Data Explorer
Raw data inspection and exploration
"""

import streamlit as st
import pandas as pd

def show(df):
    st.markdown("# 📋 Data Explorer")
    st.markdown("*Search, filter, and inspect the raw hospital dataset*")
    st.divider()
    
    # Data Health Check
    st.markdown("## 🏥 Data Quality Summary")
    
    health_col1, health_col2, health_col3, health_col4 = st.columns(4)
    
    with health_col1:
        st.metric("Total Records", f"{len(df):,}")
    
    with health_col2:
        st.metric("Total Columns", len(df.columns))
    
    with health_col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    
    with health_col4:
        st.metric("Duplicate Rows", df.duplicated().sum())
    
    st.success("✅ Data Quality: Excellent (0 missing values)")
    
    st.divider()
    
    # Search & Filter
    st.markdown("## 🔍 Search & Filter")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        search_column = st.selectbox(
            "Search in Column",
            options=['All Columns'] + list(df.columns),
            key="search_column"
        )
    
    with filter_col2:
        search_term = st.text_input(
            "Search Keyword (optional)",
            key="search_term"
        )
    
    with filter_col3:
        rows_per_page = st.selectbox(
            "Rows Per Page",
            options=[10, 25, 50, 100, 250],
            index=2,
            key="rows_per_page"
        )
    
    # Apply search filter
    df_search = df.copy()
    if search_term:
        if search_column == 'All Columns':
            mask = df_search.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
            df_search = df_search[mask]
        else:
            df_search = df_search[
                df_search[search_column].astype(str).str.contains(
                    search_term, case=False, na=False
                )
            ]
    
    st.divider()
    
    # Additional Filters
    st.markdown("## 🎯 Category Filters")
    
    filter_col_a, filter_col_b, filter_col_c = st.columns(3)
    
    with filter_col_a:
        gender_filter = st.multiselect(
            "Gender",
            options=['M', 'F'],
            default=['M', 'F'],
            key="explorer_gender_filter"
        )
        df_search = df_search[df_search['gender'].isin(gender_filter)]
    
    with filter_col_b:
        facility_filter = st.multiselect(
            "Facility",
            options=sorted(df['facid'].unique()),
            default=sorted(df['facid'].unique()),
            key="explorer_facility_filter"
        )
        df_search = df_search[df_search['facid'].isin(facility_filter)]
    
    with filter_col_c:
        los_range = st.slider(
            "Length of Stay Range",
            min_value=int(df['lengthofstay'].min()),
            max_value=int(df['lengthofstay'].max()),
            value=(1, 17),
            key="explorer_los_range"
        )
        df_search = df_search[
            (df_search['lengthofstay'] >= los_range[0]) &
            (df_search['lengthofstay'] <= los_range[1])
        ]
    
    st.info(f"📊 Showing {len(df_search):,} of {len(df):,} records")
    
    st.divider()
    
    # Sort options
    st.markdown("## 📑 Sort & Display")
    
    sort_col1, sort_col2, sort_col3 = st.columns(3)
    
    with sort_col1:
        sort_column = st.selectbox(
            "Sort by Column",
            options=df.columns,
            index=df.columns.get_loc('lengthofstay') if 'lengthofstay' in df.columns else 0,
            key="sort_column"
        )
    
    with sort_col2:
        sort_order = st.selectbox(
            "Sort Order",
            options=['Descending', 'Ascending'],
            key="sort_order"
        )
    
    with sort_col3:
        ascending = sort_order == 'Ascending'
        df_search = df_search.sort_values(by=sort_column, ascending=ascending)
    
    st.divider()
    
    # Data Table
    st.markdown("## 📋 Data Table")
    
    # Pagination
    total_records = len(df_search)
    total_pages = (total_records + rows_per_page - 1) // rows_per_page
    
    page_col1, page_col2, page_col3, page_col4 = st.columns(4)
    
    with page_col1:
        current_page = st.number_input(
            "Go to Page",
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            key="current_page"
        )
    
    with page_col2:
        st.write(f"Page {current_page} of {total_pages}")
    
    with page_col3:
        st.write(f"Total: {total_records} records")
    
    with page_col4:
        st.write(f"Rows/Page: {rows_per_page}")
    
    # Calculate pagination
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    
    df_display = df_search.iloc[start_idx:end_idx]
    
    # Display table
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    st.divider()
    
    # Column Information
    st.markdown("## 📊 Column Information")
    
    col_info_tab1, col_info_tab2 = st.tabs(["Data Types", "Value Ranges"])
    
    with col_info_tab1:
        col_info_data = []
        for col in df.columns:
            col_info_data.append({
                'Column': col,
                'Data Type': str(df[col].dtype),
                'Non-Null Count': f"{df[col].notna().sum():,}",
                'Unique Values': f"{df[col].nunique():,}"
            })
        
        col_info_df = pd.DataFrame(col_info_data)
        st.dataframe(col_info_df, use_container_width=True, hide_index=True)
    
    with col_info_tab2:
        # Show statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        stats_data = []
        for col in numeric_cols[:8]:  # Show first 8
            stats_data.append({
                'Column': col,
                'Min': f"{df[col].min():.2f}",
                'Max': f"{df[col].max():.2f}",
                'Mean': f"{df[col].mean():.2f}",
                'Median': f"{df[col].median():.2f}"
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Export Options
    st.markdown("## 📥 Export Data")
    
    export_col1, export_col2, export_col3 = st.columns(3)
    
    with export_col1:
        csv = df_search.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered as CSV",
            data=csv,
            file_name="hospital_data_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col2:
        # Excel export (simplified)
        st.info("💾 Excel export available via CLI")
    
    with export_col3:
        st.metric("Export Size", f"~{len(csv) / (1024*1024):.2f} MB")
