# Step 1: Start with a Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements first (Docker caches this layer)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the code
COPY src/ src/

# Step 6: Expose the port the app runs on
EXPOSE 5000

# Step 7: Command to run the app
CMD ["python", "src/app.py"]