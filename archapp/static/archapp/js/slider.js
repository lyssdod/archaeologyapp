$( window ).load(function() {
var centuries = {
  // TODO:
  // move this data to fixtures

}
$(function() {
  $( "#slider" ).slider({
    range: true,
  min: 1,
  max: 9,
  values: [ 3, 8],

  slide: function( event, ui ) {
    var val1 = ui.values[0];
    var val2 = ui.values[1];

    $( "#id_datingfrom" ).val(val1);
    $( "#id_datingto" ).val(val2);
    $( "#dating" ).html(val1 + " - " + val2);
  }
  });
});
//$('#slider').toggle('slide');
//$('#slider').show();
});
