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
from pyface.action.menu_manager import MenuManager
from pyface.tasks.traits_dock_pane import TraitsDockPane
from traits.api import Int, Property, List
from traitsui.editors import TabularEditor
from traitsui.handler import Handler
from traitsui.menu import Action
from traitsui.tabular_adapter import TabularAdapter
from traitsui.tree_node import TreeNode
from traitsui.api import View, UItem, VGroup, EnumEditor
# ============= standard library imports ========================
# ============= local library imports  ==========================
from uncertainties import nominal_value, std_dev
from pychron.core.helpers.color_generators import colornames
from pychron.core.helpers.formatting import floatfmt

from pychron.core.ui.tree_editor import TreeEditor
from pychron.pipeline.engine import Pipeline
from pychron.pipeline.nodes.base import BaseNode
from pychron.pipeline.nodes.data import DataNode
from pychron.pipeline.nodes.figure import IdeogramNode, SpectrumNode, SeriesNode
from pychron.pipeline.nodes.filter import FilterNode
from pychron.pipeline.nodes.grouping import GroupingNode
from pychron.pipeline.nodes.persist import PDFNode
from pychron.pipeline.tasks.tree_node import SeriesTreeNode, PDFTreeNode, GroupingTreeNode, SpectrumTreeNode, \
    IdeogramTreeNode, FilterTreeNode, DataTreeNode


def node_adder(func):
    def wrapper(obj, info, o):
        name = func.func_name
        f = getattr(info.object, name)
        f(o)

    return wrapper


class PipelineHandler(Handler):
    def delete_node(self, info, obj):
        info.object.remove_node(obj)

    def enable(self, info, obj):
        self._toggle_enable(info, obj, True)

    def disable(self, info, obj):
        self._toggle_enable(info, obj, False)

    def _toggle_enable(self, info, obj, state):
        obj.enabled = state
        info.object.run_needed = True
        info.object.refresh_all_needed = True

    def configure(self, info, obj):
        info.object.configure(obj)

    @node_adder
    def add_pdf_figure(self, info, obj):
        pass

    @node_adder
    def add_data(self, info, obj):
        pass

    @node_adder
    def add_filter(self, info, obj):
        pass

    @node_adder
    def add_ideogram(self, info, obj):
        pass

    @node_adder
    def add_spectrum(self, info, obj):
        pass

    @node_adder
    def add_grouping(self, info, obj):
        pass

    @node_adder
    def add_series(self, info, obj):
        pass


class PipelinePane(TraitsDockPane):
    name = 'Pipeline'
    id = 'pychron.pipeline.pane'

    def traits_view(self):
        def menu_factory(*actions):
            return MenuManager(
                Action(name='Enable',
                       action='enable',
                       visible_when='not object.enabled'),
                Action(name='Disable',
                       action='disable',
                       visible_when='object.enabled'),
                Action(name='Configure', action='configure'),
                Action(name='Delete', action='delete_node'),
                *actions)

        def add_menu_factory():
            return MenuManager(
                # Action(name='Add Analyses',
                # action='add_analyses'),
                Action(name='Add Grouping',
                       action='add_grouping'),
                Action(name='Add Filter',
                       action='add_filter'),
                Action(name='Add Ideogram',
                       action='add_ideogram'),
                Action(name='Add Spectrum',
                       action='add_spectrum'),
                Action(name='Add Series',
                       action='add_series'),
                name='Add')

        def save_menu_factory():
            return MenuManager(Action(name='Save PDF Figure',
                                      action='add_pdf_figure'),
                               name='Save')

        def data_menu_factory():
            return menu_factory(add_menu_factory())

        def filter_menu_factory():
            return menu_factory(add_menu_factory())

        def figure_menu_factory():
            return menu_factory(add_menu_factory(), save_menu_factory())

        nodes = [TreeNode(node_for=[Pipeline],
                          children='nodes',
                          icon_open='',
                          label='name',
                          auto_open=True,
                          menu=MenuManager(Action(name='Add Data',
                                                  action='add_data'))),
                 DataTreeNode(node_for=[DataNode], menu=data_menu_factory()),
                 FilterTreeNode(node_for=[FilterNode], menu=filter_menu_factory()),
                 IdeogramTreeNode(node_for=[IdeogramNode], menu=figure_menu_factory()),
                 SpectrumTreeNode(node_for=[SpectrumNode], menu=figure_menu_factory()),
                 SeriesTreeNode(node_for=[SeriesNode], menu=figure_menu_factory()),
                 PDFTreeNode(node_for=[PDFNode], menu=menu_factory()),
                 GroupingTreeNode(node_for=[GroupingNode], menu=data_menu_factory()),
                 TreeNode(node_for=[BaseNode], label='name')]

        editor = TreeEditor(nodes=nodes,
                            editable=False,
                            # selection_mode='extended',
                            selected='selected',
                            dclick='dclicked',
                            show_disabled=True,
                            refresh_all_icons='refresh_all_needed',
                            update='update_needed')
        v = View(VGroup(
            UItem('selected_pipeline_template',
                  editor=EnumEditor(name='available_pipeline_templates')),
            UItem('pipeline',
                  editor=editor)),
                 handler=PipelineHandler())
        return v


