# ===============================================================================
# Copyright 2011 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================


#============= enthought library imports =======================

from pyface.message_dialog import warning
from pyface.tasks.task_window_layout import TaskWindowLayout
from pychron.envisage.tasks.actions import PAction as Action, PTaskAction as TaskAction
#============= standard library imports ========================
import os
#============= local library imports  ==========================
from pychron.envisage.resources import icon
from pychron.paths import paths

EXP_ID = 'pychron.experiment.task'


class ExperimentAction(Action):
    task_id = EXP_ID

    def _get_experimentor(self, event):
        return self._get_service(event, 'pychron.experiment.experimentor.Experimentor')

    def _get_service(self, event, name):
        app = event.task.window.application
        return app.get_service(name)

    def _open_editor(self, event):
        application = event.task.window.application
        application.open_task(self.task_id)


class BasePatternAction(TaskAction):
    _enabled = None

    def _task_changed(self):
        if self.task:
            if hasattr(self.task, 'open_pattern'):
                enabled = True
                if self.enabled_name:
                    if self.object:
                        enabled = bool(self._get_attr(self.object,
                                                      self.enabled_name, False))
                if enabled:
                    self._enabled = True
            else:
                self._enabled = False

    def _enabled_update(self):
        """
             reimplement ListeningAction's _enabled_update
        """
        if self.enabled_name:
            if self.object:
                self.enabled = bool(self._get_attr(self.object,
                                                   self.enabled_name, False))
            else:
                self.enabled = False
        elif self._enabled is not None:
            self.enabled = self._enabled
        else:
            self.enabled = bool(self.object)


class OpenPatternAction(BasePatternAction):
    name = 'Open Pattern...'
    method = 'open_pattern'


class NewPatternAction(BasePatternAction):
    name = 'New Pattern...'
    method = 'new_pattern'


class SendTestNotificationAction(TaskAction):
    name = 'Send Test Notification'
    method = 'send_test_notification'
    # accelerator = 'Ctrl+Shift+N'


class DeselectAction(TaskAction):
    name = 'Deselect'
    method = 'deselect'
    tooltip = 'Deselect the selected run(s)'
    id = 'pychron.deselect'


class UndoAction(TaskAction):
    name = 'Undo'
    method = 'undo'
    accelerator = 'Ctrl+Z'


class QueueConditionalsAction(Action):
    name = 'Edit Queue Conditionals'

    def perform(self, event):
        task = event.task
        if hasattr(task, 'edit_queue_conditionals'):
            task.edit_queue_conditionals()
        else:
            from pychron.experiment.conditional.conditionals_edit_view import edit_conditionals

            dnames = None
            spec = task.application.get_service(
                'pychron.spectrometer.base_spectrometer_manager.BaseSpectrometerManager')
            if spec:
                dnames = spec.spectrometer.detector_names

            edit_conditionals(None, detectors=dnames, app=task.application)


class QueueAction(ExperimentAction):
    def _open_experiment(self, event, path=None):

        app = event.task.window.application
        task = event.task
        if task.id == EXP_ID:
            task.open(path)
        else:
            task = app.get_task(EXP_ID, False)
            if task.open(path):
                task.window.open()


class NewExperimentQueueAction(QueueAction):
    description = 'Create a new experiment queue'
    name = 'New Experiment'
    id = 'pychron.new_experiment'

    def perform(self, event):
        if event.task.id == EXP_ID:
            event.task.new()
        else:
            application = event.task.window.application
            win = application.create_window(TaskWindowLayout(EXP_ID))
            task = win.active_task
            task.new()
            win.open()


class OpenLastExperimentQueueAction(QueueAction):
    description = 'Open last executed experiment'
    name = 'Open Last Experiment...'
    id ='pychron.open_last_experiment'

    def __init__(self, *args, **kw):
        super(OpenLastExperimentQueueAction, self).__init__(*args, **kw)
        self.enabled = bool(self._get_last_experiment())

    def perform(self, event):
        path = self._get_last_experiment()
        if path:
            self._open_experiment(event, path)
        else:
            warning(None, 'No last experiment available')
            # if os.path.isfile(paths.last_experiment):
            #     with open(paths.last_experiment, 'r') as fp:
            #         path = fp.readline()
            #         if os.path.isfile(path):
            #             self._open_experiment(event, path)
            #         else:
            #             print 'asdfasdf', path
            # else:
            #     warning(None, 'No last experiment available')

    def _get_last_experiment(self):
        if os.path.isfile(paths.last_experiment):
            with open(paths.last_experiment, 'r') as fp:
                path = fp.readline()
                if os.path.isfile(path):
                    return path


class OpenExperimentQueueAction(QueueAction):
    description = 'Open experiment'
    name = 'Open Experiment...'
    image = icon('project-open')
    id = 'pychron.open_experiment'

    def perform(self, event):
        path = '/Users/ross/Pychrondata_dev/experiments/Current Experiment.txt'
        # path = '/Users/ross/Pychrondata_dev/experiments/test.txt'
        self._open_experiment(event, path)


#===============================================================================
# Utilities
#===============================================================================
class SignalCalculatorAction(ExperimentAction):
    name = 'Signal Calculator'

    def perform(self, event):
        obj = self._get_service(event, 'pychron.experiment.signal_calculator.SignalCalculator')
        app = event.task.window.application
        app.open_view(obj)


class ResetQueuesAction(TaskAction):
    method = 'reset_queues'
    name = 'Reset Queues'


#============= EOF ====================================
