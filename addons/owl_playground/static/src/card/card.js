/** @odoo-module */

import { xml, Component } from "@odoo/owl"

export class Card extends Component {

  static template = xml/* xml */`
    <div >
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <!-- This component should have three slots -->

                <!-- one slot for the title -->
                <t t-if="props.slots.title">
                    <h5 class="card-title"><t t-slot="title"/></h5>
                </t>

                <!-- one for the content (the default slot)  -->
                <p class="card-text"><t t-slot="default"/></p>

                <!-- one for the YS custom  -->
                <p class="card-text" style="color:red"><t t-slot="YS_custom"/></p>

            </div>
        </div>
    </div>
  `

  static props = {
    slots: {
      type: Object,
      shape: {
        default: Object,
        title: { type: Object, optional: true },
        YS_custom: { type: Object, optional: true },
      },
    },
  }

}

