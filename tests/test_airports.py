import pytest

from src.airports import AirportNotFoundError, get_airport_coordinates


# Valid lookups
def test_icao_lookup():
    # KJFK is JFK's 4-letter ICAO code.
    lat, lon = get_airport_coordinates("KJFK")
    assert lat == pytest.approx(40.6398, abs=0.01)
    assert lon == pytest.approx(-73.7789, abs=0.01)


def test_iata_lookup_matches_icao():
    # The 3-letter IATA code should give the same result as the ICAO code.
    assert get_airport_coordinates("JFK") == get_airport_coordinates("KJFK")


def test_western_hemisphere_longitude_is_negative():
    # LAX is in the western hemisphere, so longitude must keep its sign.
    lat, lon = get_airport_coordinates("KLAX")
    assert lat > 0
    assert lon < 0


def test_southern_hemisphere_latitude_is_negative():
    # Sydney (YSSY) is in the southern hemisphere.
    lat, lon = get_airport_coordinates("YSSY")
    assert lat < 0
    assert lon > 0


def test_returns_floats():
    lat, lon = get_airport_coordinates("KJFK")
    assert isinstance(lat, float)
    assert isinstance(lon, float)


def test_ICAO_code_with_digits():
    # Some ICAO codes contain digits (e.g. small US airfields).
    lat, lon = get_airport_coordinates("00AA")
    assert lat == pytest.approx(38.704, abs=0.01)


# Input normalization
@pytest.mark.parametrize("code", ["kjfk", "KjFk", "  KJFK  ", "KJFK\n"])
def test_case_and_whitespace_are_ignored(code):
    assert get_airport_coordinates(code) == get_airport_coordinates("KJFK")


# Errors
@pytest.mark.parametrize(
    "code",
    [
        "ZZZZ",  # right length, but not a real airport
        "ZZZ",  # unknown IATA code
        "JF",  # too short
        "KJFKX",  # too long
        "K JFK",  # space in the middle
        "0000",  # digits only
        "é",  # non-ASCII character
        "US-0001",  # punctuation
    ],
)
def test_unknown_code_raises_clear_error(code):
    with pytest.raises(AirportNotFoundError, match="Unknown airport code"):
        get_airport_coordinates(code)


@pytest.mark.parametrize("bad", ["", "   ", None, 123, ["KJFK"]])
def test_invalid_input_raises_clear_error(bad):
    # Empty, blank, or non-string input is rejected before any lookup.
    with pytest.raises(AirportNotFoundError, match="Invalid airport code"):
        get_airport_coordinates(bad)


def test_error_message_includes_the_bad_code():
    with pytest.raises(AirportNotFoundError, match="ZZZZ"):
        get_airport_coordinates("ZZZZ")


def test_error_is_a_value_error():
    # Callers can catch ValueError without importing our custom error.
    with pytest.raises(ValueError):
        get_airport_coordinates("ZZZZ")
