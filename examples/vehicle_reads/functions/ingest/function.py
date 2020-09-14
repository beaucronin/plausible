import plausible as pbl

def handler():
    obj = pbl.function.current_trigger.payload
    vehicle_id = obj["vehicle_id"]
    vehicle_oem = 