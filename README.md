# Marstek Energy Controller

Local controller for Marstek Venus E 3.0.

Logic: day 50%, night tariff 100%, planned outage >=3h -> 80%. All thresholds are configurable.

Architecture: FastAPI web UI + local UDP Marstek Open API adapter + pluggable outage provider.

First run with DRY_RUN=true. See .env.example.

The official VinnytsiaOblEnergo outage page is the authoritative source for Vinnytsia schedules, but automated access can return HTTP 403, so the provider is deliberately isolated behind an adapter rather than hard-coded scraping.
