// Initialize jQuery UI date picker
$(function () {
  $("#datePicker").datepicker();
});

// Handle Predict button click
$("#predictBtn").on("click", function () {
  const dateValue = $("#datePicker").val().trim();
  const predictionCard = $("#predictionCard");
  const predictionLeft = $("#predictionLeft");
  const predictionRight = $("#predictionRight");

  if (dateValue) {
    // Show the card
    predictionCard.show();

    // Populate the left side
    predictionLeft.html(`
        <h1 class="display-1 fw-bold">87%</h1>
        <p class="fs-5">
          Lot D21 and B2<br />
          Lot S23 and R4<br />
          Lot D2 and K8
        </p>
      `);

    // Populate the right side
    predictionRight.html(`
        <h3 class="fw-bold">LOREM IPSUM TEXT</h3>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
          Quisque in quam non orci venenatis tempor. 
          Vivamus euismod dui in erat tempus, quis pharetra eros tincidunt.
        </p>
        <p>
          Fusce dignissim ex sit amet tellus tempus, 
          non varius lorem imperdiet. Sed scelerisque tortor 
          nec lorem blandit, eget facilisis magna luctus.
        </p>
      `);
  } else {
    // Hide the card if no date is selected
    predictionCard.hide();
    predictionLeft.empty();
    predictionRight.empty();
  }
});
