import React, {useEffect, useState} from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import axios from 'axios';
export default function MapView(){
  const [hotspots, setHotspots] = useState([]);
  useEffect(()=>{ fetchData() },[]);
  async function fetchData(){
    try{
      const res = await axios.get('/api/hotspots?date=2021-05-01');
      setHotspots(res.data);
    }catch(e){ console.error(e) }
  }
  return (
    <MapContainer center={[-26.2041,28.0473]} zoom={6} style={{height:600}}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {hotspots.map(h=>(
        <CircleMarker key={h.district} center={[h.lat,h.lon]} radius={5+Math.log(1+h.incident_count)*3}>
          <Popup>
            <div><b>{h.district}</b><br/>Incidents: {h.incident_count}<br/>Alert: {h.alert ? 'Yes' : 'No'}</div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  )
}
