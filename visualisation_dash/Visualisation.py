import dash
from dash import dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd
import time
import plotly
import dash_table
import datetime as dt
from datetime import datetime
from pyhive import presto

external_stylesheets=['https:/codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally=True

current_refresh_time_temp=None
presto_cur=None
data=pd.DataFrame()
def prestoConnection():
    global presto_cur
    presto_conn = presto.connect(
    host='localhost',
    port=8090,
    catalog='hive',
    schema='default'
    )
    presto_cur = presto_conn.cursor()

def getData():
    global data
    presto_cur.execute('SELECT * FROM default.weather_detail order by currenttime desc limit 60')
    records_list=presto_cur.fetchall()
    data = pd.DataFrame(records_list, columns=['city', 'Temperature', 'Humidity','currentTime','lon','lat'])

prestoConnection()
getData()
print(data.head())

# static data
#decommmente this start
# records_list=[]
# refresh_time_1=time.strftime("%Y-%m-%d %H:%M:%S")
# record_1={"city":"casablanca","Temperature":290,"Humidity":56,"refreshTime":refresh_time_1,"lon":-7.603869,"lat":33.589886}
# records_list.append(record_1)
# record_2={"city":"Fès","Temperature": 312,"Humidity":45,"refreshTime":refresh_time_1,"lon":-5.0033,"lat":34.0433}
# records_list.append(record_2)
# record_3={"city":"rabat","Temperature":322,"Humidity":62,"refreshTime":refresh_time_1,"lon":-6.841650,"lat":34.020882}
# records_list.append(record_3)
# record_4={"city":"mohamedia","Temperature":285,"Humidity":49,"refreshTime":refresh_time_1,"lon":-7.3833,"lat":33.6833}
# records_list.append(record_4)
# record_5={"city":"Tangier","Temperature":313,"Humidity":44,"refreshTime":refresh_time_1,"lon":-5.8039,"lat":35.7767}
# records_list.append(record_5)
# refresh_time_2_temp=datetime.strptime(refresh_time_1,"%Y-%m-%d %H:%M:%S")
# refresh_time_2=(refresh_time_2_temp + dt.timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S")
# record_6={"city":"casablanca","Temperature":312,"Humidity":66,"refreshTime":refresh_time_2,"lon":-7.603869,"lat":33.589886}
# records_list.append(record_6)
# record_7={"city":"Fès","Temperature":314,"Humidity":55,"refreshTime":refresh_time_2,"lon":-5.0033,"lat":34.0433}
# records_list.append(record_7)
# record_8={"city":"rabat","Temperature":332,"Humidity":62,"refreshTime":refresh_time_2,"lon":-6.841650,"lat":34.020882}
# records_list.append(record_8)
# record_9={"city":"mohamedia","Temperature":324,"Humidity":49,"refreshTime":refresh_time_2,"lon":-7.3833,"lat":33.6833}
# records_list.append(record_9)
# record_10={"city":"Tangier","Temperature":315,"Humidity":54,"refreshTime":refresh_time_2,"lon":-5.8039,"lat":35.7767}
# records_list.append(record_10)
# temp_dict={"casablanca":290,"Fès":320,"rabat":110,"mohamedia":340,"Tangier":400}
# humid_dict={"casablanca":10,"Fès":20,"rabat":300,"mohamedia":20,"Tangier":13}
# data=pd.DataFrame(records_list)
#decommmente this end



col_options = data['city'].unique()

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}



PAGE_SIZE = 5

