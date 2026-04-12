# Forecast

A full-stack time series forecasting and anomaly detection application with AI-powered insights. Especially curated for non-tech people so that they can leverage the benefits of Data Science. Forecast uses multiple statistical models to predict future trends and automatically detects outliers in your data.

## Features

- **Multiple Forecasting Models**
  - Moving Average forecasting
  - Linear Trend prediction
  - Holt-Winters Exponential Smoothing (with seasonal decomposition)
  - Intelligent model selection based on data characteristics

- **Anomaly Detection**
  - Statistical anomaly detection using z-score (2σ threshold)
  - Automatic identification of outliers in time series data

- **AI-Powered Insights**
  - Integration with Google Generative AI for natural language insights
  - Query-based analysis of forecasts and data patterns
  - Automatic anomaly explanation and recommendations

- **Flexible Data Input**
  - Direct API calls with numerical arrays
  - CSV file uploads with targeted column selection
  - Support for large datasets with built-in validation

- **Feature Analysis**
  - Automatic feature extraction (seasonality, trend strength, noise level)
  - Model selection based on data characteristics
  - Performance metrics (MAPE) for model evaluation

- **Modern UI**
  - React + TypeScript frontend
  - Responsive design with Tailwind CSS
  - Real-time forecasting visualization
  - Interactive data upload and analysis

ML explores hidden patterns, LLM explains it

## 🛠️ Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn
- Google Generative AI API key (for LLM features)

## 📦 Installation

### Backend Setup

1. Clone the repository and navigate to the project directory:
```bash
cd d:\forecast
```

2. Create and activate a Python virtual environment:
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google Generative AI API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Return to the project root:
```bash
cd ..
```

## 🚀 Running the Application

### Start the Backend Server

```bash
# Make sure you're in the project root with the virtual environment activated
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

### Start the Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🔌 API Endpoints

### POST `/forecast`
Make a forecast with a data array and optional query.

**Request:**
```json
{
  "values": [10, 12, 15, 14, 16, 18, 20, 19, 22],
  "query": "What trend do you see in this data?"
}
```

**Response:**
```json
{
  "forecast": [...],
  "anomalies": [...],
  "features": {...},
  "selected_model": "holt_winters",
  "insights": "..."
}
```

### POST `/forecast/csv`
Upload a CSV file and forecast a specific column.

**Form Data:**
- `file`: CSV file (multipart/form-data)
- `target_column`: Column name to forecast
- `user_query`: Optional query for insights

**Response:** Same as `/forecast` endpoint

## Project Structure

```
forecast/
├── backend/
│   ├── main.py              # FastAPI application and endpoints
│   ├── pipeline.py          # Data processing pipeline
│   ├── models.py            # Forecasting models (moving average, linear trend, Holt-Winters)
│   ├── anomaly.py           # Anomaly detection logic
│   ├── features.py          # Feature extraction for data analysis
│   ├── graph.py             # LangChain/agentic workflow for insights
│   ├── llm.py               # Google Generative AI integration
│   ├── insight.py           # Insight generation
│   └── config.py            # Configuration settings
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app component
│   │   ├── main.tsx         # React entry point
│   │   └── index.css        # Global styles
│   ├── public/              # Static assets
│   ├── vite.config.ts       # Vite configuration
│   └── package.json         # Frontend dependencies
├── tests/
│   ├── test_api.py          # API endpoint tests
│   ├── test_data.csv        # Test dataset
│   └── seasonal_test_data.csv
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata and config
└── README.md               # This file
```

## Supported Forecasting Models

| Model | Best For | Characteristics |
|-------|----------|-----------------|
| **Moving Average** | Noisy data, high noise levels | Simple, smooths out fluctuations |
| **Linear Trend** | Trending data | Captures consistent directional change |
| **Holt-Winters** | Seasonal data, strong trends | Captures trends and seasonality |

The system automatically selects the best model based on:
- Seasonality strength (>0.5 → Holt-Winters)
- Trend strength (>0.5 → Holt-Winters)
- Noise level (>0.6 → Moving Average)

## Running Tests

Run the test suite using pytest:

```bash
# Activate virtual environment first
pytest tests/ -v
```

Test files include:
- `test_api.py` - API endpoint tests
- Sample test data files for validation

## 🔧 Development

### Backend Development

- Backend server runs with `--reload` flag for hot reloading
- Edit files in `backend/` and changes will automatically reload

### Frontend Development  

- Frontend runs with Vite dev server for instant updates
- Watch mode automatically rebuilds TypeScript and triggers browser refresh

### Code Quality

Lint the frontend code:
```bash
cd frontend
npm run lint
```

Build for production:
```bash
# Backend runs as-is with uvicorn
# Frontend
npm run build
```

## Key Dependencies

### Backend
- **FastAPI** - Web framework
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **scikit-learn** - Machine learning models
- **statsmodels** - Time series analysis (Holt-Winters)
- **scipy** - Scientific computing
- **google-generativeai** - LLM integration
- **python-dotenv** - Environment variable management

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Component library
- **Lucide React** - Icon library
- **Motion** - Animation library

## AI Features

The application integrates Google Generative AI to:
- Explain forecast trends in natural language
- Answer questions about data patterns
- Provide recommendations based on anomalies
- Generate insights from statistical analysis

## Data Validation

The system validates input data to ensure quality forecasts:
- Rejects non-numeric columns
- Removes NaN values automatically
- Ensures minimum data length requirements
- Sanitizes responses to prevent JSON serialization errors
- Handles edge cases (zero-variance data, very small datasets)

## Known Considerations

- **Zero-Variance Data**: Features module guards against zero-variance inputs to prevent NaN/inf values
- **Small Datasets**: Models default to moving average for very small datasets (≤5 values)
- **JSON Serialization**: Non-finite float values (NaN, inf) are sanitized to null before response

## Environment Variables

Create a `.env` file in the project root:

```env
# Google Generative AI
GOOGLE_API_KEY=your_api_key_here

# FastAPI (optional)
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```
## 📊 Flowchart

```mermaid
flowchart TD

A[Start] --> B[Input Data\n(API / CSV / UI)]

B --> C[Data Cleaning & Validation]

C --> D[Feature Extraction]
D --> D1[Trend]
D --> D2[Seasonality]
D --> D3[Noise]

D --> E[Select Model]

E -->|Stable / Noisy| F[Moving Average]
E -->|Trend Detected| G[Linear Trend]
E -->|Seasonality Detected| H[Holt-Winters]

F --> I[Generate Forecast]
G --> I
H --> I

I --> J[Estimate Uncertainty\n(Residual Std)]

J --> K[Create Prediction Range\n(Lower & Upper Bounds)]

I --> L[Detect Anomalies\n(Deviation Check)]

I --> M[Compare with Baseline\n(MAPE)]

I --> N[Generate Insights]

N --> O[LLM Explanation\n(Simple Language)]

K --> P[Final Output]
L --> P
M --> P
O --> P

P --> Q[Display Results\n(Charts + Alerts)]

Q --> R[End]

## Deployment

### Backend
- Use `uvicorn` with production settings:
  ```bash
  uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```

### Frontend
- Build for production:
  ```bash
  cd frontend && npm run build
  ```
- Serve the `dist/` folder with your preferred web server

## License

Add your license here

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or feedback, please open an issue on the repository.

---

**Made with ❤️ for time series forecasting**
