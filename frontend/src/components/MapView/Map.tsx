// Map component
"use client";
import React, { useEffect, useState, useRef } from 'react'

import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

import { GetMapTiles } from '@/utils/Map/Tiler/script';
import { GetLocation } from '@/utils/Map/LocationFetcher/script';
import { SendViewport } from '@/utils/Map/ViewStats/script';

interface prop {
    className?: string
};

class MapError extends Error {
    constructor(message: ErrorEvent, readonly status: number = 500) {
        super(String(message));
        this.name = "MapError";
    }
};

export const Map = ({ className = '' }: prop) => {
    const mapRef = useRef<maplibregl.Map>(null);

    useEffect(() => {
        if (mapRef.current) return;
        const initmap = async () => {
            try {
                const style = await GetMapTiles();
                const Location = await GetLocation();// Auto location fetch at init
                if (style) {
                    const map = new maplibregl.Map({
                        container: 'map',
                        style: style, // style
                        center: [Location?.longitude || 0, Location?.latitude || 0], // longitude,latitude
                        zoom: Location ? 15 : 2, // if location active then default zoom 15 else 2
                        attributionControl: false,
                        renderWorldCopies: false,
                    });

                    map.dragRotate.disable();
                    map.touchZoomRotate.disableRotation();

                    // map controls
                    map.addControl(new maplibregl.FullscreenControl(), "top-right"); // toggle fullscreen controller
                    map.addControl(new maplibregl.NavigationControl(), "bottom-right"); // map navigation controller


                    map.on("load", () => {
                        console.log("MAP LOADED");
                    });

                    map.on("error", (e) => {
                        throw new MapError(e);
                    });


                    // Send map zoom and viewport bounding on cursor move
                    map.on('moveend', () => {
                        const zoom = map.getZoom();
                        const bounds = map.getBounds();

                        // Format as an array or object to send to an API or state manager
                        const viewport = {
                            zoom: zoom,
                            bbox: [
                                bounds.getWest(),  // Min Longitude
                                bounds.getSouth(), // Min Latitude
                                bounds.getEast(),  // Max Longitude
                                bounds.getNorth()  // Max Latitude
                            ]
                        };
                        SendViewport(viewport);
                        console.log("Map Viewport:", viewport);
                    });

                    mapRef.current = map;
                    return () => {
                        if (map) map.remove(); // clean up
                    }
                }

                if (!Location) throw new Error("Location permission denied or unavailable please retry!");
            } catch (err) {
                console.log(err);
            }
        };
        initmap();
    }, []);

    return (
        <div id="map" className={` ${className}`}></div>
    )
}