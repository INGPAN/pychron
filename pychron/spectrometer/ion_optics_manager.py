#===============================================================================
# Copyright 2012 Jake Ross
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
from traits.api import Range, Instance, Bool, \
    Button, Any, Str, Float, Enum, HasTraits, List
from traitsui.api import View, Item, EnumEditor, Handler, HGroup
import apptools.sweet_pickle as pickle
#============= standard library imports ========================
#============= local library imports  ==========================
from pychron.managers.manager import Manager
from pychron.graph.graph import Graph
from pychron.spectrometer.jobs.peak_center import PeakCenter
# from threading import Thread
from pychron.spectrometer.thermo.detector import Detector
from pychron.pychron_constants import NULL_STR, QTEGRA_INTEGRATION_TIMES
from pychron.core.ui.thread import Thread
from pychron.paths import paths
import os
from pychron.core.helpers.isotope_utils import sort_isotopes
# from pychron.core.ui.gui import invoke_in_main_thread


class PeakCenterConfigHandler(Handler):
    def closed(self, info, isok):
        if isok:
            info.object.dump()
        return isok


class PeakCenterConfig(HasTraits):
    detectors = List(transient=True)
    detector = Instance(Detector, transient=True)
    detector_name = Str
    isotope = Str('Ar40')
    isotopes = List(transient=True)
    dac = Float
    use_current_dac = Bool(True)
    integration_time = Enum(QTEGRA_INTEGRATION_TIMES)
    directions = Enum('Increase', 'Decrease', 'Oscillate')

    def _integration_time_default(self):
        return QTEGRA_INTEGRATION_TIMES[4] #1.048576

    def dump(self):
        p = os.path.join(paths.hidden_dir, 'peak_center_config')
        with open(p, 'wb') as fp:
            pickle.dump(self, fp)

    def _detector_changed(self):
        if self.detector:
            self.detector_name = self.detector.name

    def traits_view(self):
        v = View(Item('detector', editor=EnumEditor(name='detectors')),
                 Item('isotope', editor=EnumEditor(name='isotopes')),
                 HGroup(Item('use_current_dac',
                             label='Use Current DAC'),
                        Item('dac', enabled_when='not use_current_dac')),
                 Item('integration_time'),
                 Item('directions'),
                 buttons=['OK', 'Cancel'],
                 kind='livemodal',
                 title='Peak Center',
                 handler=PeakCenterConfigHandler
        )
        return v


