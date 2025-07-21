"use client";
import { createContext, useContext, useState, ReactNode } from "react";

type UserPictureType = {
  profilePicture: string | null;
  setProfilePicture: (pic: string | null) => void;
};

export const UserPictureContext = createContext<UserPictureType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [profilePicture, setProfilePicture] = useState<string | null>(null);

  return (
    <UserPictureContext.Provider value={{ profilePicture, setProfilePicture }}>
      {children}
    </UserPictureContext.Provider>
  );
}

export function useUserPicture() {
  const context = useContext(UserPictureContext);
  if (!context) throw new Error("useUserPicture must be used within a UserProvider");
  return context;
}