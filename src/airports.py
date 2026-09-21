# Looks up airport coordinates by code using the airportsdata package.
# Package docs: https://pypi.org/project/airportsdata/

import airportsdata

_AIRPORTS_BY_ICAO = airportsdata.load("ICAO")
_AIRPORTS_BY_IATA = airportsdata.load("IATA")


class AirportNotFoundError(ValueError):
    # Raised when an airport code is invalid or unknown.
    pass


def get_airport_coordinates(code):
    # Return (latitude, longitude) for an ICAO (e.g. "KJFK") or IATA
    # (e.g. "JFK") airport code. Raises AirportNotFoundError if the code
    # is not a string, is empty, or is not a known airport.
    if not isinstance(code, str) or not code.strip():
        raise AirportNotFoundError(
            f"Invalid airport code {code!r}: expected a 3-letter IATA or 4-letter ICAO code."
        )
    key = code.strip().upper()
    airport = _AIRPORTS_BY_ICAO.get(key) or _AIRPORTS_BY_IATA.get(key)
    if airport is None:
        raise AirportNotFoundError(f"Unknown airport code {code!r}: no matching airport found.")
    return airport["lat"], airport["lon"]
