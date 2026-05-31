import plotly.graph_objects as go
import plotly.express as px

def build_forecast_chart(weekly_df, forecast_df):
    last_hist_date = weekly_df['ds'].max()
    
    # Filter forecast_df for future dates
    future_forecast = forecast_df[forecast_df['ds'] > last_hist_date]
    
    fig = go.Figure()
    
    # Historical Revenue (Blue solid line)
    fig.add_trace(go.Scatter(
        x=weekly_df['ds'],
        y=weekly_df['y'],
        mode='lines',
        name='Historical Revenue',
        line=dict(color='blue', width=2)
    ))
    
    # Forecast Confidence Band (Amber shaded)
    # Using 'toself' to fill the area between lower and upper bounds
    x_band = future_forecast['ds'].tolist() + future_forecast['ds'].tolist()[::-1]
    y_band = future_forecast['yhat_upper'].tolist() + future_forecast['yhat_lower'].tolist()[::-1]
    
    fig.add_trace(go.Scatter(
        x=x_band,
        y=y_band,
        fill='toself',
        fillcolor='rgba(255, 191, 0, 0.3)', # Amber with opacity
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # Forecast Revenue (Orange dashed line)
    fig.add_trace(go.Scatter(
        x=future_forecast['ds'],
        y=future_forecast['yhat'],
        mode='lines',
        name='Forecast',
        line=dict(color='orange', width=2, dash='dash')
    ))
    
    # Vertical line at forecast start
    forecast_start = future_forecast['ds'].min()
    fig.add_shape(
        type="line",
        x0=forecast_start,
        y0=0,
        x1=forecast_start,
        y1=1,
        yref="paper",
        line=dict(color="gray", width=2, dash="dot")
    )
    fig.add_annotation(
        x=forecast_start,
        y=1,
        yref="paper",
        text="Forecast start",
        showarrow=False,
        xanchor="left",
        yanchor="bottom"
    )
    
    # Layout configuration
    fig.update_layout(
        title="Weekly Revenue — Historical & 12-Week Forecast",
        plot_bgcolor="white",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray'
        )
    )
    
    return fig

def build_pie_chart(df):
    country_rev = df.groupby('Country')['TotalSales'].sum().reset_index()
    # Sort and take top 10
    country_rev = country_rev.sort_values('TotalSales', ascending=False).head(10)
    fig = px.pie(
        country_rev, 
        values='TotalSales', 
        names='Country', 
        title='Revenue Share by Top Countries',
        hole=0.4
    )
    fig.update_layout(plot_bgcolor="white")
    return fig

def build_bar_chart(df):
    prod_qty = df.groupby('Description')['Quantity'].sum().reset_index()
    prod_qty = prod_qty.sort_values('Quantity', ascending=False).head(10)
    fig = px.bar(
        prod_qty, 
        x='Quantity', 
        y='Description', 
        orientation='h',
        title='Top 10 Products by Quantity Sold',
        color='Quantity',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        plot_bgcolor="white",
        yaxis={'categoryorder': 'total ascending'}
    )
    return fig
