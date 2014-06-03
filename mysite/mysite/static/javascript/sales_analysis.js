function show(day,num,commodity) {
	var datas = new Array();
	for (var i = 0; i < num.length; i++) {
		var temp = new Array();
		var myDate=new Date();
		temp.push(Date.UTC(day[i][0],  day[i][1]-1));
		temp.push(num[i]);
  		datas.push(temp);
	}
	
    $('#container1').highcharts({
        chart: {
            type: 'spline'
        },
        title: {
           text: '商品总评论数走势图'
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
				day: '%Y  %b',
				week: '%e. %b',
				month: '%Y  %b',
				year: '%Y  %b'
            }
        },
        yAxis: {
            title: {
                text: 'Review count'
            },
            min: 0
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%Y.%b', this.x) +': '+ this.y;
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