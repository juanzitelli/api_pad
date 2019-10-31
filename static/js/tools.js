 function getUrl(v) {
 	var xmlhttp = new XMLHttpRequest();
 	xmlhttp.onreadystatechange = function () {
 		if (this.responseText.length > 0) {
 			vresp = this.responseText;
 		} else {
 			vresp = "Error en la función de STRUBBIA";
 		}
 	}
 	xmlhttp.open("GET", v, false);
 	xmlhttp.send();
 	return vresp;
 }