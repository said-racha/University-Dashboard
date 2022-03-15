actualiserDonnees_spe1();

////////////////SPECIALITE_1/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function actualiserDonnees_spe1(){
	
	//*****************************GroupedBar************************************ */
	httpRequest_spe_GroupedBar1 = new XMLHttpRequest();	
	httpRequest_spe_GroupedBar1.open('GET', '/api/spe-GroupedBar1');
	httpRequest_spe_GroupedBar1.onreadystatechange = function () {
		if (httpRequest_spe_GroupedBar1.readyState === 4 && httpRequest_spe_GroupedBar1.status === 200) {
			jsonData_spe_GroupedBar1 = JSON.parse(httpRequest_spe_GroupedBar1.response);
			spe_GroupedBar(jsonData_spe_GroupedBar1);
		}
	};
	httpRequest_spe_GroupedBar1.send();
	
	//*****************************cartes************************************ */
	httpRequest_spe_carteMoy1 = new XMLHttpRequest();	
	httpRequest_spe_carteMoy1.open('GET', '/api/spe-CarteMoy1');
	httpRequest_spe_carteMoy1.onreadystatechange = function () {
		if (httpRequest_spe_carteMoy1.readyState === 4 && httpRequest_spe_carteMoy1.status === 200) {
			jsonData_spe_carteMoy1= JSON.parse(httpRequest_spe_carteMoy1.response);
			spe_carteMoy1(jsonData_spe_carteMoy1);
		}
	};
	httpRequest_spe_carteMoy1.send();
	


	//***************************** PIE ************************************ */
	//afficher par defaut le plus recent (soit celui de 2021)
	httpRequest_spe_admis1 = new XMLHttpRequest();	
	httpRequest_spe_admis1.open('GET', '/api/spe-admis1-2021');
	httpRequest_spe_admis1.onreadystatechange = function () {
		if (httpRequest_spe_admis1.readyState === 4 && httpRequest_spe_admis1.status === 200) {
			jsonData1 = JSON.parse(httpRequest_spe_admis1.response);
			spe_admis1(jsonData1,2021);
		}
	};
	httpRequest_spe_admis1.send();

}

//PIE-2019
function btn_spe_admis1_2019()
{   httpRequest_spe_admis1 = new XMLHttpRequest();	
	httpRequest_spe_admis1.open('GET', '/api/spe-admis1-2019');
	httpRequest_spe_admis1.onreadystatechange = function () {
		if (httpRequest_spe_admis1.readyState === 4 && httpRequest_spe_admis1.status === 200) {
			jsonData1 = JSON.parse(httpRequest_spe_admis1.response);
			spe_admis1(jsonData1,2019);
		}
	};
	httpRequest_spe_admis1.send();
}

//PIE-2020
function btn_spe_admis1_2020()
{   httpRequest_spe_admis1 = new XMLHttpRequest();	
	httpRequest_spe_admis1.open('GET', '/api/spe-admis1-2020');
	httpRequest_spe_admis1.onreadystatechange = function () {
		if (httpRequest_spe_admis1.readyState === 4 && httpRequest_spe_admis1.status === 200) {
			jsonData1 = JSON.parse(httpRequest_spe_admis1.response);
			spe_admis1(jsonData1,2020);
		}
	};
	httpRequest_spe_admis1.send();
}

//PIE-2021
function btn_spe_admis1_2021()
{   httpRequest_spe_admis1 = new XMLHttpRequest();	
	httpRequest_spe_admis1.open('GET', '/api/spe-admis1-2021');
	httpRequest_spe_admis1.onreadystatechange = function () {
		if (httpRequest_spe_admis1.readyState === 4 && httpRequest_spe_admis1.status === 200) {
			jsonData1 = JSON.parse(httpRequest_spe_admis1.response);
			spe_admis1(jsonData1,2021);
		}
	};
	httpRequest_spe_admis1.send();
}



