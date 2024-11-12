import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import category_encoders as ce

# Sample TLD list for binary encoding
tld_list = ['com', 'de', 'uk', 'org', 'in', 'ie', 'hu', 'ru', 'gq', 'es', 'jp',
       'guru', 'app', 'io', 'club', 'fr', 'au', 'today', 'cloud', 'br',
       'pt', 'co', 'lt', 'ca', 'xyz', 'sk', 'pl', 'dk', 'dev', 'ga',
       'edu', 'space', 'ws', '123', 'cf', 'rs', 'games', 'nl', 'me',
       'net', 'life', 'ua', 'id', 'mx', 'asia', 'store', 'nz', 'eus',
       'qa', 'fi', 'ch', 'site', 'shop', 'hr', 'cz', 'im', 'ee', 'sg',
       'travel', 'tz', 'top', 'info', 'tokyo', 'at', 'gr', 'cc', 'tv',
       'online', 'lk', 'review', 'us', 'bar', 'link', 'ng', 'cl', 'ar',
       'one', 'ph', 'tr', 'mil', 'se', '94', 'live', 'cn', 'ir', 'it',
       'gd', 'eu', 'win', 'no', 'su', 'gov', 'bg', 'ro', 'kr', 'eg',
       'biz', 'il', 'page', 'pm', 'sh', 'pk', 'my', 'quest', 'be', 'sa',
       'tk', 'vip', 'agency', 'cyou', 'kz', 'uy', 'network', '128', 'ml',
       'hk', 'media', 'az', 'aero', 'news', 'lu', 'is', 'coop', 'art',
       'download', 'si', 'fm', 'bt', 'am', 'finance', 'mn', 'kh', 'ug',
       'ae', 'cool', 'za', 'th', 'energy', 'lv', 'global', 'tw', 'ke',
       'moe', 'icu', '103', 'fun', '130', 'cm', 'int', 'xn--c1avg', 'vg',
       'gi', 'red', 'gal', 'sy', 'na', 'bo', 'land', 'je', 'st', 'by',
       'ly', 'bid', 'bio', 'world', 'law', 'digital', 'ai', 'science',
       'li', 'email', 'ruhr', 'hn', 'blog', 'stream', 'ht', 'lc',
       'website', 'np', 'cy', 'gp', 'vn', 'kw', 're', 'sv', 'cat', 'lb',
       'to', 'cfd', 'nyc', 'ba', 'mobi', 'pw', 'marketing', 'ge', 'band',
       'koeln', 'pro', 'studio', 'tl', 'loan', 'zw', 'al', 'xn--p1ai',
       'buzz', 'bw', 'bd', 'photo', '160', 'so', '197', 'jo', 'nu',
       'click', 'lol', 'bayern', 'design', 'fund', 'pe', 'cash', 'uz',
       'gle', 'beauty', '232', 'ps', 'tours', 'cab', 'work', 'ink',
       'best', 'gs', 'vu', 'cv', 'goog', 'vc', 'eco', 'gy', 'tech', 'ad',
       'krd', 'wiki', 'london', 'name', 'la', 'ls', 'tn', 'help',
       'fitness', 'gh', '171', 'limo', 'ax', 'pa', 'af', 'bz', 've',
       '181', '108', 'rugby', '111', 'dm', 'wales', 'health', '125',
       'swiss', 'mom', 'do', 'kred', 'as', 'kg', 'exchange', 'ky', 'bf',
       '234', 'soy', 'bond', 'game', 'cu', 'mk', 'auto', 'pet', '238',
       'lighting', 'center', 'cx', '214', 'cr', 'date', 'city', 'supply',
       'ao', '26', 'group', 'trade', 'gl', 'run', 'pn', 'money', '146',
       'team', 'ltd', '33', 'ac', 'mm', 'sd', 'tc', 'va', 'kn', 'movie',
       'plus', 'church', 'scot', 'sbs', 'rest', 'technology', 'careers',
       'bike', 'nf', 'skin', 'dj', 'lr', 'bh', 'zm', 'tf', 'sport', 'ma',
       'aw', 'bn', 'works', 'gg', '120', 'ec', 'vet', 'host', 'audio',
       'mz', 'mt', 'capital', 'tt', 'consulting', 'ninja', 'homes', 'pg',
       'cards', 'pink', 'codes', 'ki', 'sn', 'ms', 'international',
       'press', 'mu', 'kim', 'chat', 'land:443', 'autos', '86', 'cars',
       'istanbul', 'rw', '41', 'rocks', 'yachts', 'mv', 'services', 'gt',
       'iq', 'md', '78', 'clothing', '69', 'institute', 'business', '30',
       '117', 'ni', 'bank', 'bm', 'direct', '67', 'cafe', 'photography',
       'taxi', 'love', 'ovh', 'report', 'et', 'guide', 'cd', 'build',
       'monster', 'solutions', '148', 'mr', 'py', 'vlaanderen',
       'holdings', 'pub', 'coach', 'cymru', 'tatar', 'ag', 'tj', 'tools',
       'cleaning', 'mg', 'bj', 'africa', '158', 'gift', 'investments',
       'dz', 'tm', 'sz', 'hair', '95', 'care', 'jm', 'garden', 'academy',
       '163', 'jobs', 'company', '220', '154', 'com:443', 'fo', '100',
       'pics', 'sx', 'paris', '145', 'fyi', 'ngo', 'domains', '223',
       'place', 'mc', '24', 'cam', 'post', 'ooo', 'cern', '134', 'museum',
       'market', 'corsica', 'bb', 'reviews', 'om', 'nagoya', 'systems',
       'events', '240:8087', '13', '116', 'pf', '80:8085', '177', 'zone',
       'vote', 'sc', 'kiwi', 'casa', '149', 'mw', 'com:2096', 'maison',
       'xn--mk1bu44c', 'radio', 'ss', '230', 'study', 'tips', '162', '39',
       'vi', 'immo', 'photos', '199', 'mba', 'farm', 'google', 'berlin',
       'legal', 'gf', 'tg', 'camera', 'lat', 'salon', 'gifts', '182',
       '206', 'camp', '87', '221', '12', '51', 'fit', 'delivery',
       'social', 'house', 'sm', '242', '150', 'coffee', 'yoga', '38',
       'ci', 'green', '184', '167', '237', 'theater', 'lundbeck', 'party',
       'flights', 'condos', '20', 'town', '155', 'rentals', 'com:9595',
       'youtube', 'earth', 'ck', 'menu', 'community', '225', '140',
       'watch', 'school', 'gives', 'rip', '185', 'engineering', 'holiday',
       '216', '227', 'bi', 'limited', 'racing', '52', 'boutique',
       '68:8080', 'beer', 'taipei', 'crs', 'dog', 'markets', 'video',
       '121', 'furniture', 'expert', 'family', 'mo', 'education', '101',
       'sb', 'citic', 'bet', 'gallery', 'wtf', '189', '47', 'sharp',
       'wine', 'faith', 'foundation', '243', 'management', 'makeup',
       '196', 'tattoo', '107', 'tirol', '203', 'lgbt', '211', 'nrw',
       'college', 'fashion', 'vegas', '252', '21', '231', 'sr', 'cc:8443',
       '222', 'wf', 'hosting', 'archi', 'recipes', 'training', 'pl:443',
       'fj', 'fr:443', 'tel', 'trading', '28', 'uno', '187', 'diamonds',
       'golf', 'mp', 'industries', 'builders', '173', 'aq', 'software',
       'repair', 'ye', 'com:4000', 'support', 'gold', '178', 'amsterdam',
       'neustar', 'xn--p1acf', '250', 'hamburg', 'fk', 'basketball', '84',
       '188:10003', 'gmbh', '211:8383', 'xn--90ais', '233', 'mortgage',
       '126:8080', 'barcelona', '106', '136', 'bs', 'yt', 'tax', '161',
       'express', '126', '15', 'nr', 'gdn', 'parts', 'ski', 'kitchen',
       'associates', 'dental', '240', '198', '165', '249:8080', 'guitars',
       'mma', 'navy', '11', 'car', '235', 'xn--6frz82g', 'computer',
       'show', 'schule', '133:8080', '210', 'gay', 'toys', '27', 'nc',
       'promo', 'miami', 'sexy', 'ventures', '200', 'healthcare', '42',
       '43', '80', '71', 'moscow', 'weber', 'mq', '110', '254:30332',
       '63', 'black', '166', 'ist', 'shoes', '14', 'ntt', '151', 'madrid',
       '46', 'film', 'ne']
