from . import kamstrup_403
from . import sagemcom_T210_D_r
from . import dummy

from config import settings

read_client_dict = {
    "kamstrup_403": kamstrup_403.read_client,
    "sagemcom_T210_D_r": sagemcom_T210_D_r.read_client,
    "dummy": dummy.read_client
}

read_client = read_client_dict.get(settings.client.id)
