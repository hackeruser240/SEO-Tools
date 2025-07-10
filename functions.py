import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
import random
from collections import Counter
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from nltk import ngrams
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from serpapi import GoogleSearch
from gtts import gTTS
from pydub import AudioSegment, silence
from pydub.playback import play
import easyocr
from PIL import Image
import xml.etree.ElementTree as ET 
from datetime import datetime, timezone
import concurrent.futures
from ip2geotools.databases.noncommercial import DbIpCity
from pydub.silence import detect_silence
import re
import whois
from urllib.parse import urlparse
from deep_translator import GoogleTranslator
from bitarray import bitarray


def get_extracted_text(image):
    try:
        executer=concurrent.futures.ThreadPoolExecutor()
        future=executer.submit(extract_text_from_image,image)
        results=(future.result())
        return results
    except Exception as e:
        print(e)
        return None


def password_protect_pdf(file, password):
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    output_buffer = BytesIO()
    writer.write(output_buffer)
    return output_buffer.getvalue()


def generate_meta_tags(title,descriptions,keywords,language,revisit_after,
                       robots,author,content_type,index):

    meta_title = f'<meta name="title" content="{title}">'
    meta_description = f'<meta name="description" content="{descriptions}">'
    meta_keywords = f'<meta name="keywords" content="{keywords[0], keywords[1], keywords[2]}">'
    meta_language = f'<meta name="language" content="{language}">'
    meta_robots = f'<meta name="robots" content="{index}index,{robots}follow">'
    meta_revist_after = f'<meta name="revisit-after" content="{revisit_after} day">'
    meta_author = f'<meta name="author" content="{author}">'
    meta_content=f'<meta http-equiv="Content-Type" content="text/html; charset={content_type}">'

    return meta_title,meta_description,meta_keywords,meta_content,meta_language,meta_author,meta_robots,meta_revist_after


def generate_password(length, use_numbers=True, use_special_chars=True, use_capital_chars=True):
    characters = string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    if use_capital_chars:
        characters += string.ascii_uppercase

    if not (use_numbers or use_special_chars or use_capital_chars):
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password



