/** @odoo-module */

import { registry } from "@web/core/registry"
import { CharField } from "@web/views/fields/char/char_field"
import { Component, xml } from "@odoo/owl"

class ImagePreviewField extends Component { }

ImagePreviewField.components = { CharField }
ImagePreviewField.supportedTypes = ["char"]
ImagePreviewField.template = xml/* xml */`
    <t t-name="awesome_tshirt.ImagePreviewField" owl="1">
        <CharField t-props="props"/>
        <img t-att-src="props.value"/>
    </t>
`

registry.category("fields").add("image_preview", ImagePreviewField)
