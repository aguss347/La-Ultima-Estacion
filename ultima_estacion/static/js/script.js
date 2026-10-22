// Coloca el año actual en el pie de página.
const elementoAnio = document.getElementById("anio");
if (elementoAnio) {
    elementoAnio.textContent = new Date().getFullYear();
}
