// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });

let alertWrapper = document.querySelector(".alert")
let alertButton = document.querySelector(".alert__close")

if (alertWrapper) {
  alertButton.addEventListener('click', () => {
    alertWrapper.style.display = 'none'
  })
}