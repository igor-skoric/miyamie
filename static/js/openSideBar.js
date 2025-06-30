document.addEventListener('DOMContentLoaded', function () {
  const sidebarContainer = document.getElementById("sidebarContainer");
  const openButtons = document.querySelectorAll(".openSidebarBtn");

  let isOpen = false;

  openButtons.forEach(button => {
    button.addEventListener("click", (event) => {
      event.stopPropagation(); // Spreči da klik van zatvori odmah

      if (isOpen) {
        // Zatvori sidebar
        sidebarContainer.classList.remove("translate-x-0");
        sidebarContainer.classList.add("translate-x-[320px]");
        isOpen = false;
      } else {
        // Otvori sidebar
        sidebarContainer.classList.remove("translate-x-[320px]");
        sidebarContainer.classList.add("translate-x-0");
        isOpen = true;
      }
    });
  });

  // Klik van sidebara zatvara ga
  document.addEventListener("click", (event) => {
    if (
      isOpen &&
      !event.target.closest("#sidebarContainer") &&
      !event.target.closest(".openSidebarBtn")
    ) {
      sidebarContainer.classList.remove("translate-x-0");
      sidebarContainer.classList.add("translate-x-[320px]");
      isOpen = false;
    }
  });
});