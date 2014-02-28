# -*- coding: utf-8 -*-

import module
from module import use_module
import fields

class GazController(module.Base):
    public_name = 'Control du gaz'
    update_rate = 10

    co_gaz = use_module('COSensor')
    alarm = use_module('Alarm')

    butane = fields.proxy.basic('butane', 'ButaneGaz', 'butane')
    butane_actuator = fields.proxy.basic('butane_actuator', 'ButaneGaz', 'but_actuator')
    butane_lie = fields.proxy.basic('butane_lie', 'ButaneGaz', 'limit_value_but')
    butane_alarm = fields.proxy.basic('butane_alarm', 'ButaneGaz', 'message_but')

    methane = fields.proxy.basic('methane', 'MethaneGaz', 'methane')
    methane_actuator = fields.proxy.basic('methane_actuator', 'MethaneGaz', 'meth_actuator')
    methane_lie = fields.proxy.basic('methane_lie', 'MethaneGaz', 'limit_value_meth')
    methane_alarm = fields.proxy.basic('methane_alarm', 'MethaneGaz', 'message_meth')

    propane = fields.proxy.basic('propane', 'PropaneGaz', 'propane')
    propane_actuator = fields.proxy.basic('propane_actuator', 'PropaneGaz', 'prop_actuator')
    propane_lie = fields.proxy.basic('propane_lie', 'PropaneGaz', 'limit_value_prop')
    propane_alarm = fields.proxy.basic('propane_alarm', 'PropaneGaz', 'message_prop')

    co = fields.proxy.basic('co', 'COSensor', 'co')
    co_lie = fields.proxy.basic('co_lie', 'COSensor', 'limit_value_co')
    co_alarm = fields.proxy.basic('co_alarm', 'COSensor', 'message_co')

    alarm = fields.proxy.basic('alarm', 'Alarm', 'alarm')
