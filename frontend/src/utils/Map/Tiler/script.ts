export class TileError extends Error {
    constructor(message: string, readonly status: number) {
        super(message);
        this.name = "TileError";
    }
}

export const GetMapTiles = async (endpoint = "/routes/get-tiles") => {
    const response = await fetch(endpoint);
    const payload = await response.json().catch(() => null);

    if (!response.ok) {
        throw new TileError(payload?.error?.message ?? "Failed to fetch tiles", response.status);
    }
    return payload.data;
};