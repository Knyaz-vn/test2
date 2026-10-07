from dataclasses import dataclass
from datetime import datetime
import os,httpx

@dataclass
class Outage:
 start:datetime
 end:datetime

class OutageProvider:
 async def get_outages(self):
  url=os.getenv("OUTAGE_FEED_URL","").strip()
  if not url:return []
  async with httpx.AsyncClient(timeout=10) as c:r=await c.get(url);r.raise_for_status();rows=r.json()
  return [Outage(datetime.fromisoformat(x["start"]),datetime.fromisoformat(x["end"])) for x in rows]
