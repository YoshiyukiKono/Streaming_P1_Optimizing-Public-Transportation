"""Defines core consumer functionality"""
import logging

import confluent_kafka
from confluent_kafka import Consumer
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from tornado import gen


logger = logging.getLogger(__name__)


class KafkaConsumer:
    """Defines the base kafka consumer class"""

    def __init__(
        self,
        topic_name_pattern,
        message_handler,
        is_avro=True,
        offset_earliest=False,
        sleep_secs=1.0,
        consume_timeout=0.1,
    ):
        """Creates a consumer object for asynchronous use"""
        self.topic_name_pattern = topic_name_pattern
        self.message_handler = message_handler
        self.sleep_secs = sleep_secs
        self.consume_timeout = consume_timeout
        self.offset_earliest = offset_earliest

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        #self.broker_properties = {
        #    #
        #    # TODO
        #    #
        #    "kafka" : "PLAINTEXT://localhost:9092",
        #    "schema_registry" : "http://localhost:8081"
        #}
        self.broker_properties = {
            "bootstrap.servers": "localhost:9092",
            #"bootstrap.servers": "PLAINTEXT://localhost:9092",
            "group.id": "udacity",
            "auto.offset.reset": "earliest" if offset_earliest else "latest"
        }

        # TODO: Create the Consumer, using the appropriate type.
        if is_avro is True:
            self.broker_properties["schema.registry.url"] = "http://localhost:8081"
            self.consumer = AvroConsumer(self.broker_properties)
            #self.consumer = AvroConsumer(
            #    {
            #        "bootstrap.servers": self.broker_properties["kafka"],
            #        "schema.registry.url": self.broker_properties["schema_registry"],
            #        "group.id": "0",
            #        "auto.offset.reset": "earliest"
            #        self.broker_properties["schema.registry.url"] = "http://localhost:8081"
            #        
            #    }
            #)
            logger.info("__init__ - AvroConsumer was created")
        else:
            self.consumer = Consumer(self.broker_properties)
            #self.consumer = Consumer(
            #    {
            #        "bootstrap.servers": self.broker_properties["kafka"],
            #        "group.id": "0",
            #        "auto.offset.reset": "earliest"
            #    }
            #)
            #pass
            logger.info("__init__ - Consumer was created")

        #
        #
        # TODO: Configure the AvroConsumer and subscribe to the topics. Make sure to think about
        # how the `on_assign` callback should be invoked.
        #
        #
        logger.info("Consumer will subscribe - %s", self.topic_name_pattern)
        self.consumer.subscribe([self.topic_name_pattern], on_assign=self.on_assign)

    def on_assign(self, consumer, partitions):
        """Callback for when topic assignment takes place"""
        # TODO: If the topic is configured to use `offset_earliest` set the partition offset to
        # the beginning or earliest
        #logger.info("on_assign is incomplete - skipping")
        logger.info("on_assign - self.topic_name_pattern: %s", self.topic_name_pattern)
        logger.info("on_assign - partitions: %s", partitions)
        logger.info("on_assign - self.consumer: %s", self.consumer)
        #for partition in partitions:
        #    pass
        #    #
        #    #
        #    # TODO
        #    #
        #    #

        for partition in partitions:
            logger.info("on_assign - partition: %s", partition)
            partition.offset = OFFSET_BEGINNING
    
        logger.info("BEFORE partitions assigned for %s", self.topic_name_pattern)
        consumer.assign(partitions)
        logger.info("AFTER partitions assigned for %s", self.topic_name_pattern)

    async def consume(self):
        """Asynchronously consumes data from kafka topic"""
        while True:
            num_results = 1
            while num_results > 0:
                num_results = self._consume()
            await gen.sleep(self.sleep_secs)

    def _consume(self):
        """Polls for a message. Returns 1 if a message was received, 0 otherwise"""
        #
        #
        # TODO: Poll Kafka for messages. Make sure to handle any errors or exceptions.
        # Additionally, make sure you return 1 when a message is processed, and 0 when no message
        # is retrieved.
        #
        #
        #logger.info("_consume is incomplete - skipping")
        #return 0
        message = self.consumer.poll(1.0)
        if message is None:
            logger.info("no message received by consumer: %s", self.topic_name_pattern)
            #logger.info("no message received by consumer")
            return 0
        elif message.error() is not None:
            logger.info(f"error from consumer {message.error()}")
            return 0
        else:
            logger.info(f"consumed message {message.key()}: {message.value()}")
            self.message_handler(message)
            return 1


    def close(self):
        """Cleans up any open kafka consumers"""
        #
        #
        # TODO: Cleanup the kafka consumer
        #
        #
        self.consumer.close()
