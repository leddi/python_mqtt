# install python-influxdb
# or
# git clone https://github.com/influxdata/influxdb-python.git
# take care of dependencies
# python-tz
# python-dateutil
#
from influxdb import InfluxDBClient

INFLUXDB_SERVER = 127.0.0.1
PORT            = 8086
DATABASE        = 'database'


def influxdb_send(sensor = SENSOR, message):
    influxdb_client = InfluxDBClient(INFLUXDB_SERVER, PORT, None, None, DATABASE)
    influxdb_client.switch_database(DATABASE)
    points = [{'measurement': DATABASE,'tags': {'sensor': sensor},'fields': {'value': message}}]
    influxdb_client.write_points(points)
