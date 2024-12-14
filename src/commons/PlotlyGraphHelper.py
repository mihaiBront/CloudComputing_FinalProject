import plotly
from io import StringIO
import numpy as np
from src.commons.DateTimeHelper import DateTimeHelper

class PlotlyGraphHelper():
    
    @staticmethod
    def glucosePredictionGraphHtml(
        dictGlucoseData, dictGlucosePrediction, **kwargs):
        
        ymin, ymax = kwargs.get('ymin', -1), kwargs.get('ymax', -1) 
        if ymin < 0:
            ymin = np.min(
                np.concat((
                    dictGlucoseData['glucose'],dictGlucosePrediction['glucose'])
                          )
                )
        
        if ymax < 0:
            ymax = np.max(
                np.concat((
                    dictGlucoseData['glucose'],dictGlucosePrediction['glucose'])
                          )
                )      
        
        # make graph
        fig = plotly.graph_objects.Figure()
        fig.add_trace(plotly.graph_objects.Scatter(
            x=dictGlucoseData['time'],
            y=dictGlucoseData['glucose'],
            mode='lines+markers',
            name='Glucose Data'
        ))
        
        fig.add_trace(plotly.graph_objects.Scatter(
            x=dictGlucosePrediction['time'],
            y=dictGlucosePrediction['glucose'],
            mode='lines+markers',
            name='Glucose Prediction'
        ))
        
        timeAggregate = []
        timeAggregate.extend(dictGlucoseData['time'])
        timeAggregate.extend(dictGlucosePrediction['time'])
        
        timeAggregate = [DateTimeHelper.dateTimeFromStr(t) for t in timeAggregate]
        
        fig.update_layout(
            title='Glucose Levels Over Time',
            xaxis_title='Time',
            yaxis_title='Glucose Level',
            xaxis=dict(
                # type='date',  # Ensure the axis is treated as datetime
                # showgrid=True,  # Optional: adds grid lines for clarity
                range=[min(timeAggregate), max(timeAggregate)]
            ),
            yaxis=dict(
                range=[ymin, ymax]
            )
        )
        
        # fig.show()
        html_buffer = StringIO() 
        fig.write_html(html_buffer)  
        html_string = html_buffer.getvalue()  
        html_buffer.close() 
        
        return html_string
        
        