# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

#pip install pandas pgeocode # for extracting district based on pincode

import pandas
import pgeocode
import json


class ActionHelloLoc(Action):

    def name(self) -> Text:
        return "action_get_loc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_name = tracker.get_slot("state")

        print("slotname", slot_name)

        dispatcher.utter_message(
            text="So You Live In " + slot_name.title() + " , Here Are Your Location's Corona Stats: \n")

        return []

class Actioncoronastats(Action):

    def name(self) -> Text:
        return "actions_corona_state_stat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        responses = requests.get("https://api.covid19india.org/data.json").json()

        entities = tracker.latest_message['entities']
        print("Now Showing Data For:", entities)
        state = None

        for i in entities:
            if i["entity"] == "state":
                state = i["value"]

        message = "Please Enter Correct State Name !"

        if state == "india":
            state = "Total"
        for data in responses["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Now Showing Cases For --> " + state.title() + " Since Last 24 Hours : "+ "\n" + "Active: " + data[
                    "active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data[
                              "recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n" + "As Per Data On: " + data[
                              "lastupdatedtime"]

        print(message)
        dispatcher.utter_message(message)
        
        return []


class Actioncoronastatspin(Action):

    def name(self) -> Text:
        return "actions_corona_pincode_stat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        responses = requests.get("https://api.covid19india.org/v4/min/data.min.json").json()

        entities = tracker.latest_message['entities']
        print("Now Showing Data For:", entities)
        pincode = None

        for i in entities:
            if i["entity"] == "pincode":
                pincode = i["value"]
        
        nomi = pgeocode.Nominatim('In')
        postal_info = nomi.query_postal_code(pincode)
        state =  postal_info[3]
        district = postal_info[5]
        statecode = {"Andhra Pradesh" :"AP",
          "Arunachal Pradesh" : "AR",
          "Assam" : "AS",
          "Bihar" : "BR",
          "Chhattisgarh": "CT",
          "Goa": "GA",
          "Gujarat" : "GJ",
          "Haryana": "HR",
          "Himachal Pradesh" : "HP",
          "Jammu and Kashmir": "JK",
          "Jharkhand": "JH",
          "Karnataka": "KA",
          "Kerala": "KL",
          "Madhya Pradesh": "MP",
          "Maharashtra": "MH",
          "Manipur": "MN",
          "Meghalaya": "ML",
          "Mizoram": "MZ",
          "Nagaland": "NL",
          "Odisha": "OR",
          "Punjab": "PB",
          "Rajasthan": "RJ",
          "Sikkim": "SK",
          "Tamil Nadu": "TN",
          "Telangana": "TG",
          "Tripura": "TR",
          "Uttar Pradesh": "UP",
          "Uttarakhand": "UT",
          "West Bengal": "WB",
          "Andaman and Nicobar Islands": "AN",
          "Chandigarh": "CH",
          "Dadra and Nagar Haveli": "DN",
          "Daman and Diu": "DD",
          "Lakshadweep": "LD",
          "Delhi": "DL",
          "Pondicherry": "PY"}

          
        def method1(dict, search_age):
            for name, age in dict.items():
                if name == search_age:
                    return age
        
        state1 = method1(statecode, state)
        message = "Please Enter Correct Pincode !"
        

        for data in responses[state1]:
            plot = responses[state1]
            for data in plot['districts']:
                plot1 = plot['districts']
                for data in plot1[district]:
                    plot2 = plot1[district]
                    for data in plot2['total']:
                        plot3 = plot2['total']
                        message =  "Total Stats for your District : " + " \n"+ district +" \n"+ " \n" +"Confirmed: " + str(plot3["confirmed"]) +" \n" + "Recovered: " + str(plot3["recovered"]) + " \n" + "Vaccinated1: " + str(plot3["vaccinated1"]) + " \n" + "Vaccinated2: " + str(plot3["vaccinated2"])
                     
        

        print(message)
        dispatcher.utter_message(message)
        return[]