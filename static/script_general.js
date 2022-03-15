actualiserDonnees();

let bool_general_line=0; //booleen pour reconnaitre le line chart de general_line

function actualiserDonnees(){	
	
//*****************************cartes************************************ */
	//total etudiants
	httpRequest_general_carte_nbrT = new XMLHttpRequest();	
	httpRequest_general_carte_nbrT.open('GET', '/api/general-nbrTotal');
	httpRequest_general_carte_nbrT.onreadystatechange = function () {
		if (httpRequest_general_carte_nbrT.readyState === 4 && httpRequest_general_carte_nbrT.status === 200) {
			json_general_carte_nbrT = JSON.parse(httpRequest_general_carte_nbrT.response);
			general_carte(json_general_carte_nbrT,0);			
		}
	};
	httpRequest_general_carte_nbrT.send();


	//nbr filles
	httpRequest_general_carte_nbrF = new XMLHttpRequest();	
	httpRequest_general_carte_nbrF.open('GET', '/api/general-nbrFilles');
	httpRequest_general_carte_nbrF.onreadystatechange = function () {
		if (httpRequest_general_carte_nbrF.readyState === 4 && httpRequest_general_carte_nbrF.status === 200) {
			json_general_carte_nbrF = JSON.parse(httpRequest_general_carte_nbrF.response);
			general_carte(json_general_carte_nbrF,1);			
		}
	};
	httpRequest_general_carte_nbrF.send();

	//nbr garcons
	httpRequest_general_carte_nbrG = new XMLHttpRequest();	
	httpRequest_general_carte_nbrG.open('GET', '/api/general-nbrGarcons');
	httpRequest_general_carte_nbrG.onreadystatechange = function () {
		if (httpRequest_general_carte_nbrG.readyState === 4 && httpRequest_general_carte_nbrG.status === 200) {
			json_general_carte_nbrG = JSON.parse(httpRequest_general_carte_nbrG.response);
			general_carte(json_general_carte_nbrG,2);			
		}
	};
	httpRequest_general_carte_nbrG.send();



//*****************************BAR chart************************************ */	
	httpRequest_Bar_nbrEtudAn = new XMLHttpRequest();	
	httpRequest_Bar_nbrEtudAn.open('GET', '/api/general-BAR-nbrEtudAn');
	httpRequest_Bar_nbrEtudAn.onreadystatechange = function () {
		if (httpRequest_Bar_nbrEtudAn.readyState === 4 && httpRequest_Bar_nbrEtudAn.status === 200) {
			jsonData_Bar_nbrEtudAn = JSON.parse(httpRequest_Bar_nbrEtudAn.response);
			general_Bar_nbrEtudAn(jsonData_Bar_nbrEtudAn);
		   		
		}
	};
	httpRequest_Bar_nbrEtudAn.send();

	
	//*****************************LINE chart************************************ */

	httpRequest_LINE_nbrEtudSpe = new XMLHttpRequest();	
	httpRequest_LINE_nbrEtudSpe.open('GET', '/api/general-LINE-nbrEtudSpe');
	httpRequest_LINE_nbrEtudSpe.onreadystatechange = function () {
		if (httpRequest_LINE_nbrEtudSpe.readyState === 4 && httpRequest_LINE_nbrEtudSpe.status === 200) {
			jsonData_LINE_nbrEtudSpe = JSON.parse(httpRequest_LINE_nbrEtudSpe.response);
			bool_general_line=0;
			general_Line(jsonData_LINE_nbrEtudSpe);
		}
	};
	httpRequest_LINE_nbrEtudSpe.send();


	httpRequest_LINE_MoyAnSpe = new XMLHttpRequest();	
	httpRequest_LINE_MoyAnSpe.open('GET', '/api/general-LINE-MoyAnSpe');
	httpRequest_LINE_MoyAnSpe.onreadystatechange = function () {
		if (httpRequest_LINE_MoyAnSpe.readyState === 4 && httpRequest_LINE_MoyAnSpe.status === 200) {
			jsonData_LINE_MoyAnSpe = JSON.parse(httpRequest_LINE_MoyAnSpe.response);
			bool_general_line=1;
			general_Line(jsonData_LINE_MoyAnSpe);
		}
	};
	httpRequest_LINE_MoyAnSpe.send();

		
	//*****************************RADAR chart************************************ */

	httpRequest_radar = new XMLHttpRequest();	
	httpRequest_radar.open('GET', '/api/general-radar');
	httpRequest_radar.onreadystatechange = function () {
		if (httpRequest_radar.readyState === 4 && httpRequest_radar.status === 200) {
			jsonData_radar = JSON.parse(httpRequest_radar.response);
			general_radar(jsonData_radar);
		}
	};
	httpRequest_radar.send();


	
}

