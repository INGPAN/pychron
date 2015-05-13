# ===============================================================================
# Copyright 2015 Jake Ross
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
from traits.api import HasTraits, Str, Instance, List, Event
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.envisage.browser.view import BrowserView
from pychron.pipeline.nodes.data import UnknownNode, ReferenceNode
from pychron.loggable import Loggable
from pychron.pipeline.nodes.figure import IdeogramNode, SpectrumNode
from pychron.pipeline.nodes.filter import FilterNode


class Pipeline(HasTraits):
    name = Str('Pipeline')
    nodes = List

    def add_after(self, after, node):
        idx = self.nodes.index(after)
        self.nodes.insert(idx + 1, node)


class PipelineEngine(Loggable):
    dvc = Instance('pychron.dvc.dvc.DVC')
    pipeline = Instance(Pipeline, ())

    unknowns = List
    references = List
    run_needed = Event

    def refresh_analyses(self):
        unks = []
        refs = []
        for node in self.pipeline.nodes:
            if isinstance(node, ReferenceNode):
                refs.extend(node.analyses)
            elif isinstance(node, UnknownNode):
                unks.extend(node.analyses)

        self.unknowns = unks
        self.references = refs

    def add_test_filter(self):
        node = self.pipeline.nodes[0]
        newnode = FilterNode()
        newnode.add_filter('uage', '<', '10')
        self.pipeline.add_after(node, newnode)

    def add_filter(self, node):
        """
        add filter after this node
        :param node:
        :return:
        """
        newnode = FilterNode()
        if newnode.configure():
            self.pipeline.add_after(node, newnode)
            self.run_needed = True

    def add_spectrum(self, node=None):
        if node is None:
            node = self._get_last_node()

        if node:
            ideo_node = SpectrumNode()
            self.pipeline.add_after(node, ideo_node)

    def add_ideogram(self, node=None):
        if node is None:
            node = self._get_last_node()

        if node:
            ideo_node = IdeogramNode()
            self.pipeline.add_after(node, ideo_node)

    def _get_last_node(self):
        if self.pipeline.nodes:
            idx = len(self.pipeline.nodes) - 1

            return self.pipeline.nodes[idx]

    def select_default(self):
        node = self.pipeline.nodes[0]

        self.browser_model.select_sample(idx=0)
        records = self.browser_model.get_analysis_records()
        analyses = self.dvc.make_analyses(records)
        node.analyses.extend(analyses)
        self.refresh_analyses()

    def add_analyses(self, node):
        """
        add analyses to node

        select analyses from popup browser
        :param node:
        :return:
        """
        browser_view = BrowserView(model=self.browser_model)
        info = browser_view.edit_traits(kind='livemodal')
        if info.result:
            records = self.browser_model.get_analysis_records()
            if records:
                analyses = self.dvc.make_analyses(records)
                node.analyses.extend(analyses)

                self.refresh_analyses()

    def add_data(self):
        """

        add a default data node
        :return:
        """
        self.debug('add data node')
        self.pipeline.nodes.append(UnknownNode(name='default'))
        self.refresh_analyses()

    # def add_node(self, name):
    #
    # node = BaseNode(name=name)
    # self.pipeline.nodes.append(node)

    def run(self, state):
        self.debug('pipeline started')
        for node in self.pipeline.nodes:
            node.run(state)
        self.debug('pipeline finished')

        self.unknowns = state.unknowns
        self.references = state.references

# if __name__ == '__main__':
# from traitsui.api import TreeNode, Handler
# from pychron.core.ui.tree_editor import TreeEditor
# from pyface.action.menu_manager import MenuManager
#     from pychron.pipeline.nodes.base import BaseNode
#     from traitsui.menu import Action
#     from pychron.envisage.resources import icon
#     from pychron.core.helpers.logger_setup import logging_setup
#
#     logging_setup('pipeline')
#     class PipelineHandler(Handler):
#         def add_data(self, info, obj):
#             info.object.add_data()
#
#     class DataTreeNode(TreeNode):
#         def get_icon( self, object, is_expanded ):
#             return icon('table')
#
#     e = PipelineEngine()
#     # e.add_data()
#     # e.add_node('foo')
#     # e.add_node('bar')
#     nodes = [TreeNode(node_for=[Pipeline],
#                       children='nodes',
#                       icon_open='',
#                       label='name',
#                       auto_open=True,
#                       menu=MenuManager(Action(name='Add Data',
#                                                    action='add_data'))),
#              # TreeNode(node_for=[BaseNode],
#              #
#              #          label='name'),
#              DataTreeNode(node_for=[DataNode],
#                           label='name')
#              ]
#     editor = TreeEditor(nodes=nodes,
#                         editable=False,
#                         selection_mode='extended',
#                         selected='selected',
#                         dclick='dclicked',
#                         show_disabled=True,
#                         refresh_all_icons='refresh_all_needed',
#                         refresh_icons='refresh_needed'
#                         )
#     v = View(UItem('pipeline',
#                    editor=editor),
#              handler=PipelineHandler())
#     e.configure_traits(view=v)


# ============= EOF =============================================



