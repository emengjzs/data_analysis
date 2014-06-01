function show(day,num,commodity) {
	var datas = new Array();
	for (var i = 0; i < num.length; i++) {
		var temp = new Array();
		temp.push(Date.UTC(day[i][0],  day[i][1]-1, day[i][2]));
		temp.push(num[i]);
  		datas.push(temp);
	}
	
    $('#container').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: '修正评分走势图'
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
                text: 'Review point'
            },
            min: 0
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%e. %b', this.x) +': '+ this.y +' star';
            }
        },
        
        series: [{
            name: commodity,
            // Define the data points. All series have a dummy year
            // of 1970/71 in order to be compared on the same x axis. Note
            // that in JavaScript, months start at 0 for January, 1 for February etc.
            data: datas
        }]
    });
}