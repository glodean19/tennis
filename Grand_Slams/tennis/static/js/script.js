/** Some reference: https://www.w3schools.com/django/django_add_js_file.php 
 https://stackoverflow.com/questions/71090033/how-to-connect-django-rest-api-to-a-html-css-js-frontend
*/

const CATEGORY_TITLES = {
  tournaments: "Tournaments",
  players: "Players",
  years: "Years",
  1: "Which players have the most effective serves?",
  2: "Which countries produce the highest-performing players?",
  3: "How does a player's right or left-hand use affect match outcomes?",
};

const ERROR_MESSAGE = "Error loading data. Please try again later.";

/** it initiates a fetch request to the API endpoint, clears the answer-container content
     fetch the data from a specified endpoint and it render the fetched data on the page */
function fetchData(category) {
  const answerContainer = document.getElementById("answer-container");
  answerContainer.innerHTML = "";

  // Fetch data from the API
  let apiUrl = "";
  switch (category) {
    case "tournaments":
      apiUrl = "/api/tournaments/";
      break;
    case "years":
      apiUrl = "/api/years/";
      break;
    case 1:
      apiUrl = "/api/players/most-aces/";
      break;
    case 2:
      apiUrl = "/api/countries/most-wins/";
      break;
    case 3:
      apiUrl = "/api/performance-by-hand/";
      break;
    default:
      return;
  }

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched data:", data);
      renderData(category, data);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      answerContainer.innerHTML = `<p>${ERROR_MESSAGE}</p>`;
    });
}

/** it renders the HTML content based on the category and the data fetched */
function renderData(category, data) {
  const answerContainer = document.getElementById("answer-container");
  let html = `<h2>${CATEGORY_TITLES[category]}</h2>`;

  if (data.length === 0) {
    html += "<p>No data available.</p>";
  }else {
    html += getCategorySpecificHtml(category, data);
  }

  answerContainer.innerHTML = html;
}

/** this function specifies the HTML structure based on the category and the data received
    Data are displayed in tables, list or grid, based on their categories */
function getCategorySpecificHtml(category, data) {
  switch (category) {
    case 1:
      return getTableHtml(
        data,
        ["Player Name", "Total Aces"],
        ["player_name", "total_aces"]
      );
    case 2:
      return getTableHtml(
        data,
        ["Country", "Wins"],
        ["player_id__ioc__country_name", "wins"]
      );
    case 3:
      return getTableHtml(
        data,
        ["Hand", "Wins", "Losses"],
        ["player_id__hand__hand_description", "wins", "losses"]
      );
    default:
      return getListHtml(category, data);
  }
}

function fetchPlayersByLetter(letter) {
  const apiUrl = `/api/players/by-letter/${letter}/`;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched players:", data);
      renderPlayers(data);
    })
    .catch((error) => {
      console.error("Error fetching players:", error);
    });
}

function renderPlayers(data) {
  const answerContainer = document.getElementById("answer-container");
  let html = "<ul>";

  data.forEach((player) => {
    html += `<li>${player.player_name}</li>`;
  });

  html += "</ul>";
  answerContainer.innerHTML = html;
}

/** this function displays the fetched data in a table */
function getTableHtml(data, headers, properties) {
  let html = `<table><tr>${headers
    .map((header) => `<th class="table-header">${header}</th>`)
    .join("")}</tr>`;
  data.forEach((item) => {
    html += `<tr>${properties
      .map((property) => `<td class="table-cell">${item[property]}</td>`)
      .join("")}</tr>`;
  });
  html += "</table>";
  return html;
}
/** this function displays the fetched data in a list */
function getListHtml(category, data) {

  let html = "<ul>";

  // Convert single object to array if necessary
  if (!Array.isArray(data)) {
      data = [data];
  }

  // category of data displayed in list only
  data.forEach(item => {
      if (category === "tournaments" || category === "players" || category === "years") {
          html += `<li>${item[Object.keys(item)[0]]}</li>`;
      } 
  });
  html += "</ul>";
  return html;
}

// Function to handle form submission and add new player.  
// The data extracted are displayed in the answer-container
function add(event) {
  event.preventDefault();
  const form = document.getElementById('player-form');
  const formData = new FormData(form);
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  // construct the object data with the fields extracted from the form
  const data = {
    fullname: formData.get('fullname'),
    country: formData.get('country'),
    height: formData.get('height'),
    hand: formData.get('hand')
  };

  // Some reference: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  // https://stackoverflow.com/questions/76047301/working-with-csrf-token-in-javascript-via-fetch-api
  fetch('/api/manage-player/', {
    method: 'POST',
    headers: {
      // retrieves the CSRF token from the form for security
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(data)
  })
 .then(response => {
    console.log('Raw response:', response);
    return response.json();
  })
 .then(data => {
    if (data.status === 'success') {
      // Extract the player object
      const playerData = data.data.player; 
      const answerContainer = document.getElementById('answer-container');
      renderDataForNewEntry(answerContainer, playerData);
      // Clear the form
      form.reset(); 
    } else {
      console.error('Failed to add player:', data);
      alert('Failed to add player. Please check your input and try again.');
    }
  })
 .catch(error => {
    console.error('Error adding player:', error);
    alert('Failed to add player. Please try again.');
  });
}

function delete_record(event, playerId) {
  event.preventDefault();
  // display confirmation message before to delete the record
  if (!confirm('Are you sure you want to delete this record?')) {
    return;
  }

  // retrieves the csrf token https://stackoverflow.com/questions/65485435/how-can-i-send-a-csrf-token-in-a-form
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  fetch(`/api/manage-player/${playerId}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Remove the new entry created in the answer-container 
      const entry = document.querySelector(`.record-entry[data-player-id="${playerId}"]`);
      if (entry) {
        entry.remove();
      }
    } else {
      alert('Failed to delete player. Please try again.');
    }
  })
  .catch(error => {
    console.error('Error deleting player:', error);
    alert('Failed to delete player. Please try again.');
  });
}

function renderDataForNewEntry(container, data) {
  // template literal to construct the new entry
  let html = `<div class="record-entry" data-player-id="${data.player_id}">
                <div>
                    <p>Player: ${data.player_name}</p>
                </div>
                <div>
                    <p>Country: ${data.ioc}</p>
                </div>
                <div>
                    <p>Height: ${data.height}</p>
                </div>
                <div>
                    <p>Hand: ${data.hand}</p>
                </div>
                <button onclick="delete_record(event, '${data.player_id}')">Delete</button>
              </div>`;

  // Prepend new entry to maintain order. All new entries are appended at the top
  container.innerHTML = html + container.innerHTML; 
}

