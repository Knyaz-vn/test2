# Marstek Energy Controller

Controller for Marstek Venus E 3.0.

Confirmed device: Venus E 3.0, Control firmware v150, IP 192.168.31.96.

For v150 the safe architecture is UDP Open API for read-only telemetry and Modbus TCP over Ethernet for writes/control. Venus E v3 exposes writable target SoC register 42011 and force mode register 42010. Do not use UDP ES.SetMode for automatic control until a firmware-specific write test is completed; community testing has reported Open API control writes wedging the UDP API on some Venus E v3 builds.

Logic: daytime 50%, night tariff 100%, planned outage >=3h -> 80%. Thresholds are configurable. Global automation ON/OFF. Local operation does not depend on cloud access.

Safety: DRY_RUN=true by default. No control writes should be enabled until Modbus has been verified.

The screenshot shows the station on Wi-Fi. For the safe control path connect Venus E 3.0 to Ethernet/LAN and expose TCP/502.
