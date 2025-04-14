# import requests

# url = "http://127.0.0.1:5000/predict"

# payload = {
#     "fish_count": 25000,
#     "history": [
#         {
#             "date": "2025-04-06",
#             "max_temp": 18.5,
#             "min_temp": 7.1,
#             "dec_rain": 2.3,
#             "calmar_rain": 3.1,
#             "spring_temp": 49.7
#         },
#         {
#             "date": "2025-04-07",
#             "max_temp": 19.0,
#             "min_temp": 8.0,
#             "dec_rain": 1.8,
#             "calmar_rain": 2.5,
#             "spring_temp": 49.8
#         },
#         {
#             "date": "2025-04-08",
#             "max_temp": 20.2,
#             "min_temp": 9.1,
#             "dec_rain": 0.5,
#             "calmar_rain": 1.0,
#             "spring_temp": 50.1
#         }
#     ],
#     "forecast": [
#         {
#             "date": "2025-04-09",
#             "max_temp": 21.5,
#             "min_temp": 10.2,
#             "dec_rain": 0.3,
#             "calmar_rain": 0.6,
#             "spring_temp": 0.0
#         },
#         {
#             "date": "2025-04-10",
#             "max_temp": 22.0,
#             "min_temp": 11.0,
#             "dec_rain": 0.4,
#             "calmar_rain": 0.5,
#             "spring_temp": 0.0
#         }
#     ]
# }

# response = requests.post(url, json=payload)

# if response.ok:
#     for row in response.json():
#         print(row)
# else:
#     print("Error:", response.status_code, response.text)
