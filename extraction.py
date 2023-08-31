import re
import base64
import pandas as pd
import easyocr as ocr

reader = ocr.Reader(['en'], gpu=True, model_storage_directory='.')
result = reader.readtext(r'C:\Users\sprav\Desktop\My Projects\BizCard\bizcard4.png')


def extract_text(result):
    # reader = ocr.Reader(['en'], gpu=True, model_storage_directory='.')
    # result = reader.readtext('/content/bizcard.png')
    lst = []

    for text in result:
        lst.append(text[1])

    return lst

def replacement():
    combine = ' '
    card = combine.join(extract_text(result))
    replacements = [
        (";", ""),
        (',', ''),
        ("WWW ", "www."),
        ("www ", "www."),
        ('www', 'www.'),
        ('www.', 'www'),
        ('wwW', 'www'),
        ('wWW', 'www'),
        ('.com', 'com'),
        ('com', '.com'),
    ]

    for old, new in replacements:
        card = card.replace(old, new)

    return card

def extract_url():
    url_pattern = r"www\.[A-Za-z0-9]+\.[A-Za-z]{2,3}"
    card = replacement()
    host_name = re.findall(url_pattern, card)
    url = ''

    for host in host_name:
        url = url + host
        card = card.replace(host, '')

    return url

def extract_pincode():
    pincode_pattern = r'\d+'
    card = replacement()
    matching = re.findall(pincode_pattern, card)
    pincode = ''

    for code in matching:
      if len(code) == 6 or len(code) == 7:
        pincode = pincode + code
        card = card.replace(code, '')

    return pincode

def extract_phoneNo():
  phoneNo_pattern = r"\+*\d{2,3}-\d{3}-\d{4}"
  card = replacement()
  phone_number = re.findall(phoneNo_pattern, card)
  phone = ''

  for number in phone_number:
    phone = phone + ' ' + number
    card = card.replace(number, '')

  return phone

def extract_mail():
  mailId_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}\b"
  card = replacement()
  mail = re.findall(mailId_pattern, card)
  mail_id = ''

  for id in mail:
    mail_id = mail_id + id
    card = card.replace(id, '')

  return mail_id

def extract_name():
  name_match = []
  name_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
  card = extract_text(result)

  for name in card:
    if re.findall(name_pattern, name):
      name_match.append(name)
  return name_match[0].capitalize()

def extract_desgination():
  degination_match = []
  degination_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
  card = extract_text(result)

  for degination in card:
    if re.findall(degination_pattern, degination):
      degination_match.append(degination)
  return degination_match[1].capitalize()

def extract_company():
  company_match = []
  company_pattern = r'^[A-Za-z]+ [A-Za-z]+$|^[A-Za-z]+$|^[A-Za-z]+ & [A-Za-z]+$'
  card = extract_text(result)

  for company in card:
    if re.findall(company_pattern, company):
      company_match.append(company)
  # return company_match
  if company_match[2] == 'WWW':
    return company_match[3].capitalize() + ' ' + company_match[4].lower()
  elif company_match[1] == 'DATA MANAGER':
    return company_match[2].capitalize() + ' ' + company_match[3].lower()
  elif company_match[1] == 'General Manager':
    return company_match[2].capitalize() + ' ' + company_match[3].lower()
  elif company_match[1] == 'Marketing Executive':
    return company_match[2].capitalize() + ' ' + company_match[3].lower()
  else:
    return company_match[2].capitalize()

def extract_district():
  district_match = replacement().split()
  if district_match[5] == 'St':
    district = district_match[6].capitalize()
  elif district_match[6] == 'St':
    district = district_match[7].capitalize()
  elif district_match[7] == 'St':
    district = district_match[8].capitalize()
  elif district_match[8] == 'St':
    district = district_match[9].capitalize()
  elif district_match[9] == 'St':
    district = district_match[10].capitalize()
  elif district_match[9] == 'global':
    district = district_match[10].capitalize()
  else:
    pass
  return district

def extract_state():
  state_match = replacement().split()
  if state_match[5] == 'St':
    state = state_match[7].capitalize()
  elif state_match[6] == 'St':
    state = state_match[8].capitalize()
  elif state_match[7] == 'St':
    state = state_match[9].capitalize()
  elif state_match[8] == 'St':
    state = state_match[10].capitalize()
  elif state_match[9] == 'St':
    state = state_match[12].capitalize()
  elif state_match[9] == 'global':
    state = state_match[12].capitalize()
  else:
    return None
  return state

def extract_street():
  street_match = replacement().split()
  if street_match[3] == '123':
    street = street_match[3] + ' ' + street_match[4] + ' ' + street_match[5]
  elif street_match[7] == '123':
    street = street_match[7] + ' ' + street_match[8] + ' ' + street_match[9]
  elif street_match[8] == '123':
    street = street_match[8] + ' ' + street_match[9] + ' ' + street_match[15]
  else:
    return None
  return street

def biz_card():
    
    image_data = {
                "card_holder" : [],
                "company_name" : [],
                "designation" : [],
                "mobile_number" :[],
                "email" : [],
                "website" : [],
                "street" : [],
                "district" : [],
                "state" : [],
                "pin_code" : [],
                "image" : []
              }
    
    image_path = r'C:\Users\sprav\Desktop\My Projects\BizCard\bizcard4.png'
    
    with open(image_path, 'rb') as image_file:
        data = image_file.read()
        encoded_image = base64.b64encode(data).decode('utf-8')
    
    image_data['card_holder'].append(extract_name())
    image_data['company_name'].append(extract_company())
    image_data['designation'].append(extract_desgination())
    image_data['mobile_number'].append(extract_phoneNo())
    image_data['email'].append(extract_mail())
    image_data['website'].append(extract_url())
    image_data['street'].append(extract_street())
    image_data['district'].append(extract_district())
    image_data['state'].append(extract_state())
    image_data['pin_code'].append(extract_pincode())
    image_data['image'].append(encoded_image)
    
    biz_card = pd.DataFrame(image_data)
    return biz_card
    