const useScrapperBtn = document.getElementById('search-btn');
useScrapperBtn.onclick = use_scraper;

const addToChartBtn = document.getElementById('addToChart-btn');
addToChartBtn.onclick = addToChart;

const dropTableBtn = document.getElementById('dropTable-btn');
dropTableBtn.onclick = () => {
    try {
        dropTable('table');
    } catch (error) {
        console.log(error)
    }
    try {
        dropTable('chart_table');
    } catch (error) {
        console.log(error)
    }
};

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = scrollFunction;

//On click scroll up to the top of the page
const scrollButton = document.getElementById('scrollButton');
scrollButton.onclick = topFunction;

// Loading jQuery from npm module, so error doesn't show
window.jQuery = window.$ = require('jquery');