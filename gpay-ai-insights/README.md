# GPay AI Insights Engine

A modular engine to extract, analyze, and generate insights from your Google Pay Takeout data.

---

## How to Use

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/gpay-ai-insights-engine.git
   cd gpay-ai-insights-engine/gpay-ai-insights
   ```

2. **(Recommended) Use Docker and Makefile:**

   - Build the Docker image:
     ```
     make build
     ```
   - (Optional) Train the ML categorizer if you have labeled data:
     ```
     make train-ml-categorizer
     ```
   - Run the CLI:
     ```
     make
     ```
   - Or launch the Streamlit UI:
     ```
     make ui
     ```
     Then open [http://localhost:8501](http://localhost:8501) in your browser.

3. **Or, run locally with Python:**

   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the CLI:
     ```
     python app/main.py data/sample_transactions.csv
     ```
   - Or launch the UI:
     ```
     streamlit run ui/streamlit_app.py
     ```

4. **Upload your own Google Pay data:**
   - Download your data from Google Takeout and place the HTML file in the `data/` folder.
   - Use the UI or CLI to analyze your transactions.

See below for more details on setup, training, and advanced features.

---

## Project Structure

```
gpay-ai-insights/
├── data/
│   └── sample_transactions.csv
├── app/
│   ├── main.py
│   ├── insights.py
│   ├── categorizer.py
│   └── recommender.py
├── notebooks/
│   └── prompt_engineering.ipynb
├── ui/
│   └── streamlit_app.py
├── tests/
│   └── test_categorizer.py
├── requirements.txt
├── README.md
└── .env.example
```

## Features

- Parse Google Pay "My Activity.html" and extract transactions
- Analyze spending, income, top merchants, and more
- **Automatically categorize spending** (groceries, fuel, travel, food delivery, shopping, utilities, etc.) using merchant/description keywords
- Categorize transactions and generate recommendations
- Extensible: add your own insights, categorization, or UI

## Setup

1. Clone this repo or copy the folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Place your Google Pay Takeout HTML in the `data/` folder.

## Usage

Run the main script to extract and analyze transactions:

```
python app/main.py data/My\ Activity.html
```

Or launch the Streamlit UI (optional):

```
streamlit run ui/streamlit_app.py
```

## Docker & Makefile Quickstart

> **Prerequisite:**  
> Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running on your system before using these commands.

You can use Docker and the provided Makefile to run everything with a single command—no need to install Python or pip on your system.

### Build the Docker image

If you make changes to the code or dependencies, or if you see errors about missing files, run:

```
make build
```

- This builds (or rebuilds) the Docker image for the project.

### Build and Run (CLI):

```
make
```

- This builds the Docker image and runs the CLI on your sample data.

### Run the CLI (analyze transactions):

```
make cli
```

### Launch the Streamlit UI:

```
make ui
```

- Then open [http://localhost:8501](http://localhost:8501) in your browser.

### Clean up Docker images:

```
make clean
```

## Training the ML Categorizer

To use AI/NLP-based categorization, you need to create a labeled CSV and train the model:

1. **Create a labeled CSV:**  
   Save a file as `data/labeled_transactions.csv` with columns: `merchant`, `raw`, `category`.  
   Example:

   ```
   merchant,raw,category
   bigbasket,"Paid ₹1200.00 to BigBasket using Bank Account XXXXXX3609 1 Jul 2025, 10:00:00 GMT+05:30",groceries
   indian oil,"Paid ₹2000.00 to Indian Oil using Bank Account XXXXXX3609 2 Jul 2025, 11:00:00 GMT+05:30",fuel
   ...
   ```

2. **Train the model:**

   ```
   make train-ml-categorizer
   ```

   This will train the model and save it to `model/categorizer.pkl`.

3. **(Optional) Integrate the model:**  
   Update the code to load and use the trained model for categorization.

## Environment Variables

Copy `.env.example` to `.env` and fill in any required values.

## TODO / Planned Features

- [ ] **Smart, human-readable insights** (e.g., "Your monthly travel expenses increased by 30%", "Top 3 merchants: Amazon, BigBasket, Swiggy")
- [ ] **Budgeting tips and suggestions**

## License

MIT