class IonOpticsManager(Manager):
    magnet_dac = Range(0.0, 6.0)
    graph = Instance(Graph)
    peak_center_button = Button('Peak Center')
    stop_button = Button('Stop')

    alive = Bool(False)
    spectrometer = Any

    peak_center = Instance(PeakCenter)
    peak_center_config = Instance(PeakCenterConfig)
    canceled = False

    peak_center_result = None

    _ointegration_time = None

    def get_mass(self, isotope_key):
        spec = self.spectrometer
        molweights = spec.molecular_weights
        return molweights[isotope_key]

    def position(self, pos, detector, use_dac=False, update_isotopes=True):
        """
            pos can be str or float
            "Ar40", "39.962", 39.962

            to set in DAC space set use_dac=True
        """
        if pos == NULL_STR:
            return

        spec = self.spectrometer
        mag = spec.magnet

        det = spec.get_detector(detector)
        self.debug('detector {}'.format(det))

        if use_dac:
            dac = pos
        else:
            self.debug('POSITION {} {}'.format(pos, detector))
            if isinstance(pos, str):
                try:
                    pos = float(pos)
                except ValueError:
                    # pos is isotope
                    if update_isotopes:
                        # if the pos is an isotope then update the detectors
                        spec.update_isotopes(pos, detector)
                    pos = self.get_mass(pos)

                mag.mass_change(pos)

            # else:
            #     #get nearst isotope
            #     self.debug('rounding mass {} to {}'.format(pos, '  {:n}'.format(round(pos))))
            #     spec.update_isotopes('  {:n}'.format(round(pos)), detector)

            # pos is mass i.e 39.962
            dac = mag.map_mass_to_dac(pos, det.name)

        if det:
            dac = spec.correct_dac(det, dac)

            self.info('positioning {} ({}) on {}'.format(pos, dac, detector))
            return mag.set_dac(dac)

    def get_center_dac(self, det, iso):
        spec = self.spectrometer
        det = spec.get_detector(det)

        molweights = spec.molecular_weights
        mass = molweights[iso]
        dac = spec.magnet.map_mass_to_dac(mass, det.name)

        # correct for deflection
        return spec.correct_dac(det, dac)

    def do_peak_center(self,
                       save=True,
                       confirm_save=False,
                       warn=False,
                       new_thread=True,
                       message='',
                       on_end=None):
        self.debug('doing pc')

        self.canceled = False
        self.alive = True

        args = (save, confirm_save, warn, message, on_end)
        if new_thread:
            t = Thread(name='ion_optics.peak_center', target=self._peak_center,
                       args=args)
            t.start()
            self._thread = t
            return t
        else:
            self._peak_center(*args)

    def setup_peak_center(self, detector=None, isotope=None,
                          integration_time=1.04,
                          directions='Increase',
                          center_dac=None, plot_panel=None, new=False,
                          standalone_graph=True, name=''):

        self._ointegration_time = self.spectrometer.integration_time

        if detector is None or isotope is None:
            pcc = self.peak_center_config
            pcc.dac=self.spectrometer.magnet.dac

            info = pcc.edit_traits()
            if not info.result:
                return
            else:

                detector = pcc.detector.name
                isotope = pcc.isotope
                directions = pcc.directions
                integration_time=pcc.integration_time

                if not pcc.use_current_dac:
                    center_dac = pcc.dac

        self.spectrometer.set_integration_time(integration_time)
        period = int(integration_time * 1000 * 0.9)

        if isinstance(detector, (tuple, list)):
            ref = detector[0]
            detectors = detector
        else:
            ref = detector
            detectors = (ref,)

        if center_dac is None:
            center_dac = self.get_center_dac(ref, isotope)

        self._setup_peak_center(detectors, isotope, period,
                                center_dac, directions, plot_panel, new,
                                standalone_graph, name)
        return self.peak_center

    def _setup_peak_center(self, detectors, isotope, period,
                           center_dac, directions, plot_panel, new,
                           standalone_graph, name):


        spec = self.spectrometer

        ref = detectors[0]
        self.reference_detector = ref
        self.reference_isotope = isotope

        if len(detectors) > 1:
            ad = detectors[1:]
        else:
            ad = []

        pc = self.peak_center
        if not pc or new:
            pc = PeakCenter()

        pc.trait_set(center_dac=center_dac,
                     period=period,
                     directions=directions,
                     reference_detector=ref,
                     additional_detectors=ad,
                     reference_isotope=isotope,
                     spectrometer=spec)

        self.peak_center = pc
        graph = pc.graph
        graph.name = name
        if plot_panel:
            plot_panel.set_peak_center_graph(graph)
        else:
            graph.close_func = self.close
            if standalone_graph:
                # bind to the graphs close_func
                # self.close is called when graph window is closed
                # use so we can stop the timer
                # set graph window attributes
                graph.window_title = 'Peak Center {}({}) @ {:0.3f}'.format(ref, isotope, center_dac)
                graph.window_width = 300
                graph.window_height = 250
                self.open_view(graph)

    def _peak_center(self, save, confirm_save, warn, message, on_end):

        pc = self.peak_center
        spec = self.spectrometer
        ref = self.reference_detector
        isotope = self.reference_isotope

        dac_d = pc.get_peak_center()

        self.peak_center_result = dac_d
        if dac_d:
            args = ref, isotope, dac_d
            self.info('new center pos {} ({}) @ {}'.format(*args))

            det = spec.get_detector(ref)

            ## correct for hv
            #dac_d /= spec.get_hv_correction(current=True)
            #
            ## correct for deflection
            #dac_d = dac_d - det.get_deflection_correction(current=True)
            #
            ## convert dac to axial units
            #dac_a = dac_d / det.relative_position
            dac_a = spec.uncorrect_dac(det, dac_d)
            self.info('converted to axial units {}'.format(dac_a))

            if save:
                save = True
                if confirm_save:
                    msg = 'Update Magnet Field Table with new peak center- {} ({}) @ RefDetUnits= {}'.format(*args)
                    save = self.confirmation_dialog(msg)
                if save:
                    spec.magnet.update_field_table(det, isotope, dac_a, message)
                    spec.magnet.set_dac(self.peak_center_result)

        elif not self.canceled:
            msg = 'centering failed'
            if warn:
                self.warning_dialog(msg)
            self.warning(msg)

            # needs to be called on the main thread to properly update
            # the menubar actions. alive=False enables IonOptics>Peak Center
        #        d = lambda:self.trait_set(alive=False)
        # still necessary with qt? and tasks

        if on_end:
            on_end()

        self.trait_set(alive=False)
        if self._ointegration_time:
            self.spectrometer.set_integration_time(self._ointegration_time)

    def close(self):
        self.cancel_peak_center()

    def cancel_peak_center(self):
        self.alive = False
        self.canceled = True
        self.peak_center.canceled = True
        self.peak_center.stop()
        self.info('peak center canceled')

    #===============================================================================
    # handler
    #===============================================================================
    def _peak_center_config_default(self):
        config = None
        p = os.path.join(paths.hidden_dir, 'peak_center_config')
        if os.path.isfile(p):
            try:
                with open(p) as fp:
                    config = pickle.load(fp)
                    config.detectors = dets = self.spectrometer.detectors
                    config.detector = next((di for di in dets if di.name == config.detector_name), None)

            except Exception, e:
                print 'peak center config', e

        if config is None:
            config = PeakCenterConfig()
            config.detectors = self.spectrometer.detectors
            config.detector = config.detectors[0]

        keys = self.spectrometer.molecular_weights.keys()
        config.isotopes = sort_isotopes(keys)

        return config


