Vue.options.delimiters = ["[[", "]]"];

var app_vuetify = new Vue({ 
  el: '#app',
  data: {
    message: 'test',
    picked: null,
    toggle: null,
    chosen_board: null,
    boolean:null,
    color: null,
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



