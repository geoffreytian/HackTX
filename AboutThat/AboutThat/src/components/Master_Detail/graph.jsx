import React, { Component } from "react";
import { Bar } from 'react-chartjs-2';

class Graph extends Component {
	constructor(props) {
		super(props);

		this.state = {
			chartData: this.props.data
		}

		console.log(this.props.data);
	}


	render() {
		return (
			<div style={{position: 'relative', left: '15%', width: '70%', color: 'white', fontFamily: 'PT Sans Narrow'}}>
				<Bar data={this.props.data} height={300} width={150} options={{	maintainAspectRatio: false,
																						responsive: true,
																						legend: {
																							display: false,
																							position: 'bottom'
																						},
																						hover: {
																							mode: 'label'
																						},
																						scales: {
																							xAxes: [{
																									display: true,
																									ticks: {
																										fontSize: 18,
																										fontColor: "whitesmoke"
																									},
																									gridLines: {
																										display: true,
																										color: "white",
																										lineWidth: 0.5
																									  },
																								}],
																							yAxes: [{
																									display: true,
																									ticks: {
																										beginAtZero: true,
																										max: 1
																									},
																									gridLines: {
																										display: true,
																										color: "white",
																										lineWidth: 0.5
																									  }
																								}]
																						},
																						title: {
																							display: true,
																							text: 'Sentiment by Source',
																							fontSize: '24',
																							fontFamily: 'PT Sans Narrow',
																							fontColor: "whitesmoke"
																						}
            }} />
			</div>
			
		)
	}
}

export default Graph;
