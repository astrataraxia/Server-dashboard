import psutil
import platform
import time
import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

psutil.cpu_percent(interval=None)

# --- Pydantic Models ---
class SystemInfo(BaseModel):
    os: str
    hostname: str

class HardwareInfo(BaseModel):
    cpu_model: str
    cpu_cores: int
    total_memory_gb: float
    total_disk_gb: float

class StaticInfoResponse(BaseModel):
    system_info: SystemInfo
    hardware_info: HardwareInfo

class LoadAverage(BaseModel):
    one_min: float
    five_min: float
    fifteen_min: float

class NetworkIO(BaseModel):
    bytes_sent_total: int
    bytes_recv_total: int

class LiveStatusResponse(BaseModel):
    uptime: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_average: LoadAverage
    network_io: NetworkIO

# --- Synchronous Helper Functions ---
def get_cpu_model():
    if platform.system() == "Linux":
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if "model name" in line:
                        return line.split(':', 1)[1].strip()
        except Exception:
            return "Unknown"
    return "Unknown"

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    return str(datetime.timedelta(seconds=int(uptime_seconds)))

def get_static_info_sync():
    """Synchronous function to gather static system info."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return StaticInfoResponse(
        system_info=SystemInfo(
            os=f"{platform.system()} {platform.release()}",
            hostname=platform.node()
        ),
        hardware_info=HardwareInfo(
            cpu_model=get_cpu_model(),
            cpu_cores=psutil.cpu_count() or 0,
            total_memory_gb=round(mem.total / (1024**3), 1),
            total_disk_gb=round(disk.total / (1024**3), 1)
        )
    )

def get_live_status_sync():
    """Synchronous function to gather live system status."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    load_avg = psutil.getloadavg()
    net_io = psutil.net_io_counters()
    return LiveStatusResponse(
        uptime=get_uptime(),
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory_percent=mem.percent,
        disk_percent=disk.percent,
        load_average=LoadAverage(
            one_min=load_avg[0],
            five_min=load_avg[1],
            fifteen_min=load_avg[2]
        ),
        network_io=NetworkIO(
            bytes_sent_total=net_io.bytes_sent,
            bytes_recv_total=net_io.bytes_recv
        )
    )

# --- API Endpoints ---
@app.get("/api/v1/system/info", response_model=StaticInfoResponse)
def get_static_info():
    return get_static_info_sync()

@app.get("/api/v1/system/live", response_model=LiveStatusResponse)
def get_live_status():
    return get_live_status_sync()