/** @odoo-module */

import { registry } from "@web/core/registry"
import { BooleanField } from "@web/views/fields/boolean/boolean_field"
import { xml } from "@odoo/owl"

class LateOrderBooleanField extends BooleanField { }

LateOrderBooleanField.template = "awesome_tshirt.LateOrderBooleanField"

registry.category("fields").add("late_boolean", LateOrderBooleanField)
