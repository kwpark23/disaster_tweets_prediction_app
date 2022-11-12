
import pickle

import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from pycaret import *
from pycaret.clustering import *
from pycaret.datasets import *
from pycaret.nlp import *
from pycaret.regression import *

app = Flask(__name__)
CORS(app)

airlines_model = load_model('Final RF Model 14Oct2022')
fifa_model = load_model('Final Kmeans Model CSML Oct2022')
tweet_model = load_model('Final Model 11Nov2022v2')

# parse cluster_list.txt to get all cluster data
cluster_list = []
with open('cluster_list_with_portraits.txt', 'r', encoding='UTF-8') as f:
     for line in f:
          line = line.strip()
          # create a dictionary for each line
          cluster_dict = {}
          # split the line into a list
          line_list = line.split(',')
          cluster_dict['PID'] = line_list[0]
          cluster_dict['name'] = line_list[1]
          cluster_dict['overall'] = line_list[2]
          cluster_dict['age'] = line_list[3]
          cluster_dict['wage_eur'] = line_list[4]
          cluster_dict['value_eur'] = line_list[5]
          cluster_dict['diving'] = line_list[6]
          cluster_dict['handling'] = line_list[7]
          cluster_dict['kicking'] = line_list[8]
          cluster_dict['positioning'] = line_list[9]
          cluster_dict['reflexes'] = line_list[10]
          cluster_dict['speed'] = line_list[11]
          cluster_dict['Cluster'] = line_list[12]
          cluster_dict['portrait'] = line_list[13]

          cluster_list.append(cluster_dict)


@app.route('/results', methods=['POST'])
def results():
    results = request.get_json()
    hour = results['Time']//60
    hourfull = float(results['Time']/60)
    minutes = results['Time'] - (hour * 60)
    lengthhour = float(results['Length']/60)

    input_dict = {'Airline' : results['Airline'], 'Flight' : results['Flight'], 'AirportFrom' : results['AirportFrom'], 'AirportTo' : results['AirportTo'], 'DayOfWeek' : results['DayOfWeek'],  'Time' : results['Time'], 'Length': results['Length'], 'Hour_full': hourfull , 'Hour': hour, 'Minutes': minutes, 'Length_hour': lengthhour}

    data_unseen = pd.DataFrame([input_dict])
    prediction = predict_model(airlines_model, data=data_unseen)
#     print(results)
#     print(results['Airline'])
#     print(results['AirportFrom'])
#     print(results['AirportTo'])
#     print(results['DayOfWeek'])
#     print(results['Time'])
#     print(results['Length'])
#     print(results['Flight'])
#     # return results

#     print(prediction)
#     print(prediction['Label'])
#     print(prediction['Label'][0])

    if prediction['Label'][0] == 1:
         print('The flight will get Delayed')
         return ('The flight will get Delayed')
    elif prediction['Label'][0] == 0:
         print('The flight will not get Delayed')
         return('The flight will not get Delayed')


@app.route('/fifa_results', methods=['POST'])
def fifa_results():
     results = request.get_json()

     input_dict = {
          'Name': 'Prediction',
          'overall': results['overall'],
          'age': results['age'],
          'wage_eur': results['wage'],
          'value_eur': None,
          'diving': results['diving'],
          'handling': results['handling'],
          'kicking': results['kicking'],
          'reflexes': results['reflexes'],
          'speed': results['speed'],
          'positioning': results['positioning']
     }

     data_unseen = pd.DataFrame([input_dict])
     prediction = predict_model(fifa_model, data=data_unseen)

     print(results)
     print(prediction)


     dataset = pd.read_pickle("Final Kmeans Model CSML Oct2022.pkl")

     clusterName = prediction['Cluster'][0]

     # return all elements from cluster_list that have the same cluster name
     cluster_data = [x for x in cluster_list if x['Cluster'] == clusterName]
     return cluster_data


@app.route('/tweet_results', methods=['POST'])
def tweet_results():
     results = request.get_json()

     input_dict = {
          'text': results['text'],
          'keyword': "",
          'location': results['location']
     }
     # parse string looking for hashtags
     # if hashtag found, add to keyword list and remove from text
     if '#' in results['text']:
          for word in results['text'].split():
               if word[0] == '#':
                    # remove word from text
                    input_dict['text'] = input_dict['text'].replace(word, '')
                    word=word[1:]
                    input_dict['keyword'] = input_dict['keyword'] + " " + word

                    
     input_dict['keyword'] = input_dict['keyword'].strip() 
     input_dict['text'] = input_dict['text'].strip()
     
     data_unseen = pd.DataFrame([input_dict])
     predictions = predict_model(estimator=tweet_model, data=data_unseen)
     print(predictions)

     isDisaster = False
     if predictions['Label'][0] == 1:
          isDisaster = True

     return {"tweet": results['text'], "location": results['location'], "isDisaster": isDisaster}
