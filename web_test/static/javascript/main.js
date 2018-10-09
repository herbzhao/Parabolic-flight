Vue.options.delimiters = ["[[", "]]"];

new Vue({
    el: '#app',
    data: () => ({
      drawer: null,
      serial_command: '',
      chosen_arduino_board: '',
      arduino_boards: ['parabolic', 'waterscope', 'fergboard'],
      led_switch: true
    })
  })