/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown"
import { DropdownItem } from "@web/core/dropdown/dropdown_item"
import { useService } from "@web/core/utils/hooks"
import { registry } from "@web/core/registry"
import { debounce } from "@web/core/utils/timing"
import { ErrorHandler } from "@web/core/utils/components"
import { NavBar } from "@web/webclient/navbar/navbar"
import { patch } from "@web/core/utils/patch"

import {
  Component,
  onWillDestroy,
  useExternalListener,
  useEffect,
  useRef,
  onWillUnmount,
} from "@odoo/owl"
const systrayRegistry = registry.category("systray")

const getBoundingClientRect = Element.prototype.getBoundingClientRect

/********************************************************************************
*
          方法 1 : extends
*
*********************************************************************************/
// export class Func01NavBar extends NavBar {

//   setup () {
//     super.setup()
//   }

// }

/********************************************************************************
*
          方發 2 : patch NavBar
*
*********************************************************************************/
patch(NavBar.prototype, {
  setup () {
    super.setup()
  }
})

NavBar.template = "func01.NavBar"
// NavBar.prototype.components = { ...NavBar.components }
