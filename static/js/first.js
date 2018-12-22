var ctx1 = document.getElementById("bubble").getContext('2d');

d3.json("/jobsatisfaction").then(function(d){
  label=d.label;
  data=d.data;
  data = {
    datasets: [{
        data: data,
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#42e913","#8b6013","#8b60c5"]
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: label
}
var option={"legend":{"position":"right",
"position":"top"}};
var myDoughnutChart = new Chart(ctx1, {
    type: 'doughnut',
    data: data,
    options:option
    
});

});