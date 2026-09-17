import { NextRequest, NextResponse } from "next/server";

export async function GET(_req: NextRequest) {
    try {
        const base = process.env.BACKEND_URL;
        if (!base) throw new Error("BACKEND_URL is not configured");

        const response = await fetch(`${base}/map/tiles`, { cache: "no-store" });

        if (!response.ok) {
            const detail = await response.text().catch(() => "");
            console.error("[get-tiles] upstream failed", response.status, detail);
            return NextResponse.json(
                { error: { message: "Failed to fetch map tiles", status: response.status } },
                { status: response.status },
            );
        }

        return NextResponse.json({ data: await response.json() }, { status: 200 });
    } catch (err) {
        console.error("[get-tiles]", err); // stack stays on the server
        const message = err instanceof Error ? err.message : "Unknown error";
        return NextResponse.json({ error: { message } }, { status: 500 });
    }
}