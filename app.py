# -- coding: utf-8 --
from flask import Flask, render_template
import ipinfo
import os
import socket
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import json
import urllib
import re
import plotvars

reload(sys)  
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.debug=1


@app.route('/plot/')
def draw_plotly():
    #Get hold of the current IP address where the container is running
    url = "http://checkip.dyndns.org"
    request = urllib.urlopen(url).read()

    match = re.findall(ur"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", request)
    ipa=match[0]

    #Mapbox and Plotly stuff
    mapbox_access_token = plotvars.mapbox_access_token
    plotly.tools.set_credentials_file(username=plotvars.plotly_username, api_key=plotvars.plotly_apikey)
    #ipinfo stuff
    access_token = plotvars.ipinfo_access_token
    handler = ipinfo.getHandler(access_token)
    ip_address = ipa.encode('utf-8')
    details = handler.getDetails(ip_address)

 
    latitude = details.latitude
    longitude = details.longitude

    graphs = [
        dict(
            data = [
                go.Scattermapbox(
                lat=[latitude],
                lon=[longitude],
                mode='markers',
                marker=dict(
                size=30,
                color='rgb(250, 105, 15)'
            ),
            text=['Current IP Location'],
                )
            ],

            layout = go.Layout(
                autosize=True,
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=int(round(float(latitude))),
                        lon=int(round(float(longitude)))
                    ),
                    pitch=0,
                    zoom=5
                ),
            )
        )
    ]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Container position' for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plotly.html', ids=ids, graphJSON=graphJSON)

@app.route('/plotip/<ipaddress>')
def draw_ip(ipaddress):
    #Mapbox and Plotly stuff
    mapbox_access_token = plotvars.mapbox_access_token
    plotly.tools.set_credentials_file(username=plotvars.plotly_username, api_key=plotvars.plotly_apikey)
    #ipinfo stuff
    access_token = plotvars.ipinfo_access_token
    handler = ipinfo.getHandler(access_token)
    ip_address = ipaddress.encode('utf-8')
    details = handler.getDetails(ip_address)

 
    latitude = details.latitude
    longitude = details.longitude

    graphs = [
        dict(
            data = [
                go.Scattermapbox(
                lat=[latitude],
                lon=[longitude],
                mode='markers',
                marker=dict(
                size=30,
                color='rgb(250, 105, 15)'
            ),
            text=['Current IP Location'],
                )
            ],

            layout = go.Layout(
                autosize=True,
                hovermode='closest',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=int(round(float(latitude))),
                        lon=int(round(float(longitude)))
                    ),
                    pitch=0,
                    zoom=5
                ),
            )
        )
    ]
    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['Container position' for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plotly.html', ids=ids, graphJSON=graphJSON)


@app.route('/geoinfo/<ipa>')
def geoinfo(ipa):
    access_token = '8686afa12f5a73'
    handler = ipinfo.getHandler(access_token)
    ip_address = ipa.encode('utf-8')
    details = handler.getDetails(ip_address)
    city = details.city.encode('utf-8')

 
    latitude = details.latitude
    longitude = details.longitude
        
    return render_template('geoinfo.html',ip_address=ip_address, city=city.encode('utf-8'), latitude=latitude, longitude=longitude)



@app.route('/ipaddress/')
def ipaddress():
    url = "http://checkip.dyndns.org"
    request = urllib.urlopen(url).read()

    ip_address = re.findall(ur"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", request)
    
    return ip_address[0] 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

