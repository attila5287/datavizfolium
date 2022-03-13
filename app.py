""" flask_example.py

  Required packages:
  - flask
  - folium

  Usage:

  Start the flask server by running:

    $ python flask_example.py

  And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask
import csv
import urllib.request
import json
import requests
import folium
from folium.plugins import TimeSliderChoropleth
from branca.colormap import linear
from datetime import datetime 
from collections import defaultdict
app = Flask(__name__)

@app.route('/usd')
def usd():
  pass
  urlcsv = 'https://gist.githubusercontent.com/attila5287/3e9ca129a6b29b0d91c4fc786434f1cb/raw/b84a2d1b65ee3d01f94f4a2fc0d6fcbb9fe00e91/currency.csv'
# urlcsv = 'https://gist.githubusercontent.com/attila5287/d61f5d3ecab4a9170dc5e78c81dec14d/raw/6956d45832acb3518c2747fd73bd044bd50eb475/usd.csv'

  response = urllib.request.urlopen(urlcsv)
  lines = [ l.decode('utf-8') for l in response.readlines() ]
  cr = csv.reader(lines)
  d = defaultdict(list)
  dates = []
  for row in [r for r in cr][1:]:
      pass
  #     print(row)
      dates.append(row[-3])
      d[row[0]].append(float(row[-2]))
  # print(d['TUR'])

  colors = d
  for country, rates in d.items():
      pass
      cmap = linear.RdPu_09.scale( min(rates), max(rates) )
      colors[country] = [ cmap(rate) for rate in rates ]

  datetimes = [
      str(round(datetime(i, 1, 1, 0).timestamp())) 
      for i in range( int(min(dates)),int(max(dates))  )
  ]

  style_dict = {}
  for state, cols in colors.items():
      pass
      d={}
      for date, col in zip(datetimes, cols):
          pass
          d[date] = {
              'color' : col,
              'opacity' : 0.66,
          }
          style_dict[state] = d

  urljson = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/world_countries.json'
  geo = json.loads(requests.get(urljson).text)

  m = folium.Map(
      [36, -10], 
      tiles="stamentoner", 
      zoom_start=4,
      control_scale=True,
      )

  g = TimeSliderChoropleth(
      geo,
      styledict=style_dict,
      ).add_to(m)
  
  title_html = '''
             <h5 align="center">
             <a href="https://github.com/attila5287/datavizfolium/">
             Internal Comparison for USD vs Exchange  Rate 2001-2021
             </a>
             </h5>
             '''
  m.get_root().html.add_child(folium.Element(title_html))


  return m._repr_html_()

@app.route('/')
def index():
  pass
  urljson = 'https://raw.githubusercontent.com/python-visualization/'\
  +'folium/main/examples/data/us-states.json'  

  urlcsv = 'https://gist.githubusercontent.com/attila5287/ab110dd7ca5dd9d3cdad110af4ef322d'+ \
  '/raw/ce1575f6289219b31f4e86595f2f882d37d63758/stateue.csv'
  response = urllib.request.urlopen(urlcsv)
  lines = [l.decode('utf-8') for l in response.readlines()]
  cr = csv.reader(lines)
  raw = {}
  for row in cr:
      pass
      raw[row[0]] = row[1:]
  raw.pop('State')

  listed = {}
  for state, lst in raw.items():
      pass
      if state == 'D.C.':
          pass
          state_name = 'DistrictofColumbia'
      else:
          pass
          state_name = state.replace(' ', '')
      listed[state_name] = [
          float(n) for n in lst
          ]

  mins= [
      min(v) for k,v in listed.items()
  ]
  maxs= [
      max(v) for k,v in listed.items()
  ]
  minrate = min(mins)    
  maxrate = max(maxs)

  from branca.colormap import linear
  cmap = linear.RdPu_09.scale( minrate, maxrate)
  # cmap

  colors = listed
  for state, rates in listed.items():
      pass
      colors[state] = [
          cmap(rate) for rate in rates
      ]


  dates = [str(round(datetime(2021, i+1, 1, 12).timestamp())) for i in range(len(colors['Colorado']))]

  style_dict = {}
  for state, cols in colors.items():
      pass
      d={}
      for date, col in zip(dates, cols):
          pass
          d[date] = {
              'color' : col,
              'opacity' : 0.66,
          }
          style_dict[state] = d

  geo = json.loads(requests.get(urljson).text)
  for g in geo[ 'features' ]:
    pass
    g['id'] = g['properties']['name'].replace(' ', '')
    g['properties']['name'] = g['properties']['name'].replace(' ', '')
      
  # geo['features'][0]

  m = folium.Map(
      [36, -99], 
      tiles="stamentoner", 
      zoom_start=4,
      control_scale=True,
      )

  g = TimeSliderChoropleth(
      geo,
      styledict=style_dict,
      ).add_to(m)
  #specify the min and max values of your data
  colormap = cmap
  colormap.caption = 'State Unemployment Rate'
  colormap.add_to(m)
  m

  title_html = '''
             <h5 align="center">
             <a href="https://github.com/attila5287/datavizfolium/">
             Interactive Monthly Unemployment Rate 2021
             </a>
             </h5>
             '''
  m.get_root().html.add_child(folium.Element(title_html))

  
  return m._repr_html_()


 
if __name__ == '__main__':
  app.run(debug=True)
