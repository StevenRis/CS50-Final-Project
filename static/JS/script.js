// "use strict"

window.addEventListener('load', (event) => {
    console.log('page is fully loaded');
    showSpinner();
})

//Display spinner while loading the page content
function showSpinner(){
    document.querySelector("#loading").style.display = "none";
    document.querySelector("#content").style.display = "block";
    document.querySelector("footer").style.display = "block";
}

// Get the button
let goTopButton = document.querySelector(".goTopButton");

// Listen to scroll event and display button
window.addEventListener('scroll', () => {
    scrollFunction()
})

// When the user clicks on the button, scroll to the top of the document
goTopButton.addEventListener('click', () => {
    topFunction()
})

// Display button when the user scrolls down 20px from the top of the document
function scrollFunction() {
    if (window.scrollY > 20) {
        goTopButton.style.display = 'block';
    } else {
        goTopButton.style.display = 'none';
    }
}

// Scroll to the top of the document
function topFunction() {
    document.documentElement.scrollTop = 0;
}
