# Master-Thesis

This project is part of my master thesis called 'Treament and Data Visualization after an Access Right'. The notebooks at the root of this repository unify some data obtained from 
Facebook, Google, Instagram, Snapchat, Swisscom and Whatsapp into a Pandas DataFrame. Once all data are treated, they can be visualized as an
interactive app ran through dash.plotly. The visualization produced display a timeline of all the interactions found in the data, a map of the
locations and a table with the interactions found for a specific day.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You will need to get your [Facebook](https://facebook.com/help/contact/2032834846972583), [Google](https://support.google.com/accounts/answer/3024190), 
[Instagram](https://facebook.com/help/instagram/181231772500920), [Snapchat](https://support.snapchat.com/a/download-my-data),
[WhatsApp](https://faq.whatsapp.com/android/23756533/?category=5245251) data. For Swiss people Swisscom communications can be found on
your Swisscom acccount as csv files for the last 6 months. 

You will need to be able to run jupyter notebook on your computer in order to run the .ipynb files from this repository. 
The [following link](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook) will help you to install and use jupyter
notebook.

The following python packages will need to be installed:

#### General.ipynb - Treament
* [dateutil](https://dateutil.readthedocs.io/en/stable/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)


#### Visualization.ipynb - Visualization
* [plotly](https://plotly.com/python/reference/) and [dash](https://dash.plotly.com/) with the following components in particular:
  * dash_core_components
  * dash_html_components
  * dash_table

A step-by-step series of examples that tell you how to install the environment can be found 
[here](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/).

But most of the time the following code snippet executed in a notebook cell should work:
```
# Install a pip package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install
```
Last but not least, you will need to create a [mapbox account](https://account.mapbox.com/auth/signup/) and add your token in 
Visualization.ipynb

### Get the General and Locations Data Grame 
Once the data have been obtained, gather all of the individual dump files in the same folder as the notebooks `General.ipynb` and `Visualisation.ipynb`, and follow the instruction written on top of the `General.ipynb` notebook.
Attention: some of the files (especially for Google) have to be renamed manually (ex: Google Photos --> Google_Photos)

### Example 
```python

from Package.reader import ReaderComposite
from Package.facebook_sub_readers.like_page import FacebookLikePageReader

#create a ReaderComposite
facebook = ReaderComposite()

#read the `like` page from the facebook data dump and add it to the reader
facebook.add(FacebookLikePageReader('Arthur_Rimbaud_Facebook_Data/likes_and_reactions/pages.json'))

```
Of course you can use all the different readers individually. However, if you want a 'general' DataFrame with all the information that can be treated,
fill in all filepaths in the notebook and run everything. You will obtain an unified DataFrame of the following form: 

Date                | Type     | Label        | Year | Month | Day | Hour
--------------------| ---------|--------------|------|-------|-----|-----
2011-11-26 15:40:26 | Facebook | Message sent | 2011 | 11 | 26 | 15
2012-04-24 03:12:06 | Instagram| Story        | 2012 | 04 | 24 | 03
2013-09-06 12:12:12 | WhatsApp | Sent         | 2013 | 09 | 06 | 12

If you need more informations, change the value of the variables `ALL_INDEX` or `ALL_GENERAL` you can find on top of each reader files in each  submodule. The first one (`ALL_INDEX`) will give you all information treated and the second (`ALL_GENERAL`)
the two most important ones.

At the end of the execution of `General.ipynb`, the final resulting DataFrame as well as 3 other DataFrames of location data are saved as .pkl files which can be read in `Visualisation.ipynb`. 

### Visualization 

If you have localisations data in your Facebook, Google Photos and Snapchat dataset, no particular action with the code from `Visualisation.ipynb` is required. However, if some of them are missing, just erase
missing sets in the Data Treatment section. 

### Thanks and Inspiration 
Huge thanks to my dear friend [Cedric Viaccoz](https://github.com/cedricviaccoz) who gave me the permission to use and change his 
[WhatsAppDataAnalysis](https://github.com/cedricviaccoz/WhatsAppDataAnalysis) repository in this work and helped me through technical 
difficulties.

Another big thanks to my close friend [Arnaud Pannatier](https://github.com/ArnaudPannatier) for his kindness, curly hairs, and huge help all along
this project.

Don't miss the opportunity to check the amazing work proposed by Justin Ellis to get a Pandas DataFrame from Gmail data 
[here](https://jellis18.github.io/post/2018-01-17-mail-analysis/)


### License

This project is licensed under the MIT License - see the LICENSE.md file for details
Acknowledgments
