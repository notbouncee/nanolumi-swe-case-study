# Thought process throughout

1. Read through the Product Brief and understood that a simple webapp with a backend and frontend will be built to monitor water quality.
2. Read through the Simulator Protocol and understood the API that the simulator exposes.
3. Started the simulator and confirmed that I could call `GET /health` and `GET /api/devices`.
4. Decided to use Python(FastAPI) for the backend, React + vite for the frontend and PostgreSQL for the database.
5. Since it needs to be runnable across different devices, I decided to use Docker and Docker Compose for containerising the application and database. This ensures that it runs the same way on other devices.
6. My File structure will rougly look like this based on my previous experience:

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

7. Now I need to create an Agent Plan document detailing what my AI Agent should do to help me build this product.
8. I asked the AI Agent to follow the product plan to create the fullstack web application in 2 phases: Phase 1 - Backend and Phase 2 - Frontend
9. In Phase 1, the agent created the backend service, including docker, tortoiseORM, FastAPI application. However there were some issues with the backend implementation:
   a. I missed out on a ORM to use initially and decided to use tortoiseORM as I have used it before.
   b. Mock http request was used in order to test the backend quickly without the full application. However, a seperate test was created for E2E test.
10. In Phase 2, the agent created the frontend with the use of shadcn components, tailwindcss and react + vite. It created a map view of the devices and also a modal to view the measurements of each device. There was some issues with api flow between the frontend, backend and simulator. This was resolved by checking the payload being sent from the frontend and the expected payload that the backend was expecting for the measurement api.
11. I found out that the backend's validation schema for measurementRequest had an additional field of `device_id` which was missing from the frontend's payload. I then removed it from the schema as the URL already had the `device_id`.
12. I have tested the frontend operator user experience manually, now i will create a automated test using playwright for the operator user experience from frontend to backend to simulator and confirm it works as expected.
13. I experienced a edge case where the simulator returns `busy` and my frontend considered it to be an `actively processing` state instead of a `terminal` state and got stuck in a never-ending `delayed` response. I fixed it by removing the `delayed` status in DeviceModal so the request measurement button is immediately available again for the operator to try again.

# Future Improvements for optimisation and scaling

1. User Management and Authentication system using JWT and refresh token rotation (with local accounts or internal SSO like Active Directory) with a dedicated admin role for the user management system, that can add, remove and update the roles of different operators.

2. Kafka can be used when scaling the backend to handle large numbers of devices, different companies, different countries, etc.

3. With Kafka, we can implement a constant call to the simulator to get the latest data from all devices at intervals (e.g. every 5 seconds) and persist the data into the database and a time-series database like InfluxDB. This ensures that the data is always up-to-date and can be queried quickly.

4. With Kafka, we can also implement an alert microservice that sends notifications to the operator for when a parameter is outside of expected operating ranges. We can also make a consumer microservice, in case the database is down, no data is lost as it will be in queue in Kafka. This can also be used for generating reports for different time periods.

5. A page for historical data display can be built to show the trend of each parameter over time, using the data in the time-series database like InfluxDB. This allows operators to see the historical performance of each device and identify any issues that may be affecting its operation. We can give them the option to export the data to a CSV file for further analysis.
