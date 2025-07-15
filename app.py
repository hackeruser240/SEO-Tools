from flask import Flask,flash,render_template,request, send_file, send_from_directory,flash, jsonify, redirect
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.parse
import hashlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import socket
import qrcode
import pyshorteners
from itertools import zip_longest
from time import time
import datetime
from forms import *
from functions import *
app=Flask(__name__)
app.config['SECRET_KEY']='asdassdasdasqeqwqweqwe'
app.jinja_env.filters['regex_replace'] = regex_replace

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"),500
    
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"),404



@app.route('/')
def homepage():
    user_ip = request.remote_addr
    ip,city,region,country,lats,longs=printDetails(user_ip)
    # Get current timestamp
    timestamp = datetime.now()

    # Log user access information
    with open('user_information.txt', 'a') as log_file:
        log_file.write(f"User accessed at {timestamp} from IP address {ip} from {city},{country}\n")
    return render_template("home.html")
    
    
@app.route('/all-seo-tools')
def all_tools():
    return render_template("seo_tools.html")
    
@app.route('/keyword-seo-tools')
def keyword_tools():
    return render_template("keyword_based.html")
    
@app.route('/website-seo-tools')
def website_tools():
    return render_template("website_based.html")
    
@app.route('/domain-seo-tools')
def domain_tools():
    return render_template("domain_based.html")
    
@app.route('/miscellaneous-seo-tools')
def miscellaneous_tools():
    return render_template("extra.html")
    
@app.route('/word-seo-tools')
def word_tools():
    return render_template("word_based.html")
    
    
def main():
    form=SearchResults()
    to_search = []
    count = 0
    if form.validate_on_submit():
        url=form.url.data
        keywords=form.keyword.data

        google = f'https://www.google.com/search?q={keywords}&num=50'
        response = requests.get(google)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if 'url?q=' in a['href']]
        # Extracting website URLs from backlinks
        websites = [link.split('url?q=')[1].split('&sa=')[0] for link in links]
        to_search.extend(websites)
        try:
            position=to_search.index(f'{url}/')
            position=position+1
        except ValueError:
            print("url was not found")
        for link in to_search:
            if url in link:
                count+=1
        return render_template('google.html',url=url,count=count,position=position,form=form)
    return render_template('google.html',form=form,to_search=to_search)
@app.route("/find-fix-broken-links", methods=['GET', 'POST'])
def broken_link():
    form = Broken_Link_Form()
    url=form.url.data
    string={}
    if form.validate_on_submit():
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url=response.url
            links = [a['href'] for a in soup.find_all('a', href=True)]
            for link in links:
                absolute_url=urljoin(base_url,link)
                response = requests.get(absolute_url)
                string[absolute_url] = response
            if string:
                return render_template("results.html",form=form,string=string)
            else:
                flash('info no links were found on the webiste','info')
        except:
            flash('error fetching url','error')
    
    return render_template('results.html',form=form)

@app.route('/advanced-online-paraphrasing-tool',methods=['GET','POST'])
def paraphrase():
    form = Article_Rewriter()
    text = ""  # Initialize text for GET requests or if form validation fails

    if form.validate_on_submit():
        content = form.paragraph.data
        print(f"DEBUG: Input content received: {content[:100]}...") # Print first 100 characters of input

        try:
            text = rewrite_article(content)
            print(f"DEBUG: Rewritten text generated: {text[:100]}...") # Print first 100 characters of output
        except Exception as e:
            text = f"An error occurred during article rewriting: {e}"
            print(f"ERROR: rewrite_article function failed: {e}")

        return render_template('paraphrase.html', text=text, form=form)
    
    # This block handles GET requests or when form validation fails (e.g., initial page load)
    return render_template("paraphrase.html", form=form, text=text)

@app.route("/discover-profitable-keywords",methods=['POST',"GET"])
def keyword():
    form=SearchForm()
    if form.validate_on_submit():
        url = "https://auto-suggest-queries.p.rapidapi.com/suggestqueries"

        querystring = {"query":form.searchbar.data}

        headers = {
	    "X-RapidAPI-Key": "099cfd811cmsh3102e8b20caed64p102e0ajsn9443cc66db66",
	    "X-RapidAPI-Host": "auto-suggest-queries.p.rapidapi.com"
                }
        response = requests.get(url, headers=headers, params=querystring)
        tohtml=response.json()
        return render_template("keyword.html",form=form,tohtml=tohtml)
    return render_template("keyword.html",form=form)
