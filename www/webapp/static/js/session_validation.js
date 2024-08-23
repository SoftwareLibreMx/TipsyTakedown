  // Check if session storage has a specific key
  if (sessionStorage.getItem('token')) {
    // Get the value from session storage
    const value = sessionStorage.getItem('token');

    // Show the div based on the value
    if (value) {
        document.getElementById('sign-up').classList.add("d-none");
        document.getElementById('sign-out').classList.remove("d-none");
    }
  }