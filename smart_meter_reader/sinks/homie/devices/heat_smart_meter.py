from .smart_meter import SmartMeter

DATA_DEFINITION = [{
    "id": "energy",
    "name": "Energy consumption meters",
    "attributes": [{
        "id": "imported-total",
        "data_type": "integer",
        "unit": "kWh"
    }]
}, {
    "id": "power",
    "name": "Actual power meters",
    "attributes": [{
        "id": "current-usage",
        "data_type": "integer",
        "unit": "kW"
    }]
}, {
    "id": "temperatures",
    "name": "Temperature meters",
    "attributes": [{
        "id": "temp1",
        "data_type": "integer",
        "unit": "°C"
    }, {
        "id": "temp2",
        "data_type": "integer",
        "unit": "°C"
    }, {
        "id": "temp-diff",
        "data_type": "integer",
        "unit": "K"
    }]
}, {
    "id": "flow",
    "name": "Flow meters",
    "attributes": [{
        "id": "flow",
        "data_type": "integer",
        "unit": "l/h"
    }, {
        "id": "volume",
        "data_type": "integer",
        "unit": "m3"
    }]
}, {
    "id": "ops",
    "name": "Operational parameters",
    "attributes": [{
        "id": "hour-counter",
        "data_type": "integer",
        "unit": "h"
    }]
}]


class HeatSmartMeter(SmartMeter):
    def __init__(self):
        super().__init__(DATA_DEFINITION)
