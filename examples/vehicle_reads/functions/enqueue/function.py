import plausible as pbl
from plausible.keyvalue import Field, Timestamp, MINUTES_AGO

def handler():
    vehicles = pbl.resource.keyvalue_store.vehicles_kv
    results = vehicles.query.lt(Field("last_read"), Timestamp(15, MINUTES_AGO))
    for result in results:
        oem = result["oem"]
        if oem == "subaru":
            pbl.function.output.subaru.emit(result)
        elif oem == "toyota":
            pbl.function.output.toyota.emit(result)
        else:
            pbl.function.error(f"No handler found for OEM {oem}")
