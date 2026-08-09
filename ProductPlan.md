1. Read through the Product Brief markdown file and understand the requirements.
2. Read through the Simulator Protocol markdown file and understand the API.
3. Create the necessary files and directories using the file structure I shown below:

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
5. For the backend, create a FastAPI application that can list devices from the simulator, send POST measurement commands to the simulator, and receive callback results from the simulator on a webhook endpoint. Ensure CORS is explicitly configured so the frontend can communicate with the backend. Make sure to take into account the different potential scenarios when calling the simulator for measurements as seen in the Simulator Protocol.
6. For the frontend, create a React + Vite application that displays the devices on an interactive map. The operator should be able to click on a device to open a device modal. This modal should display the device details, the most recent measurements from the measurements table, and have a button to request new measurements. Implement an approach to show if a measurement request has been acknowledged, failed, completed, rejected, delayed, or remain incomplete. Use Tailwind CSS for styling and implement your own custom components, implement shadcn components into the respective folders in the frontend components folder, make sure that the components follow the requested file structure.
7. For the database, create the necessary files for a PostgreSQL database including the .env.example.
8. Instead of hardcoding seed data, have the backend automatically sync with the simulator by calling its GET /api/devices endpoint on startup and populating the database. Create the necessary schema for a `devices` table, a `device_measurements` table, and potentially a mock session for the operator (a full `user` authentication table can be skipped initially to save time).
9. Use Docker to containerise the application and database.
10. Use Docker Compose to orchestrate the containers so my root docker-compose.yml file should have all the configurations of the frontend, backend, database and simulator. It should also allow for easy spinning up and down of the application.
11. Create a few automated tests to verify the application works. Split the complex webhook testing into reliable, isolated tests: one test that verifies the backend correctly sends a POST request to the simulator when a measurement is requested, and another test that mocks a POST callback request to the webhook endpoint to verify the database updates correctly.
12. Create a simple README.md to explain how to run the application.
13. Document any assumptions or limitations in the README.md or in comments in the code.
