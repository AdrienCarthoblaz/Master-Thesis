# Master-Thesis

This project is part of my master thesis called 'Treament and Data Visualization after an Access Right'. This notebook unifies some data obtained from 
Facebook, Google, Instagram, Snapchat, Swisscom and Whatsapp into a Pandas Data Frame. Once data are treated they can be visualized as an
interactive app thanks to dash.plotly. This visualization gives you a timeline of all the interactions found in your data, a map of your
locations and a table with the interactions found for a specific day.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You will need to get your [Facebook](https://fr-fr.facebook.com/help/contact/2032834846972583), [Google](https://support.google.com/accounts/answer/3024190), 
[Instagram](https://fr-fr.facebook.com/help/instagram/181231772500920), [Snapchat](https://support.snapchat.com/fr-FR/a/download-my-data),
[WhatsApp](https://faq.whatsapp.com/fr/android/23756533/?category=5245251) data. For Swiss people Swisscom communications can be found on
your Swisscom acccount as csv files for the last 6 months. 

You will need to be able to run jupyter notebook on your computer in order to run the .ipynb files of this repository. 
The [following link](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook) will help you to install and use jupyter
notebook.

The following python packages will need to be installed :

#### General.ipynb - Treament
* ast
* dateutil
* numpy
* pandas


#### Visualization.ipynb - Visualization
* plotly.graph_objs
* dash
* dash_core_components
* dash_html_components
* dash_table

A step by step series of examples that tell you how to install the environment can be found 
[here](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/).

But most of the time the following command will work:
```
# Install a pip package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install
```
Last but not least you will need to create a [mapbox account](https://account.mapbox.com/auth/signup/) and add your token in 
Visualization.ipynb

### Get the General and Locations Data Grame 
Once data have been obtained gather all of them into the same file (where the algorithms are). And just complete paths in general.ipynb.
Attention: some of the files (especially for Google) has to be renamed manually (ex: Google Photos --> Google_Photos)

Example: 
```
facebook.add(FacebookLikePageReader('Arthur_Rimbaud_Facebook_Data/likes_and_reactions/pages.json'))

```
Of course you can use all the reader individually. But if you want a 'general' Data Frame with all the informations which can be treated
just complete all paths and run everything. You will obtained an unified Data Frame of the following form : 

Date                | Type     | Label        | Year | Month | Day | Hour
--------------------| ---------|--------------|------|-------|-----|-----
2011-11-26 15:40:26 | Facebook | Message sent | 2011 | 11 | 26 | 15
2012-04-24 03:12:06 | Instagram| Story        | 2012 | 04 | 24 | 03
2013-09-06 12:12:12 | WhatsApp | Sent         | 2013 | 09 | 06 | 12

If you need more informations change ALL_INDEX or ALL_GENERAL in modules. The first one will give you all informations treated and the second
the two most important ones.

The final Data Frame and location ones are saved as .pkl file which will be read in the visulization files. 

### Visualization 

If you have localisations in your Facebook, Google Photos and Snapchat data, the code is ready to run. If some of them are missing just erease
missing set in the Data Treatment section. 

### Thanks and Inspiration 
Huge thanks to my dear friend [Cedric Viaccoz](https://github.com/cedricviaccoz) who gave me the permission to use and change his 
[WhatsAppDataAnalysis](https://github.com/cedricviaccoz/WhatsAppDataAnalysis) repository in this work and help me through technical 
difficulties.

Another big thanks to my close friend [Arnaud Pannatier](https://github.com/ArnaudPannatier) for his kindness and huge help all along
this project.

Don't miss the opportunity to check the amazing work proposed by Justin Ellis to get a Pandas Data Frame from Gmail data 
[here](https://jellis18.github.io/post/2018-01-17-mail-analysis/)


### License

This project is licensed under the MIT License - see the LICENSE.md file for details
Acknowledgments
