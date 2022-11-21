// "use strict"

window.addEventListener('load', (event) => {
    console.log('page is fully loaded');
    showSpinner();
})

//preloader
function showSpinner(){
    document.querySelector("#loading").style.display = "none";
    document.querySelector("#content").style.display = "block";
    document.querySelector("footer").style.display = "block";
}

// Get all a tags with class .car-setup
// It returns node list of a tags
// const setup_links = document.querySelectorAll('form');
// console.log(setup_links);

// // loop through a tags
// function changeTag() {
//     for (let i = 0; i < setup_links.length; i++) {
//         // Get a tag href value and slice it
//         // 21 symbols from the beginnning and 4 symbols from the end
//         const new_url = setup_links[i].action.slice(26).split(' ').join('_');
//         // const new_url = setup_links[i].action.replace('', '1');
//         console.log(new_url);
//         // Make change on the page
//         setup_links[i].action = new_url;
//     }
// }

// changeTag()
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
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
