import requests
import random
import string
import time


class RequestCollection:
    def __init__(self):
        self.API = "https://gql.tokopedia.com/graphql/"
        self.headers = {
            "Host": "gql.tokopedia.com",
            "Connection": "keep-alive",
            "X-Version": "16cc668",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "accept": "*/*",
            "X-Source": "tokopedia-lite",
            "X-Tkpd-Lite-Service": "test",
            "Origin": "https://tiket.tokopedia.com",
            "Referer": "https://tiket.tokopedia.com/kereta-api/"
        }

    def get_TrainStations(self, keywords):
        if keywords is None:
            return {
                "status": "error",
                "message": "Keywords is required"
            }

        try:

            payload = "[{\"operationName\":\"getTrainStations\",\"variables\":{\"input\":{\"keyword\":\"" + keywords + "\"}},\"query\":\"query getTrainStations($input: TrainStationsRequest) {\\n  trainStations(input: $input) {\\n    data {\\n      label\\n      items {\\n        label\\n        sublabel\\n        code\\n        searchFormLabel\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}]"
            get_train_stations = requests.post(self.API, data=payload, headers=self.headers)
            if len(get_train_stations.json()[0]['data']['trainStations']['data'][0]['items']) == 0:
                return {
                    "status": "error",
                    "message": "No data found"
                }
            else:
                return {
                    "status": "success",
                    "data": get_train_stations.json()[0]['data']['trainStations']['data'][0]['items']
                }

        except ConnectionError:
            return {
                "status": "error",
                "message": "Connection Error"
            }

    def get_ScheduleTrain(self, date, originStation, destinationStation, numPerson):
        if date and originStation and destinationStation and numPerson is None:
            return {
                "status": "error",
                "message": "Keywords is required"
            }

        needRefresh = True
        count_try = 0
        while needRefresh:
            if count_try >= 5:
                return {
                    "status": "error",
                    "message": "Tidak ada jadwal keberangkatan"
                }
            else:
                random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                payload = "[{\"operationName\":\"trainSchedules\",\"variables\":{\"input\":{\"date\":\"" + date + "\",\"originStation\":\"" + originStation + "\",\"destinationStation\":\"" + destinationStation + "\",\"ut\":" + numPerson + ",\"tid\":\"" + random_string + "\"}},\"query\":\"query trainSchedules($input: TrainScheduleRequest) {\\n  trainSchedules(input: $input) {\\n    data {\\n      origin\\n      originName\\n      destination\\n      destinationName\\n      trainNo\\n      trainName\\n      departureDate\\n      departureTime\\n      arrivalDate\\n      arrivalTime\\n      subClass\\n      class\\n      adultFareNumeric\\n      availableSeats\\n      duration\\n      durationDisplay\\n      fareDisplay\\n      classDisplay\\n      departureTimeDisplay\\n      arrivalTimeDisplay\\n      overnightTrip\\n      tripID\\n      scheduleID\\n      __typename\\n    }\\n    meta {\\n      needRefresh\\n      refreshTime\\n      maxRetry\\n      __typename\\n    }\\n    include {\\n      originCityName\\n      DestinationCityName\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}]"
                get_ScheduleTrain = requests.post(self.API, data=payload, headers=self.headers)
                if get_ScheduleTrain.json()[0]['data']['trainSchedules']['meta']['needRefresh'] == True:
                    needRefresh = True
                    time.sleep(1)
                    count_try += 1
                else:
                    if len(get_ScheduleTrain.json()[0]['data']['trainSchedules']['data']) == 0:
                        needRefresh = True
                        time.sleep(1)
                        count_try += 1
                    else:
                        return {
                            "status": "success",
                            "data": get_ScheduleTrain.json()[0]['data']['trainSchedules']['data']
                        }
