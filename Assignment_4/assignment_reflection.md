# Assignment 4 — Reflection

## Challenges Faced
One of the main challenges was ensuring that all microservices and the API gateway were running within the same environment and communicating correctly across ports. Another challenge involved handling authentication mechanisms consistently at the gateway level while keeping the underlying services simple.

## How the API Gateway Simplified Access
The API gateway provided a single entry point for clients, eliminating the need to call multiple services directly. Clients interact with one endpoint, while the gateway handles routing and communication with the appropriate microservices behind the scenes.

## Benefits of API Composition
API composition reduces client-side complexity by combining data from multiple services into a single response. This reduces the number of requests required by the client and improves overall efficiency and usability.

## Importance of Authentication
Authentication ensures that only authorized users can access protected resources. Implementing authentication at the gateway level centralizes security and prevents unauthorized access before requests reach backend services.

## Improvements for Production Use
For a production environment, this setup could be improved by adding centralized logging, better error handling, environment-based configuration, secure secret storage, HTTPS, and persistent databases instead of mock data.

## Testing Approach
Each component was tested individually using curl, followed by integration testing through the API gateway. In a larger system, automated unit tests, integration tests, and load testing would be appropriate.

## Rate Limiting and Caching
Rate limiting protects services from abuse and excessive traffic, while caching improves performance by reducing redundant calls to backend services.

## Connection to Lecture Concepts
This hands-on project directly applied lecture concepts related to microservices, API gateways, authentication strategies, and system scalability, reinforcing theoretical knowledge through practical implementation.
