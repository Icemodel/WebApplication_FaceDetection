import PersonIcon from "./personIcon";

export default function FloorList() {
    return (
        <div className="flex-1 flex-col rounded-2xl shadow-lg border border-gray-200">
          <div className="flex flex-row m-4 gap-4">
            <h2 className="text-xl font-semibold text-gray-800 flex">
              X Floor
            </h2>
            <div className="flex flex-row h-auto w-auto border border-blue-700 rounded-2xl">
              <p className="m-2 text-xs text-blue-700">X People</p>
            </div>
          </div>
          <div className="flex flex-row m-4 gap-4">
            <PersonIcon />
            <PersonIcon />
            <PersonIcon />
            <PersonIcon />
          </div>
        </div>
    );
};