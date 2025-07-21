import Header from "./component/header";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import axios from "axios";
import { UserProvider } from "./Context/userPictureContext";

axios.defaults.withCredentials = true;
axios.interceptors.request.use((config) => {
  config.withCredentials = true;
  return config;
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Face Rec",
  description: "Web Application for Face Recognition",
};

export default function RootLayout({ children, }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <UserProvider>
          <div className="min-h-screen bg-gray-50">
            <Header />
            {children}
          </div>
        </UserProvider>
      </body>
    </html>
  );
};
