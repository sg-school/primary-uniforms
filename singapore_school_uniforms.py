#!/usr/bin/env python3
"""
Singapore Primary School Uniform Scraper

This script scrapes images and information about Singapore primary school uniforms
from the web and saves the data for display on a webpage.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin, quote_plus
import logging

# import numpy as np

# Load the MobileNetV2 model
# model = MobileNetV2(weights='imagenet')

# Create directories for storing data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'school_uniforms')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Set up logging to a file
log_file_path = os.path.join(BASE_DIR, 'scraper.log')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])
logger = logging.getLogger(__name__)

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# List of Singapore primary schools to search for
SCHOOLS = [
    "Admiralty Primary School",
    "Ahmad Ibrahim Primary School",
    "Ai Tong School",
    "Alexandra Primary School",
    "Anchor Green Primary School",
    "Anderson Primary School",
    "Ang Mo Kio Primary School",
    "Anglo-Chinese School (Junior)",
    "Anglo-Chinese School (Primary)",
    "Angsana Primary School",
    "Balestier Hill Primary School",
    "Beacon Primary School",
    "Beatty Primary School",
    "Bedok Green Primary School",
    "Bedok West Primary School",
    "Bendemeer Primary School",
    "Blangah Rise Primary School",
    "Boon Lay Garden Primary School",
    "Bukit Panjang Primary School",
    "Bukit Timah Primary School",
    "Bukit View Primary School",
    "Canberra Primary School",
    "Canossa Catholic Primary School",
    "Cantonment Primary School",
    "Casuarina Primary School",
    "Catholic High School (Primary)",
    "Cedar Primary School",
    "Changkat Primary School",
    "Chij (Katong) Primary",
    "Chij (Kellock)",
    "Chij Our Lady of Good Counsel",
    "Chij Our Lady of Nativity",
    "Chij Our Lady of the Nativity",
    "Chij Our Lady Queen of Peace",
    "Chij Primary (Toa Payoh)",
    "Chij St. Nicholas Girls' School (Primary)",
    "Chongfu School",
    "Chongzheng Primary School",
    "Chua Chu Kang Primary School",
    "Clementi Primary School",
    "Compassvale Primary School",
    "Concord Primary School",
    "Coral Primary School",
    "Corporation Primary School",
    "Da Qiao Primary School",
    "Damai Primary School",
    "Dazhong Primary School",
    "De La Salle School",
    "East Coast Primary School",
    "East Spring Primary School",
    "East View Primary School",
    "Edgefield Primary School",
    "Elias Park Primary School",
    "Endeavour Primary School",
    "Eunos Primary School",
    "Evergreen Primary School",
    "Fairfield Methodist School (Primary)",
    "Farrer Park Primary School",
    "Fengshan Primary School",
    "Fernvale Primary School",
    "First Toa Payoh Primary School",
    "Frontier Primary School",
    "Fuchun Primary School",
    "Gan Eng Seng Primary School",
    "Geylang Methodist School (Primary)",
    "Gongshang Primary School",
    "Greendale Primary School",
    "Greenridge Primary School",
    "Greenwood Primary School",
    "Guangyang Primary School",
    "Henry Park Primary School",
    "Holy Innocents' Primary School",
    "Hong Wen School",
    "Horizon Primary School",
    "Hougang Primary School",
    "Huamin Primary School",
    "Innova Primary School",
    "Jiemin Primary School",
    "Jing Shan Primary School",
    "Junyuan Primary School",
    "Jurong Primary School",
    "Jurong West Primary School",
    "Juying Primary School",
    "Keming Primary School",
    "Kheng Cheng School",
    "Kong Hwa School",
    "Kranji Primary School",
    "Kuo Chuan Presbyterian Primary School",
    "Lakeside Primary School",
    "Lianhua Primary School",
    "Loyang Primary School",
    "MacPherson Primary School",
    "Maha Bodhi School",
    "Maris Stella High School (Primary)",
    "Marymount Convent School",
    "Mayflower Primary School",
    "Meridian Primary School",
    "Methodist Girls' School (Primary)",
    "Montfort Junior School",
    "Nan Chiau Primary School",
    "Nan Hua Primary School",
    "Nanyang Primary School",
    "Naval Base Primary School",
    "New Town Primary School",
    "Ngee Ann Primary School",
    "North Spring Primary School",
    "North View Primary School",
    "North Vista Primary School",
    "Northland Primary School",
    "Oasis Primary School",
    "Opera Estate Primary School",
    "Palm View Primary School",
    "Park View Primary School",
    "Pasir Ris Primary School",
    "Paya Lebar Methodist Girls' School (Primary)",
    "Pei Chun Public School",
    "Pei Hwa Presbyterian Primary School",
    "Pei Tong Primary School",
    "Pioneer Primary School",
    "Poi Ching School",
    "Princess Elizabeth Primary School",
    "Punggol Cove Primary School",
    "Punggol Green Primary School",
    "Punggol Primary School",
    "Punggol View Primary School",
    "Qifa Primary School",
    "Qihua Primary School",
    "Queenstown Primary School",
    "Raffles Girls' Primary School",
    "Red Swastika School",
    "River Valley Primary School",
    "Rivervale Primary School",
    "Rosyth School",
    "Rulang Primary School",
    "Sembawang Primary School",
    "Seng Kang Primary School",
    "Sengkang Green Primary School",
    "Shuqun Primary School",
    "Si Ling Primary School",
    "South View Primary School",
    "Springdale Primary School",
    "St Anthony's Canossian Primary School",
    "St Anthony's Primary School",
    "St Gabriel's Primary School",
    "St Hilda's Primary School",
    "St Joseph's Institution Junior",
    "St Margaret's Primary School",
    "St Stephen's School",
    "Stamford Primary School",
    "Tampines North Primary School",
    "Tampines Primary School",
    "Tanjong Katong Primary School",
    "Tao Nan School",
    "Teck Ghee Primary School",
    "Teck Whye Primary School",
    "Telok Kurau Primary School",
    "Temasek Primary School",
    "Townsville Primary School",
    "Unity Primary School",
    "Valour Primary School",
    "Waterway Primary School",
    "Wellington Primary School",
    "West Grove Primary School",
    "West Spring Primary School",
    "West View Primary School",
    "Westwood Primary School",
    "White Sands Primary School",
    "Woodgrove Primary School",
    "Woodlands Primary School",
    "Woodlands Ring Primary School",
    "Xinghua Primary School",
    "Xingnan Primary School",
    "Xinmin Primary School",
    "Xishan Primary School",
    "Yangzheng Primary School",
    "Yew Tee Primary School",
    "Yio Chu Kang Primary School",
    "Yishun Primary School",
    "Yu Neng Primary School",
    "Yuhua Primary School",
    "Yumin Primary School",
    "Zhenghua Primary School",
    "Zhonghua Primary School",
]

# User agents to rotate through to avoid being blocked
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
]

def get_random_user_agent():
    """Return a random user agent from the list"""
    return random.choice(USER_AGENTS)


def download_image(url, save_path):
    """Download an image from the provided URL and save it to the specified path"""
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        logger.info(f"Attempting to download image from: {url}")
        
        # Use a session to handle redirects properly
        session = requests.Session()
        session.headers.update(headers)
        
        # Follow redirects to get the final URL
        response = session.get(url, timeout=15, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        # If we were redirected, use the final URL
        final_url = response.url
        if final_url != url:
            logger.info(f"Redirected to: {final_url}")
        
        # Check content length to ensure it's substantial enough to be an image
        content_length = int(response.headers.get('Content-Length', 0))
        if content_length < 5000 and content_length > 0:  # Less than 5KB is suspicious for an image
            logger.warning(f"Content is too small ({content_length} bytes), might not be a valid image")
            
            # Only skip if we're certain about the content length
            if content_length > 100:  # If it's just a few bytes, it's definitely not an image
                return False
        
        # Check if the response is likely an image
        content_type = response.headers.get('Content-Type', '')
        
        # Check both content type and file extension
        is_image = content_type.startswith('image/') or any(final_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
        
        # If we're not sure it's an image based on content-type, check the content
        if not is_image and len(response.content) > 0:
            # Most image files start with specific byte sequences
            magic_numbers = {
                b'\xff\xd8\xff': '.jpg',  # JPEG
                b'\x89PNG\r\n\x1a\n': '.png',  # PNG
                b'GIF87a': '.gif',  # GIF
                b'GIF89a': '.gif',  # GIF
                b'RIFF': '.webp',  # WEBP
            }
            
            for signature, ext in magic_numbers.items():
                if response.content.startswith(signature):
                    is_image = True
                    break
        
        if not is_image:
            logger.warning(f"URL {final_url} might not be an image (Content-Type: {content_type})")
            
            # If filename has image extension, we might still try
            if not any(final_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                # If it's not obviously an image by extension or content type, don't save it
                return False
                
            logger.info("Attempting to save anyway because filename has image extension")
        
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        # Verify the file was saved properly and is a valid image
        file_size = os.path.getsize(save_path)
        
        if file_size < 1000:  # Less than 1KB is suspicious
            logger.warning(f"Downloaded file is too small ({file_size} bytes), might not be a valid image")
            os.remove(save_path)  # Remove tiny files that aren't likely to be valid images
            return False
            
        # Additional validation - try to verify it's a valid image file
        try:
            from PIL import Image
            img = Image.open(save_path)
            img.verify()  # Verify it's a valid image
            width, height = img.size
            
            # Higher resolution requirements
            if width < 150 or height < 150:  # Higher minimum dimensions for better quality
                logger.warning(f"Image dimensions too small: {width}x{height}")
                os.remove(save_path)
                return False
                
            # Check total resolution (pixel count)
            pixel_count = width * height
            if pixel_count < 36000:  # At least ~500x500 equivalent
                logger.warning(f"Image resolution too low: {pixel_count} pixels")
                os.remove(save_path)
                return False
                
            logger.info(f"Successfully saved high-resolution image to {save_path} ({file_size} bytes, {width}x{height}, {pixel_count} pixels)")
            
           
        except ImportError:
            logger.info(f"PIL not available for image validation, relying on file size check only")
        except Exception as e:
            logger.warning(f"Invalid image file: {str(e)}")
            if os.path.exists(save_path):
                os.remove(save_path)
            return False
        
        # Small delay to be respectful to the server
        time.sleep(random.uniform(0.5, 1.5))
        return True
    except Exception as e:
        logger.error(f"Error downloading image from {url}: {str(e)}")
        if os.path.exists(save_path):
            os.remove(save_path)  # Clean up any partial downloads
        return False

def search_duckduckgo_images(query, limit=8):
    """Search DuckDuckGo Images for the given query and return image URLs"""
    try:
        # More specific search query including "school uniform singapore"
        query = quote_plus(f"{query} school uniform singapore")
        
        # Use the vqd parameter to access the API - we'll need to get this first
        # Start with a regular search page
        logger.info(f"Searching DuckDuckGo for: {query}")
        initial_url = f"https://duckduckgo.com/?q={query}&ia=images&iax=images"
        
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # First request to get the vqd token
        response = requests.get(initial_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Find the vqd token in the page
        vqd_match = re.search(r'vqd="([^"]+)"', response.text)
        if not vqd_match:
            vqd_match = re.search(r'vqd=([^&]+)&', response.text)
            
        if not vqd_match:
            logger.warning("Could not find vqd token for DuckDuckGo search")
            return []
            
        vqd = vqd_match.group(1)
        logger.info(f"Found DuckDuckGo vqd token: {vqd}")
        
        # Now we can make the actual image search request
        image_api_url = f"https://duckduckgo.com/i.js?q={query}&o=json&vqd={vqd}&f=,,,,,&p=1"
        
        api_headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': initial_url,
            'Origin': 'https://duckduckgo.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        api_response = requests.get(image_api_url, headers=api_headers, timeout=15)
        api_response.raise_for_status()
        
        # Parse the JSON response
        image_data = api_response.json()
        
        # Extract image URLs
        image_urls = []
        if 'results' in image_data:
            for result in image_data['results'][:limit*2]:  # Get twice as many as needed in case some fail
                if 'image' in result:
                    image_urls.append(result['image'])
        
        # If we don't get enough images, try a fallback approach
        if len(image_urls) < limit:
            # Use the HTML page itself and extract image elements
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for images in the tiles-wrap section
            for img in soup.select(".tile--img__img, .tile-wrap img, .tile img"):
                src = img.get('src', '')
                data_src = img.get('data-src', '')
                img_url = data_src if data_src else src
                
                # Some images might be base64 encoded or relative, skip those
                if img_url and (img_url.startswith('http') or img_url.startswith('//')) and img_url not in image_urls:
                    # Convert protocol-relative URLs
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                        
                    image_urls.append(img_url)
                    
                    if len(image_urls) >= limit * 2:
                        break
        
        # If still not enough, try searching Google as a fallback
        if len(image_urls) < limit:
            logger.info("Not enough results from DuckDuckGo, falling back to Google search")
            google_urls = search_google_images(query, limit=limit)
            for url in google_urls:
                if url not in image_urls:
                    image_urls.append(url)
                    if len(image_urls) >= limit * 2:
                        break
        
        logger.info(f"Found {len(image_urls)} potential image URLs from DuckDuckGo and fallbacks")
        return image_urls
            
    except Exception as e:
        logger.error(f"Error searching DuckDuckGo for images: {str(e)}")
        # Fall back to Google if DuckDuckGo fails
        logger.info("Falling back to Google search due to DuckDuckGo error")
        return search_google_images(query, limit)

def search_google_images(query, limit=8):
    """Search Google Images for the given query and return image URLs"""
    # More specific queries targeting high-resolution images
    query = quote_plus(f"{query} school uniform singapore")
    search_url = f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:lt,islt:1mp"  # tbs=isz:l prefers large images
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        logger.info(f"Searching Google Images for high-resolution: {query}")
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Try to extract image URLs using multiple methods
        image_urls = []
        
        # Method 1: Extract from JSON data in script tags (most reliable for Google Images)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        # Look for the script that contains image data
        for script in scripts:
            if script.string and "AF_initDataCallback" in script.string:
                # Various patterns Google uses to store image URLs
                patterns = [
                    r'\"(https?://[^\"]+\.(?:jpg|jpeg|png|gif|webp))\"',
                    r'\"ou\":\"(https?://[^\"]+)\"',
                    r'\"(https?://[^\"]+\.(?:jpg|jpeg|png|gif|webp)[^\"]*?)\"',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, script.string)
                    for match in matches:
                        if len(image_urls) >= limit * 2:  # Get more than we need in case some fail
                            break
                        
                        # Clean up the URL - Google sometimes has escaped characters
                        url = match.replace('\\u003d', '=').replace('\\u0026', '&')
                        
                        if url not in image_urls and url.startswith('http'):
                            # Prefer URLs that suggest high resolution
                            priority = 0
                            res_indicators = ['large', 'high', 'hd', '1024', '2048', 'full', 'original']
                            for indicator in res_indicators:
                                if indicator in url.lower():
                                    priority += 1
                            
                            # Avoid URLs that suggest small images
                            low_res_indicators = ['thumb', 'small', 'icon', 'tiny', '100x', '200x']
                            if any(indicator in url.lower() for indicator in low_res_indicators):
                                continue
                            
                            # Give higher priority to 'full' size image URLs
                            if priority > 0:
                                # Insert higher priority URLs toward the front
                                image_urls.insert(min(priority, len(image_urls)), url)
                            else:
                                image_urls.append(url)
        
        # Method 2: Look for image tags
        if len(image_urls) < limit:
            for img in soup.find_all('img'):
                if len(image_urls) >= limit * 2:
                    break
                
                src = img.get('src', '')
                data_src = img.get('data-src', '')
                img_url = data_src if data_src and data_src.startswith('http') else src
                
                # Check for indications of image size in attributes
                width = img.get('width', '0')
                height = img.get('height', '0')
                
                try:
                    width = int(width)
                    height = int(height)
                    # Skip small images
                    if width > 0 and height > 0 and (width < 400 or height < 400):
                        continue
                except ValueError:
                    pass
                
                if img_url and img_url.startswith('http') and img_url not in image_urls:
                    if not img_url.startswith('https://www.google.com'):
                        image_urls.append(img_url)
        
        # Try Bing as an alternative for high resolution images
        # if len(image_urls) < limit:
        #     try:
        #         logger.info("Trying Bing image search for high resolution images")
        #         bing_query = quote_plus(f"{query} school uniform Singapore")
        #         # Using Bing filter for large images
        #         bing_url = f"https://www.bing.com/images/search?q={bing_query}&qft=+filterui:imagesize-large"
                
        #         bing_response = requests.get(bing_url, headers=headers, timeout=15)
        #         bing_response.raise_for_status()
                
        #         bing_soup = BeautifulSoup(bing_response.text, 'html.parser')
                
        #         # Extract image URLs from Bing
        #         for img in bing_soup.select('.mimg'):
        #             if len(image_urls) >= limit * 2:
        #                 break
                    
        #             src = img.get('src', '')
        #             data_src = img.get('data-src', '')
        #             img_url = data_src if data_src and data_src.startswith('http') else src
                    
        #             if img_url and img_url.startswith('http') and img_url not in image_urls:
        #                 image_urls.append(img_url)
                
        #         # Also check JSON data in Bing's page
        #         bing_scripts = bing_soup.find_all('script')
        #         for script in bing_scripts:
        #             if script.string and "var IG=" in script.string:
        #                 urls = re.findall(r'"murl":"(https?://[^"]+)"', script.string)
        #                 for url in urls:
        #                     if len(image_urls) >= limit * 2:
        #                         break
        #                     if url not in image_urls:
        #                         image_urls.append(url)
        #     except Exception as e:
        #         logger.warning(f"Bing search failed: {str(e)}")
        
        
        
        logger.info(f"Found {len(image_urls)} potential image URLs")
        
        # Filter images that are too small or from irrelevant domains
        filtered_urls = []
        for url in image_urls:
            # Skip tiny thumbnails or icons
            skip = False
            size_indicators = ['thumb', 'icon', '16x16', '32x32', '64x64', '100x100', 'thumbnail']
            for indicator in size_indicators:
                if indicator in url.lower():
                    skip = True
                    break
                    
            # Skip irrelevant image hosting
            irrelevant_sources = ['emoji', 'emoticon', 'icon', 'clipart', 'button']
            for source in irrelevant_sources:
                if source in url.lower():
                    skip = True
                    break
                    
            # Prioritize URLs with high-resolution indicators
            if not skip:
                priority = 0
                hires_indicators = ['large', 'high', 'original', 'full', '1024x', '2048x', 'highres']
                for indicator in hires_indicators:
                    if indicator in url.lower():
                        priority += 1
                
                # Insert higher-priority URLs at the front
                if priority > 0 and filtered_urls:
                    filtered_urls.insert(0, url)
                else:
                    filtered_urls.append(url)
        
        logger.info(f"Filtered to {len(filtered_urls)} URLs that look promising for high-resolution images")
        return filtered_urls
    except Exception as e:
        logger.error(f"Error searching for images: {str(e)}")
        return []

def fetch_school_website(school_name):
    """Try to find the school's official website"""
    try:
        # Use a more specific query for official school websites
        query = quote_plus(f"{school_name} official school website singapore moe.edu.sg")
        search_url = f"https://www.google.com/search?q={query}"
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(search_url, headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the first few search results to find official sites
        for result in soup.select(".tF2Cxc"):
            link = result.select_one("a")
            if link and link.has_attr('href'):
                url = link['href']
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                
                # Prefer official MOE school sites which typically have these domains
                if any(domain in url.lower() for domain in ['moe.edu.sg', '.edu.sg', 'school.sg', 'schools.gov.sg']):
                    return url
                
                # Skip common non-school sites
                if any(domain in url.lower() for domain in ['wikipedia', 'facebook', 'instagram', 'twitter', 'linkedin']):
                    continue
                    
                return url
        
        # Second pass - be less strict if we didn't find anything
        for result in soup.select(".tF2Cxc"):
            link = result.select_one("a")
            if link and link.has_attr('href'):
                url = link['href']
                if url.startswith('/url?q='):
                    url = url.split('/url?q=')[1].split('&')[0]
                
                # Skip non-websites
                if not url.startswith('http'):
                    continue
                    
                return url
                
        # If all else fails, return MOE schoolfinder + school name
        school_query = quote_plus(school_name)
        return f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={school_query}"
    except Exception as e:
        logger.error(f"Error finding school website: {str(e)}")
        # More specific fallback with school name
        school_query = quote_plus(school_name)
        return f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={school_query}"

def fetch_school_description_from_duckduckgo(school_name):
    """Get a school description from DuckDuckGo search results"""
    try:
        query = quote_plus(f"{school_name} singapore primary school information history")
        logger.info(f"Searching DuckDuckGo for description of {school_name}")
        
        # Use DuckDuckGo HTML search
        search_url = f"https://duckduckgo.com/html/?q={query}"
        
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        description_candidates = []
        
        # Parse the results
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for result snippets
        for result in soup.select(".result__snippet, .result-snippet"):
            text = result.get_text(strip=True)
            # Check if the snippet is about our school
            if school_name.lower() in text.lower() and len(text) > 100:
                description_candidates.append(text)
        
        # Also look for full answers that sometimes appear
        for answer in soup.select(".result__a--no-result, .result-highlight"):
            text = answer.get_text(strip=True)
            if len(text) > 100:
                # Give higher priority to these direct answers
                description_candidates.insert(0, text)
        
        # If we found descriptions, select the best one
        if description_candidates:
            # Sort by relevance and length
            description_candidates.sort(key=lambda desc: (
                school_name.lower() in desc.lower(),  # First prioritize by whether it mentions the school
                len(desc)  # Then by length
            ), reverse=True)
            
            description = description_candidates[0]
            
            # Clean and truncate if needed
            description = re.sub(r'\s+', ' ', description).strip()
            if len(description) > 300:
                description = description[:297] + "..."
                
            logger.info(f"Found description from DuckDuckGo: {description[:50]}...")
            return description
            
        logger.info("No suitable description found from DuckDuckGo")
        return None
    
    except Exception as e:
        logger.error(f"Error getting description from DuckDuckGo: {str(e)}")
        return None

def fetch_school_location_from_duckduckgo(school_name):
    """Get a school's location information from DuckDuckGo search results"""
    try:
        query = quote_plus(f"{school_name} singapore primary school address location")
        logger.info(f"Searching DuckDuckGo for location of {school_name}")
        
        # Use DuckDuckGo HTML search
        search_url = f"https://duckduckgo.com/html/?q={query}"
        
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        location_candidates = []
        
        # Parse the results
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for snippets in results
        for result in soup.select(".result__snippet, .result-snippet"):
            text = result.get_text(strip=True)
            
            # Look for postal code pattern (Singapore postal codes are 6 digits)
            postal_match = re.search(r'singapore\s+\d{6}', text, re.IGNORECASE)
            if postal_match:
                location_candidates.append(postal_match.group(0).title())
                
            # Look for address pattern
            if 'address' in text.lower() and 'singapore' in text.lower():
                # Try to extract the full address
                address_match = re.search(r'address[^:]*:\s*([^\.]+)', text, re.IGNORECASE)
                if address_match:
                    address = address_match.group(1).strip()
                    if 'singapore' in address.lower():
                        location_candidates.append(address)
        
        # If we found location info, select the best one
        if location_candidates:
            # Prefer entries with postal codes
            postal_entries = [loc for loc in location_candidates if re.search(r'\d{6}', loc)]
            if postal_entries:
                # Sort by length (prefer shorter, cleaner entries)
                postal_entries.sort(key=len)
                return postal_entries[0].strip()
            else:
                # Otherwise, use the first entry
                return location_candidates[0].strip()
                
        logger.info("No suitable location found from DuckDuckGo")
        return None
    
    except Exception as e:
        logger.error(f"Error getting location from DuckDuckGo: {str(e)}")
        return None

def fetch_school_description(school_name, website_url):
    """Generate a custom description for a school by searching online or extracting from the school website"""
    try:
        description_candidates = []
        
        # NEW: Try DuckDuckGo first for description
        duckduckgo_description = fetch_school_description_from_duckduckgo(school_name)
        if duckduckgo_description:
            description_candidates.append(duckduckgo_description)
        
        # CHANGED: First try to search online (prioritize internet search)
        logger.info(f"Searching for school information online: {school_name}")
        
        # Try Google search first
        search_query = quote_plus(f"{school_name} singapore primary school information history mission")
        search_url = f"https://www.google.com/search?q={search_query}"
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract snippets from search results
        for snippet in soup.select(".VwiC3b"):
            snippet_text = snippet.get_text(strip=True)
            if len(snippet_text) > 100 and school_name.lower() in snippet_text.lower():
                description_candidates.append(snippet_text)
        
        # Try to extract from MOE schoolfinder specifically (often has official descriptions)
        try:
            school_query = quote_plus(school_name)
            moe_url = f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={school_query}"
            
            moe_response = requests.get(moe_url, headers=headers, timeout=15)
            moe_response.raise_for_status()
            
            moe_soup = BeautifulSoup(moe_response.text, 'html.parser')
            
            # Look for description or special features sections
            description_keywords = ['description', 'about', 'overview', 'special feature']
            
            # Combine all text sections that might contain the description
            all_moe_text = moe_soup.get_text()
            
            # Extract chunks of text after each keyword
            for keyword in description_keywords:
                if keyword.lower() in all_moe_text.lower():
                    start_idx = all_moe_text.lower().find(keyword.lower())
                    if start_idx != -1:
                        # Skip the keyword itself
                        start_idx = start_idx + len(keyword)
                        # Get chunk of text after the keyword (up to 500 chars)
                        text_chunk = all_moe_text[start_idx:start_idx+500]
                        
                        # Clean up the chunk
                        text_chunk = text_chunk.strip()
                        if text_chunk.startswith(':'):
                            text_chunk = text_chunk[1:].strip()
                            
                        # Further clean up and truncate
                        if len(text_chunk) > 50:
                            text_chunk = re.sub(r'\s+', ' ', text_chunk).strip()
                            
                            # If there's a logical end point, use it
                            period_idx = text_chunk.find('.')
                            if 50 < period_idx < 400:
                                text_chunk = text_chunk[:period_idx+1]
                            elif len(text_chunk) > 300:
                                text_chunk = text_chunk[:297] + "..."
                            
                            description_candidates.append(text_chunk)
        except Exception as e:
            logger.warning(f"Error getting description from MOE: {str(e)}")
            
        # Try Wikipedia for school descriptions
        try:
            wiki_query = quote_plus(f"{school_name} singapore school wiki")
            wiki_search_url = f"https://www.google.com/search?q={wiki_query}"
            
            wiki_response = requests.get(wiki_search_url, headers=headers, timeout=15)
            wiki_response.raise_for_status()
            
            wiki_soup = BeautifulSoup(wiki_response.text, 'html.parser')
            
            # Look for Wikipedia links
            for result in wiki_soup.select(".tF2Cxc"):
                link = result.select_one("a")
                if link and link.has_attr('href'):
                    url = link['href']
                    if url.startswith('/url?q='):
                        url = url.split('/url?q=')[1].split('&')[0]
                    
                    # Check if it's a Wikipedia page
                    if 'wikipedia.org' in url.lower():
                        wiki_page_response = requests.get(url, headers=headers, timeout=15)
                        wiki_page_soup = BeautifulSoup(wiki_page_response.text, 'html.parser')
                        
                        # Get the first few paragraphs from the Wikipedia page
                        wiki_paragraphs = wiki_page_soup.select("#mw-content-text p")
                        for i, paragraph in enumerate(wiki_paragraphs):
                            p_text = paragraph.get_text(strip=True)
                            if len(p_text) > 100 and not p_text.startswith('[') and i < 3:
                                description_candidates.append(p_text)
                        break
        except Exception as e:
            logger.warning(f"Error getting description from Wikipedia: {str(e)}")
            
        # Only fall back to the school website if we didn't find anything useful online
        if not description_candidates and website_url and website_url.startswith('http') and not 'schoolfinder' in website_url:
            try:
                logger.info(f"Falling back to school website for description: {website_url}")
                # ... existing website extraction code ...
            except Exception as e:
                logger.warning(f"Error extracting description from website: {str(e)}")
        
        # If we found at least one good description, use it
        if description_candidates:
            # Sort by length (prefer longer, more informative descriptions)
            # But also prioritize descriptions that mention the school name
            description_candidates.sort(key=lambda desc: (
                school_name.lower() in desc.lower(),  # First prioritize by whether it mentions the school
                len(desc)  # Then by length
            ), reverse=True)
            
            description = description_candidates[0]
            
            # Clean it up
            description = re.sub(r'\s+', ' ', description).strip()
            # Truncate if too long
            if len(description) > 300:
                description = description[:297] + "..."
                
            return description
        
        # ... existing fallback code ...
    
    except Exception as e:
        logger.error(f"Error generating description for {school_name}: {str(e)}")
        return f"{school_name} is a primary school in Singapore known for its quality education and commitment to nurturing well-rounded students."

def fetch_school_location(school_name, website_url):
    """Extract precise location information for a school from online sources"""
    try:
        location_candidates = []
        
        # NEW: Try DuckDuckGo first for location
        duckduckgo_location = fetch_school_location_from_duckduckgo(school_name)
        if duckduckgo_location:
            location_candidates.append(duckduckgo_location)
        
        # CHANGED: Try Google Maps and search engines (prioritize internet search)
        logger.info(f"Searching online for school location: {school_name}")
        
        # Try direct Google search for the school's address
        search_query = quote_plus(f"{school_name} address postal code")
        search_url = f"https://www.google.com/search?q={search_query}"
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for address information in search results
        for result in soup.select(".VwiC3b, .yXK7lf, .N54PNb, .BNeawe"):
            result_text = result.get_text()
            if 'singapore' in result_text.lower():
                # Look for postal code pattern
                postal_match = re.search(r'singapore\s+\d{6}', result_text, re.IGNORECASE)
                if postal_match:
                    location_candidates.append(postal_match.group(0).title())
                    
                # Look for more detailed address patterns
                address_pattern = re.search(r'address.*?:(.+?)(?:\.|\n|$)', result_text, re.IGNORECASE)
                if address_pattern:
                    address = address_pattern.group(1).strip()
                    if 'singapore' in address.lower() and 10 < len(address) < 150:
                        location_candidates.append(address)
        
        # Try to get location from MOE school finder
        try:
            school_query = quote_plus(school_name)
            moe_url = f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={school_query}"
            
            moe_response = requests.get(moe_url, headers=headers, timeout=15)
            moe_response.raise_for_status()
            
            moe_soup = BeautifulSoup(moe_response.text, 'html.parser')
            page_text = moe_soup.get_text()
            
            # Look for address or postal code
            address_patterns = ['Address:', 'Location:', 'Postal Code:']
            
            for pattern in address_patterns:
                if pattern in page_text:
                    # Extract text around the address pattern
                    start_idx = page_text.find(pattern)
                    if start_idx != -1:
                        # Get a chunk of text after the pattern
                        address_chunk = page_text[start_idx:start_idx+200]
                        # Extract up to newline or period
                        end_idx = min(
                            address_chunk.find('\n') if address_chunk.find('\n') != -1 else len(address_chunk),
                            address_chunk.find('.') if address_chunk.find('.') != -1 else len(address_chunk)
                        )
                        address_block = address_chunk[:end_idx].strip()
                        
                        # Clean up the address
                        address_clean = re.sub(r'\s+', ' ', address_block)
                        location_candidates.append(address_clean)
                        
                        # Try to extract postal code
                        postal_code = re.search(r'Singapore\s+\d{6}', address_block, re.IGNORECASE)
                        if postal_code:
                            location_candidates.append(postal_code.group(0))
                            break  # We found the best possible match
        except Exception as e:
            logger.warning(f"Error getting location from MOE: {str(e)}")
            
        # Only fall back to the school website if we didn't find anything useful online
        if not location_candidates and website_url and website_url.startswith('http') and not 'schoolfinder' in website_url:
            try:
                logger.info(f"Falling back to school website for location: {website_url}")
                # ... existing website extraction code ...
            except Exception as e:
                logger.warning(f"Error extracting location from website: {str(e)}")
        
        # Use the best location information found
        if location_candidates:
            # Prefer entries with postal codes
            postal_entries = [loc for loc in location_candidates if re.search(r'\d{6}', loc)]
            if postal_entries:
                # Pick the entry with the cleanest format
                postal_entries.sort(key=len)  # Shorter entries are often cleaner
                return postal_entries[0].strip()
            else:
                # Clean up and return the most informative location
                # Sort by length but prefer entries that mention "Singapore"
                location_candidates.sort(key=lambda loc: (
                    "singapore" in loc.lower(),  # First prioritize by whether it mentions Singapore
                    len(loc)  # Then by length
                ), reverse=True)
                return location_candidates[0].strip()
        
        # ... existing fallback code ...
            
    except Exception as e:
        logger.error(f"Error finding school location: {str(e)}")
        return "Singapore"

def fetch_school_website_from_moe(school_name):
    """Get the official school website from MOE school finder page"""
    try:
        # Construct the MOE school finder URL
        school_query = quote_plus(school_name)
        moe_url = f"https://www.moe.gov.sg/schoolfinder/schooldetail?schoolname={school_query}"
        
        logger.info(f"Fetching school website from MOE for: {school_name}")
        
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(moe_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for website link on MOE page - typically in a specific format
        website_link = None
        
        # Look for links with text like "School Website" or containing website/http
        for link in soup.find_all('a'):
            link_text = link.get_text(strip=True).lower()
            link_href = link.get('href', '')
            
            # if ('website' in link_text or 'official site' in link_text) and link_href.startswith('http'):
            #     website_link = link_href
            #     break
            
            # Sometimes the website URL is just listed directly
            if link_href.startswith('http') and ('.edu.sg' in link_href or '.moe.edu.sg' in link_href):
                website_link = link_href
                break
        
        if website_link:
            logger.info(f"Found official website from MOE: {website_link}")
            return website_link
        else:
            # If no direct link found, try to extract from text
            content = soup.get_text()
            urls = re.findall(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)', content)
            
            for url in urls:
                if '.edu.sg' in url or '.moe.edu.sg' in url:
                    logger.info(f"Extracted website URL from MOE page text: {url}")
                    return url
            
            # If still not found, fall back to traditional search
            logger.info("No website found on MOE page, using general search method")
            return fetch_school_website(school_name)
            
    except Exception as e:
        logger.error(f"Error fetching from MOE school finder: {str(e)}")
        # Fall back to regular website search on failure
        return fetch_school_website(school_name)

def search_school_website_for_images(school_name):
    """Search the school's official website for uniform images"""
    try:
        # Get school website from MOE first
        website_url = fetch_school_website_from_moe(school_name)
        
        if not website_url or not website_url.startswith('http'):
            logger.warning(f"Could not find valid website for {school_name}")
            return []
            
        logger.info(f"Searching for uniform images on school website: {website_url}")
        
        image_urls = []
        visited_pages = set()
        pages_to_visit = [website_url]
        
        # Keywords that might indicate uniform-related pages or images
        uniform_keywords = ['uniform', 'dress code', 'attire', 'school dress', 'appearance', 'dress regulation']
        
        # Limit the crawl depth and number of pages
        max_pages = 10
        pages_visited = 0
        
        headers = {'User-Agent': get_random_user_agent()}
        
        # First try to find uniform-specific pages
        while pages_to_visit and pages_visited < max_pages:
            current_url = pages_to_visit.pop(0)
            
            if current_url in visited_pages:
                continue
                
            visited_pages.add(current_url)
            pages_visited += 1
            
            try:
                logger.info(f"Visiting: {current_url}")
                response = requests.get(current_url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check page title and content for uniform-related keywords
                page_text = soup.get_text().lower()
                page_title = soup.title.string.lower() if soup.title else ""
                
                is_uniform_page = any(keyword in page_text for keyword in uniform_keywords) or \
                                  any(keyword in page_title for keyword in uniform_keywords)
                
                # If this is the main page or seems uniform-related, extract images
                if pages_visited == 1 or is_uniform_page:
                    # Find all images on the page
                    for img in soup.find_all('img'):
                        src = img.get('src', '')
                        if not src:
                            continue
                            
                        # Convert relative URLs to absolute
                        if not src.startswith(('http://', 'https://')):
                            src = urljoin(current_url, src)
                            
                        # Check if the image appears to be a uniform image based on attributes
                        img_alt = img.get('alt', '').lower()
                        img_class = ' '.join(img.get('class', [])).lower()
                        img_id = img.get('id', '').lower()
                        
                        # Analyze if image is potentially a uniform image
                        is_potential_uniform = any(keyword in img_alt for keyword in uniform_keywords) or \
                                               any(keyword in img_class for keyword in uniform_keywords) or \
                                               any(keyword in img_id for keyword in uniform_keywords) or \
                                               any(keyword in src.lower() for keyword in uniform_keywords)
                        
                        # If it's potentially a uniform image and not a tiny icon
                        if is_potential_uniform and not any(x in src.lower() for x in ['icon', 'logo', 'banner']):
                            if src not in image_urls:
                                logger.info(f"Found potential uniform image: {src}")
                                image_urls.append(src)
                
                # Queue additional uniform-related pages for crawling
                for link in soup.find_all('a'):
                    link_text = link.get_text().lower()
                    href = link.get('href', '')
                    
                    # Only follow links that might be about uniforms
                    is_uniform_link = any(keyword in link_text for keyword in uniform_keywords)
                    
                    if is_uniform_link and href:
                        # Handle relative URLs
                        if not href.startswith(('http://', 'https://')):
                            href = urljoin(current_url, href)
                            
                        # Stay within the same domain
                        if href.startswith(website_url) and href not in visited_pages:
                            pages_to_visit.append(href)
            
            except Exception as e:
                logger.warning(f"Error processing page {current_url}: {str(e)}")
        
        # If no specific uniform images found, try to extract all reasonably-sized images
        if not image_urls and len(visited_pages) > 0:
            logger.info("No specific uniform images found. Extracting all reasonably-sized images from main page.")
            try:
                main_page_url = next(iter(visited_pages))  # Get the first visited page (usually the main page)
                response = requests.get(main_page_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if not src:
                        continue
                        
                    # Convert relative URLs to absolute
                    if not src.startswith(('http://', 'https://')):
                        src = urljoin(main_page_url, src)
                        
                    # Skip tiny images, logos, and icons
                    width = img.get('width', '0')
                    height = img.get('height', '0')
                    
                    try:
                        width = int(width)
                        height = int(height)
                        # Skip small images that are likely icons
                        if width > 0 and height > 0 and (width < 100 or height < 100):
                            continue
                    except ValueError:
                        pass
                        
                    # Skip common non-uniform elements
                    if any(x in src.lower() for x in ['icon', 'logo', 'banner', 'button']):
                        continue
                        
                    if src not in image_urls:
                        image_urls.append(src)
            except Exception as e:
                logger.warning(f"Error extracting alternative images: {str(e)}")
        
        logger.info(f"Found {len(image_urls)} potential uniform images on school website")
        return image_urls
        
    except Exception as e:
        logger.error(f"Error searching school website for images: {str(e)}")
        return []

def search_school_uniforms():
    """
    Search for school uniform images and download them
    """
    school_data = []
    
    # Try to load existing data first, so we don't start from scratch
    json_path = os.path.join(DATA_DIR, 'school_uniforms.json')
    existing_data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_school_data = json.load(f)
                # Convert to dict for easy lookup
                existing_data = {school['name']: school for school in existing_school_data}
                logger.info(f"Loaded {len(existing_data)} existing school entries")
        except Exception as e:
            logger.error(f"Error loading existing data: {str(e)}")
    
    for i, school in enumerate(SCHOOLS, 1):
        logger.info(f"Processing {i}/{len(SCHOOLS)}: {school}")
        
        # Get or fetch the school's website URL
        website_url = fetch_school_website_from_moe(school)
        
        # Create base data for the school - REMOVED DESCRIPTION
        school_info = {
            "name": school,
            "location": "",  # Will be populated with custom location
            "uniform_image": "",
            "image_url": "",
            "website": website_url
        }
        
        # Generate custom location (BUT NOT DESCRIPTION)
        logger.info(f"Generating custom location for {school}")
        school_info["location"] = fetch_school_location(school, website_url)
        
        # First try to get images directly from the school website
        logger.info(f"Searching for uniform images on school website for {school}")
        # website_image_urls = search_school_website_for_images(school)
        
        # If school website search didn't yield results, fall back to Google/Bing search
        # image_urls = website_image_urls
        image_urls = 0
        if not image_urls:
            logger.info(f"No uniform images found on school website, falling back to search engines for {school}")
            # Search for uniform image - try up to 3 times
            max_retries = 3
            for retry in range(max_retries):
                if retry > 0:
                    logger.info(f"Retry {retry} for uniform image of {school}")
                    time.sleep(random.uniform(3, 5))  # Wait longer between retries
                    
                query = f"{school} uniform"
                image_urls = search_duckduckgo_images(query, limit=5)  # Get 5 URLs
                
                if image_urls:
                    break
        
        # Try multiple search engines for better results
        for search_engine in ["duckduckgo", "google"]:
            logger.info(f"Trying {search_engine} search for {school} uniform images")
            
            if search_engine == "duckduckgo":
                image_urls = search_duckduckgo_images(f"{school} uniform", limit=5)
            elif search_engine == "google":
                image_urls = search_google_images(f"{school} uniform", limit=5)
            
            if image_urls:
                logger.info(f"Found images using {search_engine}")
                break
        
        # Download the image
        image_downloaded = False
        for url in image_urls:
            # Clean up school name for filename
            school_name_clean = school.lower().replace(' ', '_').replace('(', '').replace(')', '')
            school_name_clean = school_name_clean.replace("'", "")
            image_filename = f"{school_name_clean}_uniform.jpg"
            image_path = os.path.join(IMAGES_DIR, image_filename)
            
            # Try the URL
            if download_image(url, image_path):
                school_info["uniform_image"] = image_filename
                school_info["image_url"] = url
                image_downloaded = True
                logger.info(f"Downloaded uniform image for {school}")
                break
            else:
                logger.warning(f"Failed to download uniform image for {school} from {url}")
        
        # Add the school data if we got the image
        if image_downloaded:
            school_data.append(school_info)
            logger.info(f"Added {school} with uniform image and custom description")
        else:
            logger.warning(f"Skipping {school} - no image found")
        
        # Save after each school in case of interruption
        with open(os.path.join(DATA_DIR, 'school_uniforms.json'), 'w', encoding='utf-8') as f:
            json.dump(school_data, f, indent=2)
        
        # Be respectful of servers - longer delay between schools
        time.sleep(random.uniform(3, 6))
    
    logger.info(f"Data saved to {os.path.join(DATA_DIR, 'school_uniforms.json')}")
    logger.info(f"Generated {len(school_data)} school uniform entries")
    
    return school_data

def generate_html(school_data):
    """
    Generate an HTML file to display the school uniform information
    """
    html_path = os.path.join(BASE_DIR, 'singapore_school_uniforms.html')
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Singapore Primary School Uniforms</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Singapore Primary School Uniforms</h1>
        <p>A visual collection of uniforms from primary schools across Singapore</p>
    </header>
    
    <div class="filters">
        <input type="text" id="searchInput" placeholder="Search for schools...">
    </div>
    
    <div class="schools-container" id="schoolsContainer">
"""
    
    # Add each school to the HTML - WITHOUT THE DESCRIPTION SECTION
    for school in school_data:
        html_content += f"""
        <div class="school-card">
            <h2>{school['name']}</h2>
            <p class="school-location">{school['location']}</p>
            <div class="uniform-image">
                <img src="school_uniforms/{school['uniform_image']}" alt="{school['name']} uniform">
                <p><a href="{school['image_url']}" target="_blank">Original Image Source</a></p>
            </div>
            <a href="{school['website']}" target="_blank" class="school-website">Visit School Website</a>
        </div>
"""
    
    html_content += """
    </div>
    
    <footer>
        <p>&copy; 2024 Singapore School Uniforms Collection</p>
    </footer>
    
    <script>
        // Simple search functionality
        document.getElementById('searchInput').addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const schoolCards = document.querySelectorAll('.school-card');
            
            schoolCards.forEach(card => {
                const schoolName = card.querySelector('h2').textContent.toLowerCase();
                if (schoolName.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML file generated at {html_path}")

def generate_css():
    """
    Generate a CSS file for styling the school uniforms webpage
    """
    css_path = os.path.join(BASE_DIR, 'styles.css')
    
    css_content = """/* Singapore School Uniforms CSS */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
    padding: 20px;
}

header {
    text-align: center;
    padding: 30px 0;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

header h1 {
    color: #e63946;
    margin-bottom: 10px;
}

.filters {
    padding: 15px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

#searchInput {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.schools-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.school-card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition: transform 0.3s ease;
}

.school-card:hover {
    transform: translateY(-5px);
}

.school-card h2 {
    color: #1d3557;
    margin-bottom: 10px;
    font-size: 1.5rem;
}

.school-location {
    color: #777;
    font-size: 0.9rem;
    margin-bottom: 15px;
}

.uniform-images {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}

.uniform-image {
    flex: 1;
    min-width: 120px;
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
}

.uniform-image img {
    width: 100%;
    height: auto;
    display: block;
}

.school-description {
    margin-bottom: 15px;
    font-size: 0.95rem;
}

.school-website {
    display: inline-block;
    background-color: #1d3557;
    color: #fff;
    text-decoration: none;
    padding: 8px 15px;
    border-radius: 5px;
    font-size: 0.9rem;
    transition: background-color 0.2s ease;
}

.school-website:hover {
    background-color: #457b9d;
}

footer {
    text-align: center;
    margin-top: 30px;
    padding: 20px 0;
    color: #777;
    font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .schools-container {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
}

@media (max-width: 480px) {
    .schools-container {
        grid-template-columns: 1fr;
    }
    
    .school-card {
        padding: 15px;
    }
}
"""
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"CSS file generated at {css_path}")

def main():
    """Main function to run the scraper and generate the website"""
    print("Script is running...")
    logger.info("Starting Singapore Primary School Uniform Scraper...")
    
    try:
        # Try to install PIL/Pillow if not available
        try:
            from PIL import Image
        except ImportError:
            logger.info("PIL not found, attempting to install it...")
            try:
                import subprocess
                subprocess.check_call(['pip', 'install', 'Pillow'])
                logger.info("Successfully installed Pillow (PIL)")
            except Exception as e:
                logger.warning(f"Failed to install Pillow: {str(e)}. Will continue without image validation.")
        
        # Try to install TensorFlow if not available
        try:
            import tensorflow as tf
        except ImportError:
            logger.info("TensorFlow not found, attempting to install it...")
            try:
                import subprocess
                subprocess.check_call(['pip', 'install', 'tensorflow'])
                logger.info("Successfully installed TensorFlow")
            except Exception as e:
                logger.warning(f"Failed to install TensorFlow: {str(e)}. Will continue without image recognition.")
        
        # First, check for existing JSON data and validate it
        json_path = os.path.join(DATA_DIR, 'school_uniforms.json')
        fixed_data = []
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                logger.info(f"Loaded existing data with {len(existing_data)} schools")
                
                # Check and fix each entry
                for school in existing_data:
                    school_name = school.get('name')
                    logger.info(f"Validating data for {school_name}")
                    
                    # Check if website is generic MOE link and fix if needed
                    if 'schoolfinder' in school.get('website', ''):
                        logger.info(f"Fixing generic website for {school_name}")
                        school['website'] = fetch_school_website(school_name)
                    
                    # Check each image
                    valid_images = []
                    for img_file in school.get('uniform_images', []):
                        img_path = os.path.join(IMAGES_DIR, img_file)
                        
                        # Verify if image exists and is valid
                        if not os.path.exists(img_path) or os.path.getsize(img_path) < 5000:
                            logger.warning(f"Invalid image found for {school_name}: {img_file}")
                            # Will be re-downloaded in search_school_uniforms
                        else:
                            try:
                                from PIL import Image
                                img = Image.open(img_path)
                                img.verify()  # Verify it's a valid image
                                valid_images.append(img_file)
                                logger.info(f"Verified valid image: {img_file}")
                            except ImportError:
                                # If PIL not available, just check file size
                                if os.path.getsize(img_path) > 5000:
                                    valid_images.append(img_file)
                            except:
                                logger.warning(f"Image verification failed for {img_file}")
                                # Will be re-downloaded in search_school_uniforms
                    
                    # Update the school with validated images
                    school['uniform_images'] = valid_images
                    fixed_data.append(school)
                
                # Save the fixed data
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(fixed_data, f, indent=2)
                logger.info(f"Updated JSON file with validated data")
            except Exception as e:
                logger.error(f"Error processing existing data: {str(e)}")
        
        # Now run the search to fill in missing images
        school_data = search_school_uniforms()
        
        # Generate HTML page to display the data
        generate_html(school_data)
        
        # Generate CSS for styling
        generate_css()
        
        logger.info("Done! You can now open singapore_school_uniforms.html in your browser.")
    except KeyboardInterrupt:
        logger.info("Scraper interrupted by user. Saving any data collected...")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        
if __name__ == "__main__":
    main()