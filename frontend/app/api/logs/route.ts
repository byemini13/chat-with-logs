import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const url = new URL(req.url);
  const repo = url.searchParams.get("repo");

  if (!repo) {
    return NextResponse.json({ error: "Repository is required" }, { status: 400 });
  }

  try {
    const backendUrl = `http://localhost:8000/logs?repo=${encodeURIComponent(repo)}`;
    const response = await fetch(backendUrl);
    const data = await response.json();

    return NextResponse.json({ logs: data.logs });
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch logs" }, { status: 500 });
  }
}
