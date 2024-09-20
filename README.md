           # Waltzing Matilda Trading System API

A scalable, high-performance trading system API built with Django, Django Ninja, Celery, and PostgreSQL. This application allows authenticated users to place buy and sell orders for stocks and track their investments. It includes asynchronous views for optimal performance, background tasks for bulk trade processing, and is containerized for deployment using Docker and Kubernetes. Observability is enhanced with logging, monitoring, and tracing using Prometheus, Grafana, and OpenTelemetry.

---

## Installation

### Prerequisites

- **Python**: Version 3.12 or higher.
- **Docker**: For containerization.
- **Docker Compose**: To orchestrate Docker containers.
- **Kubernetes**: (Optional) For deploying to a Kubernetes cluster.
- **Redis**: For Celery message brokering.
- **PostgreSQL**: As the database backend.

### Local Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/trading-system.git
   cd trading-system
   ```
2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the Database**

   Update `waltzing_matilda_trading/settings.py` with your database credentials:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'trading_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
5. **Run Migrations**

   ```bash
   python manage.py migrate
   ```
6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```
7. **Start Redis Server**

   Ensure Redis is running locally:

   ```bash
   redis-server
   ```
8. **Start Celery Worker and Beat**

   Open two separate terminals and run:

   ```bash
   celery -A waltzing_matilda_trading worker --loglevel=info
   celery -A waltzing_matilda_trading beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```
9. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

---

## Usage

### API Endpoints

#### 1. Place an Order

- **URL**: `/api/orders/order`
- **Method**: `POST`
- **Authentication**: Required (Basic Auth)
- **Payload**:

  ```json
  {
    "stock_id": 1,
    "quantity": 10,
    "order_type": "buy"  // or "sell"
  }
  ```
- **Response**:

  ```json
  {
    "success": true,
    "order_id": 123
  }
  ```

#### 2. Retrieve Total Investment

- **URL**: `/api/orders/total/{stock_id}`
- **Method**: `GET`
- **Authentication**: Required (Basic Auth)
- **Response**:

  ```json
  {
    "total_investment": 1500.00
  }
  ```

### Authentication

Use Basic Authentication with your username and password.

### Examples

#### Placing an Order with `curl`

```bash
curl -X POST http://localhost:8000/api/orders/order \
     -u username:password \
     -H 'Content-Type: application/json' \
     -d '{"stock_id":1,"quantity":10,"order_type":"buy"}'
```

#### Retrieving Total Investment with `curl`

```bash
curl -X GET http://localhost:8000/api/orders/total/1 \
     -u username:password
```

---

## Testing

### Running Tests

1. **Install Test Dependencies**

   ```bash
   pip install pytest pytest-django pytest-asyncio pytest-celery
   ```
2. **Run Tests**

   ```bash
   pytest
   ```

   This will run all tests located in the `api/tests/` directory.

---

## Docker and Docker Compose

### Building Docker Images

1. **Build the Web App Image**

   ```bash
   docker build -t trading-web:latest -f Dockerfile .
   ```
2. **Build the Celery Worker Image**

   ```bash
   docker build -t trading-worker:latest -f Dockerfile-celery .
   ```

### Running with Docker Compose

1. **Start Services**

   ```bash
   docker-compose up -d
   ```
2. **Run Migrations**

   ```bash
   docker-compose exec web python manage.py migrate
   ```
3. **Create a Superuser**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
4. **Access the Application**

   The API will be accessible at `http://localhost:8000/api/`.

### Docker Compose Services

- **web**: Django application server.
- **worker**: Celery worker for background tasks.
- **beat**: Celery Beat scheduler.
- **redis**: Redis server for message brokering.
- **db**: PostgreSQL database.

---

## Kubernetes Deployment

### Deploying to Kubernetes

1. **Build and Push Docker Images**

   Replace `your_dockerhub_username` with your actual Docker Hub username.

   ```bash
   docker build -t your_dockerhub_username/trading-web:latest -f Dockerfile .
   docker push your_dockerhub_username/trading-web:latest

   docker build -t your_dockerhub_username/trading-worker:latest -f Dockerfile-celery .
   docker push your_dockerhub_username/trading-worker:latest
   ```
2. **Apply Kubernetes Manifests**

   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml
   kubectl apply -f k8s/postgres.yaml
   kubectl apply -f k8s/redis.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
3. **Access the Application**

   Use `kubectl get svc trading-service` to find the external IP and access the API.

### Kubernetes Components

- **Deployments**: For web app, Celery worker, Redis, and PostgreSQL.
- **Services**: Expose deployments internally and externally.
- **ConfigMaps and Secrets**: Manage configuration and sensitive data.