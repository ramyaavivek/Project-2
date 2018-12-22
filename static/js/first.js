var ctx1 = document.getElementById("bubble").getContext('2d');

d3.json("/jobsatisfaction").then(function(d){
  label=d.label;
  data=d.data;
  data = {
    datasets: [{
        data: data,
        
        backgroundColor: ['rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.62)',
        'rgba(255, 206, 86, 0.62)',
        'rgba(75, 192, 192, 0.62)',
        'rgba(153, 102, 255, 0.62)',
        'rgba(255, 159, 64, 0.62)',
        'rgba(255, 159, 147, 0.62)',
        'rgba(244, 84, 63, 0.62)']
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: label
}
var option={"legend":{
"position":"top"},
"fillOpacity":0.4};
var myDoughnutChart = new Chart(ctx1, {
    type: 'doughnut',
    data: data,
    fillOpacity: .3,
    options:option
    
});

});

var c1=document.getElementById("c1");
var c2=document.getElementById("c2");
var c3=document.getElementById("c3");
var c4=document.getElementById("c4");

var p1=document.getElementById("p1");
var p2=document.getElementById("p2");
var p3=document.getElementById("p3");
var p4=document.getElementById("p4");

d3.json("/countries").then(function(d){
    var label=d.label;
    var data=d.data;
    c1.innerHTML=label[0];
    c2.innerHTML=label[1];
    c3.innerHTML=label[2];
    c4.innerHTML=label[3];

    p1.getAttributeNode("style").value="width: "+(data[0]/98000)*100+"%;";
    p2.getAttributeNode("style").value="width: "+(data[1]/98000)*100+"%;";
    p3.getAttributeNode("style").value="width: "+(data[2]/98000)*100+"%;";
    p4.getAttributeNode("style").value="width: "+(data[3]/98000)*100+"%;";

});