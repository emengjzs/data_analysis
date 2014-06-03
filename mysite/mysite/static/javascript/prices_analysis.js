function show(day,max_in,min_in,avg_in,commodity) {
	var maxList = new Array();
	var minList = new Array();
	var avgList = new Array();
	for (var i = 0; i < day.length; i++) {
		var temp1 = new Array();
		temp1.push(Date.UTC(day[i][0],  day[i][1], day[i][2]));
		temp1.push(max_in[i]);
  		maxList.push(temp1);
		var temp2 = new Array();
		temp2.push(Date.UTC(day[i][0],  day[i][1], day[i][2]));
		temp2.push(min_in[i]);
  		minList.push(temp2);
		var temp3 = new Array();
		temp3.push(Date.UTC(day[i][0],  day[i][1], day[i][2]));
		temp3.push(avg_in[i]);
  		avgList.push(temp3);
	}
	
    $('#container2').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: '商品价格走势'
        },
		subtitle: {
			text: commodity
		},
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                millisecond: '%H:%M:%S.%L',
				second: '%H:%M:%S',
				minute: '%H:%M',
				hour: '%H:%M',
				day: '%e. %b',
				week: '%e. %b',
				month: '%b \'%y',
				year: '%Y'
            }
        },
        yAxis: {
            title: {
                text: 'price (dollars)'
            },
            min: 0
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y + 'dollars';
            }
        },
        
        series: [{
            name: '最大价格走势',
            data: maxList
        },{
            name: '最小价格走势',
            data: minList
        },{
            name: '平均价格走势',
            data: avgList
        }]
    });
}