Vue.options.delimiters = ["[[", "]]"];


var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  },
})

var app2 = new Vue({
  el: '#user_input',
  data: {
    message: 'Hello Vue.js input!'
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')
    }
  }
})



var app3 = new Vue({
  el: '#axios_examples',
  data() {
    return {
      info: null
    }
  },

  methods: {
    read_api: function () {
      axios.get('/window_rest').then(response => (this.info = response.data))
    },
    stop_interval: function () {
      clearInterval(this.interval_loop)
      this.ispaused = true
    },
    start_interval: function () {
      this.interval_loop = setInterval(function () {
        this.read_api()
      }.bind(this), 100)
      this.ispaused = false
    },
    toggle_interval: function () {
      if (this.ispaused == true) {
        this.start_interval()
      } else if (this.ispaused == false) {
        this.stop_interval()
      }
    }
  },

  mounted() {
    this.read_api()
    this.start_interval()
    this.ispaused = false
  },
})





// NOTE: below is how we draw the graph
var layout = {
  xaxis: {
    title: 'time',
    },
  yaxis: {
    title: 'temperature',
  }
}

// generates a bare plot
Plotly.newPlot('chart', [{
  x: [],
  y: [],
}], layout = layout);

// update the value from axios
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
// https://hashnode.com/post/how-can-i-use-the-data-of-axioss-response-outside-cj2yddlhx003kcfk8h8czfo7k
function getData() {
  axios.get('/window_rest').then(response => {
    time = response.data.x
    temp = response.data.y
    real_time_plotting(time, temp)
  })
}

function real_time_plotting(x_value, y_value) {
  Plotly.extendTraces('chart', {
    x: [
      [x_value]
    ],
    y: [
      [y_value]
    ]
  }, [0]);

  window_size = 100
  // automatically adjust the window range - scrolling
  if (x_value > window_size) {
    Plotly.relayout('chart', {
      xaxis: {
        range: [x_value - window_size, x_value],
        title: 'time',
      }
    });
  }

}

// plot with intervals
setInterval(function () {
  getData()
}, 200);