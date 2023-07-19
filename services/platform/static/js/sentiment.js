$(document).ready(function() {
    var ctx = document.getElementById("sentimentsChart");

    var dataValues = cntValues;
    var dataLabels = [1,2,3,4,5];
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataLabels,
        datasets: [{
          data: dataValues,
          backgroundColor: 'rgb(0, 153, 153, 1)',
        }]
      },
      options: {
        title: {
            display: true,
            text: 'Number of reviews per score',
         },
        scales: {
          x: {
            title : {
                display: true,
                text: "Score given"
            },
            display: true
          },
          y: {
            title : {
                display: true,
                text: "# of reviews"
            },
            ticks: {
              beginAtZero:true
            }
          }
        },
        plugins: {
            legend: {
                display: false
            }
        }
      }
    });

 });