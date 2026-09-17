export const GetLocation = async () => {
    const res = await new Promise((resolve) => {
        navigator.geolocation.getCurrentPosition(
            // Success: Resolve with the coords object
            (position) => resolve(position.coords),

            // Error / Permission Denied
            () => resolve(null),

            // Options
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    });

    const coords = await res;
    return coords instanceof Object ? JSON.parse(JSON.stringify(coords)) : null
};