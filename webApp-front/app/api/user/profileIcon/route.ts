import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const cookie = req.headers.get("cookie") ?? "";
  
  try {
    const res = await fetch("http://localhost:3001/api/user/profileIcon", {
      headers: { cookie },
      cache: "no-store",
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    return NextResponse.json({ error: "Failed to fetch profile icon" }, { status: 500 });
  }
}