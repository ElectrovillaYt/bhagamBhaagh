export class ViewRender extends Error {
    constructor(message: string, readonly status: number) {
        super(message);
        this.name = "ViewportError";
    }
}

type ViewType = {
    zoom: number;
    bbox: number[];
};

/* @ Mwthod to send map view stats eg: map zoom level and bounding box */
export const SendViewport = async (view: ViewType, endpoint = "/routes/send-view") => {
    const response = await fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(view)
    });
    
    const payload = await response.json().catch(() => null);

    if (!response.ok) {
        throw new ViewRender(payload?.error?.message ?? "Failed to fetch tiles", response.status);
    }
    return payload;
};