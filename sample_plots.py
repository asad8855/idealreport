import time
import random
import datetime
import os
from pandas import DataFrame, to_datetime, DatetimeIndex
import numpy as np
import idealreport.create_html as ch
from idealreport.reporter import Reporter
import htmltag

# simple vertical bar chart, notice additional entry in the data field for orientation

dfhb = DataFrame({'Entity': ['Entity 1', 'Entity 2', 'Entity 3', 'Entity 4', 'Entity 5'],
                  'Stat 1': np.random.randn(5).tolist(),
                  'Stat 2': np.random.randn(5).tolist(),
                 })
dfhb = dfhb.set_index('Entity')
dfhb = dfhb.sort_values(by='Stat 1', ascending=False)

bar_plot = {
    'title': 'Vertical Bar Chart by Create HTML',
    'data': [
        {
            'df': dfhb,
            'type': 'bar',
            'orientation': 'v',
        },
    ],
    'labelX': 'Entity',
    'labelY': '%',
    'staticPlot': False
}

# stacked horizontal bar chart, notice additional entry in the data field for orientation

dfsb = DataFrame({'Entity': ['Entity 1', 'Entity 2', 'Entity 3', 'Entity 4', 'Entity 5'],
                'Foo': [8, 10, 50, 85, 42],
                'Bar': [100, 50, 10, 100, 25]})
dfsb = dfsb.set_index('Entity')
dfsb = dfsb[['Foo', 'Bar']] # make sure columns have desired order

stacked_bar_plot = {
    'title': 'Horizontal Stacked Bar Chart by Create HTML',
    'data': [
        {
            'df': dfsb,
            'type': 'stackedBar',
            'orientation': 'h',
        },
    ],
    'labelX': '$',
    'staticPlot': False
}

# simple line chart

dfl = DataFrame(np.random.randn(200, 3))
dfl.columns = ['a', 'b', 'c']
dfl.a = range(200)
dfl = dfl.set_index('a')
line_plot = {
    'title': 'Line Plot by Create HTML',
    'data': [
        {
            'df': dfl,
            'type': 'line',
        },
    ],
    'staticPlot': False
}

# scatter plot

dfsp = DataFrame(np.random.randn(20, 3))
dfsp.columns = ['a', 'b', 'c']
dfsp = dfsp.set_index('a')
scatter_plot = {
    'title': 'Scatter Plot by Create HTML',
    'data': [
        {
            'df': dfsp,
            'type': 'scatter',
        },
    ],
    'labelX': 'alpha',
    'labelY': 'beta',
    'staticPlot': False
}

# mixed plot types on one graph

df1 = DataFrame(np.random.randn(200, 2))
df1.columns = ['a', 'b1']
df1.sort_values(by='a', ascending=True, inplace=True)
df1 = df1.set_index('a')

df2 = DataFrame(np.random.randn(200, 2))
df2.columns = ['a', 'b2']
df2.sort_values(by='a', ascending=True, inplace=True)
df2 = df2.set_index('a')


multi_scatter_plot = {
    'title': 'Mixed Line and Bar Plot by Create HTML',
    'data': [
        {
            'df': df1,
            'type': 'line',
        },
        {
            'df': df2,
            'type': 'bar',
            'orientation': 'v',
        },
    ],
    'labelX': 'x label',
    'labelY': 'y label',
    'staticPlot': False
}

#different axes

dfa = DataFrame(np.random.randn(20, 2))
dfa.columns = ['x', 'a']
dfa.x = range(20)
dfa = dfa.set_index('x')
dfb = DataFrame(np.random.randn(20, 2))
dfb.columns = ['x', 'b']
dfb.x = range(20)
dfb = dfb.set_index('x')
dfb.b *= 100
multi_axis_plot = {
    'type': 'line',
    'title': 'Multi-Axis Plot by Create HTML',
    'data': [
        {
            'df': dfa,
            'type': 'line',
        },
        {
            'df': dfb,
            'type': 'line',
            'y2': True,
        },
    ],
    'labelX': 'x',
    'labelY': 'ya',
    'labelY2': 'yb',
}

output_path = '/home/jason/ideal/reports/sample_report/output'
output_file = os.path.join(output_path, 'sample_plots.html')
r = Reporter(title='Sample Plots', output_file=output_file)

# report start
r.h += htmltag.h3('This report provides an overivew of the different plot types.')

# bar charts
r.h += htmltag.h4('Bar Charts')
r.plot.bar(df=dfhb, title='Vertical Bar Chart by Reporter', xlabel='Entity', ylabel='%')
r.h += ch.plot(bar_plot)
r.plot.barh(df=dfsb, title='Horizontal Stacked Bar Chart by Reporter', stacked=True, xlabel='$')
r.h += ch.plot(stacked_bar_plot)

# line charts
r.h += htmltag.h4('Line Charts')
r.plot.line(df=dfl, title='Line Chart by Reporter', xlabel='Entity', ylabel='%')
r.h += ch.plot(line_plot)

# scatter plots
r.h += htmltag.h4('Scatter Plots')
r.plot.scatter(df=dfsp, title='Scatter Plot by Reporter', xlabel='alpha', ylabel='beta')
r.h += ch.plot(scatter_plot)

# mixed plot types
r.h += htmltag.h4('Multi Series, Mixed Type Plots')
r.plot.multi(dfs=[df1, df2], types=['line', 'bar'], title='Mixed Line and Bar Plot by Reporter', xlabel='x label', ylabel='y label')
r.h += ch.plot(multi_scatter_plot)
r.plot.multi(dfs=[dfa, dfb], types=['line', 'line'], title='Multi-Axis Plot by Reporter', xlabel='x', ylabel='ya', y2_axis=[False,True], y2label='yb')
r.h += ch.plot(multi_axis_plot)

# generate and save the report HTML
r.generate()