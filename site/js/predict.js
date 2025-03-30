$(document).ready(function () {
  // (Optional) If you want to use jQuery UI datepicker instead of native input[type="date"]:
  // $("#predict-date").datepicker();

  $(".predict-btn").on("click", function () {
    const dateValue = $("#predict-date").val().trim();
    const predictionCard = $("#predictionCard");
    const predictionLeft = $("#predictionLeft");
    const predictionRight = $("#predictionRight");

    if (dateValue) {
      // Show the prediction card if a date is selected
      predictionCard.show();

      // Populate the left side with sample prediction data
      predictionLeft.html(`
          <h1 class="display-1 fw-bold">87%</h1>
          <p class="fs-5">
            Lot D21 and B2<br />
            Lot S23 and R4<br />
            Lot D2 and K8
          </p>
        `);

      // Populate the right side with additional details (placeholder text)
      predictionRight.html(`
          <h3 class="fw-bold">LOREM IPSUM TEXT</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque in quam non orci venenatis tempor.
          </p>
          <p>
            Fusce dignissim ex sit amet tellus tempus, non varius lorem imperdiet. Sed scelerisque tortor nec lorem blandit, eget facilisis magna luctus.
          </p>
        `);
    } else {
      // Hide the prediction card and clear its contents if no date is selected
      predictionCard.hide();
      predictionLeft.empty();
      predictionRight.empty();
    }
  });
});
