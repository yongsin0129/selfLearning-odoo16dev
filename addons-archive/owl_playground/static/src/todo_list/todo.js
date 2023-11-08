/** @odoo-module */

import { Component, xml } from "@odoo/owl"

export class Todo extends Component {
  static template = xml/* xml */`
    <div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" t-att-id="props.id" t-att-checked="props.done" t-on-click="onClick"/>
            <label class="form-check-label" t-att-for="props.id" t-att-class="props.done ? 'text-decoration-line-through text-muted' : '' ">
                <t t-esc="props.id"/>.
                <t t-esc="props.description"/>
            </label>

            <span role="button" class="fa fa-remove ms-3 text-danger" t-on-click="onRemove"/>
        </div>
    </div>
  `

  onClick (ev) {
    this.props.toggleState(this.props.id)
  }

  onRemove () {
    this.props.removeTodo(this.props.id)
  }
}

// Props validation
Todo.props = {
  id: { type: Number },
  description: { type: String },
  done: { type: Boolean },
  toggleState: { type: Function },
  removeTodo: { type: Function },
}