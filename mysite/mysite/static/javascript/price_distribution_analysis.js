function show(count,range) {
	var x = new Array();
	for (var i = 0; i < count.length; i++) {
		var temp = "$"+parseInt(range[i])+"~"+parseInt(range[i+1]);
  		x.push(temp);
	}
	
    $('#container2').highcharts({
        chart: {
            type: 'column',
            margin: [ 50, 50, 100, 80]
        },
        

        title: {
            text: '手机价格分布'
        },
        xAxis: {
            categories: x,
            labels: {
                rotation: -45,
                align: 'right',
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            },
        },
        yAxis: {
            min: 0,
            title: {
                text: '购买人数 (人)'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
    		column: {
       	 	pointWidth: 45,
    		},
		},
        tooltip: {
            pointFormat: '分布<b>{point.y:.1f} 个</b> 手机',
        },
        series: [{
            name: 'Population',
            data: count,
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                x: 4,
                y: 10,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    textShadow: '0 0 3px black'
                }
            }
        }]
    });
}