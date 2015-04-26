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
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.canvas.canvas2D.scene.primitives.primitives import RoundedRectangle, Animation


class Laser(RoundedRectangle, Animation):
    cnt_tol = 6
    animate = False

    def _render_(self, gc):
        super(Laser, self)._render_(gc)
        if self.animate:
            self._draw_firing(gc)

    def _draw_firing(self, gc):
        """
        draw an led stream

        0 X X X X X
        X 0 X X X X
        X X 0 X X X
        X X X 0 X X
        X X X X 0 X
        X X X X X 0
        0 X X X X X

        :param gc:
        :return:
        """
        nleds = 6
        x, y = self.get_xy()
        gc.translate_ctm(x, y)
        radius = 5
        diam = radius * 2
        for i in range(nleds):
            gc.translate_ctm(0, -diam)
            with gc:
                if i == self.cnt:
                    color = (1, 0, 0, 1)
                else:
                    color = (1, 0.65, 0, 0.6)

                gc.set_fill_color(color)
                gc.set_stroke_color(color)

                gc.arc(0, 0, radius, 0, 360)
                gc.draw_path()

        self.increment_cnt()

# ============= EOF =============================================


