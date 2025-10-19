"use client";
import { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import type { LngLatLike } from 'mapbox-gl';
import "mapbox-gl/dist/mapbox-gl.css";
import "./App.css"
import {fetchKernalDensityPrediction} from "./fetchPredictions"

const INITIAL_CENTER: LngLatLike = [-79.3354,43.7206]
const INITIAL_ZOOM: number = 10

export default function Home() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);  
  const [currPrediction, setCurrPrediction] = useState("Click Anywhere To Get Collision Likelihood")


  useEffect(() => {
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
    
    const container = mapContainerRef.current;
    if (!container) return; // ensures it's not null

    mapRef.current = new mapboxgl.Map({
      container: container,
      style: "mapbox://styles/mapbox/streets-v11", // required
      center: INITIAL_CENTER, // Toronto
      zoom: INITIAL_ZOOM,
    });

    mapRef.current.on('click', (e: mapboxgl.MapMouseEvent) => {
      handleMapClick(e)
    });

    return () => mapRef.current?.remove();
  }, []);


 
  const handleMapClick = (e: mapboxgl.MapMouseEvent) => {
    const { lat, lng } = e.lngLat;
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
        <h3>{currPrediction}</h3>
      </div>
      
    </>
  );
}