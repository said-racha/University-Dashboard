# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask import redirect
from flask import jsonify
import json


from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] 	  = 'localhost'
app.config['MYSQL_DATABASE_PORT'] 	  = 3306
app.config['MYSQL_DATABASE_USER'] 	  = 'pravan_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pravan2021'
app.config['MYSQL_DATABASE_DB'] 	  = 'db_university'


mysql.init_app(app)

app = Flask(__name__)


@app.route('/')
def bienvenue():
	return render_template('Bienvenue-SAID.html')

#------------------------------------------------------GENERAL-----------------------------------------------
@app.route('/dashboard-SAID')
def dashboard():
	return render_template('Dashboard-SAID.html')



#********************cartes nbr etudiants ***************

#----------nbr total
@app.route('/api/general-nbrTotal')
def general_NbrTotal():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select count(DISTINCT matricule,nom,prenom) as nbrTotal from resultats")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#-------nbr filles
@app.route('/api/general-nbrFilles')
def general_NbrFilles():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select count(DISTINCT matricule,nom,prenom) as nbrFilles from resultats where sexe='F'")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)

#------------nbr garcons
@app.route('/api/general-nbrGarcons')
def general_NbrGarcons():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select count(DISTINCT matricule,nom,prenom) as nbrGarcons from resultats where sexe='H'")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************nbr etudiants par an ***************
@app.route('/api/general-BAR-nbrEtudAn')
def general_nbrEtudAn():
    
	conn = mysql.connect()	
	cursor =conn.cursor()	
	cursor.execute("select annee, count(DISTINCT matricule,nom,prenom) as Nombre_etudiants_par_an from resultats GROUP BY annee")	
    
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]
	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************evolution nbr etudiants par an et spe***************
@app.route('/api/general-LINE-nbrEtudSpe')
def general_LINE_nbrEtudSpe():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list	

	cursor.execute("SELECT DISTINCT specialite FROM resultats")	
	specialite_tuple = cursor.fetchall()
	specialite_list =  [item[0] for item in specialite_tuple]
	
	for specialite in specialite_list:
		cursor.execute("SELECT count(matricule) FROM resultats WHERE specialite='"+specialite+"' group by annee")	
		matricule_tuple = cursor.fetchall()
		matricule_list =  [item[0] for item in matricule_tuple]
		data["datasets"].append({"label":specialite, "data":matricule_list})	
	
	data_JSON = json.dumps(data)	
	return data_JSON


#**********************evolution moyenne promo par an et spe************
@app.route('/api/general-LINE-MoyAnSpe')
def general_LINE_MoyAnSpe():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list	

	cursor.execute("SELECT DISTINCT specialite FROM resultats")	
	specialite_tuple = cursor.fetchall()
	specialite_list =  [item[0] for item in specialite_tuple]
	
	for specialite in specialite_list:
		cursor.execute("SELECT AVG(moyenne) FROM resultats WHERE specialite='"+specialite+"' GROUP BY annee")	
		moyenne_tuple = cursor.fetchall()
		moyenne_list =  [item[0] for item in moyenne_tuple]
		data["datasets"].append({"label":specialite, "data":moyenne_list})	
	
	data_JSON = json.dumps(data)	
	return data_JSON
	

#**********************Demande des spécialités selon le genre des étudiants************
@app.route('/api/general-radar')
def general_radar():
	
	data = {"specialite":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT specialite FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["specialite"]=annee_list	

	cursor.execute("SELECT DISTINCT sexe FROM resultats")	
	specialite_tuple = cursor.fetchall()
	specialite_list =  [item[0] for item in specialite_tuple]
	
	for specialite in specialite_list:
		cursor.execute("SELECT count(DISTINCT matricule,nom,prenom) FROM resultats WHERE sexe='"+specialite+"' GROUP BY specialite")	
		moyenne_tuple = cursor.fetchall()
		moyenne_list =  [item[0] for item in moyenne_tuple]
		data["datasets"].append({"label":specialite, "data":moyenne_list})	
	
	data_JSON = json.dumps(data)	
	return data_JSON






#------------------------------------------SPECIALITE_1----------------------------------------
@app.route('/dashboard-SPECIALITE_1-SAID')
def dashboard_SPECIALITE_1():
	return render_template('Dashboard-SPECIALITE_1-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar1')
def spe_GroupedBar():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_1'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_1'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy1')
def spe_CarteMoy1():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_1'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis1-2019')
def spe_admis1_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_1' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_1' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis1-2020')
def spe_admis1_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_1' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_1' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis1-2021')
def spe_admis1_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_1' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_1' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)










#------------------------------------------SPECIALITE_2----------------------------------------
@app.route('/dashboard-SPECIALITE_2-SAID')
def dashboard_SPECIALITE_2():
	return render_template('Dashboard-SPECIALITE_2-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar2')
def spe_GroupedBar2():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_2'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_2'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy2')
def spe_CarteMoy2():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_2'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis2-2019')
def spe_admis2_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_2' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_2' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis2-2020')
def spe_admis2_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_2' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_2' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis2-2021')
def spe_admis2_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_2' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_2' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)




	

#------------------------------------------SPECIALITE_3----------------------------------------
@app.route('/dashboard-SPECIALITE_3-SAID')
def dashboard_SPECIALITE_3():
	return render_template('Dashboard-SPECIALITE_3-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar3')
