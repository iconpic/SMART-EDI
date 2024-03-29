import http.client
import json
import http.client
import mimetypes
from codecs import encode

# test_list = ['7705739450', '7727089950', '3721007671', '2222810899', '7215003597', '7842448766']
test_list = ['7701617450', '7814010561', '7730570800', '7722761751', '2222810899']


def authorization():
  conn = http.client.HTTPSConnection("api-ext.ru.auchan.com")
  payload = json.dumps({
    "Login": "edowg@auchan.ru",
    "Password": "12345678"
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'DiadocAuth ddauth_api_client_id=auchan-6d093803-34f7-4a3d-81b1-bd268e0494af',
    'X-Gravitee-Api-Key': '7d3ca061-edae-437b-9a72-2f6d79cc32e3'
  }
  conn.request("POST", "/edi/diadoc-out/v1/V3/Authenticate?type=password", payload, headers)
  res = conn.getresponse()
  data = res.read()
  token = data.decode("utf-8")
  return token

# x = authorization()
# print(x)
token = 'iHZBnwzPu0QISn4wXwxKaKKb2A9MVY2tqpOxMbwBR22QoFM5QJm78XGtHRtyOWEiKTFySb3jGkh6iaeLamlwmmE83Chs5aeJLsVu7U96h0tUvitNzPNkrR37Chj3acBszeDRtGKjuU1sxT8nu8c2SzA2RRopxWHb3n/rSOliVoY='


def get_to_counteragents(token, afterIndexKey = ''):
  conn = http.client.HTTPSConnection("api-ext.ru.auchan.com")
  boundary = ''
  payload = ''
  headers = {
    'Authorization': f'DiadocAuth ddauth_api_client_id=auchan-6d093803-34f7-4a3d-81b1-bd268e0494af, ddauth_token={token}',
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Gravitee-Api-Key': '7d3ca061-edae-437b-9a72-2f6d79cc32e3',
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
  }
  conn.request("GET", f"/edi/diadoc-out/v1/V2/GetCounteragents?myOrgId=13f51fdb-ee1e-43a8-bfd7-667f34b23246&counteragentStatus=IsMyCounteragent&afterIndexKey={afterIndexKey}", payload, headers)
  res = conn.getresponse()
  data = res.read()
  json_data = json.loads(data.decode("utf-8"))

  result = {}
  for i in json_data['Counteragents']:
    result[i['Organization']['Inn']] = ([i['Organization']['Inn'], i['Organization']['ShortName'], i['Organization']['Kpp'], i['Organization']['FnsParticipantId']])
  return result, i['IndexKey']


# result = get_to_counteragents(token)
# print(test_list)
# print(result[0])


# def search(inn_list, result, search_ka):
#   for i in inn_list:
#     if i not in search_ka:
#       try:
#         full_data_ka.append(result[0][f'{i}'])
#         search_ka.append(result[0][f'{i}'][0])
#       except:
#         pass
#
#
# search_ka = []
# search(test_list, result, search_ka)
# print(search_ka)


def get_organization(token, inn, kpp=''):
  try:
    conn = http.client.HTTPSConnection("api-ext.ru.auchan.com")
    boundary = ''
    payload = ''
    headers = {
      'Authorization': f'DiadocAuth ddauth_api_client_id=auchan-6d093803-34f7-4a3d-81b1-bd268e0494af, ddauth_token={token}',
      'Accept': 'application/json',
      'Content-Type': 'application/json; charset=utf-8',
      'X-Gravitee-Api-Key': '7d3ca061-edae-437b-9a72-2f6d79cc32e3',
      'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("GET",
                 f"/edi/diadoc-out/v1/GetOrganizationsByInnKpp?Inn={inn}&Kpp={kpp}",
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
  except:
    json_data = {'Organizations':[]}
  return json_data


# for i in test_list:
#   result = get_organization(token, i)
#
#   if len(result['Organizations']) == 1:
#     guid_ka_list.append(result['Organizations'][0]['FnsParticipantId'])
#   elif len(result['Organizations']) > 1:
#     print('По ИНН найдены несколько организаций')
#     guid_ka_list.append([])
#   else:
#     print('Не найдено')
#     guid_ka_list.append([])

# print(guid_ka_list)

def search_api_ka(data_all):
  guid_ka_list = []
  for i in data_all:
    result = get_organization(token, i[0], i[1])
    if len(result['Organizations']) == 1:
      guid_ka_list.append(result['Organizations'][0]['FnsParticipantId'])
    elif len(result['Organizations']) > 1:
      guid_ka_list.append('')
    else:
      guid_ka_list.append('')
  return guid_ka_list


def search_api_kas(data_all):
  guid_ka_list = []
  for i in data_all:
    guid_ka = []
    result = get_organization(token, i[0], i[1])
    for i in range(len(result['Organizations'])):
      guid_ka.append(result['Organizations'][i]['FnsParticipantId'])
    guid_ka_list.append(guid_ka)
  return guid_ka_list