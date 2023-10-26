/** @odoo-module **/

import { Counter } from "../src/counter/counter"
import { click, getFixture, mount } from "@web/../tests/helpers/utils"

let target

QUnit.module("Components", (hooks) => {
  hooks.beforeEach(async () => {
    target = getFixture()
  })

  QUnit.module("Counter")

  QUnit.test("Counter is correctly incremented", async (assert) => {

    await mount(Counter, target)

    debugger
    assert.strictEqual(target.querySelector("p[Id=test-p1]").innerHTML, "Counter: 1")

    await click(target, ".btn-primary")

    assert.strictEqual(target.querySelector("p[Id=test-p1]").innerHTML, "Counter: 2")

  })
})
