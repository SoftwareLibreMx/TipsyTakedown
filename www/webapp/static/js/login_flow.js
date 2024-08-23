let existUser = false;
let checkedEmail = false;
const btnSubmit = document.getElementById("btn-submit");
const signUpForm = document.getElementsByClassName("sign-up-form");
const signInForm = document.getElementsByClassName("sign-in-form");
const mainTitle = document.getElementById("main-title");
const errorMessage = document.getElementById("errorMessage");

async function checkMail() {
  const email = document.getElementById("email").value;

  const formData = {
    email: email,
  };

  const response = await fetch("/api/auth/check_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    for (let i = 0; i < signUpForm.length; i++) {
      signUpForm[i].classList.remove("d-none");
      requiredSignUpInputs();
    }
    checkedEmail = true;
    btnSubmit.innerText = "Sign Up";
    mainTitle.innerText = "Please fill the sign up form";
    return;
  }

  for (let i = 0; i < signInForm.length; i++) {
    signInForm[i].classList.remove("d-none");
    requiredSignInInput();
  }
  checkedEmail = true;
  existUser = true;
  btnSubmit.innerText = "Sign In";
  mainTitle.innerText = "Please enter your password";
}

async function loginForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  errorMessage.classList.add("d-none");
  
  const formData = {
    email: email,
    password: password,
  };

  const response = await fetch("/api/auth/sign_in", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    errorMessage.innerText = "Invalid email or password";
    errorMessage.classList.remove("d-none");
    return;
  }

  const data = await response.json();
  const token = data.token;
  if (token) {
    sessionStorage.setItem("token", token);
    window.location.href = "/";
  }
}

async function registerForm() {
  const given_name = document.getElementById("given_name").value;
  const surname = document.getElementById("surname").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  errorMessage.classList.add("d-none");

  const formData = {
    email: email,
    password: password,
    given_name: given_name,
    surname: surname,
  };

  const response = await fetch("/api/auth/sign_up", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    errorMessage.innerText = "Already taken the user";
    errorMessage.classList.remove("d-none");
    return;
  }
  loginForm();
}

document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission
  switch (true) {
    case !checkedEmail:
      checkMail();
      break;
    case existUser && checkedEmail:
      loginForm();
      break;
    case !existUser && checkedEmail:
      registerForm();
      break;
    default:
      break;
  }
});

function requiredSignUpInputs(){
  document.getElementById("password").setAttribute("required", "true");
  document
    .getElementById("confirm_password")
    .setAttribute("required", "true");
  document.getElementById("given_name").setAttribute("required", "true");
  document.getElementById("surname").setAttribute("required", "true");
}
function requiredSignInInput() {
  document.getElementById("password").setAttribute("required", "true");
}