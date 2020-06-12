'use strict';



//region show__
const showData= function(data){
    console.log(data.status);

    let converted_labels =[];
    let converted_data = [];
    for (const snelheid of data.status) {
        let datumsub = snelheid.Datum;
        let correctedatum = datumsub.substring(5, 22);
        console.log(correctedatum);
        converted_labels.push(correctedatum);
        converted_data.push(snelheid.Waarde);
    }
    console.log(converted_data);
    drawChart(converted_labels,converted_data);
};

const showOvertredingen= function(data){
    console.log(data.status);
    
    let converted_labels =[];
    let converted_data = [];
    for (const snelheid of data.status) {
        let datumsub = snelheid.Datum;
        let correctedatum = datumsub.substring(5, 22);
        console.log(correctedatum);
        converted_labels.push(correctedatum);
        converted_data.push(snelheid.Waarde);
    }
    console.log(converted_data);
    drawOvertredingen(converted_labels,converted_data);
};
//endregion
const drawChart = function(labels, snelheid){
    let ctx= document.getElementById('myChart').getContext('2d');
    let config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Snelheid',
                    backgroundColor: 'white',
                    borderColor: 'red',
                    data: snelheid,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Snelheidshistoriek'
            },
            tooltips:{
                mode: 'index',
                intersect: true
            },
            hover:{
                mode: 'nearest',
                intersect: true
            },
            scales:{
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Tijd'
                        },
                        ticks: {
                            maxRotation: 90
                          }
                    }
                ],
                yAxes:[
                    {
                        display: true,
                        scaleLabel:{
                            display: true,
                            labelString: 'Snelheid'
                        }
                    }
                ]
            }
        }
    };
    let myChart = new Chart(ctx, config);
};

const drawOvertredingen = function(labels, snelheid){
    let ctx= document.getElementById('ChartOvertreding').getContext('2d');
    /* let datumsub = labels;
    console.log(datumsub)
    let correctedatum = datumsub.substring(5, 25); */

    let config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Snelheid',
                    backgroundColor: 'white',
                    borderColor: 'red',
                    data: snelheid,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Overtredingshistoriek'
            },
            tooltips:{
                mode: 'index',
                intersect: true
            },
            hover:{
                mode: 'nearest',
                intersect: true
            },
            scales:{
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Tijd'
                        },
                        ticks: {
                            maxRotation: 90
                          }
                    }
                ],
                yAxes:[
                    {
                        display: true,
                        scaleLabel:{
                            display: true,
                            labelString: 'Snelheid'
                        }
                    }
                ]
            }
        }
    };
    let myChart = new Chart(ctx, config);
};

//region get__
const getSensorData = function(){
    handleData('http://192.168.1.22:5000/api/v1/metingen',showData);
}
const getOvertreding = function(){
    handleData('http://192.168.1.22:5000/api/v1/overtredingen',showOvertredingen);
}
//endregion

//region DOMContentloaded
const init = function(){
    console.info('init geladen');
    getSensorData();
    getOvertreding();
};

document.addEventListener('DOMContentLoaded', function(){
    console.info('DOM geladen');
    init();
});
//endregion