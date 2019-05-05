import soft_retrieval
import string
import json
from pydub import AudioSegment

unigrams_dict = {}
subs_path = 'C:/Users/Srivardhan/Desktop/My_Code/workspace5_audio/'

# create_inverted_indexes()
# subs_cleaner()


def get_corrected_query():

    user_input = raw_input("Enter the query:/n")
    mod_input = user_input.strip().lower()
    for p in string.punctuation:
        mod_input = mod_input.replace(p, '')
    print mod_input
    cor_query = soft_retrieval._soft_noise_remover_(mod_input)
    print 'Searching for: ' + cor_query
    return cor_query


def unigrams_indexing(data_list):

    terms_dict = {}
    for each_word in data_list:
        if each_word in terms_dict:
            terms_dict[each_word] += 1
        else:
            terms_dict[each_word] = 1

    return terms_dict


def create_inverted_indexes():

    subs_input = subs_path + 'subs.txt'
    file_open = open(subs_input, 'r')

    data = file_open.read()

    tokens_list = data.split()

    unigrams_dict = unigrams_indexing(tokens_list)
    tokens_output = subs_path + 'subs_tokens.json'
    file_write = open(tokens_output, 'w')
    json.dump(unigrams_dict, file_write)


def subs_cleaner():

    subs_input = subs_path + 'subs.srt'
    file_open = open(subs_input, 'r')
    data = file_open.read()
    data_up = data.split('/n/n')
    sub_data = []
    for i in data_up:
        content = i.split('/n')[2:]

        for c in range(0, len(content)):
            s = content[c]
            if str(content[c].split()[0])[0] != '(':
                if content[c].find(':') > 0:
                    s = ''
                    content[c] = str(content[c]).split(':')[1:]
                    for a in content[c]:
                        s += a
                    s = s[: -1].strip()

                s = s.replace('<i>', '').replace('</i>', '').replace('.', '')

                for p in string.punctuation:
                    s = s.replace(p, '')

                content[c] = s
                sub_data.append(content[c])

    file_write = open(subs_path + 'subs.txt', 'w')
    for s in sub_data:
        file_write.write(s + '/n')


def get_time(query):

    sub_dict = {}
    subs_input = subs_path + 'subs.srt'
    file_open = open(subs_input, 'r')
    subs = file_open.read()
    sub_list = subs.split('/n/n')
    for i in sub_list:
        sub_key = i.split('/n')[1]
        sub_val = i.split('/n')[2:]
        sub_dict[sub_key] = sub_val

    for i in sub_dict:
        talk = sub_dict[i]
        for t in talk:
            t = t.lower()
            for p in string.punctuation:
                t.replace(p, '')
            if t.find(query) > 0:
                return str(i)
    return 'No search results found!'


# query = get_corrected_query()
# res = get_time(query)
# print res


ffmpeg_path = 'C:/Users/Srivardhan/Desktop/My_Code/workspace5_audio'


def get_audio_cip():

    # AudioSegment.ffmpeg = ffmpeg_path
    song = subs_path + 'shape.mp3'
    print song

    sound = AudioSegment.from_mp3(song)

    # len() and slicing are in milliseconds
    halfway_point = len(sound) / 2
    second_half = sound[halfway_point:]

    # Concatenation is just adding
    second_half_3_times = second_half + second_half + second_half

    # writing mp3 files is a one liner
    second_half_3_times.export(subs_path + 'shape_new.mp3', format="mp3")


get_audio_cip()
