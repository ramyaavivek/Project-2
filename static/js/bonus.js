var ctx = document.getElementById("flot").getContext('2d');

d3.json("/degrees").then(function(d){
  label=d.label;
  data=d.data;

console.log(label);
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: label,
        datasets: [{
            label: 'Salary',
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

var tcount = document.getElementById("tcount");
var mcount = document.getElementById("mcount");

var fcount = document.getElementById("fcount");
var ocount = document.getElementById("ocount");

d3.json("/gender").then(function(d){
    var label=d.label;
    var data=d.data;
    tcount.innerHTML=data[0];
    fcount.innerHTML=data[2];
    mcount.innerHTML=data[1];
    ocount.innerHTML=data[3];
});

///////////////////////////
// Radar Chart

function buildRadarChart(sel1, sel2) {

    // get data using d3
    d3.json('/codinglanguages').then(d => {
        // log data for verificatiion
        console.log('Coding Language Data');
        console.log(d);

        // hard code the values if one of the selections is the default in the drop down
        if (sel1 == 'Select Developer Type') {
            sel1 = 'Data scientist or machine learning specialist';
        }
        if (sel2 == 'Select Developer Type') {
            sel2 = 'Back-end developer';
        }

        console.log(d[sel1]);

        var dev1= d[sel1];
        var dev2 = d[sel2];

        // use object.enteries and forEach to iterate over each dev data and push the keys to labels list and values to data list
        // define function to format data
        function dataFormatter(ob1, ob2) {
            // define empty lists to hold data and labels
            var data1 = [];
            var labels = [];
            var data2 = [];

            // loop over the input object and push the values to data list and keys to labels list
            Object.entries(ob1).forEach(([key, value]) => {
                labels.push(key);
                data1.push(value);
            });

            // labels are the same for all data
            Object.entries(ob2).forEach(([key, value]) => {
                data2.push(value);
            });

            // dictionary to hold all the lists of data
            var dataDict = {
                            data1: data1,
                            title1: sel1,
                            data2: data2,
                            title2: sel2,
                            labels: labels,
                            };

            return dataDict;
        }

        var langData = {};
        
        langData = dataFormatter(dev1, dev2);

        console.log(langData.data1, langData.data2, langData.labels);

        // All data contained in data object. Let's build the chart!
        var ctxRadar = document.getElementById('radar').getContext('2d');

        var options = {
            scale: {
                // Hides the scale
                // display: false
            }
        };

        var lineTension = 5;

        var myRadarChart = new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: langData.labels,
                datasets: [
                    {
                        data: langData.data1,
                        label: langData.title1,
                        backgroundColor: 'rgba(66, 164, 244, 0.2)',
                        pointHoverBackgroudColor: 'rgba(66, 164, 244, 0.75)',
                        lineTension: lineTension
                        
                    }, 
                    {
                        data: langData.data2,
                        label: langData.title2,
                        backgroundColor: 'rgba(244, 172, 65, 0.2)',
                        pointHoverBackgroudColor: 'rgba(244, 172, 65, 0.75)',
                        lineTension: lineTension
                    },
                ]
            },
            options: options
        });

    })
}

//////////////////
// Initializer

function init() {
    // Grab a reference to both dropdown select element on radar chart section
    var selector1 = d3.select("#selDev1");
    var selector2 = d3.select('#selDev2');
    var selectors = [selector1, selector2];
    // Start with a default search value
    var devTypes = [];
    var defaultStr = 'Select Developer Type';

    // Initial values fo rthe options list are "Select Developer Type"
    selector1.append('option').text(defaultStr).property('value', defaultStr);
    selector2.append('option').text(defaultStr).property('value', defaultStr);

    // get the keys from /codinglaguages. The keys are the devtypes
    d3.json('/codinglanguages').then((d) => {
      Object.keys(d).forEach(devType => {
        console.log(devType);
        devTypes.push(devType);
        
        // Populate both menus using a for loop
        for (var i=0; i<selectors.length;i++) {
            selectors[i]
                .append("option")
                .text(devType)
                .property("value", devType);
        }
      });
  
      // Use the first sample from the list to build the initial plots
      const dev1 = devTypes[3];
      const dev2 = devTypes[0];

      buildRadarChart(dev1, dev2);

    });
  }

  function radarOptionChanged1(devType1) {
    // select the text from the other drop down menu
    const devType2 = d3.select('#selDev2 option:checked').text();
    // Fetch new data each time a new sample is selected
    buildRadarChart(devType1, devType2);
  }

  function radarOptionChanged2(devType2) {
    // select the text from the other drop down menu
    const devType1 = d3.select('#selDev1 option:checked').text();
    // Fetch new data each time a new sample is selected
    buildRadarChart(devType1, devType2);
  }

  init();

