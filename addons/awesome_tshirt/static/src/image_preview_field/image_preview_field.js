/** @odoo-module */

import { registry } from "@web/core/registry"
import { CharField } from "@web/views/fields/char/char_field"
import { Component, xml } from "@odoo/owl"
import { useCommand } from "@web/core/commands/command_hook"

class ImagePreviewField extends Component {
    setup () {
        useCommand(this.env._t("Open image in a new tab"), () => {
            window.open(this.props.value, "_blank")
        })
    }
}

ImagePreviewField.components = { CharField }
ImagePreviewField.supportedTypes = ["char"]
ImagePreviewField.template = xml/* xml */`
    <t t-name="awesome_tshirt.ImagePreviewField" owl="1">
        <CharField t-props="props"/>
        <t t-if="props.value.length === 0">
            <p class="text-danger">MISSING TSHIRT DESIGN</p>
        </t>
        <img t-att-src="props.value"/>
    </t>
`

registry.category("fields").add("image_preview", ImagePreviewField)
