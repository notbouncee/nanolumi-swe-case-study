# Water Quality Monitoring Dashboard

This is a full-stack web application designed for operators to monitor and request real-time water quality measurements from remote IoT sensors distributed across multiple sites.

It is built as part of the Nanolumi SWE Case Study, integrating a React frontend, a FastAPI backend, a PostgreSQL database, and a simulated IoT device network.

## Tech Stack

**Frontend:**

- **React (Vite):** Fast, modern UI development.
- **TypeScript:** Strict type-checking for reliability.
- **Tailwind CSS & shadcn/ui:** Styling and accessible UI components.
- **React-Leaflet:** Interactive map rendering for device locations.
- **Playwright:** End-to-End automated UI testing.

**Backend:**

- **Python & FastAPI:** High-performance, asynchronous backend framework.
- **Tortoise ORM:** Asynchronous Object Relational Mapper.
- **PostgreSQL:** Relational database for persistent storage.
- **Pytest:** Backend unit and E2E testing.

**Infrastructure:**

- **Docker & Docker Compose:** Containerization for consistent environments across all devices.
- **Make:** Orchestration of testing and development commands.

---

## Architecture & Data Flow

The system operates across four primary containers:

1. `frontend`: The React application accessible to the user.
2. `backend`: The FastAPI server that handles business logic and acts as the central hub.
3. `db`: The PostgreSQL database storing device metadata and measurement history.
4. `simulator`: A black-box IoT simulator that mimics real-world hardware delays, network issues, and data generation.

### The "Request Measurement" API Flow

Because communicating with field IoT devices is inherently slow and unreliable, the measurement workflow is completely **asynchronous**.

When an operator clicks "Request Measurement" for a specific device, the following flow occurs:

1. **User Action:** The operator clicks the button in the frontend modal.
2. **Initial Request:** The frontend sends a `POST /api/devices/{device_id}/measurements` request to the backend.
3. **Database Logging:** The backend immediately creates a `pending` measurement record in PostgreSQL and generates a unique `request_id`.
4. **Hardware Trigger:** The backend forwards the request to the Simulator (`POST /api/devices/{device_id}/measurements`), providing the `request_id` and a Webhook `callback_url`.
5. **Immediate Response:** The Simulator instantly returns a `202 Accepted` (or a `409 Busy` / `503 Unavailable`). The backend updates the database to `acknowledged` (or `delayed`) and responds to the frontend.
6. **Frontend Polling:** Recognizing the request is actively processing, the frontend begins polling the backend every 3 seconds for updates.
7. **Asynchronous Webhook:** After 5-15 seconds, the Simulator finishes processing and fires a webhook (`POST /api/webhooks/simulator`) back to the backend containing the actual water quality data (pH, temperature, turbidity, dissolved oxygen) or a failure state (e.g. `incomplete`).
8. **Data Persistence:** The backend updates the measurement record in PostgreSQL to `completed` and saves the sensor data.
9. **UI Update:** On its next polling cycle, the frontend retrieves the completed data, stops polling, and beautifully displays the fresh measurements to the operator!

---

## How to Run

Because this entire application is containerized with Docker, running it on any new machine (Mac, Windows, Linux) is incredibly simple. You do not need to install Node, Python, or PostgreSQL on your local machine.

### Prerequisites

1. **Docker Desktop** (or Docker Engine) installed and running.
2. **Git** installed to clone the repository.
3. **Make** installed (comes pre-installed on Mac/Linux; Windows users can use WSL or Git Bash).

### Setup Instructions

**1. Clone the repository and enter the directory:**

```bash
git clone https://github.com/notbouncee/nanolumi-swe-case-study.git
cd nanolumi-swe-case-study
```

**2. Start the application:**
Use Docker Compose to build and start all four containers in the background:

```bash
docker compose up -d --build
```

_(Note: The first run will take a minute or two as it downloads the images and builds the dependencies)._

**3. Access the Application:**

- **Frontend Web App:** [http://localhost:5173](http://localhost:5173)
- **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

**4. Run Automated Tests:**
You can run all unit and E2E tests (Frontend and Backend) seamlessly inside the containers using the master Makefile:

```bash
make test-all
```

**5. Stop the Application:**
When you are done, you can stop and remove the containers:

```bash
docker compose down
```
