"use client"
import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";


export default function SignInPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [formError, setFormError] = useState("");

  const handleSignIn = async () => {
    let valid = true;
    if (!username) {
        setUsernameError("Please enter your username.");
        valid = false;
    } else {
        setUsernameError("");
    }
    if (!password) {
        setPasswordError("Please enter your password.");
        valid = false;
    }else {
        setPasswordError("");
    }
    if (!valid) return;

    try {
      const res = await axios.post("/api/signin", { username, password }, { withCredentials: true });
      router.push("/monitoring");
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setFormError(err.response.data.detail);
      }
    }
  };

  return (
    <main className="flex flex-col items-center font-san w-full h-auto">
      <div>
        <h1 className="text-3xl font-bold text-blue-900 mt-8 mb-10">Sign in to Face Rec</h1>
      </div>
      <div className="border border-gray-300 rounded-md p-4 text-blue-900 bg-white w-3/12 h-8/12 shadow-lg">
        <label htmlFor="username" className="block font-semibold mb-2">
          Username
        </label>
        <input  
          type="text" 
          id="username" 
          className="border border-gray-300 rounded-md p-1.5 w-full text-black focus:outline-none focus-within:ring-1 focus-within:ring-blue-500" 
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        {usernameError && <div className="text-red-500 text-sm">{usernameError}</div>}
        <div className="flex flex-row mb-2 mt-4">
          <label htmlFor="password" className="block font-semibold ">
            Password
          </label>
          <div className="flex flex-1"></div>
          <button 
            className="text-gray-500 text-sm hover:text-blue-600 cursor-pointer"
          >
            Forgot password?
          </button>
        </div>
        <input 
          type="password" 
          id="password" 
          className="border border-gray-300 rounded-md p-1.5 w-full text-black focus:outline-none focus-within:ring-1 focus-within:ring-blue-500" 
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        {passwordError && <div className="text-red-500 text-sm">{passwordError}</div>}
        {formError && <div className="text-red-500 text-sm mt-2">{formError}</div>}
        <button 
          className="mt-4 w-full p-2 rounded-md bg-blue-600 text-white font-semibold hover:bg-blue-700 transition duration-200 ease-in-out cursor-pointer"
          onClick={handleSignIn}
        >
          Sign in
        </button>
      </div>
      <div className="flex flex-row justify-center mt-6 border border-gray-300 rounded-md p-4 bg-white w-3/12 shadow-lg">
        <p className="text-gray-500">Don't have an account?</p> 
        <button 
          className="text-blue-600 hover:text-blue-800 cursor-pointer ml-1"
          onClick={() => router.push("/sign-up/")}
        >
          Sign up
        </button>
      </div>
    </main> 
  );
};
