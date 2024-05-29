FROM python:3.11


# Expose the application port
EXPOSE 8080

# Set the working directory in the container
WORKDIR /app


# Copy the entire current directory (which should be your Streamlit folder) into /app
COPY . .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
ENTRYPOINT ["streamlit", "run", "sales_training.py", "--server.port=8080", "--server.address=0.0.0.0"]

