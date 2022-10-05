"use strict"

// Get all a tags with class .car-setup
// It returns node list of a tags
const setup_links = document.querySelectorAll('.car-setup');

// loop through a tags
for (let i = 0; i < setup_links.length; i++) {
    // Get a tag href value and slice it
    // 21 symbols from the beginnning and 4 symbols from the end
    const new_url = setup_links[i].href.slice(21, -4);
    // Make change on the page
    setup_links[i].href = new_url;

}

