# ex: set ro:
# DO NOT EDIT.
# generated by smc (http://smc.sourceforge.net/)
# from file : LaserFSM.sm


#
# Copyright (c) 2010 RossLabas
# All rights reserved.
#
# Author: Jake Ross
#


import statemap


class LaserState(statemap.State):
    '''
        G{classtree}
    '''

    def Entry(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        pass

    def Exit(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        pass

    def Disable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        self.Default(fsm)

    def Enable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        self.Default(fsm)

    def Lase(self, fsm, power, mode):
        '''
            @type fsm: C{str}
            @param fsm:

            @type power: C{str}
            @param power:

            @type mode: C{str}
            @param mode:
        '''
        self.Default(fsm)

    def Default(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        msg = "\n\tState: %s\n\tTransition: %s" % (
            fsm.getState().getName(), fsm.getTransition())
        raise statemap.TransitionUndefinedException, msg

class LaserFSM_Default(LaserState):
    '''
        G{classtree}
    '''
    pass

class LaserFSM_Disabled(LaserFSM_Default):
    '''
        G{classtree}
    '''

    def Disable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._disable_laser_()
        finally:
            fsm.setState(LaserFSM.Disabled)
            fsm.getState().Entry(fsm)

    def Enable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._enable_laser_()
        finally:
            fsm.setState(LaserFSM.Enabled)
            fsm.getState().Entry(fsm)

    def Lase(self, fsm, power, mode):
        '''
            @type fsm: C{str}
            @param fsm:

            @type power: C{str}
            @param power:

            @type mode: C{str}
            @param mode:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._warn_()
        finally:
            fsm.setState(LaserFSM.Disabled)
            fsm.getState().Entry(fsm)

class LaserFSM_Enabled(LaserFSM_Default):
    '''
        G{classtree}
    '''

    def Disable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._disable_laser_()
        finally:
            fsm.setState(LaserFSM.Disabled)
            fsm.getState().Entry(fsm)

    def Enable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        # No actions.
        pass

    def Lase(self, fsm, power, mode):
        '''
            @type fsm: C{str}
            @param fsm:

            @type power: C{str}
            @param power:

            @type mode: C{str}
            @param mode:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._set_laser_power_(power, mode)
        finally:
            fsm.setState(LaserFSM.Lasing)
            fsm.getState().Entry(fsm)

class LaserFSM_Lasing(LaserFSM_Default):
    '''
        G{classtree}
    '''

    def Disable(self, fsm):
        '''
            @type fsm: C{str}
            @param fsm:
        '''
        ctxt = fsm.getOwner()
        fsm.getState().Exit(fsm)
        fsm.clearState()
        try:
            ctxt._disable_laser_()
        finally:
            fsm.setState(LaserFSM.Disabled)
            fsm.getState().Entry(fsm)

    def Lase(self, fsm, power, mode):
        '''
            @type fsm: C{str}
            @param fsm:

            @type power: C{str}
            @param power:

            @type mode: C{str}
            @param mode:
        '''
        ctxt = fsm.getOwner()
        endState = fsm.getState()
        fsm.clearState()
        try:
            ctxt._set_laser_power_(power, mode)
        finally:
            fsm.setState(endState)

class LaserFSM(object):
    '''
        G{classtree}
    '''

    Disabled = LaserFSM_Disabled('LaserFSM.Disabled', 0)
    Enabled = LaserFSM_Enabled('LaserFSM.Enabled', 1)
    Lasing = LaserFSM_Lasing('LaserFSM.Lasing', 2)
    Default = LaserFSM_Default('LaserFSM.Default', -1)

class Laser_sm(statemap.FSMContext):
    '''
        G{classtree}
    '''

    def __init__(self, owner):
        '''
            @type owner: C{str}
            @param owner:
        '''
        statemap.FSMContext.__init__(self, LaserFSM.Disabled)
        self._owner = owner

    def __getattr__(self, attrib):
        def trans_sm(*arglist):

            self._transition = attrib
            getattr(self.getState(), attrib)(self, *arglist)
            self._transition = None
        return trans_sm

    def enterStartState(self):
        '''
        '''
        self._state.Entry(self)

    def getOwner(self):
        '''
        '''
        return self._owner

# Local variables:
#  buffer-read-only: t
# End:
