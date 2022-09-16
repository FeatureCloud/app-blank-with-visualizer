import os

from FeatureCloud.app.engine.app import AppState, app_state

import fcvisualization
from threading import Thread

TERMINAL = False


def callback_fn_terminal_state():
    global TERMINAL
    print("Transition to terminal state triggered...")
    TERMINAL = True


@app_state('initial')
class InitialState(AppState):
    def register(self):
        print('registering transition from initial to plot')
        self.register_transition('running')

    def run(self) -> str:
        path_prefix_visualizer = os.getenv("PATH_PREFIX") + 'visualizer/'
        print("PATH_PREFIX environment variable: ", path_prefix_visualizer)
        print('Plot start...')
        fc_visualization = fcvisualization.fcvisualization()
        thread_vis = Thread(target=fc_visualization.start, args=('fc', path_prefix_visualizer, callback_fn_terminal_state))
        thread_vis.start()
        return 'running'


@app_state('running')
class RunningState(AppState):
    def register(self):
        print('register transitions from plot state to terminal')
        self.register_transition('running')
        self.register_transition('terminal')

    def run(self) -> str:
        if TERMINAL is True:
            print('Running is finished. Transition to terminal state.')
            return 'terminal'
        print('AppState => running')
        return 'running'
