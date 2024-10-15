// Get the select element
const selectElement = d3.select("#vaccinationStatus");

// Add an event listener to the select element
selectElement.on("change", function() {
  const selectedValue = d3.select(this).property("value");
  if (selectedValue === "yes") {
    // Create the table container
    d3.select('#formbody').append('div').attr('id', 'table-container').attr('class','row');
    const tableContainer = d3.select("#table-container");
    tableContainer.style("display", "block");

    // Create the table
    const table = tableContainer.append("table")
      .attr("class", "table");

    // Create the table header
    const tableHeader = table.append("thead")
      .append("tr");
    tableHeader.append("th")
      .text("Que enfermedad tienes o tuviste?");
    tableHeader.append("th")
      .text("Rango de Fecha?");

    // Create the table body
    const tableBody = table.append("tbody")
      .attr("id", "table-body");

    // Create the add row button
    const addRowButton = tableContainer.append("button")
      .attr("class", "btn btn-outline-primary")
      .attr("type", "button")
      .text("Add Row");
    
    let contador=1;
    addRowButton.on("click", function() {

      // Create a new table row with two columns
      // The first column will be a text input for the disease
      // The second column will be a date range
      const newRow = tableBody.append("tr");

      // Create a text input for the disease
      newRow.append("td")
        .append("input")
        .attr("type", "text")
        .attr("class", "form-control")
        .attr("name", `enfermedad${contador}`);

      // Create a date range
      const datecol = newRow.append("td")
        .append("div")
        .attr("class", "row");

      // Create a date input for the start date
      datecol.append("div")
        .attr("class", "col")
        .append("input")
        .attr("type", "date")
        .attr("class", "form-control")
        .attr("name", `startdate${contador}`);

      // Create a date input for the end date
      datecol.append("div")
        .attr("class", "col")
        .append("input")
        .attr("type", "date")
        .attr("class", "form-control")
        .attr("name", `enddate${contador}`);

      // Increment the counter
      contador++;
    });
  } else {
    // Hide the table container if no is selected
    d3.select("#table-container")
      .style("display", "none");
  }
});