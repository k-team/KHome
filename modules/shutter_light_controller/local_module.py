# -*- coding: utf-8 -*-

import module
from module import use_module
import fields

class ShutterLightController(module.Base):
    update_rate = 500

    shutter = use_module('Shutter')
    luminosity_int = use_module('LuminosityInteriorSensor')
    luminosity_ext = use_module('LuminosityExteriorSensor')

    # To work correctly, the presence module should return the presence of a
    # human in the entire house, and not in the current room !
    human_presence = use_module('HumanPresenceSensor')

    anonym = fields.proxy.readable('luminosity_interior', 'LuminosityInteriorSensor', 'luminosity_interior')
    anonym2 = fields.proxy.readable('luminosity_exterior', 'LuminosityExteriorSensor', 'luminosity_exterior')
    anonym3 = fields.proxy.readable('shutter', 'Shutter', 'shutter')
    anonym4 = fields.proxy.readable('presence', 'HumanPresenceSensor', 'presence')

    class luminosity_limit(fields.syntax.Percentage, fields.io.Writable, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        """
        Field configuring the minimal brightness the user wants during the day.
        """
        public_name = 'Luminosité minimale souhaitée'

        init_value = 60.

    class night_detection_limit(fields.syntax.Percentage, fields.io.Writable, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        """
        Field configuring the brightness lower limit under which we can
        consider that it is night-time.
        """
        public_name = 'Seuil de luminosité détectant la nuit'

        init_value = 20.

    class controller(fields.Base):
        def always(self):
            logger = self.module.logger
            logger.info('updating control')
            try:
                lum_int = self.module.luminosity_int.luminosity_interior()[1]
                lum_ext = self.module.luminosity_ext.luminosity_exterior()[1]
                presence = self.module.human_presence.presence()[1]
                logger.info('lum_int = %s / lum_ext = %s / presence = %s',
                        lum_int, lum_ext, presence)
            except TypeError as e:
                logger.exception(e)
            else:
                if  lum_ext < self.module.night_detection_limit():
                    logger.info('closing shutter since night was detected')
                    self.module.shutter.shutter(0)
                elif not presence:
                    logger.info('closing shutter since nobody is at home')
                    self.module.shutter.shutter(0)
                else:
                    luminosity_limit = self.module.luminosity_limit()
                    if lum_int < luminosity_limit \
                            and self.luminosity_limit < lum_ext:
                        logger.info('opening shutter')
                        self.module.shutter.shutter(100)
