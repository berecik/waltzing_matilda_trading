FROM python:3.12

ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-poetry \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml /app/
COPY docker.env /app/.env
COPY README.md /app/
COPY Makefile /app/
ENV PYTHONIOENCODING utf8
RUN make docker-install

# Copy project
COPY . /app/

# Copy .env file for sure it was not overriden by the project
COPY docker.env /app/.env

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
