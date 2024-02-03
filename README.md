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