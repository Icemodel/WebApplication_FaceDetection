import EachFloorDetection from "../component/floorList";
export default function DetectionPage() {
  return (
    <div className="flex flex-col items-center font-sans">
      <main className="bg-white rounded-2xl shadow-lg mt-8 p-6 w-11/12 border border-gray-200">
        <div className="flex flex-row items-center mb-4 gap-4 bg-green-700">
          <h2 className="text-xl font-semibold flex items-center text-gray-800">
            Building Overview
          </h2>
        </div>  
        <div className="flex flex-col gap-4">
          <EachFloorDetection />
          <EachFloorDetection />
          <EachFloorDetection />
          <EachFloorDetection />
        </div>
      </main>
    </div>
  );
}
