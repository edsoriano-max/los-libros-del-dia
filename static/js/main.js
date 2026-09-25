document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-confirm-delete]").forEach(function (boton) {
        boton.addEventListener("click", function (event) {
            if (!window.confirm("¿Estás seguro de que quieres eliminar este libro?")) {
                event.preventDefault();
            }
        });
    });
});
