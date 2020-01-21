# ceneoOptimizer

Requirements:
https://nodejs.org/
https://electronjs.org
https://www.npmjs.com/package/python-shell



npm insstall - makes 3 files. package-lock, package, node_modules

# Documentation

###### Scraper: 
*engine/scraper.py*  
It's using *offer_scraper.py* for getting data from product page (product table elements) and *regex_pattern* for searching data. Methods and classes are documented in python files (*docstrings*).  
  
###### GUI:   

Function get_chart( ) - it is responsible for retrieving data from chart, where user types data.  
Function addToChart () - creates chart table and fills it with data typed by user in a form.  
Function dropTable() - drops table, so user can start searching again.  
Function topFunction() - used to scroll up the page.  
Function showScrollButton () - shows red button on the screen whenever user scrolls page. This  
button clicked scrolls up the page.  
Function console_out () - console.log() wrapper.  
Function use_scrapper() - it is a wrapper for python-shell instance which runs scrapper.py script.  
When ‚‚message’’ event occurs show_results() callback is fired, which shows data on the screen.  




