function verify() {
	var token = sessionStorage.getItem("token");
	console.log(sessionStorage.getItem("token"));
//	console.log(token);
	if (token === null){
		window.location.replace("./login.html");
	}
}
function logout() {
      sessionStorage.clear();
      alert('You are about to Logout');
      window.location.href='index.html'
    }