# Makefile for GPay AI Insights Engine

IMAGE_NAME=gpay-ai-insights
DATA_DIR=$(PWD)/data

.PHONY: all build cli ui clean train-ml-categorizer

all: build cli

build:
	docker build -t $(IMAGE_NAME) .

train-ml-categorizer:
	mkdir -p model
	docker run --rm -v "$(DATA_DIR):/app/data" -v "$(PWD)/model:/app/model" $(IMAGE_NAME) python app/train_categorizer.py data/labeled_transactions.csv model/categorizer.pkl

cli:
	docker run --rm -v "$(DATA_DIR):/app/data" $(IMAGE_NAME) python app/main.py data/sample_transactions.csv

ui:
	docker run --rm -p 8501:8501 -v "$(DATA_DIR):/app/data" $(IMAGE_NAME) streamlit run ui/streamlit_app.py

clean:
	docker rmi $(IMAGE_NAME) || true
