/** @odoo-module **/

import { Component, useState } from "@odoo/owl"
import { useService } from "@web/core/utils/hooks"
import { session } from '@web/session'

import { SidebarMenuItem } from "./menu_item"

export class SideBar extends Component {

  setup () {

    this.actionService = useService("action")
    this.menuService = useService("menu")
    this.menu_data = {}

    let post_deal_app_data = (app) => {
      this.menu_data[app.id] = app
      if (app.childrenTree) {

        for (let i = 0; i < app.childrenTree.length; i++) {
          let child = app.childrenTree[i]
          child.open = false
          child.active = false
          child.level = app.level + 1
          child.parent = app
          if (child.childrenTree) {
            post_deal_app_data(child)
          } else {
            this.menu_data[child.id] = child
          }
        }

      }
    }


    this.menu_root = this.menuService.getMenu('root')
    let apps = this.menuService.getApps()
    apps.map((app) => {
      app.active = false
      app.open = false
      app.level = 0
      app.childrenTree = this.menuService.getMenuAsTree(app.id).childrenTree
      post_deal_app_data(app)
    })

    // set the first app as active
    if (apps.length > 0) {
      apps[0].active = true
    }

    this.state = useState({
      apps,
      hovered: false,
      isMobile: false,
      sidebar_sm: false,
    })
  }

  _get_top_app (app) {
    if (app.parent) {
      return this._get_top_app(app.parent)
    } else {
      return app
    }
  }

  /**
   * on menu item click
   * @param {*} event 
   */
  _on_menu_item_click (menu, event) {
    this.menuService.selectMenu(menu)
  }

  _on_app_changed () {

    // current app
    var current_app = this.menuService.getCurrentApp()

    // get the first app
    var first_app = current_app
    while (first_app.parent) {
      first_app = first_app.parent
      first_app.open = true
    }

    // set the first app as active
    this.state.apps.map((app) => {
      app.active = false
      if (app.id == first_app.id) {
        app.active = true
      }
    })
  }

  /**
   * deactive the slibing menu
   * @param {*} menu 
   * @param {*} event 
   */
  _on_menu_item_toggled (menu, event) {
    // deactive the slide menu
    let parent = menu.parent
    if (parent) {
      let children = parent.childrenTree
      for (let i = 0; i < children.length; i++) {
        if (children[i].id != menu.id) {
          children[i].open = false
        }
      }
    } else {
      let apps = this.state.apps
      for (let i = 0; i < apps.length; i++) {
        if (apps[i].id != menu.id) {
          apps[i].open = false
        }
      }
    }
  }

  patched () {
    this._addTooltips()
  }

  willUnmount () {
    // this.env.bus.off("MENUS:APP-CHANGED", this);
  }

  get logo_url () {
    return '/web/binary/company_logo' + '?db=' + session.db + (session.company_id ? '&company=' + session.user_context.current_company : '')
  }

  get logo_url_small () {
    return '/web/binary/company_logo' + '?db=' + session.db + (session.company_id ? '&company=' + session.user_context.current_company : '')
  }

  update_logo (reload) {
    let company = session.company_id
    this.state.logo_url = '/web/binary/company_logo' + '?db=' + session.db + (company ?
      '&company=' + session.user_context.current_company : '') + moment().format('x')
  }

  /**
   * on sidebar enter
   */
  _on_sidebar_enter (event) {
    // $('body').addClass('sidebar_hovered')
  }

  /**
   * on sidebar leave
   */
  _on_sidebar_leave (event) {
    // $('body').removeClass('sidebar_hovered')
  }
}

SideBar.props = {}
SideBar.components = { SidebarMenuItem }
SideBar.template = 'func01_uimock.sidebar'
