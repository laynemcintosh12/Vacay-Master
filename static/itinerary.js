    // get trip_id
    const tripId = document.getElementById('tripId').value;


    // Get all textarea elements with class 'table-text'
    const textAreas = document.querySelectorAll('.table-text');

    // Add a blur event listener to each textarea
    textAreas.forEach((textarea) => {
        textarea.addEventListener('blur', function () {
            // Get the value of the textarea
            const val = this.value.trim();
            const row = this.parentElement.getAttribute('row');
            const col = this.parentElement.getAttribute('col');

            // Check if the textarea has a value
            if (val !== '') {
                // Get the corresponding time based on the row (1 corresponds to 8:00 AM, 2 to 9:00 AM, etc.)
                const time = (parseInt(row) + 7); // Adjust for the index starting at 0

                // Get the date from the table header corresponding to the column
                const dateHeader = document.querySelector(`.days-header th:nth-child(${parseInt(col) + 1})`);
                const date = dateHeader.textContent.trim();

                // Send the data to the backend
                sendDataToBackend(val, time, date);
            }
        });
    });


    // Function to send data to the backend
    async function sendDataToBackend(val, time, date) {
        try {
            console.log(val, time, date, tripId); // Log the trip_id
            const response = await axios.post('/save_itinerary', {
                val: val,
                time: time,
                date: date,
                tripId: tripId // Send the trip_id to the backend
            });
    
            // Handle a successful response if needed
            if (response.status === 200) {
                console.log('Data saved successfully');
            } else {
                console.error('Error saving data');
            }
        } catch (error) {
            // Handle errors if necessary
            console.error('Error saving data:', error);
        }
    }

