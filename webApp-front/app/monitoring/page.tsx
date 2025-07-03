"use client";
import { useRef, useState } from "react";
import "@/css/FaceDetection.css";

const CameraStream = () => {
  const imgRef = useRef<HTMLImageElement | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);

  const startStream = () => {
    if (socketRef.current) return;
    socketRef.current = new WebSocket("ws://127.0.0.1:3000/ws/client");
    socketRef.current.binaryType = "blob";

    socketRef.current.onopen = () => console.log("WebSocket opened");
    socketRef.current.onerror = (e) => console.error("WebSocket error", e);
    socketRef.current.onclose = () => {
      console.log("WebSocket closed");
      socketRef.current = null;
      setIsStreaming(false);
    };
    socketRef.current.onmessage = (event: MessageEvent) => {
      if (typeof event.data === "string") return;
      const blob = new Blob([event.data], { type: "image/jpeg" });
      const url = URL.createObjectURL(blob);
      if (imgRef.current) {
        imgRef.current.src = url;
      }
    };
    setIsStreaming(true);
  };

  const stopStream = () => {
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
      setIsStreaming(false);
      if (imgRef.current) imgRef.current.src = "";
    }
  };

  return (
    <div className="fd-root">
      {/* Header */}
      <div className="fd-header">
        <div className="fd-header-left">
          <span className="fd-title">Face Rec</span>
          <button className="fd-btn">Cameras</button>
          <button className="fd-btn active">Detection</button>
          <button className="fd-btn">Management</button>
        </div>
        <button className="fd-signin">Sign in</button>
      </div>

      {/* Main Card */}
      <div className="fd-card">
        {/* Camera Header */}
        <div className="fd-card-header">
          <span className="fd-card-title">📷 Single Camera</span>
          <div style={{ flex: 1 }} />
          <select className="fd-select">
            <option>Select Floors</option>
          </select>
          <select className="fd-select">
            <option>Camera Mode</option>
          </select>
        </div>
        <select className="fd-select-full">
          <option>Select camera</option>
        </select>

        {/* Camera Stream */}
        <div className="fd-stream">
          <img
            ref={imgRef}
            width={640}
            alt="stream"
            className="fd-img"
          />
        </div>

        {/* Control Buttons */}
        <div className="fd-controls">
          <button
            onClick={startStream}
            disabled={isStreaming}
            className="fd-btn start"
            style={{ cursor: isStreaming ? "not-allowed" : "pointer" }}
          >
            Start
          </button>
          <button
            onClick={stopStream}
            disabled={!isStreaming}
            className="fd-btn stop"
            style={{ cursor: !isStreaming ? "not-allowed" : "pointer" }}
          >
            Stop
          </button>
        </div>
      </div>
    </div>
  );
};

export default CameraStream;