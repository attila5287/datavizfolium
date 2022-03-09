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
import requests
import folium
import json

app = Flask(__name__)


@app.route('/')
def index():
  m = folium.Map(
    location=[36, -99], 
    tiles="stamentoner", 
    zoom_start=4,
    control_scale=True,
  )
  
  url = (
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data"
    )
  us_states = f"{url}/us-states.json"
  geo_json_data = json.loads(requests.get(us_states).text)    
    
  folium.GeoJson(geo_json_data).add_to(m)
  
  title_html = '''
             <h5 align="center" style="font-size:20px">
             <a href="https://github.com/attila5287/datavizfolium/">
             time slider coming soon
             </a>
             </h5>
             '''
  m.get_root().html.add_child(folium.Element(title_html))

  
  return m._repr_html_()


if __name__ == '__main__':
  app.run(debug=True)
