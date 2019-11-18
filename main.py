import urllib.request
from bs4 import BeautifulSoup
import re
import time

length_of_line = 100


def cut_line(string, line_length):
    length_string = len(string)
    if length_string <= line_length:
        return [string, '']
    else:
        for i in range(line_length):
            if string[line_length - 1 - i] == " ":
                line_index = line_length - i
                break
        return [string[0:line_index - 1], string[line_index:length_string]]


def divided_lines(string, line_length):
    divided_line = cut_line(string, length_of_line)
    lines = []
    lines.append(divided_line[0])
    while divided_line[1] != '':
        divided_line = cut_line(divided_line[1], length_of_line)
        lines.append(divided_line[0])
    return lines




def get_members(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print('getting members from url: ' + url)
    ourUrl = opener.open(url).read()
    soup = BeautifulSoup(ourUrl)
    band_name = soup.title.text
    band_name = re.sub(' -.*', '', band_name)
    body = soup.findAll('td')
    members = []

    for i in body:
        text = i.text
        text = re.sub('See also:\n.*', '', text)
        text = re.sub('\n', '', text)
        text = re.sub('.*\d+.*', '', text)
        if text == '':
            pass
        else:
            if "Past" in text:
                break
            else:
                if "Current" in text \
                        or "Last known" in text \
                        or "Bass" in text \
                        or 'Drums' in text \
                        or 'Vocals' in text \
                        or 'Guitars' in text\
                        or "Effects" in text\
                        or "Electronics" in text\
                        or "Modified by" in text\
                        or "xa0" in text\
                        or "Keyboards" in text\
                        or "Piano" in text\
                        or "Percussion" in text:
                    pass
                else:
                    if "Added by" in text:
                        break
                        members = []
                    else:
                        members.append(text)
    result = {}
    result['band'] = band_name
    result['members'] = members
    return result


def find_urls_on_page(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    ourUrl = opener.open(url).read()
    soup = BeautifulSoup(ourUrl)
    foundurl = []
    for link in soup.findAll('a', attrs={'href': re.compile("https://www.metal-archives.com/bands/")}):
        addurl = str(link)
        addurl = re.sub('.*="', '', addurl)
        addurl = re.sub('">.*', '', addurl)
        if addurl in foundurl:
            pass
        else:
            foundurl.append(addurl)
    return foundurl


url1 = 'https://www.metal-archives.com/bands/Entombed/7'
url2 = 'https://www.metal-archives.com/bands/Nihilist/14076'
url3 = 'https://www.metal-archives.com/labels/Abducted_Records/43005'

list_urls = find_urls_on_page(url1)
print(get_members(url1))
print(list_urls)
print(len(list_urls))


def data_mining(list_band_entry, list_urls):
    add_band_entries = []
    for url in list_urls:
        new_entry = get_members(url)
        if new_entry['members'] == []:
            pass
        else:
            if new_entry in list_band_entry:
                pass
            else:
                add_band_entries.append(new_entry)
    add_band_entries.extend(list_band_entry)
    return add_band_entries


def key_in_dictionary(dict, key):
    try:
        dict[key]
        return True
    except KeyError:
        return False

def mine_bands(number_of_urls, list_band_entry, starting_url_list, url_used_dictionary):
    next_url_list = []
    next_url_dictionary = url_used_dictionary
    list_band_entry_next = list_band_entry
    for url in starting_url_list:
        new_url_list = find_urls_on_page(url)
        for new_url in new_url_list:
            if key_in_dictionary(url_used_dictionary, new_url):
                pass
            else:
                next_url_list.append(new_url)
                list_band_entry_next.append(get_members(new_url))
                next_url_dictionary[new_url] = True
    if len(next_url_dictionary) < number_of_urls:
        print("number of urls " + str(len(next_url_dictionary)))
        print("list_band_entry_next length " + str(len(list_band_entry_next)))
        list_band_entry_next = mine_bands(number_of_urls, list_band_entry_next, next_url_list, next_url_dictionary)
        return list_band_entry_next
    else:
        print("number of urls " + str(len(next_url_dictionary)))
        print(list_band_entry_next)
        return list_band_entry_next
list_result = []
tt = time.time()

list_result = mine_bands(1400, [get_members(url1)], [url1], {url1: True})
tt = time.time() - tt
print("time for running " + str(round(tt)))

print("sorted " + str(len(list_result)) + " bands")
outfile = open('/home/misanek/PycharmProjects/metallumscraping/bands.txt', 'w')
for result in list_result:
    mem = str(result['members'])
    mem = re.sub('\]', '', mem)
    mem = re.sub('\[', '', mem)
    mem = re.sub("'", '', mem)
    outfile.write('band: ' + result['band'] + ', members: ' + mem + '\n')
print("finished")
#urlfix = 'https://www.metal-archives.com/bands/Daemon/2500'
#print(get_members(urlfix))
sorted_urls = {}
url10 ='https://www.metal-archives.com/bands/Entombed/7'
url11 = 'https://www.metal-archives.com/bands/Whore/3540322656'
sorted_urls[url10] = True
print(sorted_urls)

