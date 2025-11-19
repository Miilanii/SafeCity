import React, {useState} from 'react';
import axios from 'axios';
export default function ChatPanel(){
  const [msgs, setMsgs] = useState([]);
  const [text, setText] = useState('');
  const [district, setDistrict] = useState('');
  async function send(){
    if(!text) return;
    setMsgs(m=>[...m,{from:'user',text}]);
    try{
      const res = await axios.post('/api/chat',{message:text,district});
      setMsgs(m=>[...m,{from:'bot',text:res.data.reply, resources: res.data.resources, escalation: res.data.escalation_flag}]);
    }catch(e){
      setMsgs(m=>[...m,{from:'bot',text:'Error contacting server'}]);
    }
    setText('');
  }
  return (
    <div>
      <div style={{height:400, overflow:'auto', border:'1px solid #ccc', padding:10}}>
        {msgs.map((m,i)=>(
          <div key={i} style={{marginBottom:10}}>
            <b>{m.from}</b>: <div>{m.text}</div>
            {m.resources && m.resources.length>0 && (
              <div style={{marginTop:5}}>
                <b>Resources:</b>
                <ul>{m.resources.map((r,idx)=>(<li key={idx}>{r.name} ({r.phone}) - {r.type}</li>))}</ul>
              </div>
            )}
            {m.escalation && <div style={{color:'red'}}>Immediate danger flagged — call emergency services.</div>}
          </div>
        ))}
      </div>
      <div style={{marginTop:10}}>
        <input placeholder="District (optional)" value={district} onChange={e=>setDistrict(e.target.value)} /><br/>
        <textarea rows={4} value={text} onChange={e=>setText(e.target.value)} style={{width:'100%'}} /><br/>
        <button onClick={send}>Send</button>
      </div>
    </div>
  )
}
