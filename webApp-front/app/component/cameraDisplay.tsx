"use client";
import { useRef, useState, useEffect } from "react";
import axios from "axios";

export default function CameraDisplay({ classname = "" }) {
  const imgRef = useRef<HTMLImageElement | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);

  // State สำหรับ floor ที่มาจาก API
  const [floors, setFloors] = useState<number[]>([]);
  const [selectedFloor, setSelectedFloor] = useState<string>("");
  const [cameras, setCameras] = useState<{ id: number; camera_name: string }[]>([]);
  const [selectedCamera, setSelectedCamera] = useState<string>("");

  // โหลดชั้นของอาคาร จาก API
  useEffect(() => {
  axios.get("/api/monitoring/floors", { withCredentials: true })
    .then(res => {
      setFloors(res.data);
      if (res.data.length > 0) setSelectedFloor(res.data[0].toString());
    })
    .catch(err => {
      setFloors([]);
      // handle error ตามต้องการ
    });
}, []);

// โหลดกล้องจาก API เมื่อเลือกชั้นของอาคารแล้ว
  useEffect(() => {
  if (selectedFloor) {
    axios.get(`/api/monitoring/cameras?floor_name=${encodeURIComponent(selectedFloor)}`, { withCredentials: true })
      .then(res => {
        const data = Array.isArray(res.data) ? res.data : [];
        setCameras(data);
        if (data.length > 0) setSelectedCamera(data[0].id.toString());
        else setSelectedCamera("");
      })
      .catch(() => setCameras([]));
  } else {
    setCameras([]);
    setSelectedCamera("");
  }
}, [selectedFloor]);

  // การเริ่มและหยุดการ Streaming
  const startStream = () => {
    if (socketRef.current) {
      console.warn("WebSocket is already open or being opened.");
      return;
    }
    socketRef.current = new WebSocket("ws://127.0.0.1:3002/ws/client");
    socketRef.current.binaryType = "blob";

    socketRef.current.onopen = () => {
      console.log("WebSocket opened successfully.");
      setIsStreaming(true);
    };

    socketRef.current.onerror = (e) => {
      console.error("WebSocket error:", e);
      stopStream();
    };

    socketRef.current.onclose = () => {
      console.log("WebSocket closed.");
      socketRef.current = null;
      setIsStreaming(false);
      if (imgRef.current) {
        imgRef.current.src = "";
      }
    };

    socketRef.current.onmessage = (event: MessageEvent) => {
      if (typeof event.data === "string") {
        console.log("Received non-binary message:", event.data);
        return;
      }
      const blob = new Blob([event.data], { type: "image/jpeg" });
      const url = URL.createObjectURL(blob);
      if (imgRef.current) {
        imgRef.current.src = url;
      }
    };
  };

  const stopStream = () => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
      setIsStreaming(false);
      if (imgRef.current) {
        imgRef.current.src = "";
      }
    }
  };

  return (
    <div className="flex flex-col items-center font-sans">
        <div className="flex flex-row-reverse w-full items-center mb-4 gap-4 bg-white">
          {/* Floor Select (ดึงจาก API) */}
          <select
            value={selectedFloor}
            onChange={e => setSelectedFloor(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-1 text-gray-700 hover:bg-blue-700 hover:text-white focus:outline-none transition duration-200 ease-in-out w-full sm:w-auto"
          >
            {Array.isArray(floors) && floors.length > 0 ? (
              floors.map(floor_name => (
                <option key={floor_name} value={floor_name}>
                  Floor {floor_name}
                </option>
              ))
            ) : (
              <option>Loading...</option>
            )}
          </select>
        </div>

        {/* Camera Select */}
        <select 
          value={selectedCamera}
          onChange={e => setSelectedCamera(e.target.value)}
          className="border border-gray-300 rounded-md px-3 py-2 w-full mb-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-200 transition duration-200 ease-in-out"
        >
          {cameras.length === 0 ? (
            <option>Cameras are not found</option>
          ) : (
            cameras.map(camera => (
              <option key={camera.id} value={camera.id}>
                Camera {camera.camera_name}
              </option>
            ))
          )}
        </select>

        <div className="flex justify-center mb-6 bg-gray-100 rounded-2xl p-2">
          <img
            ref={imgRef}
            className="w-full h-auto max-w-full rounded-xl border border-gray-200 shadow-inner object-contain"
            alt="Live Stream"
            style={{ maxHeight: '600px', background: "#eee" }}
            src="https://placehold.co/800x400/D1D5DB/4B5563?text=No+Streaming+Active"
            onError={(e) => {
              e.currentTarget.src = "https://placehold.co/800x400/D1D5DB/4B5563?text=Waiting+for+Streaming";
            }}
          />
        </div>

        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center">
          <button
            onClick={startStream}
            disabled={isStreaming}
            className={`px-8 py-2 rounded-full font-semibold text-white text-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-lg
              ${isStreaming
                ? "bg-gray-400 cursor-not-allowed opacity-70"
                : "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700"
              }`}
          >
            Start Stream
          </button>
          <button
            onClick={stopStream}
            disabled={!isStreaming}
            className={`px-8 py-2 rounded-full font-semibold text-white text-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-lg
              ${!isStreaming
                ? "bg-gray-400 cursor-not-allowed opacity-70"
                : "bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700"
              }`}
          >
            Stop Stream
          </button>
        </div>
    </div>
  );
}