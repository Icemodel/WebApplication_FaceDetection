"use client";
import { useState } from "react";
import CameraDisplay from "../component/cameraDisplay";

export default function MonitoringPage() {

  // State สำหรับ select mode
  const [selectedMode, setSelectedMode] = useState("singlecamera");

  // แปลง mode เป็นชื่อที่แสดงผล
  let mode = "";
  if (selectedMode === "singlecamera") {
    mode = "Single Camera";
  } else if (selectedMode === "4cameras") {
    mode = "4 Cameras";
  } else {
    mode = "6 Cameras";
  }

  return (
    <div className="flex flex-col items-center font-sans">
      <main className={"flex flex-col rounded-2xl items-center bg-white shadow-lg mt-10 p-8 w-11/12 border border-gray-200"}>
        <div className="flex flex-row rounded w-full h-8 mb-4">
          <h2 className="text-xl font-semibold flex items-center text-gray-800">
            {mode}
          </h2>
          <div className="flex-1" />
          {/* Mode Select */}
          <select
            value={selectedMode}
            onChange={e => setSelectedMode(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-1 text-gray-700 hover:bg-blue-700 hover:text-white focus:outline-none transition duration-200 ease-in-out w-auto"
          >
            <option value="singlecamera">Single Camera</option>
            <option value="4cameras">4 Cameras</option>
            <option value="6cameras">6 Cameras</option>
          </select>
        </div>
        {mode === "Single Camera" ? (
          <div className="flex flex-row justify-center w-full">
            <CameraDisplay />
          </div>
        ) : (
          <div className="grid grid-cols-2 grid-rows-2 gap-4 w-full ">
            <CameraDisplay />
            <CameraDisplay />
            <CameraDisplay />
            <CameraDisplay />
          </div>
        )}
      </main>
    </div>
  );
};