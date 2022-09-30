import os
from threading import Thread

from FeatureCloud.app.engine.app import AppState, app_state

import fcvisualization
import plotly.express as px

TERMINAL = False
fc_visualization = None
fig = None
fig2 = None
vis_objects = []

def callback_fn_terminal_state():
    global TERMINAL
    print("Transition to terminal state triggered...")
    TERMINAL = True


@app_state('initial')
class InitialState(AppState):
    def register(self):
        print('registering transition from initial to plot')
        self.register_transition('plot')

    def run(self) -> str:
        global fc_visualization, fig, fig2
        path_prefix_visualizer = os.getenv("PATH_PREFIX") + 'visualizer/'
        print("PATH_PREFIX environment variable: ", path_prefix_visualizer)
        # Start visualization service. It will be available in app frontend url + /visualizer
        fc_visualization = fcvisualization.fcvisualization()
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_width", y="sepal_length")
        fig2 = px.scatter(df, x="sepal_length", y="sepal_width")
        # We add an extra diagram at start
        extra_visualization_content = [{
            "title": "Extra diagram",
            "fig": fig,
        }]
        print('Plot start...')
        # We start the visualization in a thread
        thread_vis = Thread(target=fc_visualization.start, args=('fc', path_prefix_visualizer, callback_fn_terminal_state, extra_visualization_content))
        thread_vis.start()
        return 'plot'


@app_state('plot')
class PlotState(AppState):
    def register(self):
        print('register transitions from plot state to terminal')
        self.register_transition('plot')
        self.register_transition('terminal')

    # this code will finish its functionality in 2 iterations
    def run(self) -> str:
        global vis_objects, fig, fig2
        # When the callback function will fire in the visualizer app, it'll trigger Finished state
        if TERMINAL is True:
            print('plot is finished')
            return 'terminal'

        original_title = "My Diagram from State machine"
        if len(vis_objects) == 2:
            # Update the diagram added in the previous iteration
            for diagram in vis_objects:
                if diagram['title'] == original_title:
                    print('Update diagram in progress')
                    diagram['title'] = original_title + ' updated'
                    diagram['fig'] = fig2
                    vis_objects = fc_visualization.update_diagram(diagram)
            # Add a one more diagram
            vis_objects = fc_visualization.add_diagram([{
                "title": "My second diagram from state machine",
                "fig": fig2,
            }])

        if len(vis_objects) == 0:
            # Add a new diagram to the UI
            print("Adding a new diagram to the UI")
            vis_objects = fc_visualization.add_diagram([{
                "title": original_title,
                "fig": fig,
            }])

        print(f'Visualization objects ==> {vis_objects}')
        print('plot is running')
        return 'plot'
