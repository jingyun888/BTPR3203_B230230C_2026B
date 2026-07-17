from datetime import datetime

class RiverStation:

    def __init__(self, name: str, state: str, wqi: float):
        self.name = name
        self.state = state
        self.wqi = wqi

    def get_class_label(self) -> str:
        return classify_wqi(self.wqi)

    def display_summary(self):
        label = self.get_class_label()
        print(f"{self.name} | {self.state} | WQI: {self.wqi:.1f} | {label}")

river_stations = {
    'Sungai Klang KL': {'state': 'Selangor', 'wqi': 68.3, 'status': ''},
    'Sungai Muar':     {'state': 'Johor',    'wqi': 54.1, 'status': ''},
    'Sungai Skudai':   {'state': 'Johor',    'wqi': 48.2, 'status': ''},
    'Sungai Pinang':   {'state': 'Penang',   'wqi': 28.5, 'status': ''},
    'Sungai Perak':    {'state': 'Perak',    'wqi': 94.0, 'status': ''}
}

reading_log = []

def classify_wqi(wqi: float) -> str:
    if wqi > 92.7:
        return "Class I (Clean)"
    elif 76.5 < wqi <= 92.7:
        return "Class II (Slightly Polluted)"
    elif 51.9 < wqi <= 76.5:
        return "Class III (Moderately Polluted)"
    elif 31.0 < wqi <= 51.9:
        return "Class IV (Polluted)"
    else:
        return "Class V (Heavily Polluted)"


def update_all_statuses():
    for data in river_stations.values():
        data['status'] = classify_wqi(data['wqi'])


def display_stations_table():
    update_all_statuses()
    print("\n" + "=" * 70)
    print(f"{'Station Name':<20} | {'State':<12} | {'WQI':<6} | {'Status'}")
    print("-" * 70)
    for name, info in river_stations.items():
        print(f"{name:<20} | {info['state']:<12} | {info['wqi']:<6.1f} | {info['status']}")
    print("=" * 70)


def add_or_update_station():
    print("\n--- Add / Update River Station ---")
    name = input("Enter Station Name: ").strip()
    if not name:
        print("Error: Station name cannot be empty.")
        return

    state = input("Enter State: ").strip()
    if not state:
        print("Error: State cannot be empty.")
        return

    try:
        wqi = float(input("Enter WQI Value (0 - 100): "))
        if not (0 <= wqi <= 100):
            print("Error: WQI value must be between 0 and 100.")
            return
    except ValueError:
        print("Error: Invalid numeric input for WQI.")
        return

    if name in river_stations:
        river_stations[name]['wqi'] = wqi
        river_stations[name]['state'] = state
        print(f"\nStation '{name}' updated with new WQI: {wqi:.1f}.")
    else:
        river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
        print(f"\nNew station '{name}' added.")

    update_all_statuses()

def log_monitoring_reading():
    print("\n--- Log Monitoring Reading ---")
    name = input("Enter Station Name: ").strip()

    if name not in river_stations:
        print(f"Error: Station '{name}' not found.")
        return

    try:
        wqi = float(input("Enter WQI Reading (0 - 100): "))
        if not (0 <= wqi <= 100):
            print("Error: WQI value must be between 0 and 100.")
            return
    except ValueError:
        print("Error: Invalid numeric input for WQI.")
        return

    timestamp = datetime.now()
    reading_log.append((timestamp, name, wqi))

    river_stations[name]['wqi'] = wqi
    update_all_statuses()

    print(f"Successfully logged reading for '{name}' at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}.")

    check_alerts()


def check_alerts():
    print("\n--- Alert System Check ---")
    alert_triggered = False
    update_all_statuses()

    for name, info in river_stations.items():
        if info['wqi'] < 51.9:
            print(f"[!] ALERT: {name} in {info['state']} is {info['status']} (WQI: {info['wqi']:.1f}).")
            alert_triggered = True

    if not alert_triggered:
        print("All monitored rivers are within acceptable quality levels.")


def view_reading_log():
    print("\n--- Monitoring Reading History ---")
    if not reading_log:
        print("No readings have been logged yet.")
        return

    print(f"{'Timestamp':<20} | {'Station Name':<20} | {'WQI Reading'}")
    print("-" * 55)
    for entry in reading_log:
        ts_str = entry[0].strftime('%Y-%m-%d %H:%M:%S')
        print(f"{ts_str:<20} | {entry[1]:<20} | {entry[2]:.1f}")

