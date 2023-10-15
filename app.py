from dash import Dash, html, dcc, callback, Output, Input, ALL, ctx
from distributions import distribution_parameters, distribution_graph
import plotly.graph_objects as go


"""Load in Distributions from Scipy"""
# continuous distributions
from scipy.stats import \
    alpha, beta, cauchy, chi, chi2, cosine, crystalball, expon, exponnorm,\
    f, fisk, gamma, laplace, levy, logistic, lognorm, loguniform, maxwell,\
    mielke, moyal, nakagami, norm, pareto, powerlaw, rayleigh, rice,\
    semicircular, t, trapezoid, weibull_min, weibull_max, uniform
    
continuous_distributions = [
    alpha, beta, cauchy, chi, chi2, cosine, crystalball, expon, exponnorm,\
    f, fisk, gamma, laplace, levy, logistic, lognorm, loguniform, maxwell,\
    mielke, moyal, nakagami, norm, pareto, powerlaw, rayleigh, rice,\
    semicircular, t, trapezoid, weibull_min, weibull_max, uniform
                           ]
# discrete distributions
from scipy.stats import \
    bernoulli, binom, betabinom, nbinom, boltzmann, geom, hypergeom, logser,\
    nchypergeom_fisher, nchypergeom_wallenius, nhypergeom, planck, poisson,\
    skellam, yulesimon, zipf, zipfian, randint
    
discrete_distributions = [
    bernoulli, binom, betabinom, nbinom, boltzmann, geom, hypergeom, logser,
    nchypergeom_fisher, nchypergeom_wallenius, nhypergeom, planck, poisson,
    skellam, yulesimon, zipf, zipfian, randint    
                          ]
distribution_names = {}
distribution_names['continuous'] = {d.name:d for d in continuous_distributions}
distribution_names['discrete'] = {d.name:d for d in discrete_distributions}
del continuous_distributions, discrete_distributions

"""Dash Application, Page Layout"""
app = Dash(__name__,  title="probability distributions")

app.layout = html.Div([ 

    # title
    html.H1('Scipy Distributions'),
    dcc.Link(html.Img(src="https://www.svgrepo.com/show/449764/github.svg",
                      title="Source code",
                      style={'height':'30px','width':'auto'}),
             href="https://github.com/nbpub/",id="source-code-link"),
    
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
    if not distribution:
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
    if not distribution or not parameters:
        return go.Figure(), go.Figure(), []
    
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
    if not distribution or not parameters:
        return go.Figure(), go.Figure(), []

    trigger = ctx.triggered_id.index.split('_')[0]
    if  trigger == 'continuous':
        distribution = distribution[0]
        d = distribution_names['continuous'][distribution]
    elif trigger == 'discrete':
        distribution = distribution[1]
        d = distribution_names['discrete'][distribution]
           
    fig, fig2 = distribution_graph(d, distribution, parameters) 
    return fig, fig2, parameters


"""Deploy application"""
if __name__ == '__main__':
    app.run_server(debug=False)