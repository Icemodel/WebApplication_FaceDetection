import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const res = await fetch("http://localhost:3001/api/signin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    credentials: "include", // สำคัญสำหรับ cookie
  });

  // ดึง cookie จาก backend
  const setCookie = res.headers.get("set-cookie");

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { detail: text };
  }

  // สร้าง response และแนบ cookie กลับไป
  const response = NextResponse.json(data, { status: res.status });
  if (setCookie) {
    response.headers.set("set-cookie", setCookie);
  }
  return response;
}