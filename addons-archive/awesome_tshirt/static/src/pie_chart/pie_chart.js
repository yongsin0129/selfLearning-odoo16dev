/** @odoo-module */

import { xml, Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl"

import { loadJS } from "@web/core/assets"
import { getColor } from "@web/views/graph/colors"


export class PieChart extends Component {
  setup () {
    this.canvasRef = useRef("canvas")

    this.labels = Object.keys(this.props.data)
    this.data = Object.values(this.props.data)
    this.color = this.labels.map((_, index) => {
      return getColor(index)
    })

    onWillStart(() => {
      return loadJS(["/web/static/lib/Chart/Chart.js"])
    })

    onMounted(() => {
      this.renderChart()
    })

    onWillUnmount(() => {
      if (this.chart) {
        this.chart.destroy()
      }
    })

  }

  onPieClick (ev, chartElem) {
    if (!chartElem[0]) return

    const clickedIndex = chartElem[0]._index
    this.props.onPieClick(this.labels[clickedIndex])
  }

  renderChart () {
    if (this.chart) {
      this.chart.destroy()
    }
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: this.labels,
        datasets: [
          {
            label: this.env._t(this.props.label),
            data: this.data,
            backgroundColor: this.color,
          },
        ],
      },
      options: {
        onClick: this.onPieClick.bind(this),
      },
    })
  }
}

PieChart.template = xml/* xml */`
    <div>
        <div t-att-class="'h-100 ' + props.class" t-ref="root">
            <div class="h-100 position-relative" t-ref="container">
                <canvas t-ref="canvas" />
            </div>
        </div>
    </div>
`
PieChart.props = {
  data: { type: Object },
  label: { type: String },
  onPieClick: { type: Function },
}