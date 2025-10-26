import argparse
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

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
    """
    Gets all relevant data from an F1 session which includes but not limited to stints, sector times, compounds, and tyrelife.
    """
    
    # Get F1 session data
    session = fastf1.get_session(year, gp, session_type)
    session.load(laps=True, telemetry=True, weather=True)

    # 1. Lap Data
    laps_df = session.laps
    laps_df.to_csv(f'{year}_{gp}_{session_type}_laps.csv', index=False)
    print(f"Lap data saved to {year}_{gp}_{session_type}_laps.csv")

    # 2. Weather Data
    weather_df = session.weather_data
    weather_df.to_csv(f'{year}_{gp}_{session_type}_weather.csv', index=False)
    print(f"Weather data saved to {year}_{gp}_{session_type}_weather.csv")

    # 3. Compound Data
    compound_df = laps_df[['Driver', 'LapNumber', 'Compound', 'TyreLife']].dropna()
    compound_df.to_csv(f'{year}_{gp}_{session_type}_compound.csv', index=False)
    print(f"Compound data saved to {year}_{gp}_{session_type}_compound.csv")

    # 4. Track Status Data
    track_status_df = session.track_status
    track_status_df.to_csv(f'{year}_{gp}_{session_type}_track_status.csv', index=False)
    print(f"Track Status data saved to {year}_{gp}_{session_type}_track_status.csv")
    

def dataTraining(year, gp, session_type):
    laps = pd.read_csv(f"{year}_{gp}_{session_type}_laps.csv")
    weather = pd.read_csv(f"{year}_{gp}_{session_type}_weather.csv")
    
    # Merge on time index (optional, or approximate by lap number)
    df = laps.merge(weather, how="left", left_on="LapStartTime", right_on="Time", suffixes=("", "_w"))
    
    # Exclude inlaps and outlaps
    df = df[df['PitOutTime'].isna() & df['PitInTime'].isna()]
    
    # Define features
    features = [
    'LapNumber', 'TyreLife', 'TrackTemp', 'AirTemp', 'Compound', 'Driver'
    ]
    
    target = 'LapTime'
    
    # Encode categorical variables
    df['LapTime'] = df['LapTime'].apply(lambda x: pd.to_timedelta(x).total_seconds())
    le_driver = LabelEncoder()
    le_compound = LabelEncoder()
    df['Driver'] = le_driver.fit_transform(df['Driver'])
    df['Compound'] = le_compound.fit_transform(df['Compound'])

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#def LapTimePrediction():
    # LapTime=f(TyreAge,Compound,FuelLoad,TrackTemp,Driver,Team,Track)
#    

#def TireDegradation():
    

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
    
    print("\n=================================== MENU ===================================")
    print("1. Visualize a driver's fastest lap in a session.")
    print("2. Get all relevant data for an F1 session. (necessary for simulating race scenarios)")
    print("==============================================================================")
    
    value = 0
    match value:
        case 1:
            print("\nPlease insert the year of the GP, GP name, session, and driver abbreviation!")
            print("Example: 2019, Monza, Q, LEC")
            year, gp, session_type, driverID = input("Enter Year, GP, Session, Driver Abbreviation (comma-separated): ").split(',')
            
            year = int(year.strip())
            gp = gp.strip()
            session_type = session_type.strip()
            driverID = driverID.strip()
            
            driverFastestLapInSessionTelemetry(year, gp, session_type, driverID)
        case 2:
            year, gp, session_type, driverID = input("Enter Year, GP, Session (comma-separated): ").split(',')
            
            year = int(year.strip())
            gp = gp.strip()
            session_type = session_type.strip()

            F1Data(year, gp, session_type)
        case 3:
            result = "three"
        case _:
            result = "unknown"

if __name__ == "__main__":
    main()