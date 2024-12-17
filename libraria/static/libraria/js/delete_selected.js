document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById("select-all");
    const Checkboxes = document.querySelectorAll(".data-checkbox");
    const deleteButton = document.getElementById("delete-selected");

    selectAllCheckbox.addEventListener("change", function () { //klo selectAllCheckbox di klik seluruhnya ikut berubah
        Checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
        toggleDeleteButton();
    });

    Checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", toggleDeleteButton);
    });

    function toggleDeleteButton() {
        const anyChecked = Array.from(Checkboxes).some(checkbox => checkbox.checked);
        deleteButton.disabled = !anyChecked;
    }
});
