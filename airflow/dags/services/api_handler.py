import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging


def fetch_data_chuck(url, chuck_size=1024 * 1024):
    """
    Fetch JSON data from a streaming API in chunks and yield parsed objects.

    Args:
        url (str): The API endpoint.
        chuck_size (int): The size of each chunk to read from the response.

    Yields:
        list: Parsed JSON objects from the response.
    """
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
            status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    response = session.get(url, stream=True)
    response.raise_for_status()

    buffer = ""
    decoder = json.JSONDecoder()

    for chunk in response.iter_content(chunk_size=chuck_size):
        buffer += chunk.decode("utf-8")

        while buffer:
            try:
                data, idx = decoder.raw_decode(buffer)
                buffer = buffer[idx:].strip()
                yield data  # Yield the parsed JSON object
            except json.JSONDecodeError:
                break  # Wait for more data to complete JSON object

    if buffer.strip():  # Handle any remaining data in the buffer
        try:
            data = json.loads(buffer)
            yield data
        except json.JSONDecodeError:
            logging.error("Incomplete or malformed JSON data received in the last chunk.")
