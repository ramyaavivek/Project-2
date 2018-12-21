var ctx = document.getElementById("myChart").getContext('2d');
var label;
var data;
d3.json("/degrees").then(function(d){
  label=d.label;
  data=d.data;

console.log(label);
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: label,
        datasets: [{
            label: 'Salary drawn by undergrad major',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 159, 147, 0.2)',
                'rgba(244, 84, 63, 0.2)',
                'rgba(103, 84, 63, 0.2)',
                'rgba(145, 30, 63, 0.2)',
                'rgba(145, 23, 233, 0.2)',
                'rgba(66, 233, 19, 0.2)'

            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 159, 147, 1)',
                'rgba(244, 84, 63, 1)',
                'rgba(103, 84, 63, 1)',
                'rgba(145, 30, 63, 1)',
                'rgba(66, 233, 19, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
})});;