# Public Transit Status with Apache Kafka

- [Project Rublic](#Rublic)

In this project, you will construct a streaming event pipeline around Apache Kafka and its ecosystem. Using public data from the [Chicago Transit Authority](https://www.transitchicago.com/data/) we will construct an event pipeline around Kafka that allows us to simulate and display the status of train lines in real time.

When the project is complete, you will be able to monitor a website to watch trains move from station to station.

![Final User Interface](images/ui.png)


## Prerequisites

The following are required to complete this project:

* Docker
* Python 3.7
* Access to a computer with a minimum of 16gb+ RAM and a 4-core CPU to execute the simulation

## Description

The Chicago Transit Authority (CTA) has asked us to develop a dashboard displaying system status for its commuters. We have decided to use Kafka and ecosystem tools like REST Proxy and Kafka Connect to accomplish this task.

Our architecture will look like so:

![Project Architecture](images/diagram.png)

### Step 1: Create Kafka Producers
The first step in our plan is to configure the train stations to emit some of the events that we need. The CTA has placed a sensor on each side of every train station that can be programmed to take an action whenever a train arrives at the station.

To accomplish this, you must complete the following tasks:

1. Complete the code in `producers/models/producer.py`
1. Define a `value` schema for the arrival event in `producers/models/schemas/arrival_value.json` with the following attributes
	* `station_id`
	* `train_id`
	* `direction`
	* `line`
	* `train_status`
	* `prev_station_id`
	* `prev_direction`
1. Complete the code in `producers/models/station.py` so that:
	* A topic is created for each station in Kafka to track the arrival events
	* The station emits an `arrival` event to Kafka whenever the `Station.run()` function is called.
	* Ensure that events emitted to kafka are paired with the Avro `key` and `value` schemas
1. Define a `value` schema for the turnstile event in `producers/models/schemas/turnstile_value.json` with the following attributes
	* `station_id`
	* `station_name`
	* `line`
1. Complete the code in `producers/models/turnstile.py` so that:
	* A topic is created for each turnstile for each station in Kafka to track the turnstile events
	* The station emits a `turnstile` event to Kafka whenever the `Turnstile.run()` function is called.
	* Ensure that events emitted to kafka are paired with the Avro `key` and `value` schemas

### Step 2: Configure Kafka REST Proxy Producer
Our partners at the CTA have asked that we also send weather readings into Kafka from their weather hardware. Unfortunately, this hardware is old and we cannot use the Python Client Library due to hardware restrictions. Instead, we are going to use HTTP REST to send the data to Kafka from the hardware using Kafka's REST Proxy.

To accomplish this, you must complete the following tasks:

1. Define a `value` schema for the weather event in `producers/models/schemas/weather_value.json` with the following attributes
	* `temperature`
	* `status`
1. Complete the code in `producers/models/weather.py` so that:
	* A topic is created for weather events
	* The weather model emits `weather` event to Kafka REST Proxy whenever the `Weather.run()` function is called.
		* **NOTE**: When sending HTTP requests to Kafka REST Proxy, be careful to include the correct `Content-Type`. Pay close attention to the [examples in the documentation](https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name)) for more information.
	* Ensure that events emitted to REST Proxy are paired with the Avro `key` and `value` schemas

### Step 3: Configure Kafka Connect
Finally, we need to extract station information from our PostgreSQL database into Kafka. We've decided to use the [Kafka JDBC Source Connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/index.html).

To accomplish this, you must complete the following tasks:

1. Complete the code and configuration in `producers/connectors.py`
	* Please refer to the [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html) for documentation on the options you must complete.
	* You can run this file directly to test your connector, rather than running the entire simulation.
	* Make sure to use the [Landoop Kafka Connect UI](http://localhost:8084) and [Landoop Kafka Topics UI](http://localhost:8085) to check the status and output of the Connector.
	* To delete a misconfigured connector: `CURL -X DELETE localhost:8083/connectors/stations`

### Step 4: Configure the Faust Stream Processor
We will leverage Faust Stream Processing to transform the raw Stations table that we ingested from Kafka Connect. The raw format from the database has more data than we need, and the line color information is not conveniently configured. To remediate this, we're going to ingest data from our Kafka Connect topic, and transform the data.

To accomplish this, you must complete the following tasks:

1. Complete the code and configuration in `consumers/faust_stream.py

#### Watch Out!

You must run this Faust processing application with the following command:

`faust -A faust_stream worker -l info`

### Step 5: Configure the KSQL Table
Next, we will use KSQL to aggregate turnstile data for each of our stations. Recall that when we produced turnstile data, we simply emitted an event, not a count. What would make this data more useful would be to summarize it by station so that downstream applications always have an up-to-date count

To accomplish this, you must complete the following tasks:

1. Complete the queries in `consumers/ksql.py`

#### Tips

* The KSQL CLI is the best place to build your queries. Try `ksql` in your workspace to enter the CLI.
* You can run this file on its own simply by running `python ksql.py`
* Made a mistake in table creation? `DROP TABLE <your_table>`. If the CLI asks you to terminate a running query, you can `TERMINATE <query_name>`


### Step 6: Create Kafka Consumers
With all of the data in Kafka, our final task is to consume the data in the web server that is going to serve the transit status pages to our commuters.

To accomplish this, you must complete the following tasks:

1. Complete the code in `consumers/consumer.py`
1. Complete the code in `consumers/models/line.py`
1. Complete the code in `consumers/models/weather.py`
1. Complete the code in `consumers/models/station.py`

### Documentation
In addition to the course content you have already reviewed, you may find the following examples and documentation helpful in completing this assignment:

* [Confluent Python Client Documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/#)
* [Confluent Python Client Usage and Examples](https://github.com/confluentinc/confluent-kafka-python#usage)
* [REST Proxy API Reference](https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name))
* [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html)

## Directory Layout
The project consists of two main directories, `producers` and `consumers`.

The following directory layout indicates the files that the student is responsible for modifying by adding a `*` indicator. Instructions for what is required are present as comments in each file.

```
* - Indicates that the student must complete the code in this file

├── consumers
│   ├── consumer.py *
│   ├── faust_stream.py *
│   ├── ksql.py *
│   ├── models
│   │   ├── lines.py
│   │   ├── line.py *
│   │   ├── station.py *
│   │   └── weather.py *
│   ├── requirements.txt
│   ├── server.py
│   ├── topic_check.py
│   └── templates
│       └── status.html
└── producers
    ├── connector.py *
    ├── models
    │   ├── line.py
    │   ├── producer.py *
    │   ├── schemas
    │   │   ├── arrival_key.json
    │   │   ├── arrival_value.json *
    │   │   ├── turnstile_key.json
    │   │   ├── turnstile_value.json *
    │   │   ├── weather_key.json
    │   │   └── weather_value.json *
    │   ├── station.py *
    │   ├── train.py
    │   ├── turnstile.py *
    │   ├── turnstile_hardware.py
    │   └── weather.py *
    ├── requirements.txt
    └── simulation.py
```

## Running and Testing

To run the simulation, you must first start up the Kafka ecosystem on their machine utilizing Docker Compose.
```%> docker-compose up```


### Install Docker
```
sudo yum install -y yum-utils   device-mapper-persistent-data   lvm2
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo docker run hello-world
```

### Install docker-compose
```
sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
### Install git and clone the repository
```
sudo yum install -y git
git clone https://github.com/YoshiyukiKono/Streaming_P1_Optimizing-Public-Transportation.git
cd Streaming_P1_Optimizing-Public-Transportation/
```
### Run Docker Compose
```
sudo /usr/local/bin/docker-compose up
```

Docker compose will take a 3-5 minutes to start, depending on your hardware. Please be patient and wait for the docker-compose logs to slow down or stop before beginning the simulation.

Once docker-compose is ready, the following services will be available:

| Service | Host URL | Docker URL | Username | Password |
| --- | --- | --- | --- | --- |
| Public Transit Status | [http://localhost:8888](http://localhost:8888) | n/a | ||
| Landoop Kafka Connect UI | [http://localhost:8084](http://localhost:8084) | http://connect-ui:8084 |
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085) | http://topics-ui:8085 |
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086) | http://schema-registry-ui:8086 |
| Kafka | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094 | PLAINTEXT://kafka0:9092,PLAINTEXT://kafka1:9093,PLAINTEXT://kafka2:9094 |
| REST Proxy | [http://localhost:8082](http://localhost:8082/) | http://rest-proxy:8082/ |
| Schema Registry | [http://localhost:8081](http://localhost:8081/ ) | http://schema-registry:8081/ |
| Kafka Connect | [http://localhost:8083](http://localhost:8083) | http://kafka-connect:8083 |
| KSQL | [http://localhost:8088](http://localhost:8088) | http://ksql:8088 |
| PostgreSQL | `jdbc:postgresql://localhost:5432/cta` | `jdbc:postgresql://postgres:5432/cta` | `cta_admin` | `chicago` |

Note that to access these services from your own machine, you will always use the `Host URL` column.

When configuring services that run within Docker Compose, like **Kafka Connect you must use the Docker URL**. When you configure the JDBC Source Kafka Connector, for example, you will want to use the value from the `Docker URL` column.

### Running the Simulation

There are two pieces to the simulation, the `producer` and `consumer`. As you develop each piece of the code, it is recommended that you only run one piece of the project at a time.

However, when you are ready to verify the end-to-end system prior to submission, it is critical that you open a terminal window for each piece and run them at the same time. **If you do not run both the producer and consumer at the same time you will not be able to successfully complete the project**.

#### Install Python 3.8
https://computingforgeeks.com/how-to-install-python-on-3-on-centos/
```
sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel
gcc --version
sudo yum -y install wget
wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
tar xvf Python-3.7.6.tgz
cd Python-3.7*/
./configure --enable-optimizations
sudo make altinstall
```
https://github.com/confluentinc/confluent-kafka-python/issues/649
```
sudo yum install -y librdkafka-devel python-devel
```
https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
```
sudo /usr/local/bin/pip3.7 install virtualenv
```
When using `virtualenv` in the later section, needed to specify python version with `-p` option when you installed Python(3.7.6) to CentOS7
```
virtualenv -p python3.7 venv
```
When `pip install -r requirements.txt` failed (`confluent-kafka[avro]==1.1.0`) with a newer version of Python(3.8.1) on CentOS7, it was succeeded to install the latest version of each package. 

#### To run the `producer`:

1. `cd producers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python simulation.py`

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

#### To run the Faust Stream Processing Application:
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `faust -A faust_stream worker -l info`


#### To run the KSQL Creation Script:
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python ksql.py`

#### To run the `consumer`:

** NOTE **: Do not run the consumer until you have reached Step 6!
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`

Once the server is running, you may hit `Ctrl+C` at any time to exit.

## Rublic

### Kafka Producer

#### Kafka topics are created with appropriate settings
- Using the Kafka Topics CLI, topics appear for arrivals on each train line in addition to the turnstiles for each of those stations.

First, I interpreted that it was suggested to have multiple topics for the same type, for example, tipic called 'station.<name>', but I eventually consolidated to the topics below, as suggested by my mentor. It sounded reasonable.

```
root@629bbe46784e:~# kafka-topics --zookeeper localhost:2181 --list
...
com.udacity.stations
...
com.udacity.turnstile
...
```

All topics.
```
root@629bbe46784e:~# kafka-topics --zookeeper localhost:2181 --list
TURNSTILE_SUMMARY
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-default__command_topic
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KSTREAM-AGGREGATE-STATE-STORE-0000000004-changelog
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-changelog
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-repartition
_confluent-metrics
_confluent-monitoring
_schemas
com.udacity.stations
com.udacity.streams.clickevents
com.udacity.streams.pages
com.udacity.streams.purchases
com.udacity.streams.users
com.udacity.turnstile
connect-configs
connect-offsets
connect-status
org.chicago.cta.station.arrivals.v1
org.chicago.cta.stations.table.v1
org.chicago.cta.weather.v1
stations-stream-__assignor-__leader
```
#### Kafka messages are produced successfully
- Using the Kafka Topics CLI, messages continuously appear for each station on the train line, for both arrivals and turnstile actions.

```
root@629bbe46784e:~# kafka-topics --zookeeper localhost:2181 --list
TURNSTILE_SUMMARY
__confluent.support.metrics
__consumer_offsets
_confluent-ksql-default__command_topic
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KSTREAM-AGGREGATE-STATE-STORE-0000000004-changelog
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-changelog
_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-repartition
_confluent-metrics
_confluent-monitoring
_schemas
com.udacity.stations
com.udacity.streams.clickevents
com.udacity.streams.pages
com.udacity.streams.purchases
com.udacity.streams.users
com.udacity.turnstile
connect-configs
connect-offsets
connect-status
org.chicago.cta.station.arrivals.v1
org.chicago.cta.stations.table.v1
org.chicago.cta.weather.v1
stations-stream-__assignor-__leader
```

org.chicago.cta.station.arrivals.v1

```
root@629bbe46784e:~# kafka-console-consumer --bootstrap-server localhost:9092 --topic org.chicago.cta.
station.arrivals.v1  --from-beginning

RL009bredin_serviceȆb



GL003a
greenin_service܁a܁
GL005b


^CProcessed a total of 8280 messages
```

com.udacity.turnstile

```
root@629bbe46784e:~# kafka-console-consumer --bootstrap-server localhost:9092 --topic com.udacity.turnstile  --from-beginningԇchicagored
 morgan
green morgan
green
 morgan
...
^CProcessed a total of 33382 messages
```


#### All messages have an associated value schema
- Using the Schema Registry API, a schema is visible for arrivals and turnstile events.

All Subjects

```
root@629bbe46784e:~# curl --silent -X GET http://localhost:8081/subjects/
["com.udacity.turnstile-key","org.chicago.cta.station.arrivals.v1-key","com.udacity.turnstile-value","_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-repartition-value","_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KTABLE-AGGREGATE-STATE-STORE-0000000009-changelog-value","org.chicago.cta.weather.v1-key","org.chicago.cta.weather.v1-value","_confluent-ksql-default_query_CTAS_TURNSTILE_SUMMARY_0-KSTREAM-AGGREGATE-STATE-STORE-0000000004-changelog-value","org.chicago.cta.station.arrivals.v1-value"]
```

arrivals

```
root@764976b2c55a:/home/workspace# curl --silent -X GET http://localhost:8081/subjects/org.chicago.cta.station.arrivals.v1-value/versions/latest
{"subject":"org.chicago.cta.station.arrivals.v1-value","version":1,"id":1,"schema":"{\"type\":\"record\",\"name\":\"value\",\"namespace\":\"arrival\",\"fields\":[{\"name\":\"station_id\",\"type\":\"int\"},{\"name\":\"train_id\",\"type\":\"string\"},{\"name\":\"direction\",\"type\":\"string\"},{\"name\":\"line\",\"type\":\"string\"},{\"name\":\"train_status\",\"type\":\"string\"},{\"name\":\"prev_station_id\",\"type\":[\"null\",\"int\"]},{\"name\":\"prev_direction\",\"type\":[\"null\",\"string\"]}]}"}root@764976b2c55a:/home/workspace# 
```

turnstile

```
root@629bbe46784e:~# curl --silent -X GET http://localhost:8081/subjects/com.udacity.turnstile-value/versions/latest 
{"subject":"com.udacity.turnstile-value","version":1,"id":5,"schema":"{\"type\":\"record\",\"name\":\"value\",\"namespace\":\"turnstile\",\"fields\":[{\"name\":\"station_id\",\"type\":\"int\"},{\"name\":\"station_name\",\"type\":\"string\"},{\"name\":\"line\",\"type\":\"string\"}]}"}root@629bbe46784e:~#
```


### Kafka Consumer
#### Messages are consumed from Kafka
- Stations, status, and weather data appear and update in the Transit Status UI.

**As I succeeded to use neither Docker environment nor workspece for Web UI, I haven't been able to confirm this**

#### Stations data is consumed from the beginning of the topic
- All Blue, Green, and Red Line stations appear in the Transit Status UI.

**As I succeeded to use neither Docker environment nor workspece for Web UI, I haven't been able to confirm this**



### Kafka REST Proxy
#### Kafka REST Proxy successfully delivers messages to the Kafka Topic
- Using the kafka-console-consumer, weather messages are visible in the weather topic and are regularly produced as the simulation runs.


```
root@764976b2c55a:/home/workspace# kafka-topics --zookeeper localhost:2181 --list | grep weather
org.chicago.cta.weather.v1
```

```
root@764976b2c55a:/home/workspace# kafka-console-consumer --bootstrap-server localhost:9092 --topic org.chicago.cta.weather.v1  --from-beginning
"<2B
windy

sunny
...
```

#### Messages produced to the Kafka REST Proxy include a value schema
- Using the Kafka Schema Registry REST API, a schema is defined for the weather topic.

```
root@629bbe46784e:~# curl --silent -X GET http://localhost:8081/subjects/org.chicago.cta.weather.v1-value/versions/latest 
{"subject":"org.chicago.cta.weather.v1-value","version":1,"id":4,"schema":"{\"type\":\"record\",\"name\":\"value\",\"namespace\":\"weather\",\"fields\":[{\"name\":\"temperature\",\"type\":\"float\"},{\"name\":\"status\",\"type\":\"string\"}]}"}root@629bbe46784e:~#
```

### Kafka Connect

#### Kafka Connect successfully loads Station data from Postgres to Kafka
- Using the kafka-console-consumer, all stations defined in Postgres are visible in the stations topic.

```
root@629bbe46784e:~#  kafka-console-consumer --bootstrap-server localhost:9092 --topic com.udacity.stations  --from-beginning
{"stop_id":30001,"direction_id":"E","stop_name":"Austin (O'Hare-bound)","station_name":"Austin","station_descriptive_name":"Austin (Blue Line)","station_id":40010,"order":29,"red":false,"blue":true,"green":false}
{"stop_id":30002,"direction_id":"W","stop_name":"Austin (Forest Pk-bound)","station_name":"Austin","station_descriptive_name":"Austin (Blue Line)","station_id":40010,"order":29,"red":false,"blue":true,"green":false}
...
Loop)","station_name":"Washington/Wabash","station_descriptive_name":"Washington/Wabash (Brown, Green, Orange, Purple & Pink Lines)","station_id":41700,"order":16,"red":false,"blue":false,"green":true}
^CProcessed a total of 230 messages
root@629bbe46784e:~# 
```

*Comment to the first submission*

> I couldn't find any stations in this topic. There should be 230 stations total in this topic.

The above comment was what I didn't expect. As you can see above copy of the console, the topic has exactly 230 messages.
I guess it was because the reviewer didn't wait until the messages were published or my registry was not perfectly synced to my workstation.

I uploaded the whole list that I optained by the following command [here](./docs/com.udacity.stations_output.txt).

```
kafka-console-consumer --bootstrap-server localhost:9092 --topic com.udacity.stations  --from-beginning > com.udacity.stations_output.txt
```

#### Kafka Connect is configured to define a Schema
- Using the Kafka Connect REST API, the Kafka Connect configuration is configured to use JSON for both key and values.

```root@764976b2c55a:/home/workspace# curl --silent -X GET http://localhost:8083/connectors 
["stations"]
root@764976b2c55a:/home/workspace# curl --silent -X GET http://localhost:8083/connectors/stations
{"name":"stations","config":{"connector.class":"io.confluent.connect.jdbc.JdbcSourceConnector","incrementing.column.name":"stop_id","connection.password":"chicago","batch.max.rows":"500","table.whitelist":"stations","mode":"incrementing","key.converter.schemas.enable":"false","topic.prefix":"com.udacity.","connection.user":"cta_admin","poll.interval.ms":"60000","value.converter.schemas.enable":"false","name":"stations","value.converter":"org.apache.kafka.connect.json.JsonConverter","connection.url":"jdbc:postgresql://localhost:5432/cta","key.converter":"org.apache.kafka.connect.json.JsonConverter"},"tasks":[{"connector":"stations","task":0}],"type":"source"}
```

- Using the Schema Registry REST API, the schemas for stations key and value are visible.

```
curl --silent -X GET http://localhost:8081/subjects/org.chicago.cta.station.arrivals.v1-key/versions/latest
{"subject":"org.chicago.cta.station.arrivals.v1-key","version":2,"id":4,"schema":"{\"type\":\"record\",\"name\":\"key\",\"namespace\":\"arrival\",\"fields\":[{\"name\":\"timestamp\",\"type\":\"long\"}]}"}
```

```
root@e32738f9b3fa:/home/workspace# curl --silent -X GET http://localhost:8081/subjects/org.chicago.cta.station.arrivals.v1-value/versions/latest
{"subject":"org.chicago.cta.station.arrivals.v1-value","version":2,"id":3,"schema":"{\"type\":\"record\",\"name\":\"value\",\"namespace\":\"arrival\",\"fields\":[{\"name\":\"station_id\",\"type\":\"int\"},{\"name\":\"train_id\",\"type\":\"string\"},{\"name\":\"direction\",\"type\":\"string\"},{\"name\":\"line\",\"type\":\"string\"},{\"name\":\"train_status\",\"type\":\"string\"},{\"name\":\"prev_station_id\",\"type\":[\"null\",\"int\"]},{\"name\":\"prev_direction\",\"type\":[\"null\",\"string\"]}]}"}
```

#### Kafka Connect is configured to load on an incrementing ID
- Using the Kafka Connect REST API, the Kafka Connect configuration uses an incrementing ID, and the ID is configured to be stop_id.

> "incrementing.column.name":"stop_id"

> "incrementing.column.name":"stop_id"

```
root@764976b2c55a:/home/workspace# curl --silent -X GET http://localhost:8083/connectors/stations
{"name":"stations","config":{"connector.class":"io.confluent.connect.jdbc.JdbcSourceConnector","incrementing.column.name":"stop_id","connection.password":"chicago","batch.max.rows":"500","table.whitelist":"stations","mode":"incrementing","key.converter.schemas.enable":"false","topic.prefix":"com.udacity.","connection.user":"cta_admin","poll.interval.ms":"60000","value.converter.schemas.enable":"false","name":"stations","value.converter":"org.apache.kafka.connect.json.JsonConverter","connection.url":"jdbc:postgresql://localhost:5432/cta","key.converter":"org.apache.kafka.connect.json.JsonConverter"},"tasks":[{"connector":"stations","task":0}],"type":"source"}
```

### Faust Streams
#### The Faust application ingests data from the stations topic
- A consumer group for Faust is created on the Kafka Connect Stations topic.

Refer to `faust_stream.py`

#### Data is translated correctly from the Kafka Connect format to the Faust table format
- Data is ingested in the Station format and is then transformed into the TransformedStation format.

Refer to `faust_stream.py`

#### Transformed Station Data is Present for each Station ID in the Kafka Topic
- A topic is present in Kafka with the output topic name the student supplied. Inspecting messages in the topic, every station ID is represented.

```
root@764976b2c55a:/home/workspace# kafka-console-consumer --bootstrap-server localhost:9092 --topic org.chicago.cta.stations.table.v1 --from-beginning
"blue"
{"station_id": 40010, "station_name": "Austin", "order": 29, "line": "blue", "__faust": {"ns": "faust_stream.TransformedStation"}}
"blue"
{"station_id": 40010, "station_name": "Austin", "order": 29, "line": "blue", "__faust": {"ns": "faust_stream.TransformedStation"}}
"green"
{"station_id": 40020, "station_name": "Harlem/Lake", "order": 0, "line": "green", "__faust": {"ns": "faust_stream.TransformedStation"}}
"green"
{"station_id": 40020, "station_name": "Harlem/Lake", "order": 0, "line": "green", "__faust": {"ns": "faust_stream.TransformedStation"}}
"green"
```

### KSQL
#### Turnstile topic is translated into a KSQL Table
- Using the KSQL CLI, turnstile data is visible in the table TURNSTILE.

```
root@629bbe46784e:~# ksql
                  
                  ===========================================
                  =        _  __ _____  ____  _             =
                  =       | |/ // ____|/ __ \| |            =
                  =       | ' /| (___ | |  | | |            =
                  =       |  <  \___ \| |  | | |            =
                  =       | . \ ____) | |__| | |____        =
                  =       |_|\_\_____/ \___\_\______|       =
                  =                                         =
                  =  Streaming SQL Engine for Apache Kafka® =
                  ===========================================

Copyright 2017-2018 Confluent Inc.

CLI v5.1.3, Server v5.1.3 located at http://localhost:8088

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql> help

Description:
        The KSQL CLI provides a terminal-based interactive shell for running queries. Each command must be on a separate line. For KSQL command syntax, see the documentation at https://github.com/confluentinc/ksql/docs/.
...
```

```
ksql> describe TURNSTILE;

Name                 : TURNSTILE
 Field        | Type                      
------------------------------------------
 ROWTIME      | BIGINT           (system) 
 ROWKEY       | VARCHAR(STRING)  (system) 
 STATION_ID   | INTEGER                   
 STATION_NAME | VARCHAR(STRING)           
 LINE         | VARCHAR(STRING)           
------------------------------------------
```

```
ksql> select * from TURNSTILE;
1583559134277 | �Ǩ�
                    | 40290 | ashland_and_63rd | green
1583559139531 | �˨�
                    | 40510 | garfield | green
^C1583559144819 | �Ш�
                      | 40940 | halsted | green
Query terminated
```

#### Turnstile table is aggregated into a summary table
- Using the KSQL CLI, verify that station IDs have an associated count column.

```
ksql> describe TURNSTILE_SUMMARY;

Name                 : TURNSTILE_SUMMARY
 Field      | Type                      
----------------------------------------
 ROWTIME    | BIGINT           (system) 
 ROWKEY     | VARCHAR(STRING)  (system) 
 STATION_ID | INTEGER                   
 COUNT      | BIGINT                    
----------------------------------------
For runtime statistics and query details run: DESCRIBE EXTENDED <Stream,Table>;

```
