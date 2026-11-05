
import os
import time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
TOKEN = os.environ.get("INFLUXDB_TOKEN")
ORG = "srs"
BUCKET = "srsran"

if not TOKEN:
    raise SystemExit("INFLUXDB_TOKEN environment variable is missing.")

url = f"{INFLUX_URL}/api/v2/write?{urlencode({'org': ORG, 'bucket': BUCKET})}"

# Generate 20 sets of measurements
for i in range(20):
    dl_bitrate = 12.5 + i * 0.2
    ul_bitrate = 3.1 + i * 0.1
    cqi = 12 + (i % 4)

    data = (
        f"ue_info,pci=1,rnti=0x0042 "
        f"dl_bitrate={dl_bitrate:.1f},"
        f"ul_bitrate={ul_bitrate:.1f},"
        f"dl_bler=0.02,cqi={cqi}i,ul_snr=18.4\n"
        "app_resource_usage "
        "cpu_usage_percent=24.5,"
        "memory_usage_MB=512.0,"
        "power_consumption_Watts=32.5"
    )

    request = Request(
        url,
        data=data.encode("utf-8"),
        headers={
            "Authorization": f"Token {TOKEN}",
            "Content-Type": "text/plain"
        },
        method="POST"
    )

    with urlopen(request, timeout=10) as response:
        print(
            f"Measurement {i + 1}: "
            f"DL={dl_bitrate:.1f}, "
            f"CQI={cqi}, "
            f"HTTP={response.status}"
        )

    time.sleep(2)
