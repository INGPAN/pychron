# ===============================================================================
# Copyright 2014 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
from traits.api import HasTraits, Button, Str, Int, Bool
from traitsui.api import View, Item, UItem, HGroup, VGroup
#============= standard library imports ========================
#============= local library imports  ==========================
from traitsui.menu import Action


class OpenFoobotAction(Action):
    name = 'Foobot'

    def perform(self, event):
        print 'open foobot'
        app = event.task.window.application
        app.open_task('pychron.foobot.task')

#============= EOF =============================================




