from datetime import datetime,time,timedelta
import os

class Controller:
 def __init__(self,marstek,outages):self.marstek,self.outages,self.enabled,self.last=marstek,outages,True,{"decision":"starting"}
 def night(self,n):
  a=time.fromisoformat(os.getenv("NIGHT_START","23:00"));b=time.fromisoformat(os.getenv("NIGHT_END","07:00"));return n.time()>=a or n.time()<b
 def desired(self,n,outages):
  if self.night(n):return int(os.getenv("NIGHT_TARGET_SOC","100")),"night_tariff"
  for o in outages:
   if n<=o.start<=n+timedelta(hours=12) and (o.end-o.start).total_seconds()>=int(os.getenv("OUTAGE_THRESHOLD_HOURS","3"))*3600:return int(os.getenv("OUTAGE_TARGET_SOC","80")),f"outage_{(o.end-o.start).total_seconds()/3600:.1f}h"
  return int(os.getenv("DAY_TARGET_SOC","50")),"day"
 async def tick(self):
  n=datetime.now().astimezone()
  if not self.enabled:self.last={"decision":"disabled","at":n.isoformat()};return self.last
  o=await self.outages.get_outages();target,reason=self.desired(n,o)
  self.last={"decision":reason,"target_soc":target,"outages":[{"start":x.start.isoformat(),"end":x.end.isoformat()} for x in o],"at":n.isoformat()}
  return self.last