def backlink_maker(url):
    websites = [
        f"https://builtwith.com/{url}",
        f"https://validator.w3.org/check?uri={url}",
        f"http://whois.tools4noobs.com/info/{url}",
        f"https://www.alexa.com/siteinfo/{url}",
        f"http://www.robtex.com/dns/{url}.html",
        f"http://www.quantcast.com/{url}",
        f"http://www.backtalk.com/?url={url}/",
        f"http://hostcrax.com/siteinfo/{url}",
        f"http://uptime.netcraft.com/up/graph?site={url}",
        f"http://www.pageheat.com/heat/{url}",
        f"http://siteranker.com/SiteInfo.aspx?url={url}/&E=1",
        f"http://www.aboutthedomain.com/{url}",
        f"http://www.onlinewebcheck.com/check.php?url={url}",
        f"http://whoisx.co.uk/{url}",
        f"https://www.whois.com/whois/{url}",
        f"https://www.urltrends.com/rank/{url}",
        f"http://www.websiteaccountant.nl/{url}",
        f"http://www.talkreviews.ro/{url}",
        f"http://www.statshow.com/www/{url}/",
        f"http://www.listenarabic.com/search?q={url}&sa=Search",
        f"http://www.keywordspy.com/research/search.aspx?q={url}&tab=domain-overview",
        f"http://www.websiteaccountant.be/{url}",
        f"http://www.altavista.com/yhs/search?fr=altavista&itag=ody&kgs=0&kls=0&q=site:{url}",
        f"http://siteanalytics.compete.com/{url}/",
        f"http://www.serpanalytics.com/#competitor/{url}/summary//1",
        f"http://hosts-file.net/default.asp?s={url}",
        f"http://whois.domaintools.com/{url}",
        f"http://www.folkd.com/detail/{url}",
        f"http://script3.prothemes.biz/{url}",
        f"http://www.who.is/whois/{url}",
        f"http://www.websitedown.info/{url}",
        f"http://www.worthofweb.com/website-value/{url}/",
        f"http://www.siteworthtraffic.com/report/{url}",
        f"http://hqindex.org/{url}",
        f"https://valueanalyze.com/show.php?url={url}",
        f"http://www.domainwhoisinfo.com/{url}",
        f"http://www.siteprice.org/website-worth/{url}",
        f"http://howmuchdomainnameworth.com/process.php?q={url}&t=auto",
        f"http://toolbar.netcraft.com/site_report?url={url}",
        f"https://semrush.com/info/{url}",
        f"http://www.siteranker.com/TrankTrend.aspx?url={url}/",
        f"https://website.ip-adress.com/{url}",
        f"http://web.horde.to/{url}",
        f"https://www.woorank.com/en/www/{url}",
        f"http://scamanalyze.com/check/{url}.html",
        f"http://www.infositeshow.com/sites/{url}",
        f"http://www.serpanalytics.com/sites/{url}",
        f"http://www.ultimate-rihanna.com/?url={url}",
        f"http://ranking.websearch.com/siteinfo.aspx?url={url}",
        f"https://deviantart.com/users/outgoing?{url}",
        f"https://proza.ru/go/{url}",
        f"https://webwiki.de/{url}",
        f"http://www.viewwhois.com/{url}/",
        f"http://w3seo.info/WSZScore/{url}/",
        f"http://www.talkreviews.com/{url}/",
        f"http://archive.is/{url}/",
        f"http://ranking.crawler.com/SiteInfo.aspx?url={url}/",
        f"http://dig.do/{url}",
        f"http://web.archive.org/web/*/{url}/",
        f"http://www.websitelooker.net/www/{url}/",
        f"http://whois.phurix.co.uk/{url}/",
        f"http://{url}.whoisbucket.com/",
        f"https://dnswhois.info/{url}",
        f"https://rbls.org/{url}",
        f"https://stuffgate.com/{url}",
        f"https://whois.de/{url}",
        f"https://statscrop.com/www/{url}",
        f"https://evi.com/q/{url}",
        f"https://similarto.us/{url}",
        f"https://mywot.com/en/scorecard/{url}",
        f"https://whoislookupdb.com/whois-{url}",
        f"http://website.informer.com/{url}",
        f"http://500v.net/site/{url}/",
        f"http://websitedetailed.com/{url}/",
        f"https://www.seoptimer.com/{url}",
        f"https://a.pr-cy.ru/{url}/",
        f"https://be1.ru/stat/{url}",
        f"https://ibm.com/links/?cc=us&lc=en&prompt=1&url=//{url}",
        f"https://addtoany.com/share_save?linkname=&linkurl={url}",
        f"http://sitevaluefox.com/website-value-calculator/show.php?url={url}",
        f"http://alexaview.com/process.php?q={url}&t=auto",
        f"http://{url}.hypestat.com",
        f"http://urlrate.com/process.php?q={url}&t=auto",
        f"http://{url}.w3lookup.net",
        f"https://spyfu.com/overview/domain?query={url}",
        f"https://transtats.bts.gov/exit.asp?url={url}",
        f"https://water.weather.gov/ahps2/nwsexit.php?url={url}",
        f"https://w3techs.com/sites/info/{url}",
        f"https://duckduckgo.com/{url}?ia=web",
        f"https://domainsigma.com/whois/{url}",
        f"https://search.com/search?q={url}"
    ]
    return websites


def generate_and_display_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
        "steps": 40,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 5,
        "samples": 1,
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
        ],
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "sk-59SJgYZOsJ4zTqTn0rsYbCCKPhb6ffpbAknJIcU1mpmbCmkW", #use this authroization key if the other one is finished sk-YWTtiWcndaoQSoh13l3h1gurT1yUnFsSNIUjpz4tJqIAwtnb
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        return "Error generating image"

    data = response.json()

    # Get the base64 image data
    image_data = data["artifacts"][0]["base64"]

    # Convert base64 to data URI
    data_uri = f"data:image/png;base64,{image_data}"

    # Display the image in the browser
    return data_uri


def bits_to_string(bits):
    bts = bitarray(bits)
    ascs = bts.tobytes().decode('utf-8')
    return ascs

