var mcintosh = ["Axx","Bxo","Bxi","Cro","Cri","Cso","Csi","Cao","Cai","Cho","Chi","Cko","Cki","Dro","Dri","Drc","Dso","Dsi","Dsc",
				"Dao","Dai","Dac","Dho","Dhi","Dhc","Dko","Dki","Dkc","Eso","Esi","Esc","Eao","Eai","Eac","Eho","Ehi","Ehc","Eko",
				"Eki","Ekc","Fho","Fhi","Fhc","Fko","Fki","Fkc","Hhx","Hkx","Hsx","Hax","Hrx","Xxx"];
var zurich = ["A","B","C","D","E","F","G","H","J","X"];


function FillCombos(id){
	var option = "";
	switch(id){
		case "McIntosh":
				for(var i = 0; i < mcintosh.length; i++){
					option += "<option>"+mcintosh[i]+"</option>";
				}
		break;
		case "Zurich":
				for(var i = 0; i < zurich.length; i++){
					option += "<option>"+zurich[i]+"</option>";
				}
		break;
	}
	document.write(option);
}

function btn_visualize_click(id){
	var imgsource = document.getElementById(id).src;
	if(imgsource.indexOf("disabled") > -1){
		document.getElementById(id).src = "./Styles/images/icons/Eye_32.png";
	}
	else{
		document.getElementById(id).src = "./Styles/images/icons/Eye_disabled_32.png";
	}
}

function btn_edit_click(id){
	$("#"+id).dialog("open");
}

function btn_okcancel_clicked(id, action){
	$("#"+id).dialog("close");
}
