
const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {

  } else {
    
  }
});

		const txtEmail=document.getElementById('txtEmail');
				const txtPassword=document.getElementById('txtPassword');
						const btnLogin=document.getElementById('btnLogin');
						btnLogin.addEventListener('click',e =>
					{
						const email=txtEmail.value;
						const pass=txtPassword.value;
						const auth=firebase.auth();
						const promise=auth.signInWithEmailAndPassword(email,pass);
						promise.catch(e => console.log(e.message));



					})
