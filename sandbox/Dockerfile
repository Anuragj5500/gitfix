# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install pytest for running tests
RUN pip install pytest

# Keep the container alive so we can send commands to it
CMD ["tail", "-f", "/dev/null"]