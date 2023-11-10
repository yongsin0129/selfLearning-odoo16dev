/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient"

import { SideBar } from "../sidebar/sidebar"

WebClient.components = {
  ...WebClient.components,
  SideBar
}

WebClient.template = "func01_uimock.WebClient"

// WebClient.props = {}
