const apiUrl = 'http://127.0.0.1:5000/search';

document.getElementById('searchForm').addEventListener('submit', async function (event) {
  event.preventDefault();
  const name = document.getElementById('searchQuery').value;
  const branch = document.getElementById('branch').value;
  const city = document.getElementById('city').value;
  const year = document.getElementById('year').value;
  const company = document.getElementById('company').value;

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, branch, city, year, company }),
    });

    if (!response.ok) {
      throw new Error('Error connecting to the server');
    }

    const filteredDocuments = await response.json();
    displayResults(filteredDocuments);
  } catch (err) {
    console.log('Error:', err.message);
  }
});


function displayResults(results) {
  const resContainer = document.querySelector('.res');
  resContainer.innerHTML = '';

  results.forEach(function (doc) {
    const resultElement = document.createElement('div');
    resultElement.innerHTML = `
      <div>
        <center>
          <img src="./182-1829287_cammy-lin-ux-designer-circle-picture-profile-girl.png" height="60px" width="60px">
          <br>
          <span>${doc.Name}</span>
          <br><br>
          <p>Branch: <span>${doc.Branch}</span></p>
          <p>Batch: <span>${doc.Year}</span></p>
          <p>Company: <span>${doc.Company}</span></p>
          <p>Location: <span>${doc.City}</span></p>
        </center>
      </div>
    `;
    resContainer.appendChild(resultElement);
  });
}
