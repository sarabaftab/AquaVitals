# # from flask import Flask, render_template, url_for, request, jsonify
# # from flask_cors import CORS
# # from datetime import datetime, timedelta
# # import pandas as pd
# # import numpy as np
# # import joblib
# # import requests
# # import os

# # os.environ["FLASK_SKIP_DOTENV"] = "1"

# # app = Flask(__name__, 
# #     static_url_path='',
# #     static_folder='static',
# #     template_folder='templates'
# # )
# # CORS(app, resources={r"/predict_api": {"origins": "*"}, r"/process_dates": {"origins": "*"}})

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/predict')
# # def predict_page():
# #     return render_template('predict.html')

# # @app.route('/about')
# # def about():
# #     return render_template('about.html')

# # @app.route('/transparency')
# # def transparency():
# #     return render_template('transparency.html')

# # def generate_time_series_features(df, cols, lags=[3,2,1], rolling_windows=[7]):
# #     df = df.copy()
# #     for col in cols:
# #         for lag in lags:
# #             df[f"{col} (Lag {lag})"] = df[col].shift(lag)
# #         for window in rolling_windows:
# #             df[f"{col} {window}-day avg"] = df[col].rolling(window=window, min_periods=window).mean()
# #     return df

# # def get_weather_data(dec_lat, dec_lon, cal_lat, cal_lon, start_date, end_date, fish_count):
# #     if isinstance(start_date, str):
# #         start_date = datetime.strptime(start_date, '%Y-%m-%d')
# #     if isinstance(end_date, str):
# #         end_date = datetime.strptime(end_date, '%Y-%m-%d')

# #     history_start = start_date - timedelta(days=5)

# #     base_url = "https://api.open-meteo.com/v1/forecast"

# #     dec_params = {
# #         "latitude": dec_lat,
# #         "longitude": dec_lon,
# #         "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
# #         "timezone": "America/Chicago",
# #         "start_date": history_start.strftime('%Y-%m-%d'),
# #         "end_date": end_date.strftime('%Y-%m-%d')
# #     }

# #     cal_params = {
# #         "latitude": cal_lat,
# #         "longitude": cal_lon,
# #         "daily": ["precipitation_sum"],
# #         "timezone": "America/Chicago",
# #         "start_date": history_start.strftime('%Y-%m-%d'),
# #         "end_date": end_date.strftime('%Y-%m-%d')
# #     }

# #     dec_response = requests.get(base_url, params=dec_params)
# #     cal_response = requests.get(base_url, params=cal_params)

# #     if dec_response.status_code == 200 and cal_response.status_code == 200:
# #         dec_data = dec_response.json()
# #         cal_data = cal_response.json()

# #         temps_max = dec_data['daily']['temperature_2m_max']
# #         temps_min = dec_data['daily']['temperature_2m_min']
# #         dec_rains = dec_data['daily']['precipitation_sum']
# #         cal_rains = cal_data['daily']['precipitation_sum']
# #         dates = dec_data['daily']['time']

# #         formatted_data = {
# #             "fish_count": fish_count,
# #             "history": [],
# #             "forecast": []
# #         }

# #         start_date_str = start_date.strftime('%Y-%m-%d')
# #         start_index = dates.index(start_date_str)

# #         for i in range(start_index):
# #             formatted_data["history"].append({
# #                 "date": dates[i],
# #                 "max_temp": round(temps_max[i] * 9/5 + 32),
# #                 "min_temp": round(temps_min[i] * 9/5 + 32),
# #                 "dec_rain": round(dec_rains[i], 1),
# #                 "calmar_rain": round(cal_rains[i], 1),
# #                 "spring_temp": round((temps_max[i] + temps_min[i]) / 2 * 9/5 + 32, 1)
# #             })

# #         for i in range(start_index, len(dates)):
# #             formatted_data["forecast"].append({
# #                 "date": dates[i],
# #                 "max_temp": round(temps_max[i] * 9/5 + 32),
# #                 "min_temp": round(temps_min[i] * 9/5 + 32),
# #                 "dec_rain": round(dec_rains[i], 1),
# #                 "calmar_rain": round(cal_rains[i], 1),
# #                 "spring_temp": round((temps_max[i] + temps_min[i]) / 2 * 9/5 + 32, 1)
# #             })

# #         return formatted_data
# #     else:
# #         return None

# # @app.route('/process_dates', methods=['POST', 'GET'])  # Add GET temporarily for debugging
# # def process_dates():
# #     print(f"📥 Method: {request.method}")
# #     if request.method == "GET":
# #         return "This endpoint requires POST", 405

# #     data = request.json

# #     start_date = data.get('start_date')
# #     end_date = data.get('end_date')
# #     fish_count = data.get('fish_count')