@app.route("/natural-sounding-speech-online", methods=['POST', 'GET'])
def text_to_speech():
    if request.method == 'POST':
        text = request.form.get('paragraph')
        button_click = request.form.get('submit-button')

        if button_click == "Speak":
            audio, segments = play_audio(text)
            temp_path = 'temp_audio.mp3'
            audio.export(temp_path, format="mp3")

            return render_template('texttospeech.html', audio_path=temp_path, segments=segments)
        elif button_click=='Download':
            audio_stream=download_audio(text)
            audio_stream.seek(0)
            flash("success File Downloaded Successfully",'success')
            return send_file(
                audio_stream,
                as_attachment=True,
                download_name='generated_audio.mp3',
                mimetype='audio/mpeg'
            )
        else:
            return "Invalid Request"
    return render_template('texttospeech.html')
    
    
    
@app.route('/analyze-keyword-density', methods=['GET', 'POST'])
def keyword_density():
    form = Keyword_Density_Form()
    if request.method=='POST':
        text=form.paragraph.data
        url = form.url.data
        button_click=request.form.get('submit-button')
        if button_click=='Download':
            print("Text logic executed")
            # print(text)
            word_frequencies = get_text_frequencies(text,1)
            print(word_frequencies)
            plot = plot_word_frequencies(word_frequencies)
            word_frequencies2 = get_text_frequencies(text,2)
            print(word_frequencies2)
            plot2 = plot_word_frequencies(word_frequencies2)
            word_frequencies3 = get_text_frequencies(text,3)
            plot3 = plot_word_frequencies(word_frequencies3)
            print(word_frequencies3)
            return render_template("density.html", form=form,
                                    plot=plot, word_frequencies=word_frequencies,plot2=plot2, word_frequencies2=word_frequencies2,
                                    plot3=plot3, word_frequencies3=word_frequencies3)
        elif button_click!='Download':
            print("this is the url")
            word_frequencies = get_word_frequencies(url,1)
            if type(word_frequencies)==str:
                flash("error provided wrong url, please try again",'error')
            else:
                plot = plot_word_frequencies(word_frequencies)
                word_frequencies2 = get_word_frequencies(url,2)
                plot2 = plot_word_frequencies(word_frequencies2)
                word_frequencies3 = get_word_frequencies(url,3)
                plot3 = plot_word_frequencies(word_frequencies3)
                return render_template("density.html", form=form,
                                    plot=plot, word_frequencies=word_frequencies,plot2=plot2, word_frequencies2=word_frequencies2,
                                    plot3=plot3, word_frequencies3=word_frequencies3)
        else:
            invalid="Something Went Wrong Please Try Again"
            return render_template("density.html",form=form,invalid=invalid)
    return render_template("density.html", form=form)

