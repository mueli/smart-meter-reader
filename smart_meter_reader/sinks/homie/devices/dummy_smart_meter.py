from .smart_meter import SmartMeter

DATA_DEFINITION = [{
    "id": "energy",
    "name": "Energy consumption meters",
    "attributes": [{
        "id": "imported-total",
        "data_type": "integer",
        "unit": "kWh"
    }]
}]


class DummySmartMeter(SmartMeter):
    def __init__(self):
        super().__init__(DATA_DEFINITION)
