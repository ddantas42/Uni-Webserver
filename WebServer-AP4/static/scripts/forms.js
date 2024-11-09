var nameRegEx = /^[\w]{1,9}$/;
var passwordRegEx = /^[\w]{3,7}$/;

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


function FormLoginValidator() {

  let form = document.FormLogin;

  let login = form.name.value;
  let password = form.password.value;

  console.log(login, password)

  if (!nameRegEx.test(login))
    alert('Username must be between 1 and 9 letters')
  else if (!passwordRegEx.test(password))
    alert('Password must be between 3 and 7 letters')
  else
    return true;
  
	return false;
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

    // alert( "SelectDistrictChangeHandleReply" );

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


function SelectCountyHandleReply() {
  if( xmlHttp.readyState === 4 ) {

    let costalSelect=document.getElementById( "postal" );
    costalSelect.options.length = 0;

    let postal = JSON.parse( xmlHttp.responseText );

    for (i=0; i<postal.length; i++) {
      let currentCounty = postal[ i ];

      let value  = currentCounty.ID;
      let option = currentCounty.Valor;

      try{
        costalSelect.add( new Option("", value), null);
      }
      catch(e) {
        costalSelect.add( new Option("", value) );
      }
      costalSelect.options[i].innerHTML = option;
    }
  }
}




function SelectCountyChange() {
  let countyID = document.getElementById( "county").value;
  
  console.log("countyID", countyID)
  xmlHttp = GetXmlHttpObject();
  xmlHttp.open( "GET", "/postal?idPostal=" + countyID , true);
  xmlHttp.onreadystatechange=SelectCountyHandleReply;
  xmlHttp.send(null);
  return false;
}