binary_encoder = ce.BinaryEncoder(cols=['TLD']).fit(pd.DataFrame({'TLD': tld_list}))

def get_tld_features(url):
    tld = urlparse(url).netloc.split('.')[-1]
    tld_df = binary_encoder.transform(pd.DataFrame({'TLD': [tld]}))
    return {f'TLD_{i}': tld_df.iloc[0, i] for i in range(len(tld_df.columns))}

def get_letter_ratio(url):
    letters = re.sub(r'[^A-Za-z]', '', url)
    return len(letters) / len(url)

def get_special_chars_count(url):
    special_chars = re.findall(r'[^A-Za-z0-9]', url)
    return len(special_chars)

def get_special_char_ratio(url):
    special_chars = re.findall(r'[^A-Za-z0-9]', url)
    return len(special_chars) / len(url)

def is_https(url):
    return 1 if urlparse(url).scheme == 'https' else 0

def get_line_of_code(html):
    return len(html.splitlines())

def get_largest_line_length(html):
    return max(len(line) for line in html.splitlines())

def get_domain_title_match_score(url, title):
    domain = urlparse(url).netloc.split('.')[0]
    return title.count(domain) / (len(title) or 1)

def has_meta_description(soup):
    return 1 if soup.find('meta', attrs={'name': 'description'}) else 0

