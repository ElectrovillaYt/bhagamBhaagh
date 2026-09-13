import React, { useEffect, useState, useRef } from 'react'
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";


export const Map = () => {
    const mapRef = useRef(null);

    useEffect(() => {
        const initmap = async () => {
            if (mapRef.current) return;
            try {

                const tiler_api = `${process.env.REACT_APP_SERVER_URL}/tiles`;

                const response = await fetch(tiler_api);
                if (!response.ok)
                    throw new Error(`Error Fetching map tiles, status: ${response.status}`);

                const style = await response.json();
                console.log("Fetched style:", style);


                const map = new maplibregl.Map({
                    container: 'map',
                    style: style, // style
                    center: [0, 0],
                    zoom: 2,
                    attributionControl: false,
                    renderWorldCopies: false,
                    antialias: true,
                    multipleWorlds: false,
                })

                map.dragRotate.disable();
                map.touchZoomRotate.disableRotation();

                map.on("load", () => {
                    console.log("MAP LOADED");
                });

                map.on("error", (e) => {
                    console.error("MAP ERROR:", e);
                });

                map.on("sourcedata", (e) => {
                    console.log("SOURCE:", e.sourceId, e.isSourceLoaded);
                });

                mapRef.current = map;
                return () => {
                    if (map) map.remove(); // clean up
                }
            } catch (err) {
                console.error("Error initializing map:", err);
            }
        };
        initmap();
    }, []);
    return (
        <div id="map"></div>
    )
}
