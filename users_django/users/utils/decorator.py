import functools
from rest_framework import status
from termcolor import colored
from ..kafka.producer import KafkaNotifier


def push_to_kafka_upon_success(func):
    """ Push to KafkaNotifier the context_data attached to the response
        returned by the decorated function if the status is successful.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response is not None and response.status_code is not None:
            if status.is_success(response.status_code):
                KafkaNotifier().send(response.context_data)
            else:
                print(colored(f'No push to Kafka {response.status_code} {response.data}>', 'red'))
        else:
            print(colored(f'No push to Kafka as response is: <{response}>', 'red'))
        return response
    return wrapper