# #     decorah_lat = 43.3017
# #     decorah_lon = -91.7853
# #     calmar_lat = 43.1833
# #     calmar_lon = -91.8666

# #     weather_data = get_weather_data(
# #         decorah_lat,
# #         decorah_lon,
# #         calmar_lat,
# #         calmar_lon,
# #         start_date,
# #         end_date,
# #         fish_count
# #     )

# #     if weather_data:
# #         return jsonify(weather_data)
# #     else:
# #         return jsonify({"error": "Failed to retrieve weather data"}), 500

# # @app.route('/predict_api', methods=["POST"])
# # def predict():
# #     data = request.get_json()

# #     fish_count = data.get("fish_count")
# #     history = data.get("history")
# #     forecast = data.get("forecast")

# #     if not fish_count or not history or not forecast:
# #         return jsonify({"error": "Missing required fields"}), 400

# #     combined = history + forecast
# #     df = pd.DataFrame(combined)

# #     df["Date"] = pd.to_datetime(df["date"])
# #     df["# fish"] = fish_count
# #     df["Season"] = df["Date"].dt.month.apply(lambda m: (
# #         "Winter" if m in [12,1,2] else
# #         "Spring" if m in [3,4,5] else
# #         "Summer" if m in [6,7,8] else "Fall"
# #     ))
# #     df["Spring_Temp x Rain"] = df["spring_temp"] * (df["dec_rain"] + df["calmar_rain"])
# #     df["Max Air Temp x Rain"] = df["max_temp"] * (df["dec_rain"] + df["calmar_rain"])
# #     df["Total Rain"] = df["dec_rain"] + df["calmar_rain"]

# #     df.rename(columns={
# #         "max_temp": "Max air temp",
# #         "min_temp": "Min air temp",
# #         "dec_rain": "Dec Rain",
# #         "calmar_rain": "Calmar Rain",
# #         "spring_temp": "Spring Temp (F)"
# #     }, inplace=True)

# #     df = generate_time_series_features(df, cols=[
# #         "Spring Temp (F)", "Dec Rain", "Calmar Rain"
# #     ], lags=[3,2,1], rolling_windows=[7])

# #     try:
# #         spring_model = joblib.load("../models/spring_temp_model.joblib")
# #         am_model = joblib.load("../models/am_transparency_model.joblib")
# #         pm_model = joblib.load("../models/pm_transparency_model.joblib")
# #         fish_model = joblib.load("../models/fish_survial_model.joblib")
# #     except Exception as e:
# #         return jsonify({"error": f"Failed to load models: {e}"}), 500

# #     results = []

# #     for i in range(len(history), len(df)):
# #         row = df.iloc[i:i+1].copy()

# #         spring_temp = spring_model.predict(row)[0]
# #         row["Spring Temp (F)"] = spring_temp
# #         row["Spring_Temp x Rain"] = spring_temp * (row["Dec Rain"] + row["Calmar Rain"])

# #         am_trans = am_model.predict(row)[0]
# #         pm_trans = pm_model.predict(row)[0]

# #         am_trans = max(0, am_trans)
# #         pm_trans = max(0, pm_trans)

# #         row["AM Transparency"] = am_trans
# #         row["PM Transparency"] = pm_trans

# #         row["AM Transparency (Lag 3)"] = am_trans - 0.5
# #         row["PM Transparency (Lag 3)"] = pm_trans - 0.5
# #         row["AM Transparency 7-day avg"] = am_trans - 0.3
# #         row["PM Transparency 7-day avg"] = pm_trans - 0.3

# #         survival = fish_model.predict(row)[0]

# #         risk = "High" if (
# #             survival < 99.8 or am_trans < 15 or pm_trans < 15 or am_trans < 0 or pm_trans < 0
# #         ) else "Low"

# #         results.append({
# #             "date": str(row["Date"].values[0])[:10],
# #             "predicted_survival": float(round(survival, 4)),
# #             "am_transparency": float(round(am_trans, 2)),
# #             "pm_transparency": float(round(pm_trans, 2)),
# #             "risk_level": risk
# #         })

# #     return jsonify(results)

# # if __name__ == "__main__":
# #     app.run(debug=True)


# from flask import Flask, render_template, url_for, request, jsonify
# from datetime import datetime, timedelta
# import requests

# app = Flask(__name__, 
#     static_url_path='',
#     static_folder='static',
#     template_folder='templates'
# )

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict')
# def predict():
#     return render_template('predict.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/transparency')
# def transparency():
#     return render_template('transparency.html')

# def get_weather_data(dec_lat, dec_lon, cal_lat, cal_lon, start_date, end_date, fish_count):
#     # Convert string dates to datetime objects if they're strings
#     if isinstance(start_date, str):
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#     if isinstance(end_date, str):
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
#     # Calculate 5 days before start_date for historical data
#     history_start = start_date - timedelta(days=5)
    
