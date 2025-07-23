import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    if (!body.question || !body.question.trim()) {
      return NextResponse.json({ error: "Question cannot be empty" }, { status: 400 });
    }

    // Forward the request to the FastAPI backend
    const backendResponse = await fetch("http://localhost:8000/api/qa", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: body.question,
        context: body.context || "",
        headings: body.headings || []
      }),
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json().catch(() => ({ error: "Backend error" }));
      return NextResponse.json(errorData, { status: backendResponse.status });
    }

    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error processing QA request:", error);
    return NextResponse.json({ error: "Failed to process QA request" }, { status: 500 });
  }
}
