
```
# Custom Fueling Calculator for Bike Rides

def calculate_fueling(weight, duration, intensity, temperature, sweat_rate):
    # Carbohydrate intake based on intensity
    if intensity.lower() == "low":
        carb_per_hour = 30
    elif intensity.lower() == "moderate":
        carb_per_hour = 45
    else:
        carb_per_hour = 60

    # Adjust sodium intake based on temperature and duration
    sodium_per_hour = 400
    if duration > 3 or temperature.lower() == "hot":
        sodium_per_hour = 1260  # High sodium for long or humid conditions

    # Adjust fluid intake based on sweat rate
    if sweat_rate.lower() == "low":
        fluid_per_hour = 500
    elif sweat_rate.lower() == "moderate":
        fluid_per_hour = 600
    else:
        fluid_per_hour = 700

    total_carb = carb_per_hour * duration
    total_sodium = sodium_per_hour * duration
    total_fluid = fluid_per_hour * duration

    result = f"""
    Fueling Plan for Your Ride:
    - Duration: {duration} hours
    - Intensity: {intensity.capitalize()}
    - Temperature: {temperature.capitalize()}
    - Sweat Rate: {sweat_rate.capitalize()}

    Per Hour:
    - Carbohydrates: {carb_per_hour} g
    - Sodium: {sodium_per_hour} mg
    - Fluids: {fluid_per_hour} ml

    Total for Ride:
    - Carbohydrates: {total_carb} g
    - Sodium: {total_sodium} mg
    - Fluids: {total_fluid} ml
    """
    return result

# Input parameters
weight = float(input("Enter your weight in kg: "))
duration = int(input("Enter ride duration in hours: "))
intensity = input("Enter intensity (Low, Moderate, High): ")
temperature = input("Enter temperature condition (Cool, Moderate, Hot): ")
sweat_rate = input("Enter sweat rate (Low, Moderate, High): ")

# Calculate fueling needs
fueling_plan = calculate_fueling(weight, duration, intensity, temperature, sweat_rate)

# Display the fueling plan
print(fueling_plan)

```
