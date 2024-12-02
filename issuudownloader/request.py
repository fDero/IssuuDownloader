import time
import requests


def _retry_request_until_success_slowing_down_attempt_rate_every_time(do_request):
    wait_time_in_seconds = 0
    while True:
        try:
            wait_time_in_seconds += 1
            request = do_request()
            request.raise_for_status()
            return request
        except:
            time.sleep(wait_time_in_seconds)
            continue


def post_request(url, params=None, **kwargs):
    return _retry_request_until_success_slowing_down_attempt_rate_every_time(
        lambda: requests.post(url, params=params, **kwargs)
    )


def get_request(url, params=None, **kwargs):
    return _retry_request_until_success_slowing_down_attempt_rate_every_time(
        lambda: requests.get(url, params=params, **kwargs)
    )
