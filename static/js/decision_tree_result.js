$(document).ready(function(){

	$('get_error_result_id').on('click',function(){
		  $.ajax({
		    type: 'GET',
		    url: '/api/decision_tree_data',
		    success: function (data) {
		      var received_json = JSON.parse(data);
		      $('result_info_id').text(received_json['accuracy_info']);
		      original_p_list = received_json['original_p_list'];
		      improved_p_list = received_json['improved_p_list'];
		      o_list = received_json['o_list'];
		      draw_line_chart(original_p_list,improved_p_list,o_list);
		    }
		  });
	});
	// these functions should be moved into decision tree vis js
	function draw_line_chart(o_p_list,i_p_list,o_list){
		// prepare dataset
		var data_array = [['original_p_list','improved_p_list','o_list']];
		for(var i=0; i< o_p_list.length; i++){
			data_array.push([o_p_list[i],i_p_list[i],o_list[i]]);	
		}
		

		google.charts.load('current', {'packages':['corechart']});
		google.charts.setOnLoadCallback(drawChart);

		function drawChart() {
	        var data = google.visualization.arrayToDataTable(data_array);
			var options = {
	          title: 'Predication VS Obervation',
	          curveType: 'function',
	          legend: { position: 'bottom' }
	        };

	        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

	        chart.draw(data, options);
	    }

	}
	


});