if __name__ == '__main__':
    io = IonOpticsManager()
    io.configure_traits()

#============= EOF =============================================
#    def _graph_factory(self):
#        g = Graph(
#                  container_dict=dict(padding=5, bgcolor='gray'))
#        g.new_plot()
#        return g
#
#    def _graph_default(self):
#        return self._graph_factory()

#     def _detector_default(self):
#         return self.detectors[0]
#     def peak_center_config_view(self):
#         v = View(Item('detector', editor=EnumEditor(name='detectors')),
#                Item('isotope'),
#                Item('dac'),
#                Item('directions'),
#                buttons=['OK', 'Cancel'],
#                kind='livemodal',
#                title='Peak Center'
#                )
#         return v
#    def graph_view(self):
#        v = View(Item('graph', show_label=False, style='custom'),
#                 width=300,
#                 height=500
#                 )
#        return v
#    def peak_center_view(self):
#        v = View(Item('graph', show_label=False, style='custom'),
#                 width=300,
#                 height=500,
#                 handler=self.handler_klass
#                 )
#        return v

#    def traits_view(self):
#        v = View(Item('magnet_dac'),
#                 Item('peak_center_button',
#                      enabled_when='not alive',
#                      show_label=False),
#                 Item('stop_button', enabled_when='alive',
#                       show_label=False),
#
#                 Item('graph', show_label=False, style='custom'),
#
#
#                  resizable=True)
#        return v
#    def _correct_dac(self, det, dac):
#        #        dac is in axial units
#
# #        convert to detector
#        dac *= det.relative_position
#
#        '''
#        convert to axial detector
#        dac_a=  dac_d / relpos
#
#        relpos==dac_detA/dac_axial
#
#        '''
#        #correct for deflection
#        dev = det.get_deflection_correction()
#
#        dac += dev
#
# #        #correct for hv
#        dac *= self.spectrometer.get_hv_correction(current=True)
#        return dac
