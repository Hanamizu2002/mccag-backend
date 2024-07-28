# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml pdm.lock README.md ./

# Install PDM
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip install pdm

RUN pdm config pypi.url https://mirrors.aliyun.com/pypi/simple/

# Install any dependencies
RUN pdm install
RUN pdm sync --clean

# Copy the rest of the application code to the container
COPY src ./src

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app/src

# Expose the port that the FastAPI app runs on
EXPOSE 8023

# Command to run the FastAPI application
CMD ["pdm", "dev"]