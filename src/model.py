"""Fields for the backend data."""

from typing import Optional

from meteostat import Point
from requests.exceptions import RequestException


# Location data
LOC_LOAD_EXCEPTION: Optional[RequestException] = None
LOC_FULL_NAME: Optional[str] = None
LOC_SHORT_NAME: Optional[str] = None
LOC_POINT: Optional[Point] = None


# Weather graph config
WGR_N_MONTHS: int = 3
WGR_N_DAYS: int = 3
