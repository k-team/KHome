import module
import fields
import fields.proxy

class Test3(module.Base):
    field = fields.proxy.readable('field', 'Test2', 'field')
