import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const floor_name = searchParams.get("floor_name");
  
  if (!floor_name) {
    return NextResponse.json([], { status: 400 });
  }

  try {
    const res = await fetch(
      `http://127.0.0.1:3001/cameras/?floor_name=${encodeURIComponent(floor_name)}`
    );
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    return NextResponse.json([], { status: 500 });
  }
}