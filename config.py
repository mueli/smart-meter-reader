
from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)

mqtt_settings = {
    'MQTT_BROKER': settings.mqtt_broker,
    'MQTT_PORT': settings.mqtt_port
}

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
