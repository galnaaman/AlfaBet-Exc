
#  AlfaBet Interview 
##### ![enter image description here](https://media.licdn.com/dms/image/D560BAQHEMjwl7ANX9w/company-logo_200_200/0/1683556333225/alpha_bets_logo?e=1715212800&v=beta&t=5jSSjs0rSV5Gp0YtasRd0zSw1B8L4lclY7t2HlCj4zI)

### Events Management API
The Events Management API is a backend solution designed for creating, managing, and broadcasting events in real-time. Built with Django and the Django REST framework, Django Channels are integrated to provide real-time functionality, enabling live updates and interactions between the server and clients through WebSockets.

# Architecture Overview and Tech Stack

- [architecture](https://drive.google.com/file/d/10kVHrsqvC6T65Sf1kl5xaVAtPtV7vc_V/view?usp=sharing)
The application is built on a modular architecture, with each component having a specific role and responsibility. Here's an overview of the architecture and the tech stack used:

## Events API

**Tech Stack:** Django and Django REST framework

**Role:** The Events API is the core interface for event CRUD operations. It handles client requests and responses.

## Database

**Tech Stack:** PostgreSQL

**Role:** The database provides reliable data persistence and complex querying capabilities for the application.

## Notifications Worker

**Tech Stack:** Django with Apscheduler

**GitHub Repo** [Notifications Worker](https://github.com/galnaaman/Alfabet_worker)

**Role:** The Notifications Worker periodically checks for imminent events and queues notifications for delivery.

## RabbitMQ

**Tech Stack:** RabbitMQ 

**GitHub Consumer Repo** [consumer](https://github.com/galnaaman/alfabet-consumer)

**Role:** RabbitMQ decouples long-running tasks from the main API, facilitating task distribution and asynchronous processing.

## Notification API

**Tech Stack:** Django REST framework

**Role:** The Notification API acts as a consumer of RabbitMQ messages and triggers notifications through external email and SMS service providers. **Didnt Actual devlop him just for the concept

## Redis

**Tech Stack:** Redis

**Role:** Redis manages WebSocket connections for real-time communication and caches frequent queries to enhance performance.

## WebSockets

**Tech Stack:** Django Channels

**Role:** WebSockets enable real-time notifications and live data updates to connected clients.

## JWT Authentication

**Tech Stack:** JSON Web Tokens (JWT)

**Role:** JWT Authentication protects endpoints and ensures that only authenticated users can subscribe to events and receive updates.

This architecture was chosen to leverage Django's strengths—a powerful ORM for database interactions, middleware support for seamless extension of HTTP request/response handling, and a well-supported ecosystem for building RESTful APIs. Django Channels add asynchronous support, crucial for implementing WebSocket communication, while Redis and RabbitMQ address performance and reliability concerns for real-time messaging and task queuing, respectively.
## System Flow


**Events API:** Clients interact with the Events API to create, update, or retrieve events. The API processes these requests and interacts with the PostgreSQL database for persistent storage.

**Real-Time Updates:**  On event updates, Django Channels handles real-time notifications. Each event has a dedicated WebSocket channel for broadcasting updates to subscribed clients.

**Notification Worker:** Scheduled tasks check for imminent events and enqueue notification messages in RabbitMQ, which manages these tasks without impacting the main API's performance.

**Message Queue Consumption:**  A separate consumer service processes the queued messages from RabbitMQ and communicates with the Notifications API.

**Notifications Dispatch:** The Notifications API triggers actions with external providers to send out emails or SMS messages to event participants, alerting them of upcoming events or changes.

**Caching and Session Management:** Redis caches frequent queries and stores session data to minimize database access and manage WebSocket connections efficiently.

**Security:** JWT authentication safeguards API endpoints, ensuring that only authorized users can trigger changes and receive notifications.



# API Documentation

## Events API

### `GET /api/v1/events/`

This endpoint retrieves a list of events. The response is paginated and each page contains 25 events.

#### Query Parameters

- `location`: Filter events by location. The value should be a string.
- `venue`: Filter events by venue. The value should be a string.
- `sort_by`: Sort events by date, popularity, or creation time. The value should be one of the following: `date`, `-date`, `popularity`, `-popularity`, `created`, `-created`.
- `page`: The page number to retrieve. The value should be an integer.

#### Response

A list of events. Each event object contains the following fields:

- `id`: The event ID.
- `name`: The event name.
- `description`: The event description.
- `location`: The event location.
- `venue`: The event venue.
- `start_time`: The event start time.
- `end_time`: The event end time.
- `participants`: A list of participant IDs.

### `POST /api/v1/events/`

This endpoint creates a new event.

#### Request Body

An event object containing the following fields:

- `name`: The event name.
- `description`: The event description.
- `location`: The event location.
- `venue`: The event venue.
- `start_time`: The event start time.
- `end_time`: The event end time.
- `participants`: A list of participant IDs.

#### Response

The created event object.

### `POST /api/v1/events/batch/`

This endpoint creates multiple new events.

#### Request Body

A list of event objects. Each event object should contain the same fields as described in the `POST /api/v1/events/` endpoint.

#### Response

A message indicating that the events were created successfully.

### `PUT /api/v1/events/batch/`

This endpoint updates multiple events.

#### Request Body

A list of event objects. Each event object should contain the same fields as described in the `POST /api/v1/events/` endpoint, plus an `id` field indicating the event to update.

#### Response

A message indicating that the events were updated successfully.

### `DELETE /api/v1/events/batch/`

This endpoint deletes multiple events.

#### Request Body

A list of event IDs to delete.

#### Response

A message indicating that the events were deleted successfully.

### `GET /api/v1/events/{event_id}`

This endpoint retrieves the details of a specific event.

#### Path Parameters

- `event_id`: The ID of the event to retrieve.

#### Response

The event object.

### `PUT /api/v1/events/{event_id}`

This endpoint updates a specific event.

#### Path Parameters

- `event_id`: The ID of the event to update.

#### Request Body

An event object containing the fields to update.

#### Response

The updated event object.

### `DELETE /api/v1/events/{event_id}`

This endpoint deletes a specific event.

#### Path Parameters

- `event_id`: The ID of the event to delete.

#### Response

A status code of 204 indicating that the event was deleted successfully.

### `POST /api/v1/events/{event_id}/subscribe/`

This endpoint subscribes a user to a specific event.

#### Path Parameters

- `event_id`: The ID of the event to subscribe to.

#### Request Body

An object containing the following field:

- `user_id`: The ID of the user to subscribe.

#### Response

A message indicating that the subscription was successful.


### `ws/events/{event_id}/`

This WebSocket endpoint is used to establish a real-time connection for a specific event.

#### Path Parameters

- `event_id`: The ID of the event to establish a WebSocket connection for.

#### Connection

To establish a WebSocket connection, the client should send a WebSocket connection request to `ws://<your-domain>/ws/events/{event_id}/`.

#### Messages

Once the connection is established, the server can send event-related messages to the client. The messages are JSON objects with the following field:

- `message`: A string containing the event-related message.

Here is an example of a valid message:

```json
{
    "message": "New participant joined the event."
}
```

#### Disconnection

The client can close the WebSocket connection at any time by sending a WebSocket close frame. The server will also close the connection if it no longer needs to send messages to the client.


### `POST /api/v1/token/`

This endpoint is used to obtain a JWT token pair (access and refresh tokens) for a user.

#### Request

The request should be a POST request to the `/api/v1/token/` endpoint. The body of the request should be a JSON object with the following fields:

- `username`: The username of the user. This should be a string.
- `password`: The password of the user. This should be a string.

Here is an example of a valid request body:

```json
{
    "username": "sampleuser",
    "password": "samplepassword"
}
```

#### Response

If the credentials are valid, the server will respond with a status code of 200 and a JSON object containing the `access` and `refresh` tokens.

Here is an example of a valid response body:

```json
{
    "access": "<access-token>",
    "refresh": "<refresh-token>"
}
```

If the credentials are invalid, the server will respond with a status code of 401 and a JSON object containing an error message.

### `POST /api/v1/token/refresh/`

This endpoint is used to obtain a new access token using a refresh token.

#### Request

The request should be a POST request to the `/api/v1/token/refresh/` endpoint. The body of the request should be a JSON object with the following field:

- `refresh`: The refresh token. This should be a string.

Here is an example of a valid request body:

```json
{
    "refresh": "<refresh-token>"
}
```

#### Response

If the refresh token is valid, the server will respond with a status code of 200 and a JSON object containing the new `access` token.

Here is an example of a valid response body:

```json
{
    "access": "<new-access-token>"
}
```

If the refresh token is invalid, the server will respond with a status code of 401 and a JSON object containing an error message.