function spe_carteMoy1(jsonData){	
	var i=1;
	for(d of jsonData){		
		carte = document.getElementById("spe_carte"+i);	
		
		label = carte.getElementsByClassName("spe1_carteLabel")[0];
		pop = carte.getElementsByClassName("spe1_carteNbr")[0];
		
		label.innerText = d["annee"];
		pop.innerText = d["moyennePromoSpe"];
		
		i++;
	}
	
	
}


function spe_admis1(jsonData,j){
	var labels = jsonData.map(function(e) {
		return e.passage;            
	 });
	 
	 var data = jsonData.map(function(e) {
		return e.nombre_etudiants;
	 });

	 if(j==2019)
	{	
		carte = document.getElementById("spe_carteNbrEtud");	
		
		
		label = carte.getElementsByClassName("spe_carteNbrEtud_Label")[0];
		pop = carte.getElementsByClassName("spe_carteNbrEtud_Nbr")[0];
		
		label.innerText = "Nombre d'étudiants";
		pop.innerText = parseInt(data[0])+parseInt(data[1]);


		new Chart(document.getElementById("spe_admis1"), {
			type: 'pie',
			data: {
			labels: labels,
			datasets: [{
				backgroundColor: ["#561d18","#b47c4b"],
				data: data
			}]
			},
			options: {
			responsive: false,
			maintainAspectRatio: true,
			title: {
				display: true,
				text: "Nombre d'étudiants admis et ajournés en 2019"
			},
			legend:{
				position:'bottom'
			}
			}
		});	
	}
	else if(j==2020)
	{
		carte = document.getElementById("spe_carteNbrEtud");	
		
		
		label = carte.getElementsByClassName("spe_carteNbrEtud_Label")[0];
		pop = carte.getElementsByClassName("spe_carteNbrEtud_Nbr")[0];
		
		label.innerText = "Nombre d'étudiants";
		pop.innerText = parseInt(data[0])+parseInt(data[1]);


		new Chart(document.getElementById("spe_admis1"), {
			type: 'pie',
			data: {
			labels: labels,
			datasets: [{
				backgroundColor: ["#561d18","#b47c4b"],
				data: data
			}]
			},
			options: {
			responsive: false,
			maintainAspectRatio: true,
			title: {
				display: true,
				text: "Nombre d'étudiants admis et ajournés en 2020"
			},
			legend:{
				position:'bottom'
			}
			}
		});	
	}
	else if(j==2021)
	{
		carte = document.getElementById("spe_carteNbrEtud");	
		
		
		label = carte.getElementsByClassName("spe_carteNbrEtud_Label")[0];
		pop = carte.getElementsByClassName("spe_carteNbrEtud_Nbr")[0];
		
		label.innerText = "Nombre d'étudiants";
		pop.innerText = parseInt(data[0])+parseInt(data[1]);


		new Chart(document.getElementById("spe_admis1"), {
			type: 'pie',
			data: {
			labels: labels,
			datasets: [{
				backgroundColor: ["#561d18","#b47c4b"],
				data: data
			}]
			},
			options: {
			responsive: false,
			maintainAspectRatio: true,
			title: {
				display: true,
				text: "Nombre d'étudiants admis et ajournés en 2021"
			},
			legend:{
				position:'bottom'
			}
			}
		});	
	}
}




function spe_GroupedBar(jsonData){
	var ctx = document.getElementById("spe_GroupedBar").getContext("2d");

	var labels = jsonData.annee;
	var data = jsonData.datasets;
	
	let backgroundColor=["#82a170","#424b35"];
	var i=0;

	for(d of jsonData.datasets){

		d.backgroundColor = backgroundColor[i]; i++;
					
	}

	var data = {
		labels:labels,
		datasets: data
	};

	var myBarChart = new Chart(ctx, {
		type: 'bar',
		data: data,
		options: {
			responsive:false,
			barValueSpacing: 20,
			
			scales: {
				yAxes: [{
					ticks: {
						min: 0,
					}
				}]
			}
		}
	});
	
}


