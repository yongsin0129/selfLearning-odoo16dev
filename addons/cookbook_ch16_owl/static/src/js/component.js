/** @odoo-module **/

import { registry } from '@web/core/registry'

"use strict"
const { Component, xml } = owl

class MyComponent extends Component {
  static template = xml/* xml */`
        <div class="bg-info text-center p-2">
            <b> Welcome to Odoo owl panel</b>
        </div>`

  setup () {
    // use hook here
  }
}



// registry.category('actions').add('owl.action', MyComponent)
registry.category('actions').add('owl.action_call_owl_panel', MyComponent)