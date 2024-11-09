var nameRegEx = /^[\d]{9}$/;
var passwordRegEx = /^[\w]{3,7}$/;
var emailRegEx = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  

var xmlHttp;

function GetXmlHttpObject() {
  try {
    return new ActiveXObject("Msxml2.XMLHTTP");
  } catch(e) {} // Internet Explorer
  try {
    return new ActiveXObject("Microsoft.XMLHTTP");
  } catch(e) {} // Internet Explorer
  try {
    return new XMLHttpRequest();
  } catch(e) {} // Firefox, Opera 8.0+, Safari
  alert("XMLHttpRequest not supported");
  return null;
}

function SelectDistrictChange() {
  let districID = document.getElementById( "district").value;

  let image = document.getElementById( "imgDistrict")
  image.src = "/static/images/distritos/" + districID + ".gif"
  
  xmlHttp = GetXmlHttpObject();
  xmlHttp.open( "GET", "/counties?idDistrict=" + districID , true);
  xmlHttp.onreadystatechange=SelectDistrictChangeHandleReply;
  xmlHttp.send(null);
}

function SelectDistrictChangeHandleReply() {   
  if( xmlHttp.readyState === 4 ) {

    alert( "SelectDistrictChangeHandleReply" );

    let countySelect=document.getElementById( "county" );
    countySelect.options.length = 0;

    let counties = JSON.parse( xmlHttp.responseText );

    for (i=0; i<counties.length; i++) {
      let currentCounty = counties[ i ];

      let value  = currentCounty.ID;
      let option = currentCounty.Valor;

      try{
        countySelect.add( new Option("", value), null);
      }
      catch(e) {
        countySelect.add( new Option("", value) );
      }
        
      countySelect.options[i].innerHTML = option;
    }
  }
}

function valida(value) {
	// https://pt.wikipedia.org/wiki/N%C3%BAmero_de_identifica%C3%A7%C3%A3o_fiscal
	
	const nif = typeof value === 'string' ? value : value.toString();
    
	const validationSets = {
      one: ['1', '2', '3', '5', '6', '8'],
      two: ['45', '70', '71', '72', '74', '75', '77', '79', '90', '91', '98', '99']
    };
	
    if ( nif.length !== 9 ) {
		return false;
	}
	
    if ( 
			!validationSets.one.includes( nif.substr(0, 1) ) && 
			!validationSets.two.includes( nif.substr(0, 2) ) ) {
		return false;
	}
	
    const total = nif[0] * 9 + nif[1] * 8 + nif[2] * 7 + nif[3] * 6 + nif[4] * 5 + nif[5] * 4 + nif[6] * 3 + nif[7] * 2;
    
	const modulo11 = (Number(total) % 11);
    
	const checkDigit = modulo11 < 2 ? 0 : 11 - modulo11;
    
	return checkDigit === Number(nif[8]);
}

function FormRegisterValidator() {
	nifValue = document.getElementById( "vatID" ).value;
	emailValue = document.getElementById( "emailID" ).value;
	passwordValue = document.getElementById( "passwordID" ).value;
	
	if ( valida( nifValue )==false ) {
		alert( "Valor do " + nifValue + " é inválido" );
		return false;
	}
	else if ( emailRegEx.test( emailValue ) == false) {

		alert( "Valor do " + emailValue + " é inválido" );
		return false
	}
	else if ( passwordRegEx.test( passwordValue ) == false) {
		alert( "Valor do " + passwordValue + " é inválido" );
		return false
	}
	
	return true;
}

function FormLoginValidator() {
	nifValue = document.getElementById( "vatID" ).value;
	
	if ( valida( nifValue )==false ) {
		alert( "Valor do " + nifValue + " é inválido" );
		return false;
	}
	return true;
}


