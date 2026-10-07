import asyncio,os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .marstek import MarstekClient
from .schedule import OutageProvider
from .controller import Controller

m=MarstekClient(os.getenv("MARSTEK_HOST","127.0.0.1"),int(os.getenv("MARSTEK_PORT","30000")),int(os.getenv("MARSTEK_DEVICE_ID","0")))
c=Controller(m,OutageProvider())

async def worker():
 while True:
  try:await c.tick()
  except Exception as e:c.last={"decision":"error","error":str(e)}
  await asyncio.sleep(int(os.getenv("POLL_SECONDS","30")))

@asynccontextmanager
async def lifespan(app):
 t=asyncio.create_task(worker());yield;t.cancel()

app=FastAPI(title="Marstek Energy Controller",lifespan=lifespan)
@app.get("/api/status")
async def status():return {"enabled":c.enabled,"controller":c.last}
@app.post("/api/enable/{value}")
async def enable(value:bool):c.enabled=value;return {"enabled":value}
@app.get("/",response_class=HTMLResponse)
async def home():return """<!doctype html><html lang='uk'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Marstek Energy Controller</title><style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:700px;margin:30px auto;padding:0 18px}button{padding:12px 18px;margin:4px;border:0;border-radius:10px}pre{background:#f3f3f3;padding:15px;border-radius:12px;white-space:pre-wrap}</style><h1>Marstek Energy Controller</h1><p><button onclick='setMode(true)'>Автоматизація ON</button><button onclick='setMode(false)'>OFF</button></p><pre id='s'>Завантаження…</pre><script>async function setMode(v){await fetch('/api/enable/'+v,{method:'POST'});load()}async function load(){let r=await fetch('/api/status');s.textContent=JSON.stringify(await r.json(),null,2)}load();setInterval(load,5000)</script></html>"""
