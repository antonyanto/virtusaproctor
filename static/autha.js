const autha=firebase.auth();
var database = firebase.database();
const btnsignup=document.getElementById("signup");
const eamail=document.getElementById("txtmail");
const paass=document.getElementById("txtPass");
const username=document.getElementById("txtUser");
const userNumber=document.getElementById("txtNumber");

btnsignup.onclick = () => {
  var mail=eamail.value;
  var password=paass.value;
  var name=username.value;
  var mob=userNumber.value;
  autha.createUserWithEmailAndPassword(mail,password).then(()=>{
window.alert("Successfully Registered In");
window.location.href="/choice"
var id=firebase.auth().currentUser.uid;
    database.ref('Users/'+id).set({
     UserName:name,
     Mobile:mob,
    });




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
