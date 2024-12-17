document.addEventListener("DOMContentLoaded", function(){
    const searchInput = document.getElementById("search");
    const tableRows = document.querySelectorAll("#data tr");

    searchInput.addEventListener("keyup", function(){
        const query = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const cells = row.querySelectorAll("td");
            let rowText = "";
            cells.forEach(cell => {
                rowText += cell.textContent.toLowerCase();
            });

            if(rowText.includes(query)){
                row.style.display = "";
            }else{
                row.style.display = "none";
            }
        });
    });
});