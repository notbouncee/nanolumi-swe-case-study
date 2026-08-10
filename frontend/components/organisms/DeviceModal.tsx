import { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { type Device, type Measurement, getDeviceMeasurements, requestMeasurement } from "@/services/backendApi";
import { Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface DeviceModalProps {
  device: Device | null;
  onClose: () => void;
}

export function DeviceModal({ device, onClose }: DeviceModalProps) {
  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [loading, setLoading] = useState(false);
  const [requesting, setRequesting] = useState(false);

  const fetchMeasurements = async () => {
    if (!device) return;
    try {
      const data = await getDeviceMeasurements(device.device_id);
      // Sort by requested_at descending
      data.sort((a, b) => new Date(b.requested_at).getTime() - new Date(a.requested_at).getTime());
      setMeasurements(data);
    } catch (e) {
      console.error("Failed to fetch measurements", e);
    }
  };

  useEffect(() => {
    if (device) {
      setLoading(true);
      fetchMeasurements().finally(() => setLoading(false));
    }
  }, [device]);

  // Polling logic when a measurement is active (pending, acknowledged, delayed)
  useEffect(() => {
    if (!device) return;
    const hasActiveMeasurement = measurements.some(
      (m) => m.status === "pending" || m.status === "acknowledged" || m.status === "delayed"
    );

    if (hasActiveMeasurement) {
      const interval = setInterval(() => {
        fetchMeasurements();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [device, measurements]);

  const handleRequestMeasurement = async () => {
    if (!device) return;
    setRequesting(true);
    try {
      await requestMeasurement(device.device_id, ["ph", "temperature_c", "turbidity_ntu", "dissolved_oxygen_mg_l"]);
      await fetchMeasurements();
    } catch (e: any) {
      console.error(e);
      alert(e.response?.data?.detail || "Failed to request measurement");
    } finally {
      setRequesting(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "bg-green-500 hover:bg-green-600 text-white";
      case "failed": return "bg-red-500 hover:bg-red-600 text-white";
      case "rejected": return "bg-red-500 hover:bg-red-600 text-white";
      case "delayed": return "bg-yellow-500 hover:bg-yellow-600 text-white";
      case "acknowledged": return "bg-blue-500 hover:bg-blue-600 text-white";
      case "incomplete": return "bg-gray-400 hover:bg-gray-500 text-white";
      default: return "bg-gray-500 hover:bg-gray-600 text-white";
    }
  };

  const latest = measurements[0];
  const hasActiveRequest = requesting || (latest && ["pending", "acknowledged", "delayed"].includes(latest.status));

  return (
    <Dialog open={!!device} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{device?.name}</DialogTitle>
          <DialogDescription>
            {device?.site_name} (ID: {device?.device_id})
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <h4 className="text-sm font-medium mb-3">Latest Measurement</h4>
          {loading && measurements.length === 0 ? (
            <div className="flex justify-center py-4">
              <Loader2 className="h-6 w-6 animate-spin text-gray-500" />
            </div>
          ) : latest ? (
            <Card>
              <CardContent className="pt-6 space-y-3">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm text-gray-500">Status:</span>
                  <Badge className={getStatusColor(latest.status)}>{latest.status.toUpperCase()}</Badge>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-500">pH</p>
                    <p className="font-medium">{latest.ph ?? "--"}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Temp</p>
                    <p className="font-medium">{latest.temperature_c !== null ? `${latest.temperature_c}°C` : "--"}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Turbidity</p>
                    <p className="font-medium">{latest.turbidity_ntu !== null ? `${latest.turbidity_ntu} NTU` : "--"}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Dissolved O2</p>
                    <p className="font-medium">{latest.dissolved_oxygen_mg_l !== null ? `${latest.dissolved_oxygen_mg_l} mg/L` : "--"}</p>
                  </div>
                </div>

                <div className="text-xs text-gray-400 mt-4 pt-4 border-t">
                  Requested: {new Date(latest.requested_at).toLocaleString()}
                </div>
              </CardContent>
            </Card>
          ) : (
            <p className="text-sm text-gray-500 text-center py-4">No measurements found for this device.</p>
          )}
        </div>

        <div className="flex justify-end">
          <Button 
            onClick={handleRequestMeasurement} 
            disabled={hasActiveRequest}
          >
            {hasActiveRequest && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            {hasActiveRequest ? "Measurement in Progress..." : "Request Measurement"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
