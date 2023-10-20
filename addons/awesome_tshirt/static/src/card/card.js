/** @odoo-module */

const { Component, xml } = owl

export class Card extends Component { }

Card.template = xml/* xml */`
    <div>
        <div class="card" style="width: 18rem;" t-att-class="props.className">
            <div class="card-body">
                <t t-if="props.slots.title">
                    <h5 class="card-title"><t t-slot="title"/></h5>
                </t>
                <p class="card-text"><t t-slot="default"/></p>
            </div>
        </div>
    </div>
`

Card.props = {
  slots: {
    type: Object,
    shape: {
      default: Object,
      title: { type: Object, optional: true },
    }
  },
  className: {
    type: String,
    optional: true,
  },
}
