let existUser = false;
let checkedEmail = false;
const btnSubmit = document.getElementById("btn-submit");
const signUpForm = document.getElementsByClassName("sign-up-form");
const signInForm = document.getElementsByClassName("sign-in-form");
const mainTitle = document.getElementById("main-title");
const errorMessage = document.getElementById("errorMessage");
const emailInput = document.getElementById('email');
let initialEmail = emailInput.value;

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
    initialEmail = emailInput.value;
    return;
  }
  body = await response.json();
  if (body.sso_provider) {
    errorMessage.innerText = "You are already registered with " + body.sso_provider;
    errorMessage.classList.remove("d-none");
    initialEmail = emailInput.value;
    checkedEmail = true;
    existUser = true;
    return;
  }

  for (let i = 0; i < signInForm.length; i++) {
    signInForm[i].classList.remove("d-none");
    requiredSignInInput();
  }
  checkedEmail = true;
  existUser = true;
  initialEmail = emailInput.value;
  btnSubmit.innerText = "Sign In";
  mainTitle.innerText = "Please enter your password";
}

async function loginForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  
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

emailInput.addEventListener('input', function() {
  const currentEmail = emailInput.value;

  if (currentEmail !== initialEmail && checkedEmail) {
    resetForm();
  }
});

document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission
  errorMessage.classList.add("d-none");
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

function requiredSignUpInputs(active = true) {
  if (active) {
    document.getElementById("password").setAttribute("required", "true");
    document.getElementById("confirm_password").setAttribute("required", "true");
    document.getElementById("given_name").setAttribute("required", "true");
    document.getElementById("surname").setAttribute("required", "true");
  } else {
    document.getElementById("password").removeAttribute("required");
    document.getElementById("confirm_password").removeAttribute("required");
    document.getElementById("given_name").removeAttribute("required");
    document.getElementById("surname").removeAttribute("required");
  }
}

function requiredSignInInput(active = true) {
  if (active) {
    document.getElementById("password").setAttribute("required", "true");
  }else{
    document.getElementById("password").removeAttribute("required");
  }
}
function resetRequiredInputs() {
  requiredSignUpInputs(false);
  requiredSignInInput(false);
}

function resetForm() {
  for (let i = 0; i < signUpForm.length; i++) {
    signUpForm[i].classList.add("d-none");
  }
  for (let i = 0; i < signInForm.length; i++) {
    signInForm[i].classList.add("d-none");
  }
  resetRequiredInputs();
  errorMessage.classList.add("d-none");
  existUser = false;
  checkedEmail = false;
  btnSubmit.innerText = "Next";
  mainTitle.innerText = "Please fill the form";
}