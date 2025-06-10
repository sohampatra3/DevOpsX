FROM python:3.7-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY Exp.py .
COPY weather.py .

# Install only required packages (optional: if requirements.txt exists)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "Exp.py"]