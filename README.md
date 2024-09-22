# Waltzing Matilda Trading System API

![Waltzing Matilda Trading Poster](static/walzing_matilda_trading.png)

---

A scalable, high-performance trading system API built with Django, Django Ninja, Celery, and PostgreSQL. This application allows authenticated users to place buy and sell orders for stocks and track their investments. It includes asynchronous views for optimal performance, background tasks for bulk trade processing, and is containerized for deployment using Docker and Kubernetes.

## Requirements

- Python 3.8+
- Poetry
- Redis
- PostgreSQL

## Install and Usage

### Clone the repository:

```bash
git clone https://github.com/berecik/waltzing_matilda_trading.git
cd waltzing_matilda_trading
```

### Create a virtual environment and install the dependencies:

```bash
poetry install
```

### Activate the virtual environment:

```bash
poetry shell
```

### Create a `.env` file in the root directory and add the following environment variables:

```bash
cp .env.example .env
```

### Edit the `.env` file, add the required values and load the environment variables:

```bash
vim .env
source .env
```

### Run the database migrations:

```bash
python manage.py migrate
```

### Create a superuser:

```bash
python manage.py createsuperuser --noinput
```

### Run the development server:

```bash
python manage.py runserver
```

## API Endpoints

#### 1. Place an Order

- **URL**: `/orders/place_order`
- **Method**: `POST`
- **Authentication**: Required (Basic Auth)
- **Payload**:

  ```json
  {
    "stock_id": 1,
    "quantity": 10,
    "order_type": "buy"
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

- **URL**: `/orders/total_investment/{stock_id}`
- **Method**: `GET`
- **Authentication**: Required (Basic Auth)
- **Response**:

  ```json
  {
    "total_investment": 1500.00
  }
  ```
  
#### 4. Generate JWT Token

- **URL**: `token/pair`
- **Method**: `POST`
- **Payload**
  {
    "username": "admin",
    "password": "admin"
  }
- **Response**:

  ```json
  {
    "username": "admin",
    "refresh": "eyJ.....",
    "access": "eyJ0eXA....."
  }
  ```

#### 5. Refresh

- **URL**: `/token/refresh`
- **Method**: `POST`
- **Payload**
    {
        "refresh": "eyJ....."
    }
- **Response**:

  ```json
  {
    "access": "eyJ0eXA....."
  }
  ```

#### 6. Verify

- **URL**: `/token/verify`
- **Method**: `POST`
- **Payload**

  ```json
  {
    "token": "eyJ0eXA....."
  }
  ```
  
- **Response**:

  ```json
  {}
  ```

#### 7. Documentation

- **URL**: `/docs`