app.layout = html.Div(
    [

        html.Div(children=[
            html.Img(src = r'assets/weather.png',style={"width":"130px","height":"130px"},className="three columns"),
            html.Div([
            html.H2(
                children="Near Real-Time Dashboard for Weather Monitoring",
                style={
                    "textAlign":"center",
                    "color":"#1C5D79",
                    "font-weight":"bold",
                    "font-family":"Verdana"
                }
            ),
            html.Div(
                children="A IDLE PLACE FOR KNOWING YOUR CITY'S WEATHER }",
                style={
                    "textAlign":"center",
                    "color":"#0F9D58",
                    "font-weight":"bold",
                    "fontSize":16,
                    "font-family":"Verdana"
                }
            ),
            html.Br(),
            html.Div(
                id ="current_refresh_time",
                children="Current Refresh Time: ",
                style={
                    "textAlign":"center",
                    "color":"black",
                    "font-weight":"bold",
                    "fontSize":16,
                    "font-family":"Verdana"
                }
            )    
            ],className="nine columns"),
            ],style={
            "backgroundColor":"#BEE1F0",
            "margin":0,
            "padding":"20px",
            "border-radius":"10px",
            "box-shadow": "0px 5px 10px 0px rgba(0, 0, 0, 0.5)"},className="row"),
        
        html.Br(),
        html.Div(
        children=[
        html.Span("Choose The city"),
            # change col_options :
            dcc.Dropdown(id="city",value="",options=col_options,multi=True), ]),
                html.Div(
            [
            dcc.RadioItems(
            id='weather', 
            options=["Temperature", "Humidity"],
            value="Temperature",
            inline=True
            ),
            dcc.Graph(id="graph"),
        ],className="row"),
        html.Div([
        html.Div(
        [
        dcc.Graph(id='live-update-graph-bar')
        ],className="six columns"),

        html.Div([
            html.Br(),

            dash_table.DataTable(
                id="datatable-paging",
                #c
                columns=[{"name": i ,"id" : i} for i in data.columns],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',
                style_header=table_header_style,
            )
        ],className="five columns")
        ],className='row'),

        dcc.Interval(
            id="interval-component",
            interval=60000,
            n_intervals=0
        ),

    ]
)
@app.callback(
    Output("graph", "figure"), 
    [Input("weather", "value"),Input("interval-component","n_intervals")])

def display_choropleth(weather,n):
    dataNew = data
    dataNew['Temperature'] = abs(dataNew['Temperature'])
    fig = px.scatter_geo(dataNew,lat='lat',lon='lon', hover_name="city",color=weather,size=weather)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


@app.callback(
    Output("current_refresh_time","children"),
    [Input("interval-component","n_intervals")]
)
def update_layout(n):
    global col_options
    getData()
    col_options = data['city'].unique()
    print(data.head())
    print(col_options)
    print("n",n)
    global current_refresh_time_temp
    current_refresh_time_temp=time.strftime("%Y-%m-%d %H:%M:%S")
    return "Current Refresh Time : {}".format(current_refresh_time_temp)

@app.callback(Output("live-update-graph-bar","figure"),[Input("city","value"),Input("interval-component","n_intervals")])
def cb(city,n):
    traces=list()
    city = city if city else []
    x=""
    y_temp,y_humid=[0],[0]
    if city == [] or city == "": 
        x=data['city'].head(5)
        y_temp=data['Temperature'].head(5)
        y_humid=data['Humidity'].head(5)
    else:
        data_checked_histo=pd.DataFrame(columns=data.columns)
        for item in city:
            result_compare=data.loc[data['city'] == item]
            data_checked_histo=pd.concat([data_checked_histo,result_compare])
        x=city
        y_temp=data_checked_histo.groupby('city')['Temperature'].mean()
        y_humid=data_checked_histo.groupby('city')['Humidity'].mean()
        print(y_temp)


    bar_1=plotly.graph_objs.Bar(
        x=list(x),
        y=list(y_temp),
        name="Temperature",
        marker={'color':"red"}
    )
    traces.append(bar_1)
    bar_2=plotly.graph_objs.Bar(
        x=list(x),
        y=list(y_humid),
        name="Humidity",
        marker={'color':"blue"}
        
    )
    traces.append(bar_2)
    layout=plotly.graph_objs.Layout(
    barmode='group',xaxis_tickangle=-45,title_text="City's Temperature and Humudity",
    title_font=dict(
        family="Verdana",
        size=12,
        color="black"
    ),
    )
    return {"data":traces,"layout":layout}

@app.callback(
    Output("datatable-paging","data"),
    [Input('datatable-paging','page_current'),
    Input('datatable-paging','page_size'),
    Input("interval-component","n_intervals"),
    Input("city","value")])
def update_table(page_current,page_size,n,city):
    if city == [] or city== "": 
        return data.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')
    else:
        data_checked=pd.DataFrame(columns=data.columns)
        for item in city:
            result_compare=data.loc[data['city'] == item]
            data_checked=pd.concat([data_checked,result_compare])
        return data_checked.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')
if __name__ == '__main__':
    app.run_server(debug=True,port=5001)