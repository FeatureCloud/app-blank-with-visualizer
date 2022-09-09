import os

from fcvisualization import fcvisualization

from FeatureCloud.app.engine.app import AppState, app_state


# FeatureCloud requires that apps define the at least the 'initial' state.
# This state is executed after the app instance is started.
@app_state('initial')
class InitialState(AppState):

    def register(self):
        self.register_transition('running')

    def run(self):
        return 'running'

@app_state('running')
class RunningState(AppState):

    def register(self):
        self.register_transition('running')

    def run(self):
        path_prefix_visualizer = os.getenv("PATH_PREFIX") + 'visualizer/'
        fc_visualization = fcvisualization()
        fc_visualization.start('fc', path_prefix_visualizer)
        return "running"