#     # Base URL for the API
#     base_url = "https://api.open-meteo.com/v1/forecast"
    
#     # Get Decorah data
#     dec_params = {
#         "latitude": dec_lat,
#         "longitude": dec_lon,
#         "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
#         "timezone": "America/Chicago",
#         "start_date": history_start.strftime('%Y-%m-%d'),
#         "end_date": end_date.strftime('%Y-%m-%d')
#     }
    
#     # Get Calmar data
#     cal_params = {
#         "latitude": cal_lat,
#         "longitude": cal_lon,
#         "daily": ["precipitation_sum"],
#         "timezone": "America/Chicago",
#         "start_date": history_start.strftime('%Y-%m-%d'),
#         "end_date": end_date.strftime('%Y-%m-%d')
#     }
    
#     # Make API requests for both locations
#     dec_response = requests.get(base_url, params=dec_params)
#     cal_response = requests.get(base_url, params=cal_params)
    
#     if dec_response.status_code == 200 and cal_response.status_code == 200:
#         dec_data = dec_response.json()
#         cal_data = cal_response.json()
        
#         # Extract the data
#         temps_max = dec_data['daily']['temperature_2m_max']
#         temps_min = dec_data['daily']['temperature_2m_min']
#         dec_rains = dec_data['daily']['precipitation_sum']
#         cal_rains = cal_data['daily']['precipitation_sum']
#         dates = dec_data['daily']['time']
        
#         # Convert to desired format
#         formatted_data = {
#             "fish_count": fish_count,
#             "history": [],
#             "forecast": []
#         }
        
#         # Find index of start_date in dates list
#         start_date_str = start_date.strftime('%Y-%m-%d')
#         start_index = dates.index(start_date_str)
        
#         # Format historical data (5 days before start_date)
#         for i in range(start_index):
#             day_data = {
#                 "date": dates[i],
#                 "max_air_temp": round(temps_max[i] * 9/5 + 32),  # Convert to Fahrenheit
#                 "min_air_temp": round(temps_min[i] * 9/5 + 32),  # Convert to Fahrenheit
#                 "dec_rain": round(dec_rains[i], 1),
#                 "calmar_rain": round(cal_rains[i], 1),
#                 "month": datetime.strptime(dates[i], '%Y-%m-%d').month
#             }
#             formatted_data["history"].append(day_data)
        
#         # Format forecast data (from start_date to end_date)
#         for i in range(start_index, len(dates)):
#             day_data = {
#                 "date": dates[i],
#                 "max_air_temp": round(temps_max[i] * 9/5 + 32),
#                 "min_air_temp": round(temps_min[i] * 9/5 + 32),
#                 "dec_rain": round(dec_rains[i], 1),
#                 "calmar_rain": round(cal_rains[i], 1),
#                 "month": datetime.strptime(dates[i], '%Y-%m-%d').month
#             }
#             formatted_data["forecast"].append(day_data)
        
#         print("\nFormatted Weather Data:")
#         print("=" * 50)
#         import json
#         print(json.dumps(formatted_data, indent=2))
        
#         return formatted_data
#     else:
#         print(f"Error: Unable to fetch data. Decorah status: {dec_response.status_code}, Calmar status: {cal_response.status_code}")
#         return None

# @app.route('/process_dates', methods=['POST'])
# def process_dates():
#     data = request.json
    
#     # Extract data from request
#     start_date = data.get('start_date')
#     end_date = data.get('end_date')
#     fish_count = data.get('fish_count')
#     year_class = data.get('year_class')
    
#     # Calculate date range
#     start = datetime.strptime(start_date, '%Y-%m-%d')
#     end = datetime.strptime(end_date, '%Y-%m-%d')
#     date_range = (end - start).days
    
#     # Coordinates for both locations
#     decorah_lat = 43.3017
#     decorah_lon = -91.7853
#     calmar_lat = 43.1833
#     calmar_lon = -91.8666
    
#     # Get weather data
#     weather_data = get_weather_data(
#         decorah_lat,
#         decorah_lon,
#         calmar_lat,
#         calmar_lon,
#         start_date,
#         end_date,
#         fish_count
#     )
    
#     # Print the original data for verification
#     print(f"""
#     Original Request Data:
#     - Start Date: {start_date}
#     - End Date: {end_date}
#     - Date Range: {date_range} days
#     - Fish Count: {fish_count}
#     - Year Class: {year_class}
#     """)
    
#     return jsonify({
#         'start_date': start_date,
#         'end_date': end_date,
#         'date_range': date_range,
#         'fish_count': fish_count,
#         'year_class': year_class
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5001) 