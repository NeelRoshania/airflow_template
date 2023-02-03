import time
from airflow_template import logger

def get_timestamp(eseconds:float) -> str:

    """
        Returns specified timestamp from epoch seconds
        https://docs.python.org/3.9/library/time.html#time.gmtime

    """

    return time.strftime("%Y%M%d %X", time.gmtime(eseconds))

def get_duration(start_time: float, end_time: float) -> float:

    """
        Calculate duration in seconds

        start_time:  time in seconds since the epoch as a floating point number
        end_time:  time in seconds since the epoch as a floating point number

    """
    return f'{end_time-start_time:.2f}s'

def some_func():
    logger.info(f'{get_timestamp(time.time())} - hello airflow!')