def string_to_bit(string):
    bstr = ' '.join(format(ord(c), '08b') for c in string)
    return bstr

def ssl_certification(url):
    try:
        response = requests.get(url)

        # Check if the URL starts with 'https://'
        if response.url.startswith('https://'):
            return f"{url} has SSL Certification"
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_meta_tag(url):
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the meta title and meta description tags
    meta_title = soup.find('meta', {'name': 'title'} or {'property': 'og:title'})
    meta_description = soup.find('meta', {'name': 'description'} or {'property': 'og:description'})

    # Extract content from the tags
    title_content = meta_title.get('content') if meta_title else None
    description_content = meta_description.get('content') if meta_description else None

    return title_content, description_content

def get_text_from_website(url):
        # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract all text content
    text_content = ' '.join([
        tag.get_text() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span','header'])
    ])
    return text_content


def tranlate_txt(txt,language):    
    dictionary={'Amharic':'am','Arabic':'ar','Basque':'eu','Bengali':'bn','English (UK)':'en-GB','Portuguese (Brazil)':'pt-BR','Bulgarian':'bg','Catalan':'ca',
            'Cherokee':'chr',"Croatian":"hr","Czech":"cs","Danish":"da","Dutch":"nl","English (US)":"en","Estonian":"et","Filipino":"fil","Finnish":"fi",
            "French":"fr","German":"de","Greek":"el","Gujarati":"gu","Hebrew":"iw","Hindi":"hi","Hungarian":"hu","Icelandic":"is","Indonesian":"id","Italian":"it",
            "Japanese":"ja","Kannada":"kn","Korean":"ko","Latvian":"lv","Lithuanian":"lt","Malay":"ms","Malayalam":"ml","Marathi":"mr","Norwegian":"no","Polish":"pl",
            "Portuguese (Portugal)":"pt-PT","Romanian":"ro","Russian":"ru","Serbian":"sr","Chinese (PRC)":"zh-CN","Slovak":"sk","Slovenian":"sl","Spanish":"es","Swahili":"sw",
            "Swedish":"sv","Tamil":"ta","Telugu":"te","Thai":"th","Chinese (Taiwan)":"zh-TW","Turkish":"tr","Urdu":"ur","Ukrainian":"uk","Vietnamese":"vi","Welsh":"cy"}
    translated=GoogleTranslator(source='auto',target=dictionary.get(language)).translate(txt)
    return translated


def find_emails(url):
    try:
            
        # Fetch the HTML content of the webpage
        response = requests.get(url)

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Use a regular expression to find email addresses
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = re.findall(email_pattern, str(soup))
        return emails
    except:
        return "Error Found"


def update(frame,ax,external_links,internal_links):
    ax.clear()

    # Bar graph data
    categories = ['External Links', 'Internal Links']
    lengths = [len(external_links), len(internal_links)]

    ax.bar(categories, lengths, color=['blue', 'green'])
    ax.set_title('Length of External and Internal Links')

def internal_external(url):
    external_links=[]
    internal_links=[]
    try:
        if "https" not in url:
            url="https://"+url
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        parse=urlparse(url)
        base_url=parse.netloc
        # print(base_url)
        for link in links:
            if base_url not in link:
                external_links.append(link)
            else:
                internal_links.append(link)
    except Exception:
        return f"Error fetching URL {url}"
    return external_links, internal_links



def domain_age(url):
    whois_info = whois.whois(url)

    creation_date = whois_info.creation_date
    expiry_date = whois_info.expiration_date

    if creation_date and expiry_date:
        today = datetime.now()

        # Calculate domain age
        age = today - creation_date
        years = age.days // 365
        months = (age.days % 365) // 30
        days = (age.days % 365) % 30
        time_until_expiry = expiry_date - today
        # Calculate time remaining until expiry
        domain_age= f"Domain Age: {years} years, {months} months, {days} days"
        create=f"Creation Date: {creation_date.strftime('%Y-%m-%d')}"
        ex_date=f"Expiry Date: {expiry_date.strftime('%Y-%m-%d')}"
        time_remaining=f"Time Remaining until Expiry: {time_until_expiry.days} days"
        registrar=f"Registrar: {whois_info.registrar}" 
        return create,domain_age,ex_date,time_remaining,registrar
    else:
        return "Creation or expiry data not found"
        
        
