import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const cookie = req.headers.get("cookie") ?? "";
  try {
    const res = await fetch("http://127.0.0.1:3001/floors/", {
      headers: { cookie },
      cache: "no-store"
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    return NextResponse.json([], { status: 500 });
  }
}