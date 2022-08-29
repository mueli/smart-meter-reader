from .smart_meter import SmartMeter

DATA_DEFINITION = [{
    "id": "energy",
    "name": "Energy consumption meters",
    "attributes": [{
        "id": "imported-total",
        "data_type": "integer",
        "unit": "Wh"
    }, {
        "id": "used-tariff-1",
        "data_type": "integer",
        "unit": "Wh"
    }, {
        "id": "used-tariff-2",
        "data_type": "integer",
        "unit": "Wh"
    }, {
        "id": "delivered-tariff-1",
        "data_type": "integer",
        "unit": "Wh"
    }, {
        "id": "delivered-tariff-2",
        "data_type": "integer",
        "unit": "Wh"
    }]
}, {
    "id": "power",
    "name": "Actual power meters",
    "attributes": [{
        "id": "current-usage",
        "data_type": "integer",
        "unit": "W"
    }, {
        "id": "current-delivery",
        "data_type": "integer",
        "unit": "W"
    }]
}]


class ElectricSmartMeter(SmartMeter):
    def __init__(self):
        super().__init__(DATA_DEFINITION)
