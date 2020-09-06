import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable
from termcolor import colored
import yaml


def on_send_success(record_metadata):
    """ Callback on delivey success.
        Parameter record_metadata is a RecordMetadata object:
        https://github.com/dpkp/kafka-python/blob/master/kafka/producer/future.py
    """
    print(colored(f'[KAFKA] PUSHED SUCCESS: {record_metadata}>', 'green'))


def on_send_error(exception):
    """ Callback on delivey failure.
        In a real service, it could be used for instance to publish another event
        to notify the other services of the failure.
    """
    print(colored(f'[KAFKA] PUSHED FAILED: {exception}>', 'red'))


class KafkaNotifier:
    """ Simple Kafka producer.
        Can be configured with the 'conf.yml' configuration file in the same directory.
        The configuration can be extended to support more features:
        https://github.com/dpkp/kafka-python/blob/master/kafka/producer/kafka.py
    """

    def __init__(self):
        self._bootstrap_servers = None
        self._default_topic = None
        self.init_from_configuration()
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[ self._bootstrap_servers],
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                retries=5,
                )
        except NoBrokersAvailable as exception:
            self.producer = None
            print(colored(f'[KAFKA] Could not initialize Kafka producer: {exception}>', 'red'))


    def __str__(self):
        return f'{self.__class__.__name__}({self._bootstrap_servers}, {self._default_topic})'


    def __del__(self):
        if self.producer is not None:
            self.producer.flush()
            self.producer.close()


    def init_from_configuration(self):
        """ Read conf.yml configuration file to setup the producer. """
        kafka_config_file = os.path.join(os.path.dirname(__file__), "conf.yml")
        with open(kafka_config_file) as file:
            conf_dict = yaml.load(file, Loader=yaml.FullLoader)
            try:
                self._bootstrap_servers = conf_dict['bootstrap_servers']
                self._default_topic = conf_dict['topic']
            except KeyError as exception:
                print(exception)

    def send(self, json_payload, topic=None):
        """
        Use _default_topic if no topic is given.
        """
        topic = topic if topic is not None else self._default_topic
        if self.producer is not None and self.producer.bootstrap_connected():
            try:
                self.producer.send(
                    topic=topic,
                    value=json_payload
                    ).add_callback(on_send_success).add_errback(on_send_error)
                print(f'[KAFKA] PUSHED {json_payload} to kafka topic <{topic}>')

            except KafkaTimeoutError as exception:
                print(colored(f"[KAFKA] Caught KafkaTimeoutError exception: {exception}", "red"))
        else:
            print(
                colored(
                    f"""[KAFKA] No push on topic [{topic}] for message:
[{json_payload}]
as NOT connected to bootstrap servers [{self._bootstrap_servers}]""", 'red'))
