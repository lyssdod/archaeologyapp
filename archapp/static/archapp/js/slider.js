$( window ).load(function() {
var centuries = {
  "1" : "VIII BCE",
  "2" : "VII BCE",
  "3" : "VI BCE",
  "4" : "V BCE",
  "5" : "IV BCE",
  "6" : "III BCE", 
  "7": "II BCE",
  "8" : "I BCE",
  "9" : "I CE"
}
$(function() {
  $( "#slider" ).slider({
    range: true,
  min: 1,
  max: 9,
  values: [ 3, 8],

  slide: function( event, ui ) {
    var val1 = ui.values[0]
    var val2 = ui.values[1]
    $( "#id_dating" ).val(centuries[val1] + " - " + centuries[val2]);
  }
  });
  $( "#id_dating" ).val( $( "#slider-range" ).slider( "values", 3 ) +
    $( "#slider-range" ).slider( "values", 8 ) );
});

});
