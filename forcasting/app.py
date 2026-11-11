import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

st.set_page_config(page_title="Enterprise Sales Forecasting System", layout="wide")

st.title("📊 Enterprise Sales Forecasting & Analytics System")
st.markdown("Upload any historical sales dataset, map your fields dynamically, and generate multi-step forecasts with confidence intervals and interactive visualizations.")

# ---------------------------------------------------------
# 1. FILE UPLOAD & DYNAMIC SCHEMA MAPPING
# ---------------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.subheader("1. Data Preview & Column Mapping")
    st.dataframe(df_raw.head(3), use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    
    all_columns = df_raw.columns.tolist()
    numeric_columns = df_raw.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df_raw.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Heuristic guessing for defaults
    date_guess = next((c for c in all_columns if "date" in c.lower() or "time" in c.lower()), all_columns[0])
    sales_guess = next((c for c in numeric_columns if "sale" in c.lower() or "revenue" in c.lower() or "qty" in c.lower()), numeric_columns[0] if numeric_columns else all_columns[-1])
    cat_guess = categorical_columns[0] if categorical_columns else None

    with col1:
        date_col = st.selectbox("Timestamp Column", all_columns, index=all_columns.index(date_guess))
    with col2:
        sales_col = st.selectbox("Target Sales Column", all_columns, index=all_columns.index(sales_guess))
    with col3:
        group_col = st.selectbox("Category/Store Column (Optional)", [None] + all_columns, index=0 if not cat_guess else all_columns.index(cat_guess)+1)
    with col4:
        forecast_horizon = st.selectbox("Forecast Horizon", [30, 60, 90], index=0)

    # ---------------------------------------------------------
    # 2. DATA PREPROCESSING & RESAMPLING
    # ---------------------------------------------------------
    try:
        cols_to_keep = [date_col, sales_col]
        if group_col:
            cols_to_keep.append(group_col)
            
        df = df_raw[cols_to_keep].copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df[sales_col] = pd.to_numeric(df[sales_col], errors='coerce')
        
        df = df.dropna(subset=[date_col, sales_col]).sort_values(by=date_col)
        
        # Aggregate to daily total
        if group_col:
            df_daily = df.groupby([date_col, group_col])[sales_col].sum().reset_index()
            # For ML core, use total daily across all groups or pivot
            df_total_daily = df.groupby(date_col)[sales_col].sum().reset_index()
            df_total_daily.set_index(date_col, inplace=True)
        else:
            df_total_daily = df.groupby(date_col)[sales_col].sum().reset_index()
            df_total_daily.set_index(date_col, inplace=True)
            
        df_total_daily = df_total_daily.asfreq('D').fillna(method='ffill')

    except Exception as e:
        st.error(f"Failed to process selected columns. Ensure date and sales columns contain valid values. Details: {e}")
        st.stop()

    st.success(f"Data ingested cleanly! Loaded records spanning from {df_total_daily.index.min().date()} to {df_total_daily.index.max().date()}.")

    # ---------------------------------------------------------
    # 3. CACHED MODEL TRAINING & CONFIDENCE INTERVALS
    # ---------------------------------------------------------
    @st.cache_data
    def train_forecasting_model(df_json, target_col):
        data = pd.read_json(df_json, orient='split')
        data.index = pd.to_datetime(data.index)
        
        # Feature Engineering
        df_feat = data.copy()
        df_feat['dayofweek'] = df_feat.index.dayofweek
        df_feat['month'] = df_feat.index.month
        df_feat['quarter'] = df_feat.index.quarter
        df_feat['lag_1'] = df_feat[target_col].shift(1)
        df_feat['lag_7'] = df_feat[target_col].shift(7)
        df_feat['lag_30'] = df_feat[target_col].shift(30)
        df_feat['rolling_mean_7'] = df_feat[target_col].shift(1).rolling(7).mean()
        df_feat['rolling_mean_30'] = df_feat[target_col].shift(1).rolling(30).mean()
        
        df_featured = df_feat.dropna()
        
        train_data = df_featured.iloc[:-30]
        test_data = df_featured.iloc[-30:]
        
        feature_cols = ['dayofweek', 'month', 'quarter', 'lag_1', 'lag_7', 'lag_30', 'rolling_mean_7', 'rolling_mean_30']
        
        model = RandomForestRegressor(n_estimators=150, random_state=42)
        model.fit(train_data[feature_cols], train_data[target_col])
        
        # Validation & Residual Standard Error for Confidence Intervals
        val_preds = model.predict(test_data[feature_cols])
        residuals = test_data[target_col] - val_preds
        std_residuals = np.std(residuals)
        
        mape = mean_absolute_percentage_error(test_data[target_col], val_preds) * 100
        rmse = np.sqrt(mean_squared_error(test_data[target_col], val_preds))
        
        return model, mape, rmse, std_residuals, feature_cols

    json_payload = df_total_daily.to_json(orient='split', date_format='iso')
    model, mape, rmse, std_residuals, feature_cols = train_forecasting_model(json_payload, sales_col)

    if len(df_total_daily) < 60:
        st.warning("Warning: Less than 60 days of history detected. Forecast accuracy improves significantly with 90+ days of data.")

    # ---------------------------------------------------------
    # 4. RECURSIVE MULTI-STEP FORECASTING
    # ---------------------------------------------------------
    last_known_date = df_total_daily.index.max()
    future_dates = [last_known_date + timedelta(days=i) for i in range(1, forecast_horizon + 1)]
    
    history_series = df_total_daily[sales_col].copy()
    future_predictions = []

    for idx, target_date in enumerate(future_dates):
        lag_1 = history_series.iloc[-1]
        lag_7 = history_series.iloc[-7] if len(history_series) >= 7 else lag_1
        lag_30 = history_series.iloc[-30] if len(history_series) >= 30 else lag_1
        
        rolling_7 = history_series.iloc[-7:].mean()
        rolling_30 = history_series.iloc[-30:].mean()
        
        features = np.array([[
            target_date.dayofweek,
            target_date.month,
            target_date.quarter,
            lag_1,
            lag_7,
            lag_30,
            rolling_7,
            rolling_30
        ]])
        
        pred_value = model.predict(features)[0]
        future_predictions.append(pred_value)
        history_series.loc[target_date] = pred_value

    # Confidence intervals widen over time horizon (sqrt of steps ahead)
    confidence_multiplier = 1.96  # 95% CI
    margins = [confidence_multiplier * std_residuals * np.sqrt(i) for i in range(1, forecast_horizon + 1)]
    
    df_forecast = pd.DataFrame({
        'Date': future_dates,
        'Forecasted_Sales': future_predictions,
        'Forecast_Lower': [max(0, p - m) for p, m in zip(future_predictions, margins)],
        'Forecast_Upper': [p + m for p, m in zip(future_predictions, margins)]
    }).set_index('Date')

    # ---------------------------------------------------------
    # 5. DASHBOARD METRICS & MULTI-CHART SUITE
    # ---------------------------------------------------------
    st.subheader("2. Executive Summary Dashboard")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Validation MAPE", f"{mape:.2f}%")
    m2.metric("Validation RMSE", f"₹{rmse:,.2f}")
    m3.metric(f"Projected Total ({forecast_horizon} Days)", f"₹{sum(future_predictions):,.2f}")
    m4.metric("Average Daily Forecast", f"₹{np.mean(future_predictions):,.2f}")

    st.markdown("---")
    st.subheader("3. Interactive Visualizations & Analytics Suite")

    # Chart 1: Main Line Chart with Confidence Interval Band
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_total_daily.index[-90:], y=df_total_daily[sales_col].iloc[-90:], 
        mode='lines', name='Historical Sales (Last 90 Days)', line=dict(color='#1f77b4', width=2)
    ))
    fig_line.add_trace(go.Scatter(
        x=df_forecast.index, y=df_forecast['Forecasted_Sales'], 
        mode='lines+markers', name=f'{forecast_horizon}-Day Forecast', line=dict(dash='dash', color='#ff7f0e', width=2)
    ))
    # Confidence Band
    fig_line.add_trace(go.Scatter(
        x=df_forecast.index.tolist() + df_forecast.index[::-1].tolist(),
        y=df_forecast['Forecast_Upper'].tolist() + df_forecast['Forecast_Lower'][::-1].tolist(),
        fill='toself', fillcolor='rgba(255, 127, 14, 0.15)',
        line=dict(color='rgba(255,255,255,0)'), name='95% Confidence Interval'
    ))
    fig_line.update_layout(title="Historical vs. Forecasted Sales Trajectory", xaxis_title="Date", yaxis_title="Sales (₹)", hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

    # Secondary Charts Row
    c1, c2 = st.columns(2)

    with c1:
        # Chart 2: Bar Chart - Average Sales by Day of Week
        temp_dow = df_total_daily.copy()
        temp_dow['DayOfWeek'] = temp_dow.index.day_name()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_avg = temp_dow.groupby('DayOfWeek')[sales_col].mean().reindex(dow_order).reset_index()
        
        fig_bar = px.bar(dow_avg, x='DayOfWeek', y=sales_col, title="Average Sales by Day of the Week",
                         labels={sales_col: "Average Sales (₹)", "DayOfWeek": "Day"}, color=sales_col, color_continuous_scale='blues')
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        # Chart 3: Pie/Donut Chart or Monthly Trend Bar Chart
        if group_col:
            # Category breakdown Donut Chart
            cat_sales = df.groupby(group_col)[sales_col].sum().reset_index()
            fig_pie = px.pie(cat_sales, names=group_col, values=sales_col, title=f"Sales Distribution by {group_col}", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            # Monthly Aggregation Bar Chart
            temp_m = df_total_daily.copy()
            temp_m['Month'] = temp_m.index.to_period('M').astype(str)
            m_sum = temp_m.groupby('Month')[sales_col].sum().reset_index()
            fig_month = px.bar(m_sum, x='Month', y=sales_col, title="Monthly Aggregated Sales Trend",
                               labels={sales_col: "Total Sales (₹)"}, color_discrete_sequence=['#2ca02c'])
            st.plotly_chart(fig_month, use_container_width=True)

    # ---------------------------------------------------------
    # 6. EXPORT FORECAST TABLE
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("4. Detailed Forecast Table & Export")
    
    display_df = df_forecast.copy()
    display_df.columns = ['Forecasted Sales (₹)', 'Lower Bound (95% CI)', 'Upper Bound (95% CI)']
    st.dataframe(display_df.style.format("₹{:,.2f}"), use_container_width=True)
    
    csv_data = df_forecast.to_csv().encode('utf-8')
    st.download_button("Download Forecast CSV", data=csv_data, file_name=f"sales_forecast_{forecast_horizon}days.csv", mime="text/csv")

else:
    st.info("👈 Please upload your CSV or Excel dataset using the sidebar file uploader to begin.")