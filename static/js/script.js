document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = [
        { button: "servicesBtn1", menu: "servicesMenu1" },
        { button: "servicesBtn2", menu: "servicesMenu2" }
    ];

    let activeMenu = null; // Drži referencu na trenutno otvoren meni

    dropdowns.forEach(({ button, menu }) => {

        const btn = document.getElementById(button);
        const menuElement = document.getElementById(menu);

        btn.addEventListener("click", (event) => {
            event.stopPropagation(); // Sprečava zatvaranje menija kada kliknemo na dugme

            if (activeMenu && activeMenu !== menuElement) {
                activeMenu.style.maxHeight = "0"; // Zatvori prethodni meni
                btn.classList.toggle("rotate-180");

            }

            if (menuElement.style.maxHeight === "0px" || !menuElement.style.maxHeight) {
                menuElement.style.maxHeight = menuElement.scrollHeight + "px"; // Otvori meni
                activeMenu = menuElement;
                btn.classList.toggle("rotate-180");
            } else {
                menuElement.style.maxHeight = "0"; // Zatvori meni ako je već otvoren
                activeMenu = null;
                btn.classList.toggle("rotate-180");
            }
        });
    });

    // Klik van menija zatvara otvoreni meni
    document.addEventListener("click", () => {
        if (activeMenu) {
            activeMenu.style.maxHeight = "0";
            activeMenu = null;
        }
    });

    // Sprečava zatvaranje kada kliknemo unutar menija
    dropdowns.forEach(({ menu }) => {
        document.getElementById(menu).addEventListener("click", (event) => {
            event.stopPropagation();
        });
    });




});