def grammar_check(text):
    url = "https://api.languagetool.org/v2/check"
    payload = {"text": text, "language": "en-US"}
    response = requests.post(url, data=payload)
    results = response.json()
    print(results)
    if 'matches' in results and results['matches'] and 'replacements' in results['matches'][0]:
        print(results)
        return results
    else:
        return "Something Went Wrong Here"


def get_header(website):
    name=[]
    result=[]
    try:
        response=requests.get(website)
        headers=response.headers
        for header in headers:
            name.append(header)
            result.append(headers.get(header))

        return name,result
    except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
        return "Please Enter A Valid URL\nExample: https://www.seomasterz.com"
        
        
def regex_replace(s, find, replace):
    return re.sub(find, replace, s)

def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    ip_address=res.ip_address
    city=res.city
    region=res.region
    country=res.country
    latitude=res.latitude
    longitude=res.longitude

    return ip_address,city,region,country,latitude,longitude
    


def get_threading_results(text):
    try:
        executer=concurrent.futures.ThreadPoolExecutor()
        future=executer.submit(get_urls,text)
        results=(future.result())
        return results
    except:
        return "Something happened"

def get_urls(base_url):
    print("Loading your website's sitemap, wait please a few moments :)")
    response=requests.get(base_url)
    try:
        soup=BeautifulSoup(response.text,'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        into_set=set(links)
        into_list=list(into_set)
        print(base_url)
        for links in into_list:
            if base_url not in links:
                into_list.remove(links)
        # print(into_list)
        return into_list
    except requests.exceptions.MissingSchema:
        return f"Such Site Does Not Exist. Please Enter A Valid Link"


def create_xml(list_of_urls):
    current_time_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    formatted_time = current_time_utc.strftime('%Y-%m-%dT%H:%M:%S%z')
    if type(list_of_urls)==str:
        return list_of_urls
    else:
        urlset_tag = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for link in list_of_urls:
            url_tag = ET.SubElement(urlset_tag, 'url')
            loc_tag = ET.SubElement(url_tag, 'loc')
            lastmod_tag = ET.SubElement(url_tag, 'lastmod')
            priority_tag = ET.SubElement(url_tag, 'priority')

            loc_tag.text = link
            lastmod_tag.text = formatted_time
            priority_tag.text = '1.00'
            ET.SubElement(urlset_tag, '').tail = '\n'


        tree = ET.ElementTree(urlset_tag)
        buffer=BytesIO()
        tree.write(buffer,encoding='utf-8', xml_declaration=True)
        return buffer.getvalue()
        

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    try:
        # Create an OCR reader using the Tesseract engine
        img=Image.open(BytesIO(image_path.read()))
        img_bytesio=BytesIO()
        img.save(img_bytesio,format='PNG')
        result=reader.readtext(img_bytesio.getvalue())
        # Extract text from the result
        text = ' '.join([entry[1] for entry in result])

        return text.strip()
    except Exception as e:
        print(e)
        return f"error: {e}"

def download_audio(text):

    tts = gTTS(text=text, lang='en')
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    return audio_stream

def play_audio(text):
    tts=gTTS(text=text,lang='en')
    audio_stream=BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    audio = AudioSegment.from_file(audio_stream, format="mp3")

    # Detect silence in the audio
    segments = silence.detect_silence(audio, silence_thresh=-40)

    return audio, segments

def interest_by_region(query):
    params = {
        "api_key": "be3c4b47861cc070d3ce811c749b41edfc43524b21f9798d91010d1b50527b3a",
        "engine": "google_trends",
        "q": query,
        "data_type": "GEO_MAP_0"
    }

    search = GoogleSearch(params)
    data = search.get_dict()
    print(data)
    locations = [item['location'] for item in data['interest_by_region']]
    values = [float(item['value']) if item['value'] != '<1' else 0.5 for item in data['interest_by_region']]   
    return locations, values 

def get_text_frequencies(text,n):
    text = text.replace('\n', ' ').replace('\t', '')

    # Tokenize the text into words
    words = text.split()

    # Remove punctuation
    words = [''.join(c for c in word if c not in string.punctuation) for word in words]

    # Filter out stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    # Generate n-grams
    n_grams = list(ngrams(words, n))

    # Count n-gram frequencies
    count_ngrams = Counter(n_grams)

    # Calculate the percentage of each n-gram's occurrence
    total_ngrams = len(n_grams)
    sorted_count = count_ngrams.most_common(20)

    for iteration in range(len(sorted_count)):
        ngram, count = sorted_count[iteration]
        percentage = round(count / total_ngrams * 100, 2)
        sorted_count[iteration] = [' '.join(ngram), count, f"{percentage}%"]

    return sorted_count

def get_word_frequencies(url,n):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text = text.replace('\n', ' ').replace('\t', '')

        # Tokenize the text into words
        words = text.split()

        # Remove punctuation
        words = [''.join(c for c in word if c not in string.punctuation) for word in words]

        # Filter out stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.lower() not in stop_words]

        # Generate n-grams
        n_grams = list(ngrams(words, n))

        # Count n-gram frequencies
        count_ngrams = Counter(n_grams)

        # Calculate the percentage of each n-gram's occurrence
        total_ngrams = len(n_grams)
        sorted_count = count_ngrams.most_common(20)

        for iteration in range(len(sorted_count)):
            ngram, count = sorted_count[iteration]
            percentage = round(count / total_ngrams * 100, 2)
            sorted_count[iteration] = [' '.join(ngram), count, f"{percentage}%"]

        return sorted_count
    except:
        return "Something Went Wrong"

def plot_word_frequencies(word_frequencies):
    words = [entry[0] for entry in word_frequencies]
    frequencies = [entry[1] for entry in word_frequencies]

    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Word Frequencies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the image as base64
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')

    return encoded_image

def get_backlinks(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        return links
    except:
        print(f"Error fetching URL:")
        return None

def check_backlink_status(backlink):
    try:
        response = requests.get(backlink)
        return response.status_code
    except:
        print(f"Error checking backlink status for {backlink}")
        return None
    

def get_wordnet_pos(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('R'):
        return wordnet.ADV
    elif tag.startswith('J'):
        return wordnet.ADJ
    else:
        return wordnet.NOUN  # default to noun if no specific mapping

def replace_synonyms(word, pos):
    synsets = wordnet.synsets(word, pos=get_wordnet_pos(pos))
    if synsets:
        synonyms = [lemma.name() for syn in synsets for lemma in syn.lemmas()]
        if synonyms:
            return random.choice(synonyms)
    return word

def rewrite_sentence(sentence):
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    lemmatizer = WordNetLemmatizer()

    new_sentence = []
    for word, pos in pos_tags:
        if pos.startswith(('NN', 'VB', 'RB', 'JJ')):
            new_word = replace_synonyms(lemmatizer.lemmatize(word, get_wordnet_pos(pos)), pos)
            new_sentence.append(new_word)
        else:
            new_sentence.append(word)

    return ' '.join(new_sentence)

def rewrite_article(article):
    sentences = sent_tokenize(article)
    rewritten_article = [rewrite_sentence(sentence) for sentence in sentences]
    return ' '.join(rewritten_article)

def read_doc_contents(file):
    word_count = 0
    if file.filename.endswith('.docx') or file.filename.endswith('.doc'):
        buffer = BytesIO(file.read())
        doc = Document(buffer)
        for paragraph in doc.paragraphs:
            word_count += len(paragraph.text.split())

    return word_count
    
def read_pdf_contents(pdf_file):
    words = []
    buffer = BytesIO(pdf_file.read())
    pdf_reader = PyPDF2.PdfReader(buffer)
    
    pages = pdf_reader.numPages
    for x in range(0, pages):
        pageObj = pdf_reader.getPage(x)
        text = pageObj.extractText()
        count = len(text.split())
        words.append(count)

    total_words = sum(words)
    return total_words