def has_social_network_links(soup):
    return 1 if soup.find_all(href=re.compile(r'(facebook|twitter|linkedin|instagram)')) else 0

def has_submit_button(soup):
    return 1 if soup.find_all('input', attrs={'type': 'submit'}) else 0

def has_copyright_info(html):
    return 1 if re.search(r'\u00A9|\(c\)', html, re.IGNORECASE) else 0

def get_image_count(soup):
    return len(soup.find_all('img'))

def get_css_count(soup):
    return len(soup.find_all('link', attrs={'rel': 'stylesheet'}))

def get_js_count(soup):
    return len(soup.find_all('script'))

def get_self_referencing_links(soup, domain):
    return len(soup.find_all(href=re.compile(domain)))

def get_external_references(soup):
    return len(soup.find_all(href=re.compile(r'^http')))

def extract_features(url):
    features = {}
    parsed_url = urlparse(url)

    # 1. TLD Features
    features.update(get_tld_features(url))
    
    # 2. Letter Ratio in URL
    features['LetterRatioInURL'] = get_letter_ratio(url)
    
    # 3. Number of Other Special Characters in URL
    features['NoOfOtherSpecialCharsInURL'] = get_special_chars_count(url)
    
    # 4. Special Character Ratio in URL
    features['SpacialCharRatioInURL'] = get_special_char_ratio(url)
    
    # 5. Is HTTPS
    features['IsHTTPS'] = is_https(url)
    
    # Fetch webpage to extract more features
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            domain = parsed_url.netloc

            # 6. Line of Code
            features['LineOfCode'] = get_line_of_code(html)
            
            # 7. Largest Line Length
            features['LargestLineLength'] = get_largest_line_length(html)
            
            # 8. Domain Title Match Score
            title = soup.title.string if soup.title else ""
            features['DomainTitleMatchScore'] = get_domain_title_match_score(url, title)
            
            # 9. Has Description Meta Tag
            features['HasDescription'] = has_meta_description(soup)
            
            # 10. Has Social Network Links
            features['HasSocialNet'] = has_social_network_links(soup)
            
            # 11. Has Submit Button
            features['HasSubmitButton'] = has_submit_button(soup)
            
            # 12. Has Copyright Info
            features['HasCopyrightInfo'] = has_copyright_info(html)
            
            # 13. Number of Images
            features['NoOfImage'] = get_image_count(soup)
            
            # 14. Number of CSS Files
            features['NoOfCSS'] = get_css_count(soup)
            
            # 15. Number of JavaScript Files
            features['NoOfJS'] = get_js_count(soup)
            
            # 16. Number of Self-Referencing Links
            features['NoOfSelfRef'] = get_self_referencing_links(soup, domain)
            
            # 17. Number of External References
            features['NoOfExternalRef'] = get_external_references(soup)
            
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")

    # Print all extracted features
    print("Extracted Features:")
    for feature, value in features.items():
        print(f"{feature}: {value}")
    
    return features

# # Example usage
# url = input("Enter a URL: ")
# features = extract_features(url)
