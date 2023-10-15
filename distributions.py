import plotly.graph_objects as go
from dash import html, dcc
import numpy as np

def distribution_parameters(d, distribution, dist_type):
    # Distribution Header Text
    name = f"{d.__dict__['name']} | {d.a} to {d.b}"
    longname = d.__dict__['_ctor_param']['longname']
    if longname:
        name = f"{name} | {longname}"
    
    # Distribution Parameter Inputs (textboxes and sliders)
    parameters = {val.name:(val.domain[0],val.domain[1]) \
                  for val in d._param_info()}
    sliders = []
    for key,val in parameters.items():
        # label with parameter bounds
        sliders.append(html.Label(f"{key} [{val[0]}, {val[1]}]"))
        
        # parameter text box, allow entire parameter domain
        sliders.append(
            dcc.Input(type='number', min=val[0], max=val[1], debounce=True, id=
                      {'type':'parameter-input','index':f"{dist_type}_{key}"},
                      ))  
        
        # confine infinity and guess/set defaults for sliders
        if np.inf in np.abs(val):
            low = val[0] if val[0] != -np.inf else -100
            high = val[1] if val[1] != np.inf else 100
            val = (low,high)
        
        if key == 'loc':
            default = 0
        elif key == 'scale':
            default = 1
        else:
            default=np.mean(val)      
        
        # slider element
        sliders.append(
            dcc.Slider(val[0], val[1], value=default, id=
                   {'type':'parameter-slider','index':f"{dist_type}_{key}",},
                       tooltip={'always_visible':True, 'placement':'bottom'},
                       marks={v:str(v) for v in val}))  
    
    # help text at bottom
    sliders.append(html.Em(\
       'vary parameters with sliders or text boxes (full range allowed)', 
                   style={ 'margin':'20px'}))          
    
    # extract scipy docs text, add link because LaTeX rendering is not adapted to HTML
    info_text = d.__dict__['__doc__']
    info_text = info_text[info_text.find('Notes\n    -----\n '):\
                info_text.find('\n\n    Examples\n')][16:]\
                .replace(':math:','').replace('.. math::\n\n','')            
    
    info_link = dcc.Link([
                f"scipy.stats.{distribution}",
                html.Img(
              src="https://docs.scipy.org/doc/scipy/_static/logo.svg",
              title="open scipy docs to see properly formatted LaTeX",
              style={'height':'30px','width':'auto', 'vertical-align':'bottom',
                     'margin-left':'15px'}
                         )
                          ], id="info-link",
                         href=\
f"https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{distribution}.html"
                        )
                        
    return name, [info_link, html.Br(),dcc.Markdown(info_text)], sliders


def distribution_graph(d, distribution, parameters):  
    
    # validate shape parameters, provide indication on empty charts if invalid
    param_names = [val.name for val in d._param_info()]
    arg_check = dict(zip(param_names,parameters))
    arg_check.pop('loc',None)
    arg_check.pop('scale',None)
    arg_check = list(arg_check.values())
    if not d._argcheck(*arg_check):
        return go.Figure().update_layout(
    {'title':f'Invalid shape parameters for {distribution} distribution',
     'font.color':'red', 'paper_bgcolor':'black'}),\
               go.Figure().update_layout(
    {'title':f'Invalid shape parameters for {distribution} distribution',
     'font.color':'red', 'paper_bgcolor':'black'}), 

    # generate array from distribution and parameters
    numbers = d.__call__(*parameters).rvs(5000)
    
    # gather info text for plots
    title_text1 = " ".join([f"| {param_names[i]}:{parameters[i]}" \
                  for i in range(len(parameters))])
    title_text2 = " | ".join(f" {key} {np.quantile(numbers,val).round(2)} "\
                  for key,val in {
               'min':0,'q1':0.25,'median':0.5,'q3':0.75,'max':1
                  }.items())
    
    # Violin Plot for underneath
    fig2 = go.Figure()
    fig2.add_trace(go.Violin(x=numbers, name='', selectedpoints=[], 
                             unselected={'marker.opacity':0}))  
    fig2.update_layout({
        'plot_bgcolor':'black',
        'paper_bgcolor':'black',
        'font.color':'khaki',
        'xaxis.gridcolor':'blueviolet',
        'yaxis.title':f'{distribution}',
        'xaxis.title':'Value',
        'title':f'&#127931; | {title_text2}',
    })
    
    # Histogram on top
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=numbers, 
                  autobinx=True, histnorm='percent',
                  hovertemplate='%{x}<br>%{y}%<extra></extra>'))

    fig.update_layout({
        'title':f"{distribution} distribution histogram {title_text1}",
        'title.font.size':20,
        'plot_bgcolor':'black',
        'paper_bgcolor':'black',
        'font.color':'khaki',
        # y axis
        'yaxis.title':'Percent',
        'yaxis.type':'linear',
        'yaxis.title.font.size':18,
        'yaxis.showgrid':True,
        'yaxis.gridcolor':'blueviolet',
        # x axis
        'xaxis.title':'Value',
        'yaxis.type':'linear',
        'xaxis.title.font.size':18,
        'xaxis.showgrid':True,
        'xaxis.gridcolor':'blueviolet',
    })
    
    return fig, fig2