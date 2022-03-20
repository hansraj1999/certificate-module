function verify(argument) {
	var token = sessionStorage.getItem("token");
	console.log(sessionStorage.getItem("token"));
	console.log(token);
	if (token === null){
		window.location.replace("./login.html");
	}
}