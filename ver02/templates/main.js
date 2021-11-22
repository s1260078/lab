var numbers = [];

var inputs = document.getElementsByClassName("value");

for (var i = 0; i < inputs.length; i++) {
  const idx = i;
  numbers.push(inputs[i].value);
  inputs[i].addEventListener("change", function(e) {
    numbers[idx] = e.target.value;
    console.log(idx);
    chart.update();
  });
}

var ctx = document.getElementById("mycanvas");
var chart = new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ["n0", "n1", "n2", "n3", "n4", "n5"],
    datasets: [{
      label: 'label here',
      data: numbers,
      borderWidth: 1,
      lineTension: 0.03
    }]
  },
  options: {
    responsiveAnimationDuration: 1000,
    responsive: false,
    scale: {
      ticks: {
        suggestedMin: 0,
        suggestedMax: 15
      }
    }
  }
});