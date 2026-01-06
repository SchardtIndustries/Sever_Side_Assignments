# Assignment 4 — Microservices with API Gateway

## Overview

This assignment demonstrates a simple microservice architecture built with Node.js and Express.  
It consists of two independent microservices (user-service and product-service) and a centralized API gateway that handles routing, API composition, authentication, rate limiting, and caching.

The goal is to show how an API gateway simplifies client interaction with multiple backend services while enforcing cross-cutting concerns such as security and performance.

---

## Project Structure

```bash
Assignment_4/
├── user-service/
├── product_service/
├── api_gateway/
├── Screenshots/
└── README.md
```

---

## Services and Ports

| Service | Description | Port |
| --- | ------------ | --- |
| user-service | Provides user data | 3000 |
| product-service | Provides product data | 3001 |
| api-gateway | Single entry point for clients | 3002 |

---

## Installation

Each service must be started separately.

### User Service

```bash
cd user-service
npm install
node index.js
```

### Product Service

```bash
cd product_service
npm install
node index.js
```

### API Gateway

```bash
cd api_gateway
npm install
node index.js
```

---

## API Gateway Endpoints

### Users (Basic Authentication Required)

```bash
GET /api/v1/users/:id
```

- Protected using HTTP Basic Authentication  
- Credentials:
  - Username: `admin`
  - Password: `password`

Example:

```bash
curl -u admin:password http://localhost:3002/api/v1/users/1
```

---

### Products (JWT Authentication Required)

```bash
GET /api/v1/products/:id
```

To obtain a token:

```bash
curl -X POST http://localhost:3002/auth   -H "Content-Type: application/json"   -d '{"username":"admin","password":"password"}'
```

Use the token:

```bash
curl http://localhost:3002/api/v1/products/1   -H "Authorization: Bearer <TOKEN>"
```

---

### API Composition

```bash
GET /api/v1/userProducts/:userId
```

This endpoint combines user data from `user-service` with product data from `product-service` and returns a single JSON response.

Example:

```bash
curl http://localhost:3002/api/v1/userProducts/1
```

---

## Advanced Features

### Rate Limiting

- Implemented at the API gateway
- Limits each client to 100 requests per 15 minutes

### Caching

- Product responses are cached for 60 seconds
- Repeated requests are served from cache to improve performance

---

## Screenshots

The `Screenshots/` folder contains evidence of:

- Direct microservice access
- Gateway routing
- API composition
- Basic Authentication
- JWT authentication
- Token usage
- Caching behavior

---

## Notes

- Mock data is used for simplicity
- All services run locally
- This setup demonstrates core microservice and gateway concepts without external dependencies
