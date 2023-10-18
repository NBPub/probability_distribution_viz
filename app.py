from dash import Dash, html, dcc, callback, Output, Input, ALL, ctx
from distributions import distribution_parameters, distribution_graph
import plotly.graph_objects as go


"""Load in Distributions from Scipy"""
from scipy import stats
distribution_names = {}

# continuous distributions  
distribution_names['continuous'] = {
    name:obj for name, obj in stats.__dict__.items() 
    if isinstance(obj, stats.rv_continuous)
                           }
# discrete distributions
distribution_names['discrete'] = {
    name:obj for name, obj in stats.__dict__.items() 
    if isinstance(obj, stats.rv_discrete)
                           }
del stats


"""Dash Application, Page Layout"""
app = Dash(__name__,  title="Probability Distributions")

app.layout = html.Div([ 

    # title
    html.H1('SciPy Probability Distributions'),
    dcc.Link(html.Img(src="https://www.svgrepo.com/show/449764/github.svg",
                      title="Source code",
                      style={'height':'30px','width':'auto'}),
             href="https://github.com/NBPub/probability_distribution_viz",
             id="source-code-link"),
    
    # Dropdown Selections
    html.Div([       
        dcc.Dropdown(list(distribution_names['continuous'].keys()), 
                     id={'type':'distribution-dropdown','index':'continuous'}, 
                     placeholder="Continuous Distributions",
                     ),
        dcc.Dropdown(list(distribution_names['discrete'].keys()), 
                     id={'type':'distribution-dropdown','index':'discrete'},  
                     placeholder="Discrete Distributions")
    ], style={'display':'flex', 'flex-direction':'row',}),        
       
    # Distribution Header
    html.Div(children=[
        html.H2(id="distribution_header"),
    ], style={}),
    
    # Distribution Parameter Sliders, Input Boxes
    html.Div(id="distribution_parameters",
             style={}),
    
    # Graphs, histogram and violin
    html.Div([
        html.Div([
            dcc.Graph(figure={},id='graph_content'),
            dcc.Graph(figure={},id='graph_content_violin'),                
                 ], className="graph-div"),
             ]),
    
    # Distribution Description
    html.Div(id="distribution_info", style={}),    
    
    # Footer
    html.Br(),
                    ])

# Dynamic Page Updates
"""Distribution Header, Description, and Parameter Inputs, update with dropdown"""
@callback(
    Output('distribution_header', 'children'), # name, bounds
    Output('distribution_info', 'children'), # description from scipy docs and link
    Output('distribution_parameters', 'children'), # parameter inputs for graphs
    Input({'type':'distribution-dropdown', 'index':ALL}, "value"), # distribution choice
)
def chosen_distribution(distribution): # add colorby later
    if not distribution or not ctx.triggered_id:
        return '','',[]

    if ctx.triggered_id.index == 'continuous':
        distribution = distribution[0]
        d = distribution_names['continuous'][distribution]
    elif ctx.triggered_id.index == 'discrete':
        distribution = distribution[1]
        d = distribution_names['discrete'][distribution]
    
    return distribution_parameters(d,distribution, ctx.triggered_id.index)


"""Parameter Input Values, set initial value to slider defaults"""
@callback(
    Output({'type':'parameter-input', 'index':ALL}, "value"), # parameter input boxes
    Input({'type':'parameter-slider', 'index':ALL}, "value"), # parameter sliders (defaults)
)
def sliders_to_inputs(values):
    return values


"""
Distribution Graph, updated with either sliders or inputs
    not figured out fully, but it works well enough for me
    enable debug mode full report: circular callback and graph updates twice
    bug is feature: fun to see two resulting distributions in succession
"""
# Graph, via sliders
@callback(
    Output('graph_content', 'figure', allow_duplicate=True), # histogram
    Output('graph_content_violin', 'figure', allow_duplicate=True), # violin
    Input({'type':'distribution-dropdown', 'index':ALL}, "value"), # distribution choice
    Input({'type':'parameter-slider', 'index':ALL}, "value"), # parameter sliders
    prevent_initial_call=True
)
def slider_graph(distribution, parameters):
    if not distribution or not parameters or not ctx.triggered_id:
        return go.Figure(), go.Figure()
    
    trigger = ctx.triggered_id.index.split('_')[0]
    if  trigger == 'continuous':
        distribution = distribution[0]
        d = distribution_names['continuous'][distribution]
    elif trigger == 'discrete':
        distribution = distribution[1]
        d = distribution_names['discrete'][distribution]
           
    fig, fig2 = distribution_graph(d, distribution, parameters) 
    return fig, fig2

# Graph, via inputs
@callback(
    Output('graph_content', 'figure'), # histogram
    Output('graph_content_violin', 'figure'), # violin
    Output({'type':'parameter-slider', 'index':ALL}, "value"), # update sliders with input values
    Input({'type':'distribution-dropdown', 'index':ALL}, "value"), # distribution choice
    Input({'type':'parameter-input', 'index':ALL}, "value"), # parameter inputs
)
def input_graph(distribution, parameters):
    if not distribution or not parameters or not ctx.triggered_id:
        return go.Figure().update_layout({
            'paper_bgcolor':'black', 'font.color':'honeydew',
            'title':'Choose a Probability Distribution above'
                                        }), \
               go.Figure().update_layout({'paper_bgcolor':'black'}), \
               []

    trigger = ctx.triggered_id.index.split('_')[0]
    if  trigger == 'continuous':
        distribution = distribution[0]
        d = distribution_names['continuous'][distribution]
    elif trigger == 'discrete':
        distribution = distribution[1]
        d = distribution_names['discrete'][distribution]
           
    fig, fig2 = distribution_graph(d, distribution, parameters) 
    return fig, fig2, parameters


"""Deploy application, not needed with WSGI. Note DEBUG setting!"""
if __name__ == '__main__':
    app.run_server(debug=True)