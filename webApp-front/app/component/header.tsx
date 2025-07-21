"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import axios from "axios";
import { useUserPicture } from "../Context/userPictureContext";

export default function Header() {
    const router = useRouter();

    const { profilePicture, setProfilePicture } = useUserPicture();

    useEffect(() => {
        axios.get("http://localhost:3001/api/user/profileIcon", { withCredentials: true })
        .then(res => setProfilePicture(res.data.profile_icon))
        .catch(() => setProfilePicture(null));
    }, []);

    return (
        <header className="w-full flex justify-between items-center px-6 sm:px-10 py-4 sm:py-6 bg-white shadow-sm">
            <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-6">
                <span className="text-2xl sm:text-3xl font-extrabold text-blue-900">Face Rec</span>
                <nav className="flex gap-2 sm:gap-4">
                    <button
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm cursor-pointer"
                        onClick={() => router.push("/monitoring/")}
                    >
                        Monitoring
                    </button>
                    <button
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm cursor-pointer"
                        onClick={() => router.push("/detection/")}
                    >
                        Detection
                    </button>
                    <button 
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm cursor-pointer"
                        onClick={() => router.push("/management/")}
                    >
                        Management
                    </button>
                    <button 
                        className="px-3 sm:px-5 py-1 sm:py-2 rounded-full font-medium text-blue-700 hover:bg-blue-100 focus:outline-none transition duration-200 ease-in-out shadow-sm cursor-pointer"
                        onClick={() => router.push("/notify/")}
                    >
                        Notify
                    </button>
                </nav>
            </div>
            {profilePicture && (
                <button 
                    className={`w-14 h-14 rounded-full font-semibold shadow-md cursor-pointer`}
                >
                    <img src={`/profile/${profilePicture}.jpg`} 
                         alt="profile" 
                         className="w-14 h-14 rounded-full object-cover"
                    />
                </button>
                )}
        </header>
    );
};