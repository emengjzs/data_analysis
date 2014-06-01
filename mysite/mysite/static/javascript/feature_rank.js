function show(x,y) {

	$('#feature-polar').highcharts({
	            
	    chart: {
	        polar: true,
	        type: 'area'
	    },
	    
	    title: {
	        text: false,
	    },
	    
	    pane: {
	    	size: '85%'
	    },
	    
	    xAxis: {
	        categories: x,
	        tickmarkPlacement: 'on',
	        lineWidth: 0,
		
	    },
	        
	    yAxis: {
	        //gridLineInterpolation: 'polygon',
	        lineWidth: 0,
	        min: 0,
		max: 100
	    },
	    
	    tooltip: {
	    	shared: true,
	        pointFormat: '优于<b>{point.y:,.0f}%</b>的手机<br/>'
	    },
		
		legend: false,
	    
	    series: [{
	        name: '参数',
	        data: y,
	        pointPlacement: 'on'
	    }]
	
	});
}