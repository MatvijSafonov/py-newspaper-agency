document.addEventListener("DOMContentLoaded", function () {
    const toggleSidebarButton = document.getElementById("toggle-sidebar");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");

    toggleSidebarButton.addEventListener("click", function () {
        sidebar.classList.toggle("open");
        mainContent.classList.toggle("sidebar-open");
    });
});