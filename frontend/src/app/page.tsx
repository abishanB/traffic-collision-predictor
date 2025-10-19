"use client";

import { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

export default function Home() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);  
  
  useEffect(() => {
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    
    const container = mapContainerRef.current;
    if (!container) return; // ensures it's not null

    mapRef.current = new mapboxgl.Map({
      container: container,
      style: "mapbox://styles/mapbox/streets-v11", // required
      center: [-79.3832, 43.6532], // Toronto
      zoom: 10,
    });

    mapRef.current.on('click', (e: mapboxgl.MapMouseEvent) => {
      handleMapClick(e)
    });

    return () => mapRef.current?.remove();
  }, []);


  const fetchPrediction = async (lat: number, long: number) => {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lat: lat, long: long })
    })
    console.log(await res.json())
  }
    
  const handleMapClick = (e: mapboxgl.MapMouseEvent) => {
    const { lat, lng } = e.lngLat;
    fetchPrediction(lat, lng)
  }
  return (
    <div id="map-container" ref={mapContainerRef} style={{ width: "100%", height: "100vh" }}/>
  );
}