@app.route("/secure-file-upload-service", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        text = request.form.get('text')
        file = request.files.get('files')

        if text:
            count = len(text.split())
            return render_template("uploadfile.html", count=count)
        elif file and (file.filename.endswith('.pdf')):
            total_words = read_pdf_contents(file)
            return render_template("uploadfile.html", total_words=total_words)
        elif file and (file.filename.endswith('.docx')) or file.filename.endswith('.doc'):
            total_words=read_doc_contents(file)
            return render_template('uploadfile.html',total_words=total_words)
        else:
            flash("error Wrong File Format. Upload PDF or DOCX Only",'error')

    return render_template("uploadfile.html")
@app.route("/md5-hash-generator",methods=['GET','POST'])
def md5_converter():
    if request.method=='POST':
        text=request.form.get("text")
        convert=hashlib.md5(text.encode('UTF-8'))
        converted_text=convert.hexdigest()
        return render_template("md5.html",converted_text=converted_text)
    return render_template("md5.html")
@app.route('/keyword-trend-analysis',methods=['GET','POST'])
def keyword_trends():
    form=Trends_Form()
    if form.validate_on_submit():
        keyword=form.keyword.data
        locations,values= interest_by_region(keyword)
        plt.figure(figsize=(10, 6))
        plt.bar(locations, values, color='blue')
        plt.xlabel('Location')
        plt.ylabel('Value')
        plt.title(f'Interest in {keyword} by Location')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the plot as an image
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        
        # Close the plot if you don't want to display it
        plt.close()
        
        # Reset the stream position to the beginning
        image_stream.seek(0)
        
        # Encode the image as base64 and return
        graph = base64.b64encode(image_stream.read()).decode('utf-8')
        return render_template('trends.html',form=form,graph=graph,locations=locations,values=values)
    return render_template("trends.html",form=form)
    
    
@app.route("/extract-text-from-images",methods=['GET','POST'])
def image_to_text():
    if request.method=="POST":
        file=request.files.get('files')
        text=get_extracted_text(file)
        if text == None:
            flash("error Please Try Again.",'error')
        else:
            return render_template('imagetotext.html',text=text)
        
    return render_template("imagetotext.html")
    
    
    
lists=[]
@app.route('/create-sitemap-for-seo', methods=['GET', 'POST'])
def create_sitemap():
    global lists

    if request.method == 'POST':
        text = request.form.get('text')
        button_click = request.form.get('submit-button')

        if button_click == "get-tables":
            # Handle generating URLs here
            urls = get_threading_results(text)
            if type(urls)==str:
                flash("error Invalid URL Provided",'error')
            else:   
                lists=urls
                return render_template("sitemap.html", lists=lists)
        else:
            return "Invalid Request"
    lists=[]
    return render_template('sitemap.html', lists=lists)
    
    
    
@app.route("/download_file",methods=["GET","POST"])
def download_file():
    global lists
        # Handle downloading file here
    xml_content = create_xml(lists)
    flash("File Downloaded Succcessfully",'success')
    return send_file(
        BytesIO(xml_content),
        mimetype='application/xml',
        as_attachment=True,
        download_name='sitemap.xml'
    )

data_to_write="" #intilizing of a global variable
@app.route("/generate-robot",methods=['GET','POST'])
def generate_roboto_txt():
    global data_to_write #using of global variable
    bytes_io=BytesIO()
    forms=Robots_Txt_Form()
    if request.method=='POST':
        button_click = request.form.get('submit-button')
        if button_click=="Speak":
            default=request.form.get("default")
            xml=forms.xml.data
            unallowed_directory0=forms.disallow0.data
            unallowed_directory=forms.disallow.data
            unallowed_directory1=forms.disallow1.data
            unallowed_directory2=forms.disallow2.data
            google=request.form.get("google")
            google_images=request.form.get("images")
            google_mobiles=request.form.get("mobile")
            msn=request.form.get("msn")
            yahoo=request.form.get("yahoo")
            yahoo_blogs=request.form.get("blogs")
            yahoo_mm=request.form.get("mm")
            gigi=request.form.get("gigi")
            dmoz=request.form.get("dmoz")
            ask=request.form.get("ask")
            nutch=request.form.get("nutch")
            alexa=request.form.get("alexa")
            baidu=request.form.get("baidu")
            pic=request.form.get("pic")
            if default=="Allow":
                if unallowed_directory0:
                    unallowed_directory0=f"Disallow:{unallowed_directory0}"

                if unallowed_directory:
                    unallowed_directory=f"Disallow:{unallowed_directory}"

                if unallowed_directory1:
                    unallowed_directory1=f"Disallow:{unallowed_directory1}"
                    
                if unallowed_directory2:
                    unallowed_directory2=f"Disallow:{unallowed_directory2}"
                if xml:
                    xml=f"Sitemap:{xml}"
                
                data_to_write=f"""#robots.txt generated by seomasterz.com\nUser-agent:*\n{unallowed_directory0}\n{unallowed_directory}\n{unallowed_directory1}\n{unallowed_directory2}\nDisallow:\n{xml}
                
                """
                # bytes_io.write(data_to_write.encode())
                # bytes_io.seek(0)
                striped=data_to_write

                return render_template("robots.html",form=forms,striped=striped)
            else:
                if google!="Allow":
                    google="User-agent: Googlebot\nDisallow: /"
                else:
                    google=""
                if google_images!="Allow":
                    google_images="User-agent: googlebot-image\nDisallow: /"
                else:
                    google_images=""
                if google_mobiles!="Allow":
                    google_mobiles="User-agent: googlebot-mobile\nDisallow: /"
                else:
                    google_mobiles=""
                if msn!="Allow":
                    msn="User-agent: MSNBot\nDisallow: /"
                else:
                    msn=""
                if yahoo!="Allow":
                    yahoo="User-agent: Slurp\nDisallow: /"
                else:
                    yahoo=""
                if yahoo_blogs!="Allow":
                    yahoo_blogs="User-agent: yahoo-blogs/v3.9\nDisallow:/"
                else:
                    yahoo_blogs=""

                if yahoo_mm!="Allow":
                    yahoo_mm="User-agent: yahoo-mmcrawler\nDisallow:/"
                else:
                    yahoo_mm=""
                if gigi!="Allow":
                    gigi="User-agent: Gigabot\nDisallow:/"
                else:
                    gigi=""
                if dmoz!="Allow":
                    dmoz="User-agent: Robozilla\nDisallow:/"
                else:
                    dmoze=""
                if ask!="Allow":
                    ask="User-agent: Teoma\nDisallow:/"
                else:
                    ask=""
                if nutch!="Allow":
                    nutch="User-agent: Nutch\nDisallow:/"
                else:
                    nutch=""
                if alexa!="Allow":
                    alexa="User-agent: ia_archiver\nDisallow:/"
                else:
                    alexa=""
                if baidu!="Allow":
                    baidu="User-agent: baiduspider\nDisallow:/"
                else:
                    baidu=""
                if pic!="Allow":
                    pic="User-agent: psbot\nDisallow:/"
                else:
                    pic=""
                data_to_write=f"""#robots.txt generated by seomasterz.com\n{google}\n{google_images}\n{google_mobiles}\n{msn}\n{yahoo}\n{gigi}\n{dmoz}\n{ask}\n{nutch}\n
                {alexa}\n{baidu}\n{pic}\n
                User-agent:*\n{unallowed_directory}\nUser-agent:*\nDisallow:\n{unallowed_directory}\n{unallowed_directory1}\n{unallowed_directory2}\n{xml}
                """
                striped=data_to_write.strip()
                return render_template("robots.html",form=forms,striped=striped)
        else:
            cleaned_lines = [' '.join(line.split()) for line in data_to_write.split('\n')]
            cleaned_data='\n'.join(cleaned_lines)
            bytes_io.write(cleaned_data.encode())
            bytes_io.seek(0)
            flash("success File Downloaded Successfully",'success')
            return send_file(
        bytes_io,
        as_attachment=True,
        download_name='robots.txt',
        mimetype='application/octet-stream'
        )


    return render_template("robots.html",form=forms)

@app.route("/ip-address-lookup",methods=['GET','POST'])
def get_ip_location():
    form=Ip_Address_Form()
    website=form.url.data
    if form.validate_on_submit():
        try:
            if 'https' in website or 'http' in website:
                domain=urlparse(website).netloc
            # print(domain)
                ip_add=socket.gethostbyname(domain)
                result=printDetails(ip_add)
                results=[result]
                return render_template("ip_address.html",form=form,results=results)
            else:
                ip_add=socket.gethostbyname(website)
                result=printDetails(ip_add)
                results=[result]
                return render_template("ip_address.html",form=form,results=results)
        except socket.gaierror as e:
            flash("error Invalid URL",'error')
    return render_template("ip_address.html",form=form)
    
    
@app.route("/http-header-status", methods=['GET', 'POST'])
def get_headers():
    form = Ip_Address_Form()
    website = form.url.data
    if form.validate_on_submit():
        if type(get_header(website)) == str:
            flash("error Please Enter A Valid URL\nExample: https://www.seomasterz.com",'error')
        else:
            headers_names, header_results = get_header(website)
            zipped_data = zip_longest(headers_names, header_results)
            return render_template("get_headers.html", form=form, zipped_data=zipped_data)
    return render_template("get_headers.html", form=form)
    

@app.route("/online-grammar-checker",methods=['GET','POST'])
def grammar():
    form=Article_Rewriter()
    if form.validate_on_submit():
        text=form.paragraph.data
        results=grammar_check(text)
        if type(results)!= dict:
            flash("info No Grammar Errors Were Found In Your Text",'info')
        else:
            # print(results)
            return render_template("grammar_check.html",form=form,results=results)
    return render_template("grammar_check.html",form=form)

@app.route("/check-domain-age",methods=['GET','POST'])
def domains_age():
    if request.method=='POST':
        url=request.form.get("text")
        content=domain_age(url)
        if type(content)==str:
            flash("error Could Not Fetch Domain Age,Please Try Again",'error')
        else:
            return render_template("domain_age.html",content=content)

    return render_template("domain_age.html")
    
    
@app.route("/linkcounter",methods=['GET','POST'])
def get_links():
    if request.method == 'POST':
        url = request.form.get('text')
        button_click = request.form.get('submit-button')

        if button_click == "get-links":
            results=internal_external(url)
            if type(results)==str:
                flash("error Error Fetching URL, Try Again",'error')
            else:
                internal_links=results[0]
                external_links=results[1]
                fig, ax = plt.subplots()

    # Set up the initial bar graph
                update(0, ax,internal_links,external_links)
                img_stream = BytesIO()
                plt.savefig(img_stream, format='png')
                img_stream.seek(0)
                
                # Encode the image in base64
                img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    
    # Embed the image data in the HTML
                return render_template("ex_in.html",results=results,img_data=img_data)
    return render_template("ex_in.html")
    
@app.route("/page-speed-checker",methods=['GET','POST'])
def get_page_speed():
    if request.method=='POST':
        url=request.form.get('text')
        try:
            start_time = time()
            response=requests.get(url)
            end_time = time()
            loading_time=round(end_time-start_time,2)
            x_values = [0, 1]
            y_values = [0, loading_time]

            plt.plot(x_values, y_values)
            plt.xlabel('Time')
            plt.ylabel('Loading Time')
            plt.title('Page Loading Time Plot')

            # Save the plot to a BytesIO object
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template("page_speed.html",loading_time=loading_time,url=url,plot_url=plot_url)
        except:
            flash('error fetching provided URL','error')
    return render_template("page_speed.html")
    
@app.route('/generate-qr-code', methods=['GET', 'POST'])
def generate_qr_code():
    if request.method == 'POST':
        url = request.form.get('text')
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create a QR code image using PIL
            qr_code_img = qr.make_image(fill_color="darkblue", back_color="white")

            # Save the QR code image to BytesIO
            qr_code_bytes = BytesIO()
            qr_code_img.save(qr_code_bytes, format="PNG")

            # Encode the BytesIO content in base64
            qr_code_base64 = base64.b64encode(qr_code_bytes.getvalue()).decode()

            # Render the HTML template with the base64-encoded image
            return render_template("qr_code.html", qr_code_base64=qr_code_base64)
        except Exception as e:
            flash("error occured while generating qr code,try again"'error')

    return render_template("qr_code.html")

@app.route("/page-size-checker",methods=['GET','POST'])
def generate_screenshot():
    if request.method=='POST':
        url=request.form.get("text")
        try:
            response = requests.get(url)
        # Check if the request was successful (status code 200)
            if response.status_code == 200:
                content_size_bytes = len(response.content)
                content_size_kb = content_size_bytes / 1024
                formatted_size = "{:.2f}".format(content_size_kb)
                return render_template('page_size.html',content_size_kb=formatted_size,content_size_bytes=content_size_bytes,url=url)
            else:
                flash('error trouble fetching URL','error')
        except:
            flash('error Trouble Fetching URL','error')
    return render_template('page_size.html')
    
@app.route("/encode-deconde-url",methods=["GET",'POST'])
def encode_decode_url():
    if request.method=='POST':
        url=request.form.get('text')
        button_click=request.form.get('submit-button')
        try:
            if button_click=='Encode':
                encoded=urllib.parse.quote(url)
                return render_template("url_encoder.html",encoded=encoded,url=url)
            elif button_click=='Decode':
                recoded=urllib.parse.unquote(url)
                return render_template("url_encoder.html",recoded=recoded,url=url)
            else:
                flash('error performing function','error')
        except:
            flash('error performing function','error')
    return render_template("url_encoder.html")


@app.route("/url-shortner", methods=['GET', 'POST'])
def url_shortner():
    if request.method == 'POST':
        long_url = request.form.get('text')
        try:
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(long_url)
            return render_template('url-shortner.html', short_url=short_url, long_url=long_url)
        except Exception as e:
            print(f"Error: {e}")
            flash('error occurred. Please try again.', 'error')
    return render_template("url-shortner.html")

@app.route("/email-privacy",methods=['GET','POST'])
def find_email():
    if request.method=='POST':
        url=request.form.get('text')
        found_email=find_emails(url)
        if "Error" in found_email:
            flash("error fetching URL, please try again",'error')
        elif not found_email:
            flash("info no emails were found on this webpage",'info')
        else:
            return render_template("find_email.html",found_email=found_email,url=url)
    return render_template("find_email.html")

@app.route("/translation",methods=['GET','POST'])
def translator():
    form=Article_Rewriter()
    if request.method=='POST':
        text=form.paragraph.data
        language=request.form.get('Language')
        print(language)
        try:
            translation=tranlate_txt(text,language)
            return render_template("translation.html",translation=translation,form=form)
        except:
            flash('error occured','error')
    return render_template("translation.html",form=form)

@app.route("/spider-simulator",methods=['GET','POST'])
def spider_simulation():
    url=request.form.get('text')
    if request.method=='POST':
        try:
            text=get_text_from_website(url)
            links=internal_external(url)
            meta=get_meta_tag(url)
            print(meta)
            return render_template("spider_simulation.html",text=text,links=links,meta=meta)
        except Exception as e:
            print(e)
            flash('error fetching URL try again','error')
    return render_template("spider_simulation.html")
    
@app.route("/ssl-certification-verified",methods=['GET','POST'])
def ssl_certified():
    url=request.form.get('text')
    if request.method == 'POST':
        certificate=ssl_certification(url)
        if certificate == 'Error':
            print(certificate)
            flash("error fetching url try again",'error')
        else:
            return render_template("ssl_certification.html",certificate=certificate,url=url)
    return render_template("ssl_certification.html")
    
@app.route("/generate-website-screenshot",methods=['GET','POST'])
def get_screenshot():
    website=request.form.get('text')
    if request.method=='POST':
        url = "https://screenshot-snapshot-site2.p.rapidapi.com/api/v1/screenshot"

        payload = {
            "url": website,
            "format": "png",
            "width": 1280,
            "height": 720,
            "delay": 0,
            "fullSize": True,
            "hideCookie": True
        }
        headers = {
            "content-type": "application/json",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-RapidAPI-Key": "099cfd811cmsh3102e8b20caed64p102e0ajsn9443cc66db66",
            "X-RapidAPI-Host": "screenshot-snapshot-site2.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        image = response.json().get('link')
        if image == 'None':
            flash("error fetching url please try again",'error')
        else:
            return render_template("screenshot.html",image=image)
    return render_template("screenshot.html")
    
def is_curl_request():
    user_agent = request.headers.get('User-Agent')
    return user_agent and 'curl' in user_agent.lower()

@app.route('/my-ip-address', methods=['GET'])
def get_client_ip():
    # Check X-Forwarded-For first
    client_ip = request.headers.get('X-Forwarded-For')
    
    if client_ip is None:
        # If X-Forwarded-For is not present, try X-Real-IP
        client_ip = request.headers.get('X-Real-IP')

    # If both headers are not present, fallback to request.remote_addr
    if client_ip is None:
        client_ip = request.remote_addr
    if is_curl_request():
        return jsonify({'ip': client_ip})
    else:
        result=printDetails(client_ip)
        results= [result]
        return render_template("user_ip_address.html",results=results)

@app.route("/terms-and-conditions-generator", methods=['GET', 'POST'])
def generate_terms():
    if request.method == 'POST':
        company_name = request.form.get("company")
        website_name = request.form.get("website-name")
        url = request.form.get("website-url")
        return render_template("terms_conditions.html", company_name=company_name,website_name=website_name,url=url)
    
    return render_template("terms_conditions.html")
    
    
    
@app.route("/text-to-binary-to-text", methods=['GET', 'POST'])
def text_to_binary():
    if request.method=='POST':
        text=request.form.get("text")
        conversion=request.form.get('conversion')
        if conversion=='Text':
            converted=string_to_bit(text)
            return render_template("text_to_bits.html",converted=converted)
        elif conversion=='Binary':
            converted=bits_to_string(text)
            return render_template("text_to_bits.html",converted=converted)
        else:
            flash('error occured please try again','error')
    return render_template("text_to_bits.html")

@app.route("/view-source-code-of-websites-online",methods=['GET','POST'])
def view_source():
    if request.method=='POST':
        url=request.form.get("url")
        print(url)
        try:
            response=requests.get(url)
            source_code=response.text
            return render_template("view_source.html",source_code=source_code,url=url)
        except:
            flash("error fetching url,try again",'error')
    return render_template("view_source.html")
    
@app.route("/google-malware-checker",methods=['GET','POST'])
def malware_checker():
    if request.method=='POST':
        url=request.form.get('url')
        return redirect(f"https://transparencyreport.google.com/safe-browsing/search?url={url}")
    return render_template("malware_checker.html")
    
@app.route("/generate-ai-image-text-to-image", methods=['GET', 'POST'])
def return_generated_image():
    if request.method == 'POST':
        sentence = request.form.get('text')
        image_data = generate_and_display_image(sentence)
        if 'Error' in image_data:
            flash("Error generating image. Please try again.", 'error')
        else:
            return render_template("generated_image.html", image_data=image_data,sentence=sentence)
    return render_template("generated_image.html")
    
@app.route("/online-adsence-calculator",methods=['GET','POST'])
def adsense_calculator():
    if request.method=='POST':
        page_views = request.form.get('views')
        ctr = request.form.get('rate')
        cpc = request.form.get('cost')
        daily_earnings_per_click = int(cpc) * int(ctr)
        daily_total_earnings = daily_earnings_per_click * int(page_views)/100
        monthly_total_earnings = daily_total_earnings * 30
        monthly_clicks=int(cpc)*30
        yearly_total_earnings = daily_total_earnings * 365
        yearly_clicks=int(cpc)*365
        return render_template("adsense_calculator.html",daily_total_earnings=daily_total_earnings,
                     monthly_total_earnings=monthly_total_earnings,yearly_total_earnings=yearly_total_earnings,yearly_clicks=yearly_clicks,
                     monthly_clicks=monthly_clicks,cpc=int(cpc))
    return render_template("adsense_calculator.html")
    
@app.route("/free-backlink-maker-seo-tool",methods=['GET','POST'])
def create_backlinks():
    if request.method=='POST':
        url=request.form.get('url')
        if 'https://' in url and 'www' in url:
            parse=urlparse(url)
            base_url=parse.netloc
            links=backlink_maker(base_url)
            return render_template('backlinks.html',links=links)
        elif 'www' not in url:
            flash('error fetching url, try www.seomasterz.com','error')
        elif 'www' in url and 'https://' not in url:
            links=backlink_maker(url)
            return render_template('backlinks.html',links=links)
        else:
            flash ('error fetching url, try www.seomasterz.com','error')
    return render_template("backlinks.html")


@app.route('/online-password-generator',methods=['GET','POST'])
def password_generator():
    if request.method == 'POST':
        length = request.form.get('length')
        uppercase = request.form.get('UpperCase') == 'yes'
        digits = request.form.get('Digits') == 'yes'
        special_char = request.form.get('special') == 'yes'
        print(f"{uppercase} {digits} {special_char}")
        password = generate_password(int(length),digits,special_char,uppercase)
        return render_template("password_generator.html",password=password)
    return render_template("password_generator.html")

@app.route("/meta-tags-generator-online", methods=['GET', 'POST'])
def create_metatags():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        keywords =  request.form.get("keywords")
        keywords = keywords.split(',')
        index = request.form.get("Allow-Robots")
        robots = request.form.get("Follow-links")
        content_type = request.form.get("Content-type")
        language = request.form.get("Language")
        revist = request.form.get("Days")
        author = request.form.get("author")
        # print(title,description,keywords,language,revist,robots,author,content_type,index)
        tags = generate_meta_tags(title,description,keywords,language,revist,robots,author,content_type,index)
        return render_template("meta_tags.html",tags=tags)
    return render_template("meta_tags.html")

@app.route("/encrypt-password-proctect-your-files",methods=['GET','POST'])
def encrypt_pdf_files():
    if request.method == 'POST':
        # --- THIS IS THE CRUCIAL CHANGE ---
        # Now expecting the file under the name 'file-upload' as defined in the HTML
        file = request.files.get('file-upload')
        # --- END OF CRUCIAL CHANGE ---

        password = request.form.get('password')

        if file and file.filename: # Check if a file was actually uploaded and has a name
            if file.filename.endswith('.pdf'):
                try:
                    file_to_download = password_protect_pdf(file, password)
                    return send_file(
                        BytesIO(file_to_download),
                        download_name="Password_Protected.pdf",
                        as_attachment=True,
                        mimetype='application/pdf' # Explicitly set mimetype for PDF download
                    )
                except Exception as e:
                    # Catch any errors during PDF processing and flash a message
                    flash(f'Error processing PDF: {e}', 'error')
                    print(f"Error processing PDF: {e}") # Log the error for debugging
            else:
                flash('Kindly upload PDF files only, other formats are not supported', 'info')
        else:
            flash('No file uploaded or file is empty.', 'info') # Handle case where no file is selected/uploaded
    return render_template("file_encryption.html")



if __name__=="__main__":
    app.run(debug=True)
    
