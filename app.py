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
app = Flask(__name__)


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


  dates = [str(round(datetime(2021, i+1, 1, 0).timestamp())) for i in range(len(colors['Colorado']))]

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
