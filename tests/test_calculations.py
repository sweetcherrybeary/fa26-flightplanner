import unittest
 
from src.calculations import (
    calculate_pressure_altitude,
    calculate_density_altitude,
    calculate_rate_of_climb,
    calculate_takeoff_distance,
    calculate_landing_distance,
    calculate_true_air_speed,
)

class TestCalculations(unittest.TestCase):
 
    def test_calculate_pressure_altitude(self):
        altimeter_setting = 30.20
        field_elevation = 1000
        expected_pressure_altitude = 720
        self.assertAlmostEqual(
            calculate_pressure_altitude(altimeter_setting, field_elevation),
            expected_pressure_altitude,
            places=2,
        )
    def test_calculate_pressure_altitude_altimeter_setting_out_of_range(self):
        altimeter_setting = 27.50
        field_elevation = 1000
        with self.assertRaises(ValueError):
            calculate_pressure_altitude(altimeter_setting, field_elevation)
 
    def test_calculate_density_altitude(self):
        temperature = 20
        field_elevation = 10000
        altimeter_setting = 30.20
        expected_density_altitude = 12652.80
        self.assertAlmostEqual(
            calculate_density_altitude(temperature, field_elevation, altimeter_setting),
            expected_density_altitude,
            places=2,
        )
 
    def test_calculate_rate_of_climb(self):
        density_altitude = 12652.80
        expected_rate_of_climb = 153.89
        self.assertAlmostEqual(
            calculate_rate_of_climb(density_altitude),
            expected_rate_of_climb,
            places=2,
        )
 
    def test_calculate_takeoff_distance_ground_run(self):
        density_altitude = 0
        expected = 785.71, 1666.67
        self.assertAlmostEqual(
            calculate_takeoff_distance(density_altitude)[0],
            expected[0],
            places=2,
        )
        self.assertAlmostEqual(
            calculate_takeoff_distance(density_altitude)[1],
            expected[1],
            places=2,
        )
 
    def test_calculate_landing_distance(self):
        density_altitude = 0
        expected = 535.71, 1075.0
        self.assertAlmostEqual(
            calculate_landing_distance(density_altitude)[0],
            expected[0],
            places=2,
        )
        self.assertAlmostEqual(
            calculate_landing_distance(density_altitude)[1],
            expected[1],
            places=2,
        )
 
    def test_calculate_true_air_speed(self):
        density_altitude = 0
        power_setting = 75
        expected = 123.88
        self.assertAlmostEqual(
            calculate_true_air_speed(density_altitude, power_setting),
            expected,
            places=2,
        )
    def test_calculate_true_air_speed_power_setting_out_of_range(self):
        density_altitude = 0
        power_setting = 45
        with self.assertRaises(Exception):
            calculate_true_air_speed(density_altitude, power_setting)
 
if __name__ == "__main__":
    unittest.main()
