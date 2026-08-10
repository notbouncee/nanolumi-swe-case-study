import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { type Device, getDevices } from "@/services/backendApi";

// Fix for default marker icon in react-leaflet
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

// Mock coordinates for different sites
const MOCK_COORDINATES: Record<string, [number, number]> = {
  "reservoir-north": [1.4426, 103.7954], // Woodlands, SG
  "treatment-outlet": [1.2722, 103.8416], // Tanjong Pagar, SG
  "distribution-tank": [1.3521, 103.9446], // Tampines, SG
  default: [1.3521, 103.8198], // Central SG
};

interface MapComponentProps {
  onDeviceSelect: (device: Device) => void;
}

export function MapComponent({ onDeviceSelect }: MapComponentProps) {
  const [devices, setDevices] = useState<Device[]>([]);

  useEffect(() => {
    getDevices().then(setDevices).catch(console.error);
  }, []);

  return (
    <div className="w-full h-screen relative z-0">
      <MapContainer
        center={[1.3521, 103.8198]}
        zoom={11}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {devices.map((device) => {
          const coords =
            MOCK_COORDINATES[device.site_id] || MOCK_COORDINATES["default"];
          return (
            <Marker
              key={device.id}
              position={coords}
              eventHandlers={{ click: () => onDeviceSelect(device) }}
            />
          );
        })}
      </MapContainer>
    </div>
  );
}
