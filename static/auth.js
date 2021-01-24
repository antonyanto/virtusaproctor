const auth=firebase.auth();
const btnlogin=document.getElementById("login");
const email=document.getElementById("txtEmail");
const pass=document.getElementById("txtPassword");
const msg=document.getElementById("message");
btnlogin.onclick = () =>{
  var mail=email.value;
  var password=pass.value;
  auth.signInWithEmailAndPassword(mail,password).then(()=>{
window.alert("Successfully Logged In");
window.location.href="/choice"
  }).catch((err)=>{
    window.alert(err.message);
  });
}
function GoogleLogin() {

    var provider=new firebase.auth.GoogleAuthProvider();
    //Login with popup window
    firebase.auth().signInWithPopup(provider).then(function () {
        //code executes after successful login

        window.location.href="/choice";
    }).catch(function (error) {
        var errorMessage=error.message;
        alert(errorMessage);
    });
}
