$( window ).load(function() {
var centuries = {
  // TODO:
  // move this data to fixtures
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
    var val1 = centuries[ui.values[0]];
    var val2 = centuries[ui.values[1]];

    $( "#id_datingfrom" ).val(val1);
    $( "#id_datingto" ).val(val2);
    $( "#dating" ).html(val1 + " - " + val2);
  }
  });
});
//$('#slider').toggle('slide');
//$('#slider').show();
});
