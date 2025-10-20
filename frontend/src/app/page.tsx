"use client";
import { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css"
import {fetchKernalDensityPrediction} from "./fetchPredictions"

const INITIAL_CENTER: [number, number] = [-79.3662,43.7150]
const INITIAL_ZOOM: number = 10.5

const MAP_BOUNDS: [[number, number], [number, number]] = [
  [-79.8298827685777 ,43.5], // Southwest coordinates
  [-78.90154616803314, 43.92] // Northeast coordinates
];

export default function Home() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);  
  const [center, setCenter] = useState<[number, number]>(INITIAL_CENTER)
  const [zoom, setZoom] = useState<number>(INITIAL_ZOOM)

  const [currPrediction, setCurrPrediction] = useState<number>(0.0)

  useEffect(() => {
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    
    const container = mapContainerRef.current;
    if (!container) return; // ensures it's not null
    
    const map = new mapboxgl.Map({
      container: container,
      style: "mapbox://styles/mapbox/streets-v11", // required
      center: INITIAL_CENTER, // Toronto
      zoom: INITIAL_ZOOM,
      maxBounds: MAP_BOUNDS
    });
    mapRef.current = map; // assign to ref once created

    mapRef.current.on('click', (e: mapboxgl.MapMouseEvent) => {
      handleMapClick(e)
    });

    mapRef.current.on('move', () => {
      const mapCenter = map.getCenter()
      const mapZoom = map.getZoom()      
      setCenter([ mapCenter.lng, mapCenter.lat ])
      setZoom(mapZoom)
    })

    return () => mapRef.current?.remove();
  }, []);


  const handleMapClick = (e: mapboxgl.MapMouseEvent) => {
    const { lat, lng } = e.lngLat;
    console.log(lng, lat)
    const promise = fetchKernalDensityPrediction(lat, lng).then()
    promise.then((kernal_density_predicition) => {
      console.log(kernal_density_predicition)
      setCurrPrediction(kernal_density_predicition.prediction)
    })
  }

  return (
    <>
      <div id="map-container" ref={mapContainerRef} />  
      <div className="sidebar">
        <h3>Collision Risk Score: {currPrediction.toFixed(2)}</h3>
        Longitude: {center[0].toFixed(4)} | Latitude: {center[1].toFixed(4)} | Zoom: {zoom.toFixed(2)}
      </div>
    </>
  );
}