//----------------------------------------------------------------------------cartes------------------------------------------------------------------------------ */
function general_carte(jsonData,j){	
	let label_nom=["Nombre total d'étudiants", "Nombre de femmes","Nombre d'hommes"];
	
	if(j==0){
		//afficher le nombre total d'etudiants	
		carte = document.getElementById("carte"+(j+1));		
		label = carte.getElementsByClassName("carteLabel")[0];
		nbr = carte.getElementsByClassName("carteNbr")[0];
	
		label.innerText = label_nom[j]; 
		nbr.innerText = jsonData[0]["nbrTotal"];
	}
	else if(j==1){ //afficher le nombre de filles
		carte = document.getElementById("carte"+(j+1));		
		label = carte.getElementsByClassName("carteLabel")[0];
		nbr = carte.getElementsByClassName("carteNbr")[0];
	
		label.innerText = label_nom[j]; 
		nbr.innerText = jsonData[0]["nbrFilles"];
	
	}
	else if(j==2){ //afficher le nombre de garcons
		carte = document.getElementById("carte"+(j+1));		
		label = carte.getElementsByClassName("carteLabel")[0];
		nbr = carte.getElementsByClassName("carteNbr")[0];
	
		label.innerText = label_nom[j]; 
		nbr.innerText = jsonData[0]["nbrGarcons"];
	}
	
	
}

//------------------------------------------------------------------------ bar------------------------------------------------------------------------------------- */
function general_Bar_nbrEtudAn(jsonData){	

	var labels = jsonData.map(function(e) {
	   return e.annee;
	});
	
	var data = jsonData.map(function(e) {
	   return e.Nombre_etudiants_par_an;
	});
	
	
	new Chart(document.getElementById("Bar_nbrEtudAn"), {
		type: 'bar',
		data: {
		  labels: labels,
		  datasets: [
			{
			  backgroundColor: ["#b47c4b","#561d18", "#171e13"],
			  data: data
			}
		  ]
		},
		options: {
		  responsive: false,
		  maintainAspectRatio: true,	
		  legend: { display: false },
		  
		}
	});
}

//------------------------------------------------------------------------- line ---------------------------------------------------------------------------------- */
function general_Line(jsonData){
	var labels = jsonData.annee;
    let backgroundColor=["#82a170","#424b35", "#9f7453","#d02a2a","#42281c", "#9e9d99","#d6834f"];
	
	var i=0,j=6;
			
	
	var data = jsonData.datasets;

	if(bool_general_line==1) //dans le cas ou il faut afficher le MoyAnSpe line chart
	{   
		for(d of jsonData.datasets){

			d.borderColor = backgroundColor[i]; i++;
			d.fill = false;				  
						
		}	
		
		new Chart(document.getElementById("general_line_moyAnSpe"), {
			type: 'line',
			data: {
				labels: labels,
				datasets: data
			},
			options: {						
				responsive: false,
				maintainAspectRatio: true,
				legend:{
					position:'right'
				}
			}
		});
	}
	else{ //dans le cas ou il faut afficher le NbrEtudAn line chart
		
		for(d of jsonData.datasets){

			d.borderColor = backgroundColor[j]; j--;
			d.fill = false;				  
						
		}	
		
		new Chart(document.getElementById("general_line_nbrEtudSpe"), {
			type: 'line',
			data: {
				labels: labels,
				datasets: data
			},
			options: {						
				responsive: false,
				maintainAspectRatio: true,
				legend:{
					position:'bottom'
				}
			}
		});
	}
}

//------------------------------------------------------------------------- Radar ---------------------------------------------------------------------------------- */
function general_radar(jsonData){
	var label=jsonData.specialite;
	var data_json = jsonData.datasets;
	let borderColor=["#9f7453","#a83b24"];
	let backgroundColor=["#9f745390","#a83a2491"]
	
	var i=0;
	for(d of jsonData.datasets){

		d.backgroundColor = backgroundColor[i]; 
		d.borderColor = borderColor[i]; 
		d.pointBorderColor="#fff"
		d.pointHoverBackgroundColor="#fff"
		d.fill = true;
					  
		i++;			
	}

	const data = {
		labels: label,
		datasets: data_json
	};

	new Chart(document.getElementById("general_radar"), {
		type: 'radar',
		data: data,
		options: {
		  responsive:false,
		  elements: {
			line: {
			  borderWidth: 3
			}
		  }
		},
	  });

}

