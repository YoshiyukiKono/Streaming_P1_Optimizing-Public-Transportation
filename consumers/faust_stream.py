"""Defines trends calculations for stations"""
import logging

import faust


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
@dataclass
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
@dataclass
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")

# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic("com.udacity.Station???", value_type=Station)

# TODO: Define the output Kafka Topic
out_topic = app.topic("com.udacity.TransformedStation???", partitions=1)

# TODO: Define a Faust Table
table = app.Table(
    "TransformedStation???",
    default=int???,
    partitions=1,
    changelog_topic=out_topic,
).hopping(
    size=timedelta(minutes=1),
    step=timedelta(seconds=10)
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#

@app.agent(topic)
async def station(station):
    if station.red == True:
        TODO
        TransformedStation[s.station_id].line??? = 'red'
    else if station.blue == True:
        TODO
        TransformedStation[s.station_id].line??? = 'blue'
    else if station.green == True:
        TODO
        TransformedStation[s.station_id].line??? = 'green'
        
    async for s in station.group_by(Station.station_id):
        TransformedStation[s.station_id] += s.number
        print(f"{s.station_id}: {TransformedStation[s.station_id].current()}")

if __name__ == "__main__":
    app.main()
