/** @odoo-module */

import { xml, Component, useState } from "@odoo/owl"

export class Counter extends Component {
  static template = xml/* xml */`
    <div >
      <p>Counter: <t t-esc="state.value"/></p>
      <button class="btn btn-primary" t-on-click="increment">Increment</button>
    </div>
  `

  setup () {
    this.state = useState({ value: 1 })
  }

  increment () {
    this.state.value = this.state.value + 1
  }
}
