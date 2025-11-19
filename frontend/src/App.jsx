import React from 'react';
import MapView from './MapView';
import ChatPanel from './ChatPanel';
export default function App(){
  return (
    <div style={{display:'flex', gap:20}}>
      <div style={{flex:1}}>
        <h2>SafeCity — GBV Hotspots</h2>
        <MapView />
      </div>
      <div style={{width:400}}>
        <h3>Support Chat</h3>
        <ChatPanel />
      </div>
    </div>
  )
}
