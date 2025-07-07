# Lightweight Dockerfile for GPay AI Insights Engine

FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system dependencies for pandas, matplotlib, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default: run CLI help
CMD ["python", "app/main.py"]

# To run Streamlit UI:
# docker run -p 8501:8501 gpay-ai-insights streamlit run ui/streamlit_app.py
