import axios from "axios";

// In a real app this would be an environment variable
// Since we are running in docker-compose or locally, we point to localhost for MVP
export const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});
