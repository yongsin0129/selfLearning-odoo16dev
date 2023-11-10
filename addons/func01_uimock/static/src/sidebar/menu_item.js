/** @odoo-module **/

import { Component, useState } from "@odoo/owl"
import { Transition } from "@web/core/transition"
import { useService } from "@web/core/utils/hooks"


export class SidebarMenuItem extends Component {

  setup () {
    this.actionService = useService("action")
    this.menuService = useService("menu")

    // set the state
    this.state = useState({
      is_current: false,
    })
  }

  get menu () {
    return this.props.menu
  }

  _get_menu_item_href (menu) {
    const parts = [`menu_id=${menu.id}`]
    if (menu.action) {
      parts.push(`action=${menu.action.split(",")[1]}`)
    }
    return "#" + parts.join("&")
  }

  _get_indent (menu) {
    let level = menu.level
    if (level > 0) {
      return level * 18 + 10 + 'px'
    } else {
      return ''
    }
  }

  _on_app_changed () {
    // current app
    var current_app = this.menuService.getCurrentApp()
    if (current_app.id == this.props.menu.id && this.props.menu.children.length == 0) {
      this.state.is_current = true
    }
  }

  _on_menu_item_click (menu, event) {
    this.props.menu_item_click(menu, event)
  }

  _toggle_sub_menu (menu, event) {

    event.stopPropagation()
    event.preventDefault()

    // slide the sub menu
    let el = event.target
    if (!menu.open) {
      el.classList.add("open")
    } else {
      el.classList.remove("open")
    }

    // find parent li
    while (el.tagName !== 'LI') {
      el = el.parentElement
    }
    if (!el) {
      return
    }

    // find sub a
    let sub_a = $(el).find('a')[0]
    if ($(sub_a).hasClass('expand')) {
      $(sub_a).removeClass('expand')
    } else {
      $(sub_a).addClass('expand')
    }

    // find sub ul
    let sub_ul = el.querySelector('ul')
    if (sub_ul) {
      // slide the sub menu
      $(sub_ul).slideToggle(200, () => {
        // add class show
        if (menu.open) {
          sub_ul.classList.add('show')
        } else {
          sub_ul.classList.remove('show')
          sub_ul.classList.remove('expand')
        }
        // notify the parent
        this.props.menu_item_toggled(menu, event)
      })
      this.props.menu_item_toggled(menu, event)
    }
    // get the slibing li
    let li_siblings = el.parentElement.children
    // close the other sub menu
    for (let i = 0; i < li_siblings.length; i++) {
      let li_sibling = li_siblings[i]
      if (li_sibling !== el) {
        let sub_ul_sibling = li_sibling.querySelector('ul')
        if (sub_ul_sibling) {
          $(sub_ul_sibling).slideUp(200)
        }
      }
    }
  }
}

SidebarMenuItem.template = 'func01_uimock.sidebar_menu_item'

SidebarMenuItem.props = {
  menu: Object,
  sidebar_sm: Boolean,
  menu_item_click: Function,
  menu_item_toggled: Function,
}

SidebarMenuItem.components = { Transition, SidebarMenuItem }