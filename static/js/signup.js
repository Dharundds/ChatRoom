const password = document.getElementById("pswrd").value;
const confirm_password = document.getElementById("pswrd-repeat").value;

show = () => {
  let pswrd = document.getElementById("pswrd");
  let icon = document.querySelector(".fas");
  if (pswrd.type === "password") {
    pswrd.type = "text";
    pswrd.style.marginTop = "1px";
    icon.style.color = "Blue";
  } else {
    pswrd.type = "password";
    icon.style.color = "black";
  }
};

//form.addEventListener('submit',(e) => {
//	let message = []
//	if (nam.value === ''||nam.value == null){
//		message.push('Name is required')
//	}
//	if (password.value.length<=6){
//		message.push('Password must be greater than 6 character')
//	}
//	if(password.value === 'password'|| password.value ==='Password'|| password.value==='PASSWORD') {
//		message.push('Password cannot be password ')
//	}
//	if (message.length >0) {
//	e.preventDefault()
//	errorElement.innerText = message.join(', ')
//	}
//})
