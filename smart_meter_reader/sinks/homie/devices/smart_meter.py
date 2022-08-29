from homie.device_base import Device_Base
from homie.node.node_base import Node_Base
from homie.node.property.property_base import Property_Base
from config import settings, mqtt_settings


class SmartMeter(Device_Base):
    """Base class for SmartMeter Homie devices

    Args:
        Device_Base (_type_):
    """
    def __init__(self, data_definition: dict):
        """Create the homie device based on the provided data_definition

        Args:
            data_definition (dict): Dictionary containg the devinition of nodes and
            attributes. See as example dummy_smart_meter.DATA_DEFINITION
        """
        super().__init__(
            device_id=settings.sink.homie.id,
            name=settings.sink.homie.name,
            mqtt_settings=mqtt_settings,
            extensions=[])

        for d_node in data_definition:
            node = Node_Base(self, d_node['id'], d_node['name'], "", True)
            for d_attr in d_node['attributes']:
                node.add_property(Property_Base(
                    node, d_attr['id'], settable=False,
                    retained=True, data_type=d_attr['data_type'], unit=d_attr['unit']
                ))
            self.add_node(node)
        self.start()

    def publish_data(self, data: dict) -> None:
        """Publishing all properties which are contained in the data dict.

        Args:
            data (dict): Dictionary (according to the queue message contract) containing
            the values to be published
        """        
        for node_id, attributes in data.items():
            node = self.get_node(node_id)
            for attr_id in attributes:
                node.get_property(attr_id).value = str(attributes[attr_id])
