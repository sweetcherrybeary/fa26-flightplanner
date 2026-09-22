def calculate_pressure_altitude(altimeter_setting, field_elevation_in_ft):
    """
    Calculate the pressure altitude.

    Parameters:
    altimeter_setting (float): The current altimeter setting in inches of mercury (inHg).
    field_elevation_in_ft (float): The elevation of the airfield in feet.

    Returns:
    float: The pressure altitude in feet.
    """
    if altimeter_setting < 28.00 or altimeter_setting > 31.00:
        raise ValueError("Altimeter setting out of range (28.00-31.00 inHg)")

    return field_elevation_in_ft + (29.92 - altimeter_setting) * 1000

def calculate_density_altitude(temperature_in_c, field_elevation_in_ft, altimeter_setting):
    """
    Calculate the density altitude.

    Parameters:
    temperature_in_c (float): The outside air temperature in degrees Celsius.
    field_elevation_in_ft (float): The elevation of the airfield in feet.
    altimeter_setting (float): The current altimeter setting in inches of mercury (inHg).
    
    Returns:
    float: The density altitude in feet.
    """ 

    sea_base_line = 15
    lapse_rate = 2

    pressure_altitude = calculate_pressure_altitude(altimeter_setting, field_elevation_in_ft)
    ISA_temperature = sea_base_line - (pressure_altitude / 1000) * lapse_rate
    
    return pressure_altitude + (120 * (temperature_in_c - ISA_temperature))

def calculate_rate_of_climb(density_altitude):
    """
    Calculate the rate of climb based on the density altitude from the piper cherokee chart.

    Parameters:
    density_altitude (float): The density altitude in feet.

    Returns:
    float: The rate of climb in feet per minute.
    """
    slope = 25
    y_intercept = 16500
    
    return (y_intercept-density_altitude)/slope

def calculate_true_air_speed(density_altitude, power_setting):
    """
    Calculate the true air speed based on the density altitude and power setting.

    Parameters:
    density_altitude (float): The density altitude in feet.
    power_setting (float): The power setting as a percentage.

    Returns:
    float: The calculated true air speed in miles per hour (mph).
    """
    if power_setting < 50 or power_setting > 75:
        raise Exception("Power setting out of range (50-75)")
    
    y_intercept = 45.653
    mph_per_density_altitude = 0.0008722
    mph_per_percent_power = 1.0430 

    return y_intercept + mph_per_density_altitude * density_altitude + mph_per_percent_power * power_setting

def calculate_landing_distance(density_altitude):
    """
    Calculate the landing distance based on the density altitude and the type of landing.

    Parameters:
    density_altitude (float): The density altitude in feet.

    Returns:
    ground_roll (float): The calculated ground roll distance in feet.
    over_50_feet_obstacle (float): The calculated distance to clear a 50-feet obstacle in feet.
    """

    y_intercept_ground_roll = 37500
    slope_ground_roll = 70
    y_intercept_over_50_feet_obstacle = 43000
    slope_over_50_feet_obstacle = 40

    ground_roll = (density_altitude/slope_ground_roll) + (y_intercept_ground_roll/slope_ground_roll)
    over_50_feet_obstacle = (density_altitude/slope_over_50_feet_obstacle) + (y_intercept_over_50_feet_obstacle/slope_over_50_feet_obstacle)

    return ground_roll, over_50_feet_obstacle

def calculate_takeoff_distance(density_altitude):
    """
    Calculate the takeoff distance based on the density altitude and the type of takeoff.

    Parameters:
    density_altitude (float): The density altitude in feet.

    Returns:
    float or str: The calculated takeoff distance in feet, or an error message if both or neither options are selected.
    """
    slope_ground_run = 14
    y_intercept_ground_run = 11000
    slope_over_50_feet_obstacle = 6
    y_intercept_over_50_feet_obstacle = 10000

    ground_run = (density_altitude/slope_ground_run) + (y_intercept_ground_run/slope_ground_run)
    over_50_feet_obstacle =(density_altitude/slope_over_50_feet_obstacle) + (y_intercept_over_50_feet_obstacle/slope_over_50_feet_obstacle)

    return ground_run, over_50_feet_obstacle
