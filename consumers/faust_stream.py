"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")

# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
#station_topic = app.topic("com.udacity.stations.table", value_type=Station)
station_topic = app.topic("com.udacity.stations", value_type=Station)

# TODO: Define the output Kafka Topic
out_topic = app.topic("org.chicago.cta.stations.table.v1", key_type=int, value_type=TransformedStation, partitions=1)

# TODO: Define a Faust Table
station_line_table = app.Table(
    "station_line",
    default=str,
    partitions=1,
    changelog_topic=out_topic,
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#
@app.agent(station_topic)
async def station(stations):
    async for station in stations:
        if station.red == True:
            station_line_table[station.station_id] = 'red'
        elif station.blue == True:
            station_line_table[station.station_id] = 'blue'
        elif station.green == True:
            station_line_table[station.station_id] = 'green'

        transformed_station = TransformedStation(
            station_id = station.station_id,
            station_name = station.station_name,
            order = station.order,
            line = station_line_table[station.station_id]
        )
        logger.info(f"transform - {station.station_id}: {transformed_station}")
        #await out_topic.send(key=station.station_id, value=transformed_station)
        await out_topic.send(value=transformed_station)


if __name__ == "__main__":
    app.main()
