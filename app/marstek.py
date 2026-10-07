import asyncio,json,socket

class MarstekClient:
 def __init__(self,host,port=30000,device_id=0): self.host,self.port,self.device_id,self._id=host,port,device_id,0
 async def call(self,method,params=None,timeout=2):
  self._id+=1; data=json.dumps({"id":self._id,"method":method,"params":params or {}},separators=(",",":")).encode()
  return await asyncio.get_running_loop().run_in_executor(None,self._send,data,timeout)
 def _send(self,data,timeout):
  s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.settimeout(timeout)
  try:
   s.sendto(data,(self.host,self.port)); raw,_=s.recvfrom(8192); return json.loads(raw.decode())
  finally: s.close()
 async def status(self): return await self.call("Bat.GetStatus",{"id":self.device_id})
 async def mode(self): return await self.call("ES.GetMode",{"id":self.device_id})
 async def charge(self,power_w,duration_s=3600,dry_run=True):
  if dry_run:return {"dry_run":True,"power_w":power_w,"duration_s":duration_s}
  return await self.call("ES.SetMode",{"id":self.device_id,"config":{"mode":"Passive","passive_cfg":{"power":-abs(power_w),"time":duration_s}}})
