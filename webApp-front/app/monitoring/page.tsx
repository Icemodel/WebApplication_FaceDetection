"use client";

import { useRef, useState } from "react";

export default function MonitoringPage() {
  const imgRef = useRef<HTMLImageElement | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);

  const startStream = () => {
    if (socketRef.current) {
      console.warn("WebSocket is already open or being opened.");
      return;
    }

    socketRef.current = new WebSocket("ws://127.0.0.1:3000/ws/client");
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
      <main className="bg-green-400 rounded-2xl shadow-lg mt-8 sm:mt-10 p-6 sm:p-8 w-11/12 max-w-4xl border border-gray-200">
        <div className="flex flex-col sm:flex-row items-center mb-4 gap-4 bg-green-700">
          <h2 className="text-xl font-semibold flex items-center text-gray-800">
            Single Camera
          </h2>
          <div className="flex-1" />
          <select className="border border-gray-300 rounded-md px-3 py-1 text-gray-700 hover:bg-blue-700 hover:text-white focus:outline-none transition duration-200 ease-in-out w-full sm:w-auto">
            <option>Floor 1</option>
            <option>Floor 2</option>
            <option>Floor 3</option>
          </select>
          <select className="border border-gray-300 rounded-md px-3 py-1 text-gray-700 hover:bg-blue-700 hover:text-white focus:outline-none transition duration-200 ease-in-out w-full sm:w-auto sm:ml-2">
            <option>Single Camera</option>
            <option>4 Cameras</option>
            <option>6 Cameras</option>
          </select>
        </div>
        <select className="border border-gray-300 rounded-md px-3 py-2 w-full mb-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-200 transition duration-200 ease-in-out">
          <option>Camera 1 (Main Entrance)</option>
          <option>Camera 2 (Lobby)</option>
          <option>Camera 3 (Server Room)</option>
        </select>

        <div className="flex justify-center mb-6 bg-gray-100 rounded-2xl p-2">
          <img
            ref={imgRef}
            className="w-full h-auto max-w-full rounded-xl border border-gray-200 shadow-inner object-contain"
            alt="Live Stream"
            style={{ maxHeight: '400px', background: "#eee" }}
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
      </main>
    </div>
  );
}
