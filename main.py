import argparse
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import pandas as pd

fastf1.Cache.enable_cache('cache') 

fastf1.plotting.setup_mpl(color_scheme='fastf1')

def driverFastestLapInSessionTelemetry(year, gp, session_type, driverID):
    # Get F1 session(s)
    # def get_session(year, gp, sessions (e.g. 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R')
    # Full Docs: https://docs.fastf1.dev/events.html#session-identifiers
    session = fastf1.get_session(year, gp, session_type)

    # Loads the sessions
    session.load()

    # Gets fastest lap in session Q (Qualifying)
    fast_driver = session.laps.pick_drivers(driverID).pick_fastest()

    # Gets all car data
    driver_car_data = fast_driver.get_car_data()

    # Gets time
    driverTime = driver_car_data['Time']

    # Gets speed
    driverVelocityCar = driver_car_data['Speed']
    
    # Gets driver's info
    driverName = session.get_driver(driverID)

    # Create Plot(s)
    fig, ax = plt.subplots()
    ax.plot(driverTime, driverVelocityCar, label=f"{driverName['Abbreviation']} Fastest Lap")
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed [Km/h]')
    ax.set_title(f"{driverName['FirstName']} {driverName['LastName'].upper()} - Fastest Lap Telemetry")
    ax.legend()
    plt.show()

def F1Data(year, gp, session_type):
    # Get F1 session data
    session = fastf1.get_session(year, gp, session_type)
    
    # Loads the session
    session.load(laps=True, telemetry=True, weather=True)

    # Gets all lap data
    # Check out: https://docs.fastf1.dev/core.html#fastf1.core.Session
    # 1. Get Lap Data
    laps_df = session.laps
    laps_df.to_csv(f'{year}_{gp}_{session_type}_laps.csv', index=False)
    print(f"Lap data saved to {year}_{gp}_{session_type}_laps.csv")

    # 2. Get Weather Data
    weather_df = session.weather
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")
    
    # 3. Get Compound
    weather_df = session.Compound
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")
    
    # 2. Get Weather Data
    weather_df = session.weather
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")
    
    # 2. Get Weather Data
    weather_df = session.weather
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")
    
    # 2. Get Weather Data
    weather_df = session.weather
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")

def main():
    print(
        r"""
        /$$$$$$$  /$$   /$$     /$$$$$$$  /$$            /$$                    
        | $$__  $$|__/  | $$    | $$__  $$|__/           |__/                    
        | $$  \ $$ /$$ /$$$$$$  | $$  \ $$ /$$ /$$    /$$ /$$ /$$$$$$$   /$$$$$$ 
        | $$$$$$$/| $$|_  $$_/  | $$  | $$| $$|  $$  /$$/| $$| $$__  $$ /$$__  $$
        | $$____/ | $$  | $$    | $$  | $$| $$ \  $$/$$/ | $$| $$  \ $$| $$$$$$$$
        | $$      | $$  | $$ /$$| $$  | $$| $$  \  $$$/  | $$| $$  | $$| $$_____/
        | $$      | $$  |  $$$$/| $$$$$$$/| $$   \  $/   | $$| $$  | $$|  $$$$$$$
        |__/      |__/   \___/  |_______/ |__/    \_/    |__/|__/  |__/ \_______/
        """
    )
    print("\nWelcome to PitDivine! (An obvious Work-In-Progress F1 program)")
    
    print("\nWhat is PitDivine?")
    print("\nPitDivine is a program that I (Archaniels) designed for both fans and engineers as an attempt to answer and explore 'What if?' race scenarios, for example: 'What if Ferrari hadn't fucked up Leclerc's race in Monaco 2022?'. This race strategy simulator utilizes real historical race data and basic machine learning models to predict optimal pit stop timing and tire strategy for any driver or circuit.")
    
    print("\nPlease insert the year of the GP, GP name, session, and driver abbreviation!")
    print("Example: 2019, Monza, Q, LEC")
    year, gp, session_type, driverID = input("Enter Year, GP, Session, Driver Abbreviation (comma-separated): ").split(',')
    
    year = int(year.strip())
    gp = gp.strip()
    session_type = session_type.strip()
    driverID = driverID.strip()
    
    driverFastestLapInSessionTelemetry(year, gp, session_type, driverID)

if __name__ == "__main__":
    main()