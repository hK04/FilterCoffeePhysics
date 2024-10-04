import matplotlib.pyplot as plt
import numpy as np


import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def plot_brewing_chart():
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax.axline((14, 1.0), (14, 1.6))
    ax.axline((26, 0.5), (26, 2.0))

    ax.axline((8, 1.0), (30, 1.0))
    ax.axline((8, 1.7), (30, 1.7))


    ax.axline((8, 1.20), (30, 1.20), linestyle='--')
    ax.axline((8, 1.45), (30, 1.45), linestyle='--')

    ax.axline((22, 1.0), (22, 1.6), linestyle='--')
    ax.axline((18, 0.5), (18, 2.0), linestyle='--')


    ax.text(22.1, 1.3, 'bitter', fontsize=12)
    ax.text(22.1, 1.5, 'strong\nbitter', fontsize=12)
    ax.text(22.1, 1.05, 'weak\nbitter', fontsize=12)

    ax.text(18.25, 1.5, 'strong', fontsize=12)
    ax.text(18.25, 1.3, 'ideal', fontsize=12)
    ax.text(18.25, 1.05, 'weak', fontsize=12)

    ax.text(14.1, 1.5, 'strong\nunder\ndeveloped', fontsize=12)
    ax.text(14.1, 1.3, 'under\ndeveloped', fontsize=12)
    ax.text(14.1, 1.05, 'weak under\ndeveloped', fontsize=12)

    ax.set_yticks(np.arange(1.0, 1.8, 0.1))
    ax.set_xticks(range(14, 27))

    #ax.scatter(EY[:-2].sum(),  tds(np.array(x2[:-2])).mean(), color='pink')


    #ax.scatter(EY[:-2], tds(np.array(x2[:-2])), color='green')
    #plt.grid()
    return fig, ax

def plotly_extraction_charts(fig):
    fig.add_trace(
        px.scatter(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'EY, %' : np.concat([[0], analyser.mass_from_tds(bevarage=volume_it) / coffee_mass * 100]),
                    }),
                   x = 'N, iteration',
                   y = 'EY, %').data[0],
        row=1,
        col=1,
    )
    
    fig.add_trace(
        px.line(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'EY, %' :  np.concat([[0], analyser.mass_from_tds(bevarage=volume_it) / coffee_mass * 100]),
                    }),
                   x = 'N, iteration',
                   y = 'EY, %').data[0],
        row=1,
        col=1
    )

    fig.add_hline(y=18, line_dash="dash", row=1, col=1, line_color='red')
    fig.add_hline(y=22, line_dash="dash", row=1, col=1, line_color='red')

    fig.add_trace(
        px.scatter(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : np.concat([[0], analyser.tds_integral()])
                    }),
                   x = 'N, iteration',
                   y = 'TDS, %').data[0],
        row=1,
        col=2,
    )

    fig.add_trace(
        px.line(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : np.concat([[0], analyser.tds_integral()])
                    }),
                   x = 'N, iteration',
                   y = 'TDS, %').data[0],
        row=1,
        col=2
    )

    fig.add_hline(y=1.20, line_dash="dash", row=1, col=2, line_color='red')
    fig.add_hline(y=1.45, line_dash="dash", row=1, col=2, line_color='red')

    fig.update_xaxes(title_text="N, iteration", row=1, col=1)
    fig.update_xaxes(title_text="N, iteration", row=1, col=2)

    fig.update_yaxes(title_text="EY, %", row=1, col=1)
    fig.update_yaxes(title_text="TDS, %", row=1, col=2)

    return fig

def plotly_brewing_chart(fig):

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = np.arange(14, 27)
        ),
        yaxis = dict(
            tickmode = 'array',
            tickvals = np.arange(1.0, 1.8, 0.1)
        )
    )

    fig.add_vline(x=14, row=1, col=1, line_color='red')
    fig.add_vline(x=26, row=1, col=1, line_color='red')

    fig.add_hline(y=1.0, row=1, col=1, line_color='red')
    fig.add_hline(y=1.7, row=1, col=1, line_color='red')

    fig.add_vline(x=22, line_dash="dash", row=1, col=1, line_color='red')
    fig.add_vline(x=18, line_dash="dash", row=1, col=1, line_color='red')

    fig.add_hline(y=1.2, line_dash="dash", row=1, col=1, line_color='red')
    fig.add_hline(y=1.45, line_dash="dash", row=1, col=1, line_color='red')

    fig.add_annotation(x=24, y=1.3,
                text='bitter',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=24, y=1.6,
                text='strong<br>bitter',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=24, y=1.1,
                text='weak<br>bitter',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=16, y=1.6,
                text='strong<br>under<br>developed',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=16, y=1.3,
                text='under<br>developed',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=16, y=1.1,
                text='weak<br>under<br>developed',
                showarrow=False, font=(dict(size = 20)))
    
    
    fig.add_annotation(x=20, y=1.6,
                text='strong',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=20, y=1.3,
                text='ideal',
                showarrow=False, font=(dict(size = 20)))
    
    fig.add_annotation(x=20, y=1.1,
                text='weak',
                showarrow=False, font=(dict(size = 20)))
    
    fig.update_layout(uniformtext_minsize=100, uniformtext_mode='hide')

    return fig 