### API Documentation for Event Management

#### 1. Create Event

- **Endpoint**: `/create`
- **Method**: `POST`
- **Description**: Creates a new events its possible to create more than one.
- **Input**: JSON payload with event details.
- **Output**: JSON object with created events details; 200 status code on success.
- **Error Handling**: Logs error; returns empty JSON object with 500 status code on failure.
- **Curl Example**:
  ```bash

    curl -X POST http://localhost:8000/create \
         -H "Content-Type: application/json" \
         -d '{
               "events": [
                   {
                       "title": "Example Event",
                       "description": "This is a sample event description.",
                       "start_time": "2023-12-01T10:00:00",
                       "end_time": "2023-12-01T12:00:00",
                       "location": "123 Example Street"
                   }
               ]
             }'

  ```

#### 2. Get Event by ID

- **Endpoint**: `/get`
- **Method**: `GET`
- **Description**: Retrieves specific event by ID.
- **Input**: `id` parameter in query string.
- **Output**: JSON object with event details; 200 status code on success.
- **Error Handling**: Logs error; returns empty JSON object with 500 status code on failure.
- **Curl Example**:
  ```bash
  curl -G "http://localhost:8000/events/get" -d 'id=1'
  ```

#### 3. Get All Events

- **Endpoint**: `/get_all`
- **Method**: `GET`
- **Description**: Retrieves all events.
- **Input**: Additional query parameters for filtering/sorting (optional).
- **Output**: JSON array of event objects; 200 status code on success.
- **Error Handling**: Logs error; returns empty JSON object with 500 status code on failure.
- **Curl Example**:
  ```bash
  curl -G "http://localhost:8000/events/get_all"
  curl -G "http://localhost:8000/events/get_all" --data-urlencode "wherekey=location" --data-urlencode "whereValue=Tel Aviv" --data-urlencode "orderBy=start_time"
  ```

#### 4. Delete Event

- **Endpoint**: `/delete`
- **Method**: `POST`
- **Description**: Deletes an event by ID.
- **Input**: JSON object with event's ID.
- **Output**: JSON object with success/failure message; 200 status code on success.
- **Error Handling**: Logs error; returns empty JSON object with 500 status code on failure.
- **Curl Example**:
  ```bash
  curl -X POST "http://localhost:8000/events/delete" \
       -H "Content-Type: application/json" \
       -d '{"id": "123"}'
  ```

#### 5. Update Event

- **Endpoint**: `/update`
- **Method**: `PUT`
- **Description**: Updates an existing event.
- **Input**: JSON payload with event ID and new values.
- **Output**: JSON object with success/failure message; 200 status code on success.
- **Error Handling**: Logs error; returns empty JSON object with 500 status code on failure.
- **Curl Example**:
  ```bash
  curl -X PUT "http://localhost:8000/events/update" -H "Content-Type: application/json" -d  '{"id":1,"values":{"title":"new_name"}}'   
  ```

### General Notes
- All endpoints should handle exceptions gracefully, logging the errors and returning a 500 status code in case of failures.
- The `/create`, `/delete`, and `/update` endpoints also emit socket events to notify about changes in real-time.
- Modify JSON payloads in `curl` examples as per your event data structure.


### Architecture Overview

#### Components:
1. **Flask (Backend Framework)**:
    - Manages HTTP requests and responses.
    - Interacts with PostgreSQL for data storage and retrieval.
    - Emits events to Redis for real-time notifications.

2. **PostgreSQL (Database)**:
    - Stores data related to events and other relevant information.
    - Accessed by Flask for CRUD (Create, Read, Update, Delete) operations.

3. **Redis (Message Broker)**:
    - Used as a broker for managing real-time socket communications.
    - Flask publishes messages to Redis, which are then relayed to clients.

4. **Nginx (Load Balancer and Reverse Proxy)**:
    - Balances load and manages connections for WebSocket servers.
    - Routes incoming HTTP and WebSocket requests to appropriate Flask instances.

5. **Background Process**:
    - Runs independently, checking every minute for events starting in the next 30 minutes.
    - If such events are found, it sends reminders through Flask to clients via Redis and WebSocket.

#### Flow of Operations:
1. **Client-Server Interaction**:
    - Clients send HTTP requests to Flask through Nginx.
    - Flask interacts with PostgreSQL to fetch or modify data.
    - For real-time features, Flask communicates with clients using WebSockets via Redis.

2. **Real-Time Notifications**:
    - Flask publishes notification messages to Redis when certain actions occur (like event creation or updates).
    - Redis relays these messages to connected clients, enabling real-time updates.

3. **Background Reminder Process**:
    - Periodically checks for upcoming events in PostgreSQL.
    - On identifying events starting within the next 30 minutes, it triggers a notification process.
    - Notifications are sent to Flask, which then publishes them to Redis.
    - Redis distributes these reminders to connected clients.

4. **Load Balancing and Connection Management**:
    - Nginx acts as a reverse proxy and load balancer.
    - It efficiently distributes incoming network traffic and WebSocket connections across multiple Flask instances.
    - This setup enhances the reliability and availability of the application.

#### Build:

1. **Build and Run the Docker Containers**:
   - Run `docker-compose up --build` in your terminal. This command builds the images and starts the containers as defined in your `docker-compose.yml`.

2. **Accessing the Application**:
   - Once the containers are up and running, open a web browser.
   - Navigate to `http://localhost:8000`. This should connect you to the Nginx server, which will route your request to the appropriate Flask instance.

3. **Viewing WebSocket Messages**:
   - In the browser, open the Developer Tools (usually F12 or right-click and select "Inspect").
   - check the console log in devloper tools

4. **Troubleshooting**:
   - If you don't see the expected output, check the logs of your Docker containers. Use `docker logs [container_name]` to view logs.

