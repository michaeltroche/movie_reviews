# movie_reviews
In this project I will be using sentiment analysis on on Rotten Tomatoes movie reviews for IMDB's top 100 most controversial movies. I do this in the hope to make accurate predictions on users star ratings from their corresponding text review. I will use techniques such as web-scraping, tokenization, stemming and text to sequence processing to get the review into an appropriate format for input into an LSTM neural network. 

### [src](https://github.com/michaeltroche/movie_reviews/tree/main/src) folder contains all source code.
- [scraper](https://github.com/michaeltroche/movie_reviews/tree/main/src/scraper) folder contains all code that scrapes the review data.
   - [movie_scraper.py](https://github.com/michaeltroche/movie_reviews/blob/main/src/scraper/movie_scraper.py) scrapes IMDB's top 100 most controversial movies and saves them to file. 
   -  [review_scraper.py](https://github.com/michaeltroche/movie_reviews/blob/main/src/scraper/review_scraper.py) loops through each movie, scrapes the relevant data and saves each as an individual dataframe.
- [analysis](https://github.com/michaeltroche/movie_reviews/tree/main/src/analysis) folder contains all code that processes and analyses the review data.
  - [sequencer.ipynb](https://github.com/michaeltroche/movie_reviews/tree/main/src/analysis/sequencer.ipynb) concatenates all the movie reviews into one dataframe and then tokenizes, stems and processes the text to numeric sequences to be used as input for the LSTM neural network.
  - [review_analysis.ipynb](https://github.com/michaeltroche/movie_reviews/tree/main/src/analysis/review_analysis.ipynb) will contain the neural network algorithm and full analysis.

### [review_dfs](https://github.com/michaeltroche/movie_reviews/tree/main/review_dfs) folder contains all the saved dfs for each movie review.
### [accesories](https://github.com/michaeltroche/movie_reviews/tree/main/accesories) folder contains a list of IMDB's top 100 most controversial movies.
