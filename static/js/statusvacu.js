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
      .text("Fecha de inicio y termino?");

    // Create the table body
    const tableBody = table.append("tbody")
      .attr("id", "table-body");

    // Create the add row button
    const addRowButton = tableContainer.append("button")
      .attr("class", "btn btn-outline-primary")
      .attr("type", "button")
      .text("Add Row");
    addRowButton.on("click", function() {
      // Create a new table row
      const newRow = tableBody.append("tr");
      newRow.append("td")
        .append("input")
        .attr("type", "text")
        .attr("class", "form-control");
      const datecol=newRow.append("td")
        .append("div")
        .attr("class", "row")
        
        datecol.append("div")
        .attr("class", "col")
        .append("input")
        .attr("type", "date")
        .attr("class", "form-control")
        .attr("id", "date")

        datecol.append("div")
        .attr("class", "col")
        .append("input")
        .attr("type", "date")
        .attr("class", "form-control")
        .attr("id", "date2")
        ;
    });
  } else {
    // Hide the table container if no is selected
    d3.select("#table-container")
      .style("display", "none");
  }
});