Vue.options.delimiters = ["[[", "]]"];

var app = new Vue({
  el: '#app',
  data: () => ({
    serial_command: '',
    chosen_arduino_board: 'parabolic',
    arduino_boards: ['parabolic', 'waterscope', 'fergboard'],
    LED_switch: null,
    recording_switch: null,
    config_update_switch: null,
    timelapse_switch: null,
    timelapse_interval: 10,
    message: 'test vue',
    stream_type: 'PiCamera',
    zoom: 1,
  }),

    // watch when data change 
    watch: {
      zoom: function(newzoom, oldzoom) {
        this.change_zoom()
      }
    },

  methods: {
    toggle_LED: function () {
      setTimeout(() => {
        if (this.LED_switch == null) {
          console.log('turn off')
        } else if (this.LED_switch == "led_on") {
          console.log('turn on')
        }
      }, 50);
    },
    toggle_recording: function () {
      setTimeout(() => {
        if (this.recording_switch == null) {
          console.log('video recording off')
        } else if (this.recording_switch == "recording") {
          console.log('video recording on')
        }
      }, 10);
    },
    toggle_config_update: function () {
      setTimeout(() => {
        if (this.config_update_switch == "config_updating") {
          console.log('updating config')
        } else if (this.config_update_switch == null) {
          console.log('stop updating config')
        }
      }, 10);
    },
    toggle_timelapse: function () {
      setTimeout(() => {
        if (this.timelapse_switch == 'waterscope_timelapse') {
          console.log('Starting waterscope timelapse')
        } else if (this.timelapse_switch == 'timelapse') {
          console.log('Starting timelapse')
        }
        else if (this.timelapse_switch == null){
          console.log('stop timelapse')
        }
      }, 10);
    },
    send_serial_command: function () {
      console.log(this.chosen_arduino_board + this.serial_command)
    },
    toggle_stream: function () {
      // DEBUG: a tiny delay is required for the toggle buttons
      setTimeout(() => {
        if (this.stream_type == null){
          this.stream_type = 'PiCamera'
        }
        console.log(this.stream_type)

      }, 10);

    },
    change_zoom () {
      console.log(this.zoom)
    },

  },

})