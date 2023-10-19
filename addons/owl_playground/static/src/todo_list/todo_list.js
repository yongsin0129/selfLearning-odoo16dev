/** @odoo-module */

import { Todo } from "./todo"
import { useAutofocus } from "../util"

import { Component, useState, xml } from "@odoo/owl"

export class TodoList extends Component {

  static template = xml/* xml */`
    <div>
        <div class="bg-white border border-primary rounded mt-3 p-3">
            <input class="form-control mb-3" type="text" placeholder="Add a todo" t-on-keyup="addTodo" t-ref="todoListInput"/>
            <t t-foreach="todoList" t-as="todo" t-key="todo.id">
                <Todo id="todo.id" description="todo.description" done="todo.done" toggleState.bind="toggleTodo" removeTodo.bind="removeTodo"/>
            </t>
        </div>
    </div>  
  `
  static components = { Todo }

  setup () {
    this.nextId = 0
    this.todoList = useState([])
    useAutofocus("todoListInput")
  }

  addTodo (ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todoList.push({ id: this.nextId++, description: ev.target.value, done: false })
      ev.target.value = ""
    }
  }

  toggleTodo (todoId) {
    const todo = this.todoList.find((todo) => todo.id === todoId)
    if (todo) {
      todo.done = !todo.done
    }
  }

  removeTodo (todoId) {
    const todoIndex = this.todoList.findIndex((todo) => todo.id === todoId)
    if (todoIndex >= 0) {
      this.todoList.splice(todoIndex, 1)
    }
  }
}

