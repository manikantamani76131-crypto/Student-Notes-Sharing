// Small client-side enhancement for the notes page.
document.addEventListener("DOMContentLoaded", function () {
    const search = document.querySelector('input[name="search"]');
    if (search) {
        search.addEventListener("keydown", function (event) {
            if (event.key === "Escape") search.value = "";
        });
    }
});
