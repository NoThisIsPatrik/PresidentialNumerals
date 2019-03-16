# PresidentialNumerals

It's Pi day, and this guy I know posted a picture of Thomas Jefferson, a dot, Washinton, and James Madison. Because, number 3, dot, 1, 4. Which is somewhat clever, took a second, though didn't grow up in the US, so perhaps I get a slight pass. Anyhow, I wondered if perhaps it should be.. whomever was 31, then 41 (which even I know was Bush Sr). Or some combination of that, in some way.

So, in the interest of driving almost any fleeting curiosity too far, here's a generator. It uses a list and a set of thumbnails from wikipedia, throuh they are included here. As is the download/parse code, which will probably break in a bit when something changes on the wikimedia pages.

![Example image](https://github.com/NoThisIsPatrik/PresidentialNumerals/blob/master/piday.jpg)

By default, it does pi, up to 32 digits, and store the image in piday.jpg. You can specify and output file, and also an input file (-f file) or a number (-n 123) if you want to do something other than Pi (reverse phone number captcha?). You can also limit the number of digits/decimals (-l 10). If you want to make this super obivious, it can also add name captions (-name) or the number itself overlayed (-numb).

![Example image](https://github.com/NoThisIsPatrik/PresidentialNumerals/blob/master/piday_with_names.jpg)

![Example image](https://github.com/NoThisIsPatrik/PresidentialNumerals/blob/master/piday_w_numbers.jpg)

It's in python3 (and won't run in 2, though not through using anything that out there). It uses PIL/pillow to manipulate images, and if you try to have it download the list of presidents/images, it'll use BeautifulSoup 4 and requests. It'll run fine witout them if it has it's files with it though.

Happy Pi day!


Oh, and the font file, AbrahamLincoln.ttf, is from https://befonts.com/presidential-dollars.html and by Behance. I wanted a font that was actually there ('cos PIL needs one for writing) and wanted one that looked like the presidential fonts look, but not super strict licenced, which I think this is. But it does have restrictions, so don't just randomly use it for other stuff without also checking if that's within whatever the limits were.

<h2>PREREQUISITS</h2>

* python 3.0 ("apt-get install python3" on debian and similar)
* PIL/pillow
* BeautifulSoup4 (optional)
* Requests (optional)

All three can, after cloning, be installed with
<pre>python3 -mpip install -r requirements.txt</pre>
or with pipenv, virtualenv, docker via k8s.. however you roll installing some super common packages while keeping a clean environment.

<h2>BUILD</h2>

Umm, no, just:

<code>git clone https://github.com/NoThisIsPatrik/PresidentialNumerals.git</code>

and you should be good to go.

