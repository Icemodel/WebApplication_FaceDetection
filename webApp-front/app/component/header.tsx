"use client";
import { useRouter } from "next/navigation";

export default function Header() {
    const router = useRouter();

    return (
        <header className="w-full flex justify-between items-center px-6 sm:px-10 py-4 sm:py-6 bg-white shadow-sm">
            <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-6">
                <span className="text-2xl sm:text-3xl font-extrabold text-blue-800">Face Rec</span>
                <nav className="flex gap-2 sm:gap-4">
                    <button
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm"
                        onClick={() => router.push("/monitoring/")}
                    >
                        Monitoring
                    </button>
                    <button
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm"
                        onClick={() => router.push("/detection/")}
                    >
                        Detection
                    </button>
                    <button 
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm"
                        onClick={() => router.push("/management/")}
                    >
                        Management
                    </button>
                    <button 
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm"
                        onClick={() => router.push("/notify/")}
                    >
                        Notify
                    </button>
                </nav>
            </div>
            <button className="px-4 sm:px-6 py-1 sm:py-2 rounded-full bg-blue-600 text-white font-semibold hover:bg-blue-700 transition duration-200 ease-in-out shadow-md">Sign in</button>
        </header>
    );
};