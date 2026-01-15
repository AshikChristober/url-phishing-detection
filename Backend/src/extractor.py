import re
from urllib.parse import urlparse
import math

def get_url_features(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
    except:
        hostname = ""
        path = ""
    
    # --- 1. Lexical Features (1-20) ---
    features = [
        len(url),                                # 1. url_len
        url.count('@'),                          # 2. @
        url.count('?'),                          # 3. ?
        url.count('-'),                          # 4. -
        url.count('='),                          # 5. =
        url.count('.'),                          # 6. .
        url.count('#'),                          # 7. #
        url.count('%'),                          # 8. %
        url.count('+'),                          # 9. +
        url.count('$'),                          # 10. $
        url.count('!'),                          # 11. !
        url.count('*'),                          # 12. *
        url.count(','),                          # 13. ,
        url.count('//'),                         # 14. //
        1 if not hostname else 0,                # 15. abnormal_url
        0 if url.startswith('https') else 1,     # 16. https
        sum(c.isdigit() for c in url),           # 17. digits
        sum(c.isalpha() for c in url),           # 18. letters
        1 if any(s in url for s in ['bit.ly', 't.co', 'goo.gl']) else 0, # 19. Shortining_Service
        1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0 # 20. having_ip_address
    ]

    # --- 2. Web/Security Features (21-46) ---
    # These 26 slots are often placeholders for API-based features.
    # We fill them to maintain the 64-feature shape.
    web_features = [0] * 26 
    web_features[12] = 1 # web_ssl_valid placeholder
    web_features[25] = 1 # web_ssl_valid.1 placeholder
    features.extend(web_features)

    # --- 3. Phishing Keywords (47-50) ---
    features.append(1 if any(w in url.lower() for w in ['urgent', 'action', 'verify', 'update']) else 0) # 47
    features.append(1 if any(w in url.lower() for w in ['secure', 'login', 'auth', 'signin']) else 0)   # 48
    features.append(0) # 49. phish_brand_mentions
    features.append(0) # 50. phish_brand_hijack
    
    # --- 4. Structural Features (51-64) ---
    features.append(1 if hostname.count('.') > 2 else 0) # 51. phish_multiple_subdomains
    features.append(1 if len(path) > 50 else 0)          # 52. phish_long_path
    features.append(1 if url.count('&') > 3 else 0)      # 53. phish_many_params
    
    suspicious_tlds = ['.xyz', '.top', '.work', '.casa', '.support', '.online', '.site']
    features.append(1 if any(url.endswith(t) for t in suspicious_tlds) else 0) # 54. phish_suspicious_tld
    
    # Entropy & Counts
    features.append(len(set(hostname)) / len(hostname) if len(hostname) > 0 else 0) # 55
    features.append(path.count('/')) # 56
    features.append(len(set(path)) / len(path) if len(path) > 0 else 0) # 57
    features.append(hostname.count('.')) # 58
    
    subdomain_div = (hostname.count('.') + 1)
    features.append(len(hostname) / subdomain_div if subdomain_div != 0 else 0) # 59
    
    # Ratios
    url_len = len(url) if len(url) > 0 else 1
    features.append(sum(1 for c in url if c.lower() not in 'aeiou' and c.isalpha()) / url_len) # 60
    features.append(sum(1 for c in url if c.lower() in 'aeiou') / url_len) # 61
    features.append(sum(c.isdigit() for c in url) / url_len) # 62
    
    # Tokens
    tokens = re.split(r'\W+', url)
    tokens = [t for t in tokens if t] # remove empty tokens
    features.append(sum(len(t) for t in tokens) / len(tokens) if tokens else 0) # 63
    features.append(len(tokens)) # 64

    return features