class UnknownsAdapter(TabularAdapter):
    columns = [('Run ID', 'record_id'),
               # ('Class','klass'),
               ('Sample', 'sample'),
               ('Age', 'age'),
               (u'\u00b11\u03c3', 'error'),
               ('Tag', 'tag'),
               ('GID', 'graph_id')]

    record_id_width = Int(80)
    sample_width = Int(80)
    age_width = Int(70)
    error_width = Int(60)
    tag_width = Int(50)
    graph_id_width = Int(30)

    font = 'arial 10'
    # record_id_text_color = Property
    # tag_text_color = Property
    age_text = Property
    error_text = Property
    colors = List(colornames)
    # klass_text = Property
    # def _get_klass_text(self):
    # return self.item.__class__.__name__.split('.')[-1]

    # def get_menu(self, object, trait, row, column):
    # return MenuManager(Action(name='Group Selected', action='group_by_selected'),
    # Action(name='Group by Labnumber', action='group_by_labnumber'),
    #                        Action(name='Group by Aliquot', action='group_by_aliquot'),
    #                        Action(name='Clear Grouping', action='clear_grouping'),
    #                        Action(name='Unselect', action='unselect'))

    def get_bg_color(self, obj, trait, row, column=0):
        c = 'white'
        # if not isinstance(self.item, IsotopeRecordView):
        if self.item.tag == 'invalid':
            c = '#C9C5C5'
        elif self.item.is_omitted():
            c = '#FAC0C0'
        return c

    def _get_age_text(self):
        r = ''
        # print self.item,not isinstance(self.item, IsotopeRecordView)
        # if not isinstance(self.item, IsotopeRecordView):
        r = floatfmt(nominal_value(self.item.uage), n=3)
        return r

    def _get_error_text(self):
        r = ''
        # if not isinstance(self.item, IsotopeRecordView):
        # r = floatfmt(std_dev(self.item.uage_wo_j_err), n=4)
        r = floatfmt(std_dev(self.item.uage), n=4)
        return r

    def get_text_color(self, obj, trait, row, column=0):
        color = 'black'
        if obj.show_group_colors:
            # n = len(colornames)
            colors = self.colors
            n = len(colors)

            gid = getattr(obj, trait)[row].group_id
            # gid = obj.items[row].group_id

            cid = gid % n if n else 0
            try:
                color = colors[cid]
            except IndexError:
                pass

        return color


class ReferencesAdapter(TabularAdapter):
    columns = [
        ('Run ID', 'record_id'), ]
    font = 'arial 10'


class AnalysesPane(TraitsDockPane):
    name = 'Analyses'
    id = 'pychron.pipeline.analyses'

    def traits_view(self):
        v = View(VGroup(UItem('unknowns',
                              editor=TabularEditor(adapter=UnknownsAdapter(),
                                                   refresh='refresh_table_needed',
                                                   operations=[])),
                        UItem('references',
                              visible_when='references',
                              editor=TabularEditor(adapter=ReferencesAdapter(),
                                                   refresh='refresh_table_needed',
                                                   operations=[]))))
        return v

        # ============= EOF =============================================


