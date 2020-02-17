"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

from confluent_kafka.avro import CachedSchemaRegistryClient

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        #self.broker_properties = {
        #    # TODO
        #    # TODO
        #    # TODO
        #    "kafka" : "PLAINTEXT://localhost:9092",
        #    "schema_registry" : "http://localhost:8081"
        #}
        self.broker_properties = {
            # TODO
            "bootstrap.servers" : "PLAINTEXT://localhost:9092",
            "schema.registry.url" : "http://localhost:8081"
        }

        # If the topic does not already exist, try to create it
        
        logger.debug("producer - init - self.topic_name:", self.topic_name)
        
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        # TODO: Configure the AvroProducer
        # self.producer = AvroProducer(
        # )
        #schema_registry = CachedSchemaRegistryClient({"url": self.broker_properties["schema_registry"]})

        #self.producer = AvroProducer(
        #    {"bootstrap.servers": self.broker_properties["kafka"]#, 
        #     #"schema.registry.url": self.broker_properties["schema_registry"]
        #    },
        #    schema_registry=schema_registry
        #)
        self.producer = AvroProducer(config=self.broker_properties, 
                                     default_key_schema=self.key_schema, 
                                     default_value_schema=self.value_schema
                                    )
        logger.debug("producer - initialized")


    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        # TODO: Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        #
        #
        #logger.info("topic creation kafka integration incomplete - skipping")
        logger.debug("producer - create_topic")
        
        #client = AdminClient({"bootstrap.servers": self.broker_properties["kafka"]})
        client = AdminClient({"bootstrap.servers": self.broker_properties["bootstrap.servers"]})
        
        logger.debug("producer - create_topic - client created")
        
        futures = client.list_topics()
        for topic in futures.topics:
            try:
                logger.debug(f"list_topics:{topic}")
                if topic == self.topic_name:
                    logger.info(f"{self.topic_name} already exist")
                    return
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass
            
        futures = client.create_topics(
            [NewTopic(topic=self.topic_name, num_partitions=self.num_partitions, replication_factor=self.num_replicas)]
        )
        for _, future in futures.items():
            try:
                future.result()
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass
        # https://knowledge.udacity.com/questions/64633
        #if self.producer is not None:
        #    logger.debug("flushing producer...")
        #    self.producer.flush()


    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #
        #logger.info("producer close incomplete - skipping")
        if self.topic_name in Producer.existing_topics:
            Producer.existing_topics.remove(self.topic_name)
            #client = AdminClient({"bootstrap.servers": self.broker_properties["kafka"], 'debug': 'broker,admin' })
            client = AdminClient({"bootstrap.servers": self.broker_properties["bootstrap.servers"], 'debug': 'broker,admin' })
            futures = client.delete_topics(
                [self.topic_name]
            )
            for _, future in futures.items():
                try:                   
                    future.result()
                except Exception as e:
                    pass
            #client.close()
        self.producer.close()

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
