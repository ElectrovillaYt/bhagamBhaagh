import { NotFoundError } from "@/lib/ErrorHandler/errors";
import { NextRequest, NextResponse } from "next/server";

export async function POST(_req: NextRequest) {
    try {
        const { zoom, bbox } = await _req.json();
        const base = process.env.BACKEND_URL;

        if (!zoom || !bbox) throw new NotFoundError("Invalidor null map states received!");

        if (!base) throw new Error("BACKEND_URL is not configured");

        const response = await fetch(`${base}/map/viewport`);

        if (!response.ok) {
            const detail = await response.text().catch(() => "");
            console.error("Error sending map states to server!", response.status, detail);
            return NextResponse.json(
                { error: { message: "Failed to send map view", status: response.status } },
                { status: response.status },
            );
        }

        return NextResponse.json({ data: await response.json() }, { status: 200 });
    } catch (err) {
        console.error("[send-viewport]", err); // stack stays on the server
        const message = err instanceof Error ? err.message : "Unknown error";
        return NextResponse.json({ error: { message } }, { status: 500 });
    }
}