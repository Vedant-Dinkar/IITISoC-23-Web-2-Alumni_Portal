// Replace the following with your Firebase configuration object
const firebaseConfig = {
    apiKey: "AIzaSyAnsdCOC5o0fG-HnOxp5TwisTNhBFYQ50Q",
    authDomain: "alumni-portal-6699.firebaseapp.com",
    projectId: "alumni-portal-6699",
    storageBucket: "alumni-portal-6699.appspot.com",
    messagingSenderId: "675305525647",
    appId: "1:675305525647:web:25bbf3557e5f09aa52fbfa",
    measurementId: "G-RZB172E0PL"
  };
  
  firebase.initializeApp(firebaseConfig);

  const provider = new firebase.auth.GoogleAuthProvider();
  
  const signButton = document.getElementById("sign");
  
  signButton.addEventListener("click", () => {
    firebase
      .auth()
      .signInWithPopup(provider)
      .then((result) => {
        const credential = result.credential;
        const token = credential.accessToken;
        const user = result.user;
        console.log(user);
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        const email = error.email;
        const credential = error.credential;
        console.error(errorCode, errorMessage, email, credential);
      });
  });