# AI Demand Forecast Narrative Generator

An AI-powered demand forecasting application developed for the Gen AI Hackathon 2026. The project combines time-series forecasting with generative AI to transform historical retail sales data into demand predictions, business insights, executive-level narratives, and actionable inventory recommendations.

The application uses the UCI Online Retail Dataset containing over 541,000 transactions. It combines data cleaning, revenue aggregation, Prophet-based forecasting, interactive analytics, and Google Gemini-powered narrative generation in an interactive Streamlit dashboard.

## Objectives

- Analyze historical retail transactions and revenue trends.
- Clean and transform transaction-level data into meaningful business metrics.
- Forecast future revenue using the Prophet time-series forecasting model.
- Visualize historical performance, forecast trends, and seasonal patterns.
- Generate executive-level business narratives using Google Gemini.
- Provide inventory planning insights and product-level stock predictions.
- Support data-driven supply chain and logistics decisions.

## Key Features

- **Demand Forecasting:** Explore historical revenue and future forecasts using Prophet-based time-series analysis.
- **Interactive Forecast Horizon:** Adjust the forecast horizon from 1 to 12 weeks.
- **Revenue Analytics:** View historical revenue summaries, peak periods, and overall trends.
- **Country-Level Analysis:** Filter sales by country and explore revenue distribution.
- **Product Analytics:** Identify top-selling products based on quantity sold.
- **Inventory Predictions:** Estimate 30-day stock requirements for the top 10 products using historical sales run rates.
- **AI Executive Narratives:** Use Google Gemini 1.5 Flash to generate business summaries and actionable recommendations.
- **Forecast Visualizations:** Explore historical revenue, predicted revenue, confidence intervals, seasonality, and Prophet components.
- **Report Export:** Download generated executive narratives and inventory action items as a text file.
- **Fallback Narrative Generation:** Provide a template-based narrative when the Gemini API key is unavailable or the API request fails.

## System Workflow

The application follows this workflow:

1. **Data Loading:** Load the Online Retail dataset and precomputed historical revenue, forecast results, and summary statistics.
2. **Data Cleaning:** Remove transactions with non-positive quantities and records with missing product descriptions.
3. **Feature Engineering:** Calculate transaction revenue using quantity multiplied by unit price.
4. **Revenue Aggregation:** Analyze historical weekly revenue and derive business summary statistics.
5. **Time-Series Forecasting:** Use Prophet-generated forecast outputs to estimate future revenue and associated confidence intervals.
6. **Interactive Analytics:** Filter countries and analyze revenue distribution, product sales, and projected inventory requirements.
7. **AI Narrative Generation:** Send forecast statistics to Google Gemini to generate an executive narrative and inventory action items.
8. **Report Export:** Display the generated report and allow users to download it as a text file.

The current application loads precomputed Prophet forecasts and a saved model file. The dashboard's interactive forecast horizon selects from the available forecast results; it does not retrain the forecasting model on every interaction.

## Technology Stack

- **Frontend and Dashboard:** Streamlit
- **Programming Language:** Python
- **Forecasting:** Prophet
- **Generative AI:** Google Gemini 1.5 Flash API
- **Data Processing:** Pandas
- **Data Visualization:** Plotly
- **Excel Processing:** OpenPyXL
- **API Integration:** Python Requests
- **Environment Configuration:** python-dotenv
- **Model Persistence:** Python Pickle

## Dataset

The project uses the **UCI Online Retail Dataset**, which contains transaction records from a UK-based online retail business.

The dataset includes information such as:

- Invoice numbers and invoice dates
- Product descriptions
- Quantities purchased
- Unit prices
- Customer identifiers
- Country information

These records support historical revenue analysis, product-level demand insights, country-level sales comparisons, and forecasting experiments.

The dataset is available through the [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail).

Users should review the dataset's terms of use and any applicable restrictions before redistributing or reusing the raw data.

## Forecasting and Analytics

The dashboard presents the following business metrics and visualizations:

- Total historical revenue
- Forecast revenue and percentage change against a comparable historical period
- Peak revenue week and associated value
- Overall historical trend direction
- Historical revenue versus forecasted revenue
- Forecast confidence intervals
- Revenue share by leading countries
- Top products by quantity sold
- Weekly revenue and monthly seasonality visualizations
- Prophet forecast components

The inventory module estimates 30-day product quantities using historical sales run rates. These values are indicative estimates rather than optimized replenishment quantities or guaranteed future demand.

## AI-Generated Business Narratives

The narrative generation module uses Google Gemini 1.5 Flash to interpret forecast statistics and produce a business-oriented report.

The generated content is designed to cover:

- Historical revenue performance
- Forecast outlook and percentage changes
- Major products and markets
- Potential business implications
- Inventory and supply chain action items

The application also includes a template-based fallback narrative when the Gemini API key is unavailable or a request fails.

AI-generated recommendations should be reviewed against actual business conditions before being used for operational decisions.

## Repository Structure

```text
ai-demand-forecast-narrative-generator/
├── app.py                    # Streamlit dashboard and application logic
├── chart_builder.py           # Forecast and analytics visualizations
├── narrative_generator.py    # Gemini API and fallback narrative generation
├── Online Retail.xlsx         # Retail transaction dataset
├── prophet_model.pkl         # Saved Prophet model artifact
├── weekly_revenue.csv        # Historical weekly revenue
├── forecast_output.csv       # Precomputed forecast results
├── stats_summary.csv         # Forecast and business summary statistics
├── forecast_chart.png        # Forecast visualization
├── monthly_seasonality.png   # Seasonality visualization
├── prophet_components.png    # Prophet component visualization
├── weekly_revenue_raw.png    # Historical revenue visualization
├── forecast_output.csv
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt          # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.10 or another Python version compatible with the project dependencies
- pip
- A Google Gemini API key for AI-powered narrative generation

### 1. Clone the Repository

```bash
git clone https://github.com/vaishzz-18/ai-demand-forecast-narrative-generator.git
cd ai-demand-forecast-narrative-generator
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a local `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key.

**Security note:** Never commit `.env` files or expose API keys in source code, screenshots, or public repositories.

If the API key is not configured, the application can fall back to template-based narrative generation.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the dashboard.

## Deployment

The application is designed to be hosted using Streamlit Community Cloud or another platform that supports Streamlit applications.

Deployment requires:

- A compatible Python environment
- The project's Python dependencies
- Access to the required dataset and precomputed forecast files
- Secure configuration of the Gemini API key

The live application URL will be added here after successful deployment.

## Limitations

- The dashboard currently relies on precomputed forecast outputs rather than retraining Prophet dynamically.
- Forecast quality depends on the historical data, preprocessing, and forecasting configuration.
- Inventory estimates use a simplified historical sales run-rate calculation.
- Gemini-generated narratives may contain inaccurate or incomplete business interpretations.
- Forecasts and inventory recommendations are estimates and should not be treated as guarantees.
- The raw dataset and saved model artifact must be available for the corresponding application functionality to work.
- The current Gemini integration uses the Gemini 1.5 Flash model identifier; API availability and model support may change over time.

## Project Information

**Project:** AI Demand Forecast Narrative Generator  
**Event:** Gen AI Hackathon 2026  
**Domain:** Supply Chain and Logistics  
**Repository:** [GitHub — AI Demand Forecast Narrative Generator](https://github.com/vaishzz-18/ai-demand-forecast-narrative-generator)

---

*Transforming retail data into demand forecasts, business narratives, and actionable inventory insights.*
