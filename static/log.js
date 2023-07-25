function initializeGoogleSignIn() {
  gapi.load('auth2', function() {
    gapi.auth2.init({
      client_id: '886588755390-1spe51df9k9uiimti149uf716fdujake.apps.googleusercontent.com',
      redirect_uri: window.location.origin
    }).then(function(auth2) {
      // Render the Google Sign-In button
      gapi.signin2.render('g_id_signin', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSignIn,
        'onfailure': onFailure
      });
    });
  });
}

function onSignIn(googleUser) {
  const id_token = googleUser.getAuthResponse().id_token;
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/google-login');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    window.location.href = xhr.responseText;
  };
  xhr.send('id_token=' + id_token);
}

function onFailure(error) {
  console.error('Google Sign-In Error: ', error);
}

initializeGoogleSignIn();



/*function initializeGoogleSignIn() {
  gapi.load('auth2', function() {
    gapi.auth2.init({
      client_id: '886588755390-1spe51df9k9uiimti149uf716fdujake.apps.googleusercontent.com',
      redirect_uri: window.location.origin
    }).then(function(auth2) {
      // Render the Google Sign-In button
      auth2.attachClickHandler('sign', {}, function(googleUser) {
        const id_token = googleUser.getAuthResponse().id_token;
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/google-login');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
          window.location.href = xhr.responseText;
        };
        xhr.send('id_token=' + id_token);
      }, function(error) {
        console.error('Google Sign-In Error: ', error);
      });
    });
  });
}

function signInWithGoogle() {
  google.accounts.id.initialize({
    client_id: '886588755390-1spe51df9k9uiimti149uf716fdujake.apps.googleusercontent.com',
    callback: handleCredentialResponse,
    auto_select: false,
  });
  google.accounts.id.prompt();
}

initializeGoogleSignIn();*/


/*function initializeGoogleSignIn() {
  gapi.load('auth2', function() {
    gapi.auth2.init({
      client_id: '886588755390-1spe51df9k9uiimti149uf716fdujake.apps.googleusercontent.com',
      redirect_uri: window.location.origin
    }).then(function(auth2) {
      // Render the Google Sign-In button
      auth2.attachClickHandler('sign', {}, function(googleUser) {
        const id_token = googleUser.getAuthResponse().id_token;
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/google-login');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
          window.location.href = xhr.responseText;
        };
        xhr.send('id_token=' + id_token);
      }, function(error) {
        console.error('Google Sign-In Error: ', error);
      });
    });
  });
}*/

/*function signInWithGoogle() {
    const auth2 = gapi.auth2.getAuthInstance();
    auth2.signIn().then(function(googleUser) {
      const id_token = googleUser.getAuthResponse().id_token;
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/google-login');
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.onload = function() {
        window.location.href = xhr.responseText;
      };
      xhr.send('id_token=' + id_token);
    });
}*/

function signInWithGoogle() {
  google.accounts.id.initialize({
    client_id: '886588755390-1spe51df9k9uiimti149uf716fdujake.apps.googleusercontent.com',
    callback: handleCredentialResponse
  });
  google.accounts.id.prompt();
}


initializeGoogleSignIn();