def run_trend_analysis():
    print("\n" + "=" * 30 + " TREND ANALYSIS " + "=" * 30)

    print("\n[1] Object-Oriented Class Summary Demonstration:")
    keys = list(river_stations.keys())
    if len(keys) >= 2:
        s1 = RiverStation(keys[0], river_stations[keys[0]]['state'], river_stations[keys[0]]['wqi'])
        s2 = RiverStation(keys[1], river_stations[keys[1]]['state'], river_stations[keys[1]]['wqi'])
        s1.display_summary()
        s2.display_summary()

    print("\n[2] Average WQI by State (Cleanest First):")
    state_wqi = {}
    state_counts = {}

    for info in river_stations.values():
        st = info['state']
        state_wqi[st] = state_wqi.get(st, 0.0) + info['wqi']
        state_counts[st] = state_counts.get(st, 0) + 1

    state_averages = {st: state_wqi[st] / state_counts[st] for st in state_wqi}
    sorted_states = sorted(state_averages.items(), key=lambda x: x[1], reverse=True)

    for st, avg in sorted_states:
        print(f" - {st:<12}: Avg WQI = {avg:.2f} ({classify_wqi(avg)})")

    print("\n[3] Historical Reading Trend Analysis:")
    station_readings = {}
    for entry in reading_log:
        s_name, wqi_val = entry[1], entry[2]
        station_readings.setdefault(s_name, []).append(wqi_val)

    valid_trends = {s: max(vals) - min(vals) for s, vals in station_readings.items() if len(vals) >= 2}

    if not valid_trends:
        print("Insufficient data for trend analysis. Please log more readings.")
    else:
        most_improved = max(valid_trends, key=valid_trends.get)
        least_improved = min(valid_trends, key=valid_trends.get)
        print(f" - Greatest WQI Variance/Improvement : {most_improved} (Δ {valid_trends[most_improved]:.1f})")
        print(f" - Least Improvement / Decline      : {least_improved} (Δ {valid_trends[least_improved]:.1f})")

    print("\n[4] Station Breakdown by WQI Class:")
    update_all_statuses()
    counts = {
        "Class I (Clean)": 0,
        "Class II (Slightly Polluted)": 0,
        "Class III (Moderately Polluted)": 0,
        "Class IV (Polluted)": 0,
        "Class V (Heavily Polluted)": 0
    }

    for info in river_stations.values():
        c_label = info['status']
        if c_label in counts:
            counts[c_label] += 1

    print("-" * 45)
    for c_name, count in counts.items():
        print(f" {c_name:<32} : {count} station(s)")
    print("-" * 45)

def export_report_to_file(filename="river_monitoring_report.txt"):
    update_all_statuses()
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for name, info in river_stations.items():
                file.write(f"{name}, {info['state']}, {info['wqi']}, {info['status']}\n")
        print(f"\nReport successfully exported to '{filename}'.")

    except PermissionError:
        print(f"Error: Permission denied. Cannot write to file '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while saving: {e}")


def load_report_from_file(filename="river_monitoring_report.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            temp_stations = {}
            for line_no, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 3:
                    print(f"Warning: Line {line_no} malformed. Skipping line.")
                    continue

                name, state, wqi_str = parts[0], parts[1], parts[2]
                wqi = float(wqi_str) 

                temp_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}

            river_stations.clear()
            river_stations.update(temp_stations)
            update_all_statuses()
            print(f"\nSuccessfully loaded {len(river_stations)} station(s) from '{filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except ValueError:
        print(f"Error: The file '{filename}' contains non-numeric WQI values.")
    except PermissionError:
        print(f"Error: Permission denied. Cannot read file '{filename}'.")
    except Exception as e:
        print(f"An unexpected error occurred while loading: {e}")

def main():

    update_all_statuses()

    while True:
        print("\n" + "=" * 8 + " Main Menu " + "=" * 8)
        print("1. Classify All Stations")
        print("2. Add / Update Station")
        print("3. Log Monitoring Reading")
        print("4. Trend Analysis")
        print("5. Export Report to File")
        print("6. Load Report from File")
        print("0. Exit")
        print("=" * 27)

        choice = input("Select an option (0-6): ").strip()

        if choice == '1':
            display_stations_table()
        elif choice == '2':
            add_or_update_station()
        elif choice == '3':
            log_monitoring_reading()
        elif choice == '4':
            run_trend_analysis()
        elif choice == '5':
            export_report_to_file()
        elif choice == '6':
            load_report_from_file()
        elif choice == '0':
            print("\nExiting River Quality Monitoring System. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu (0-6).")


if __name__ == "__main__":
    main()