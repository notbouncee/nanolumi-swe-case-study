import { useState } from "react";
import type { Device } from "@/services/backendApi";
import { MapComponent } from "@/components/organisms/MapComponent";
import { DeviceModal } from "@/components/organisms/DeviceModal";

function App() {
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);

  return (
    <div className="w-full h-screen overflow-hidden bg-gray-100 relative">
      <header className="absolute top-0 left-0 z-[1000] w-full bg-white/80 backdrop-blur-md shadow-sm border-b px-6 py-4 flex items-center pointer-events-auto">
        <h1 className="text-xl font-bold text-gray-800 tracking-tight">
          Water Quality Monitor
        </h1>
      </header>

      <MapComponent onDeviceSelect={setSelectedDevice} />

      <DeviceModal
        device={selectedDevice}
        onClose={() => setSelectedDevice(null)}
      />
    </div>
  );
}

export default App;
