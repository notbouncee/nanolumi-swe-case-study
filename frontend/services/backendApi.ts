import { apiClient } from "@/api/http";

export interface Device {
  id: number;
  device_id: string;
  name: string;
  site_id: string;
  site_name: string;
}

export interface Measurement {
  id: number;
  request_id: string;
  status: string;
  requested_at: string;
  completed_at: string | null;
  ph: number | null;
  temperature_c: number | null;
  turbidity_ntu: number | null;
  dissolved_oxygen_mg_l: number | null;
}

export const getDevices = async (): Promise<Device[]> => {
  const response = await apiClient.get("/api/devices");
  return response.data;
};

export const getDeviceMeasurements = async (deviceId: string): Promise<Measurement[]> => {
  const response = await apiClient.get(`/api/devices/${deviceId}/measurements`);
  return response.data;
};

export const requestMeasurement = async (deviceId: string, parameters: string[]): Promise<{ status: string, request_id: string }> => {
  const response = await apiClient.post(`/api/devices/${deviceId}/measurements`, { parameters });
  return response.data;
};
