import { useEffect, useMemo, useState } from "react";
import {
  CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis
} from "recharts";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const WS = API.replace(/^http/, "ws") + "/ws/live";

const fallback = {
  temp_a: 89.0, temp_b: 88.7, dirty_level: 1960, clean_level: 1810,
  flow_rate: 122.0, current_density: 43.8, output_kg: 0,
  availability: 98.5, performance: 93.5, quality: 98.6, oee: 90.9,
  downtime_minutes: 0, line_status: "CONNECTING"
};

function Metric({label,value,unit,tone=""}) {
  return <div className="kpi">
    <span>{label}</span><strong className={tone}>{value}</strong><small>{unit}</small>
  </div>;
}

function Parameter({label,value,unit,min,max}) {
  const pct = Math.max(0, Math.min(100, ((value-min)/(max-min))*100));
  return <div className="parameter">
    <div className="row"><span>{label}</span><small>{unit}</small></div>
    <strong>{Number(value).toLocaleString(undefined,{maximumFractionDigits:2})}</strong>
    <div className="track"><i style={{width:pct+"%"}} /></div>
  </div>;
}

export default function App(){
  const [live,setLive]=useState(fallback);
  const [history,setHistory]=useState([]);
  const [alarms,setAlarms]=useState([]);
  const [connected,setConnected]=useState(false);

  async function load(){
    try{
      const [currentRes,historyRes,alarmRes]=await Promise.all([
        fetch(API+"/api/current"), fetch(API+"/api/history?limit=80"), fetch(API+"/api/alarms?limit=20")
      ]);
      if(currentRes.ok) setLive(await currentRes.json());
      if(historyRes.ok) setHistory(await historyRes.json());
      if(alarmRes.ok) setAlarms(await alarmRes.json());
    }catch(e){ console.warn("API unavailable",e); }
  }

  useEffect(()=>{ load(); },[]);

  useEffect(()=>{
    const socket=new WebSocket(WS);
    socket.onopen=()=>setConnected(true);
    socket.onclose=()=>setConnected(false);
    socket.onerror=()=>setConnected(false);
    socket.onmessage=e=>{
      const sample=JSON.parse(e.data);
      setLive(sample);
      setHistory(prev=>[...prev.slice(-79),sample]);
    };
    return ()=>socket.close();
  },[]);

  useEffect(()=>{
    const id=setInterval(async()=>{
      try{
        const r=await fetch(API+"/api/alarms?limit=20");
        if(r.ok)setAlarms(await r.json());
      }catch{}
    },5000);
    return()=>clearInterval(id);
  },[]);

  async function acknowledge(id){
    const r=await fetch(API+"/api/alarms/"+id+"/acknowledge",{method:"POST"});
    if(r.ok)setAlarms(prev=>prev.map(a=>a.id===id?{...a,acknowledged:1}:a));
  }

  const active=alarms.filter(a=>!a.acknowledged).length;
  const chart=useMemo(()=>history.map((x,i)=>({
    n:i+1,tempA:x.temp_a,tempB:x.temp_b,flow:x.flow_rate,oee:x.oee
  })),[history]);

  return <div className="app">
    <header>
      <div>
        <div className="eyebrow">Industrial Digitalization Project</div>
        <h1>Production Monitoring System <em>V2</em></h1>
        <p>Full-stack DCS-inspired process historian and live operations dashboard.</p>
      </div>
      <div className={"connection "+(connected?"on":"off")}><i />{connected?"LIVE API":"API OFFLINE"}</div>
    </header>

    <section className="kpiGrid">
      <Metric label="OEE" value={live.oee.toFixed(1)+"%"} unit="Availability × Performance × Quality" tone="green"/>
      <Metric label="Output" value={live.output_kg.toFixed(1)} unit="kg · simulated shift"/>
      <Metric label="Quality" value={live.quality.toFixed(1)+"%"} unit="Good production" tone="green"/>
      <Metric label="Downtime" value={live.downtime_minutes.toFixed(1)} unit="minutes"/>
      <Metric label="Active Alarms" value={active} unit="Unacknowledged events" tone={active?"amber":"green"}/>
      <Metric label="Line Status" value={live.line_status} unit={connected?"Automatic simulation":"Waiting for backend"} tone={connected?"green":"amber"}/>
    </section>

    <section className="layout">
      <article className="panel trendPanel">
        <div className="panelTitle"><div><span>Historian</span><h2>Process Trend</h2></div><small>{history.length} samples loaded</small></div>
        <div className="chart">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chart}>
              <CartesianGrid stroke="#1c3040" vertical={false}/>
              <XAxis dataKey="n" hide/>
              <YAxis yAxisId="temp" domain={[84,94]} tick={{fill:"#7890a3",fontSize:11}} axisLine={false} tickLine={false}/>
              <YAxis yAxisId="flow" orientation="right" domain={[115,130]} tick={{fill:"#7890a3",fontSize:11}} axisLine={false} tickLine={false}/>
              <Tooltip contentStyle={{background:"#0b1722",border:"1px solid #20384a",borderRadius:10}}/>
              <Line yAxisId="temp" type="monotone" dataKey="tempA" name="Tank A °C" stroke="#55d8ff" dot={false} strokeWidth={2}/>
              <Line yAxisId="temp" type="monotone" dataKey="tempB" name="Tank B °C" stroke="#8a9dff" dot={false} strokeWidth={2}/>
              <Line yAxisId="flow" type="monotone" dataKey="flow" name="Flow L/min" stroke="#4be2a0" dot={false} strokeWidth={2}/>
            </LineChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="panel">
        <div className="panelTitle"><div><span>DCS</span><h2>Critical Parameters</h2></div><small>2 s refresh</small></div>
        <div className="parameterGrid">
          <Parameter label="Dissolution Tank A" value={live.temp_a} unit="°C" min={80} max={100}/>
          <Parameter label="Dissolution Tank B" value={live.temp_b} unit="°C" min={80} max={100}/>
          <Parameter label="Dirty Solution Tank" value={live.dirty_level} unit="mm" min={1500} max={2200}/>
          <Parameter label="Clean Solution Tank" value={live.clean_level} unit="mm" min={1500} max={2200}/>
          <Parameter label="Flow Rate" value={live.flow_rate} unit="L/min" min={100} max={140}/>
          <Parameter label="Current Density" value={live.current_density} unit="A/dm²" min={35} max={50}/>
        </div>
      </article>
    </section>

    <section className="layout lower">
      <article className="panel">
        <div className="panelTitle"><div><span>OEE</span><h2>Efficiency Breakdown</h2></div></div>
        <div className="oeeGrid">
          <div><b>{live.availability.toFixed(1)}%</b><span>Availability</span></div>
          <div><b>{live.performance.toFixed(1)}%</b><span>Performance</span></div>
          <div><b>{live.quality.toFixed(1)}%</b><span>Quality</span></div>
        </div>
        <p className="formula">OEE = Availability × Performance × Quality</p>
      </article>

      <article className="panel alarmPanel">
        <div className="panelTitle"><div><span>Events</span><h2>Alarm Management</h2></div><small>{active} active</small></div>
        <div className="alarmList">
          {alarms.length===0 && <div className="empty">No alarms recorded yet.</div>}
          {alarms.map(a=><div className={"alarm "+a.severity.toLowerCase()+" "+(a.acknowledged?"acked":"")} key={a.id}>
            <div><b>{a.severity}</b><span>{a.source}</span></div>
            <p>{a.message}</p>
            <button disabled={!!a.acknowledged} onClick={()=>acknowledge(a.id)}>{a.acknowledged?"ACKNOWLEDGED":"ACK"}</button>
          </div>)}
        </div>
      </article>
    </section>

    <footer>
      <span>Simulated manufacturing data only · No confidential plant data</span>
      <a href="../">← V1 static demo</a>
    </footer>
  </div>
}
