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
9. In Phase 1, the agent created the fullstack web application with the backend. However there were some issues with the backend implementation:
    a. I missed out on a ORM to use initially and decided to use tortoiseORM as I have used it before. 
    b. Mock http request was used in order to test the backend quickly without the full application. However, a seperate test was created for E2E test. 
    
    
