/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar"
import { patch } from "@web/core/utils/patch"

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
