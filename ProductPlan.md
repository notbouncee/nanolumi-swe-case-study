You are an expert senior full-stack software engineer. Your objective is to build a production-ready MVP for a water-quality monitoring dashboard that interfaces with a hardware simulator.

**Tech Stack:**

- Backend: Python (FastAPI)
- Frontend: React + Vite (TypeScript, Tailwind CSS, shadcn/ui)
- Database: PostgreSQL
- Infrastructure: Docker & Docker Compose

**Guidelines:**

- Write clean, maintainable, and well-documented code.
- Prioritise robust error handling and edge cases (especially regarding asynchronous webhooks).
- Do not skip steps. If a step fails, stop immediately, explain the error, and wait for my input to debug it together.

The following are the exact steps I want you to take to build this application:

1. Read through the Product Brief markdown file and understand the requirements.
2. Read through the Simulator Protocol markdown file and understand the API.
3. Read through the examples folder for examples of payload requests and responses.
4. Create the necessary files and directories using the file structure I shown below:

```
nanolumi-swe-case-study/
├── backend/            # FastAPI application
│   ├── src/
│   └── tests/
├── frontend/           # React + Vite application
│   ├── api/
│   ├── app/
│   ├── components/
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── ui/
│   ├── hooks/
│   ├── services/
│   └── utils/
├── scripts/            # utility scripts
├── database/           # PostgreSQL
└── simulator/          # Simulator
```

4. When coding out the application, include short comments in the codes to explain what each function does, what each function takes in and what each function returns.
5. For the backend, create a FastAPI application that can list devices from the simulator, send POST measurement commands, and receive callback results on a webhook endpoint. Ensure CORS is explicitly configured. Handle the different potential simulator response scenarios (accepted, delayed, rejected). Generate a unique `request_id` for each new operator request, but implement an idempotency safeguard: if a duplicate request for the same device arrives within a 5-second window, gracefully handle it (e.g. return a 429 status or re-use the in-flight request) rather than spamming the simulator.
6. For the database, create the necessary files for a PostgreSQL database including the .env.example.
7. Instead of hardcoding seed data, have the backend automatically sync with the simulator by calling its GET /api/devices endpoint on startup and populating the database. Create the necessary schema for a `devices` table, a `device_measurements` table, and potentially a mock session for the operator (a full `user` authentication table can be skipped initially to save time).
8. Before moving on to the frontend, make sure that request/callback loop works end to end by testing it using pytest or other means neccessary. If it does not work, stop here, show me the error or prompt and we will debug it together.
9. For the frontend, create a React + Vite application that displays the devices on an interactive map. The operator should be able to click on a device to open a device modal. This modal should display the device details, the most recent measurements from the measurements table, and have a button to request new measurements. Disable the "Request Measurement" button immediately upon click and show a loading state to prevent accidental double-clicks. Implement an approach to show if a measurement request has been acknowledged, failed, completed, rejected, delayed, or remain incomplete. Use Tailwind CSS for styling and implement your own custom components, implement shadcn components into the respective folders in the frontend components folder, make sure that the components follow the requested file structure.
10. Use Docker to containerise the application and database.
11. Use Docker Compose to orchestrate the containers so my root docker-compose.yml file should have all the configurations of the frontend, backend, database and simulator. It should also allow for easy spinning up and down of the application.
12. Create a few automated tests to verify the application works. Split the complex webhook testing into reliable, isolated tests: one test that verifies the backend correctly sends a POST request to the simulator when a measurement is requested, and another test that mocks a POST callback request to the webhook endpoint to verify the database updates correctly.
13. Create a simple README.md to explain how to run the application.
14. Document any assumptions or limitations in the README.md or in comments in the code.
