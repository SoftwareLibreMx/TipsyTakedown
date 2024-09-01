const submitActionsEnum = Object.freeze({
  'CHECK_EMAIL': 0,
  'LOGIN': 1,
  'REGISTER': 2
})

// Fist action is to check the email
const btnSubmit = document.getElementById("btn-submit");
const signUpForm = document.getElementsByClassName("sign-up-form");
const signInForm = document.getElementsByClassName("sign-in-form");
const mainTitle = document.getElementById("main-title");
const errorMessage = document.getElementById("errorMessage");
const emailInput = document.getElementById('email');
let initialEmail = emailInput.value;

function setSubmitBtnSpinner() {
  btnSubmit.innerHTML = `
    <div class="spinner-border" role="status">
    </div>
  `;
}

async function checkMail() {
  const email = document.getElementById("email").value;

  const formData = {
    email: email,
  };
    
  setSubmitBtnSpinner();
  const response = await fetch("/api/auth/check_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    //TODO: find a way to remove this loop
    for (let i = 0; i < signUpForm.length; i++) {
      signUpForm[i].classList.remove("d-none");
      requiredSignUpInputs();
    }
    
    btnSubmit.setAttribute("action", submitActionsEnum.REGISTER);
    btnSubmit.innerText = translations.sign_up;
    mainTitle.innerText = translations.sign_up_title;
    initialEmail = emailInput.value;
    return;
  }

  const body = await response.json();

  if (body.sso_provider) {
    errorMessage.innerText = translations.error.sso_exists + body.sso_provider;
    errorMessage.classList.remove("d-none");
    initialEmail = emailInput.value;
    btnSubmit.setAttribute("action", submitActionsEnum.CHECK_EMAIL);
    return;
  }
    
  //TODO: find a way to remove this loop
  for (let i = 0; i < signInForm.length; i++) {
    signInForm[i].classList.remove("d-none");
    requiredSignInInput();
  }
    
  btnSubmit.setAttribute("action", submitActionsEnum.LOGIN);
  initialEmail = emailInput.value;
  btnSubmit.innerText = translations.login_button;
  mainTitle.innerText = translations.login_title;
}

async function loginForm() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  
  const formData = {
    email: email,
    password: password,
  };

  setSubmitBtnSpinner();
  const response = await fetch("/api/auth/sign_in", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    errorMessage.innerText = translations.error.invalid_email;
    errorMessage.classList.remove("d-none");
    return;
  }

  const data = await response.json();

  sessionStorage.setItem("token", data?.token);
  window.location.href = `/?token=${data?.token}`;
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
  
  setSubmitBtnSpinner();
  const response = await fetch("/api/auth/sign_up", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  if (!response.ok) {
    errorMessage.innerText = translations.error.user_exists;
    errorMessage.classList.remove("d-none");
    return;
  }
  loginForm();
}

emailInput.addEventListener('input', function() {
  const currentEmail = emailInput.value;
  const btnSubmitAction = btnSubmit.getAttribute("action");

  if (currentEmail !== initialEmail && btnSubmitAction !== submitActionsEnum.CHECK_EMAIL) {
    resetForm();
  }
});


document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission
  errorMessage.classList.add("d-none");

  const action = btnSubmit.getAttribute("action");
  const actionFunctions = {
    [submitActionsEnum.CHECK_EMAIL]: checkMail,
    [submitActionsEnum.LOGIN]: loginForm,
    [submitActionsEnum.REGISTER]: registerForm
  }

  actionFunctions[action]();
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
  btnSubmit.setAttribute("action", submitActionsEnum.CHECK_EMAIL);
  btnSubmit.innerText = translations.next_button;
  mainTitle.innerText = translations.main_title;
}
