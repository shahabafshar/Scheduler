FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scheduler/ ./scheduler/
COPY documents/ ./documents/

# Expose Streamlit port
EXPOSE 8501

# Health check (using Python since curl is not in slim image)
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "scheduler/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