def spe_GroupedBar3():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_3'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_3'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy3')
def spe_CarteMoy3():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_3'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis3-2019')
def spe_admis3_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_3' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_3' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis3-2020')
def spe_admis3_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_3' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_3' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis3-2021')
def spe_admis3_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_3' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_3' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)





	

#------------------------------------------SPECIALITE_4----------------------------------------
@app.route('/dashboard-SPECIALITE_4-SAID')
def dashboard_SPECIALITE_4():
	return render_template('Dashboard-SPECIALITE_4-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar4')
def spe_GroupedBar4():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_4'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_4'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy4')
def spe_CarteMoy4():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_4'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis4-2019')
def spe_admis4_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_4' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_4' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis4-2020')
def spe_admis4_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_4' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_4' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis4-2021')
def spe_admis4_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_4' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_4' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)






#------------------------------------------SPECIALITE_5----------------------------------------
@app.route('/dashboard-SPECIALITE_5-SAID')
def dashboard_SPECIALITE_5():
	return render_template('Dashboard-SPECIALITE_5-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar5')
def spe_GroupedBar5():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_5'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_5'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy5')
def spe_CarteMoy5():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_5'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis5-2019')
def spe_admis5_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_5' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_5' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis5-2020')
def spe_admis5_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_5' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_5' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis5-2021')
def spe_admis5_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_5' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_5' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)





	


#------------------------------------------SPECIALITE_6----------------------------------------
@app.route('/dashboard-SPECIALITE_6-SAID')
def dashboard_SPECIALITE_6():
	return render_template('Dashboard-SPECIALITE_6-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar6')
def spe_GroupedBar6():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_6'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_6'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy6')
def spe_CarteMoy6():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_6'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis6-2019')
def spe_admis6_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_6' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_6' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis6-2020')
def spe_admis6_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_6' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_6' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis6-2021')
def spe_admis6_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_6' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_6' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)





	
	

#------------------------------------------SPECIALITE_7----------------------------------------
@app.route('/dashboard-SPECIALITE_7-SAID')
def dashboard_SPECIALITE_7():
	return render_template('Dashboard-SPECIALITE_7-SAID.html')


#*******Max et min des moyennes de la promo par an*********
@app.route('/api/spe-GroupedBar7')
def spe_GroupedBar7():
	
	data = {"annee":[], "datasets":[]}
	
	conn = mysql.connect()	
	cursor =conn.cursor()	
    
	cursor.execute("SELECT DISTINCT annee FROM resultats")	
	annee_tuples = cursor.fetchall()
	annee_list =  [item[0] for item in annee_tuples]
	data["annee"]=annee_list
    
	
	cursor.execute("Select min(moyenne) from resultats where specialite='SPECIALITE_7'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Min moyenne", "data":moyenne_list})	

	
	cursor.execute("Select max(moyenne) from resultats where specialite='SPECIALITE_7'  group by annee")	
	moyenne_tuple = cursor.fetchall()
	moyenne_list =  [item[0] for item in moyenne_tuple] 
	data["datasets"].append({"label":"Max moyenne", "data":moyenne_list})	

    
	data_JSON = json.dumps(data)	
	return data_JSON



#********************Carte moyennes de la promo par an*********

@app.route('/api/spe-CarteMoy7')
def spe_CarteMoy7():
	conn = mysql.connect()	
	cursor =conn.cursor() 
	
	cursor.execute("select annee, TRUNCATE(AVG(moyenne),2) as moyennePromoSpe from resultats where specialite='SPECIALITE_7'  group by annee")	
	data = cursor.fetchall()	
	row_headers=[x[0] for x in cursor.description]

	cursor.close()

	json_data=[]
	for result in data:
		json_data.append(dict(zip(row_headers,result)))					
					
	return jsonify(json_data)


#********************Poucentage d'admis et d'ajournés*********

#---------------en 2019
@app.route('/api/spe-admis7-2019')
def spe_admis7_2019():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_7' and moyenne>=10 and annee=2019")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_7' and moyenne<10 and annee=2019")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#-------------en 2020
@app.route('/api/spe-admis7-2020')
def spe_admis7_2020():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_7' and moyenne>=10 and annee=2020")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_7' and moyenne<10 and annee=2020")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)

#------------en 2021
@app.route('/api/spe-admis7-2021')
def spe_admis7_2021():
	conn = mysql.connect()	
	cursor =conn.cursor()

	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Admis from resultats where specialite='SPECIALITE_7' and moyenne>=10 and annee=2021")	
	data_admis = cursor.fetchall()		 
	
	cursor.execute("select  count(DISTINCT matricule,nom,prenom) as nbr_Ajournes from resultats where specialite='SPECIALITE_7' and moyenne<10 and annee=2021")	
	data_ajr = cursor.fetchall()		 
	
	cursor.close()

	json_data=[]
	json_data.append({"passage":"admis","nombre_etudiants":data_admis[0][0]})	
	json_data.append({"passage":"ajournes","nombre_etudiants":data_ajr[0][0]})	
  					
	return jsonify(json_data)





	

if __name__ == '__main__':
	app.run(port=5000)
	
	