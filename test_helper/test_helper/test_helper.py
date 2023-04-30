import hashlib
from PIL import Image
import numpy as np
import requests
from requests_oauthlib import OAuth1
from dateutil import parser
import tweepy
import json
from datetime import timedelta
from sklearn.metrics import accuracy_score
from bs4 import BeautifulSoup
import gensim
import site

class TestFailure(Exception):
    pass
class PrivateTestFailure(Exception):
    pass

class Test(object):
    passed = 0
    numTests = 0
    failFast = False
    private = False

    @classmethod
    def setFailFast(cls):
        cls.failFast = True

    @classmethod
    def setPrivateMode(cls):
        cls.private = True

    @classmethod
    def assertTrue(cls, result, msg="", msg_success=""):
        cls.numTests += 1
        if result == True:
            cls.passed += 1
            print("1 test passed. " + msg_success)
        else:
            print("1 test failed. " + msg)
            if cls.failFast:
                if cls.private:
                    raise PrivateTestFailure(msg)
                else:
                    raise TestFailure(msg)

    @classmethod
    def assertEquals(cls, var, val, msg="", msg_success=""):
        cls.assertTrue(var == val, msg, msg_success)

    @classmethod
    def assertEqualsHashed(cls, var, hashed_val, msg="", msg_success=""):
        cls.assertEquals(cls._hash(var), hashed_val, msg, msg_success)

    @classmethod
    def assertEqualsImagesHashed(cls, img_path, hashed_img, hashed_img_mode, hashed_img_size, msg="", msg_success=""):
        # We show the correct image size and mode without hashing
        assert cls._img_mode(img_path) == hashed_img_mode, "Different kinds of images. The image mode should be {}.".format(hashed_img_mode)
        assert cls._img_size(img_path) == hashed_img_size, "Different sizes. The image size should be {}.".format(hashed_img_size)
        cls.assertEquals(cls._dhash(img_path), hashed_img, msg, msg_success)

    @classmethod
    def printStats(cls):
        print("{0} / {1} test(s) passed.".format(cls.passed, cls.numTests))

    @classmethod
    def _hash(cls, x):
        return hashlib.sha1(str(x).encode()).hexdigest()

    @classmethod
    def _dhash(cls, image_path, hash_size=8):
        # Grayscale and shrink the image in one step.
        image = Image.open(image_path)
        image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )
        # Compare adjacent pixels.
        difference = []
        for row in xrange(hash_size):
            for col in xrange(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)
        # Convert the binary array to a hexadecimal string.
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        return ''.join(hex_string)

    @classmethod
    def _img_mode(cls, image_path):
        image = Image.open(image_path)
        return image.mode

    @classmethod
    def _img_size(cls, image_path):
        image = Image.open(image_path)
        return image.size

    # Some specific cases:
    # Lab 3.1 Ex. 4
    @classmethod
    def euclideanDistMatrix(cls, a, b, det, msg="", msg_success=""):
        if type(a) != np.ndarray or type(b) != np.ndarray:
            print('Arrays "a" and "b" should be numpy arrays')
            cls.assertEquals(False, True, msg, msg_success)
            return
        mask = lambda x: len(zip(*np.where((x < -100) | (x > 100)))) == 0 and 'int' in str(x.dtype)
        if not mask(a) or not mask(b):
            print('Arrays "a" and "b" should contain integer numbers from -100 to 100')
            cls.assertEquals(False, True, msg, msg_success)
            return
        c = np.sqrt(np.power(a,2) + np.power(b,2))
        cls.assertEquals(det, np.linalg.det(c), msg, msg_success)

    # Lab 5 Ex. 1.1
    @classmethod
    def checkClassifier(cls, classifier, tfidf_vectorizer, msg="", msg_success=""):
        examples = [
            'Free Viagra call today!',
            "I'm going to attend the Linux users group tomorrow.",
            'Pay the best price by the product',
            'Explode your business right now',
            'London is the capital of Great Britain',
            'Important information regarding you job',
            'Free Windows installation on your computer',
            'The sky is blue',
            'What Are the Differences Between the Rich and the Poor?',
            'What are you waiting for?'
        ]
        try:
            example_tfidf = tfidf_vectorizer.transform(examples)
            predictions = classifier.predict(example_tfidf)
            cls.assertEquals([1, 0, 1, 1, 0, 1, 1, 0, 0, 1], list(predictions), msg, msg_success)
        except:
            cls.assertEquals(False, True, msg, msg_success)

    # Lab 5 Ex. 1.2
    @classmethod
    def accuracy_scoreSpamHam1(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 1500:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('spam_ham_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.75, msg, msg_success)
    @classmethod
    def accuracy_scoreSpamHam2(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 1500:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('spam_ham_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.9, msg, msg_success)
    @classmethod
    def accuracy_scoreSpamHam3(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 1500:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('spam_ham_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.95, msg, msg_success)
    @classmethod
    def accuracy_scoreSpamHam4(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 1500:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('spam_ham_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.975, msg, msg_success)
    @classmethod
    def accuracy_scoreSpamHam5(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 1500:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('spam_ham_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.9875, msg, msg_success)

    # Lab 5 Ex. 2
    @classmethod
    def accuracy_scoreTitanic1(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 393:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('titanic_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.5, msg, msg_success)
    @classmethod
    def accuracy_scoreTitanic2(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 393:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('titanic_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.7, msg, msg_success)
    @classmethod
    def accuracy_scoreTitanic3(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 393:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('titanic_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.75, msg, msg_success)
    @classmethod
    def accuracy_scoreTitanic4(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 393:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('titanic_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.775, msg, msg_success)
    @classmethod
    def accuracy_scoreTitanic5(cls, preds, msg="", msg_success=""):
        preds = np.array(preds)
        if preds.size != 393:
            cls.assertEquals(True, False, 'Incorrect amount of predicted labels', '')
            return
        y_test = np.loadtxt('titanic_test_labels.txt')
        ac = accuracy_score(y_test, np.array(preds))
        cls.assertEquals(True, ac > 0.8, msg, msg_success)

    # Lab 7.1 Ex. 2
    @classmethod
    def checkScrappedData(cls, data, url_input, msg="", msg_success="", is_matrix_data=True):
        url = "http://www.imdb.com/search/title?sort=num_votes,desc&start=1&title_type=feature&year=1900,2015"
        if url_input != url:
            cls.assertEquals(True, False, 'Incorrect URL', '')
            return
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'html.parser')
        compare_title = "The Matrix" if is_matrix_data else "The Godfather"
        for movie in bs.findAll('td','title'):
            title = movie.find('a').contents[0]
            if title == compare_title:
                genres = movie.find('span','genre').findAll('a')

                dirs, acts = str(movie.find('span','credit')).split("With:")
                dirs = BeautifulSoup(dirs + '</span>')
                acts = BeautifulSoup('<span>' + acts)

                directors = []
                for i in dirs.findAll('a'):
                    try:
                        i.contents[0]
                        directors.append(cls._get_person_data('http://www.imdb.com' + i['href'], i.contents[0]))
                    except:
                        continue

                actors = []
                for i in acts.findAll('a'):
                    try:
                        i.contents[0]
                        actors.append(cls._get_person_data('http://www.imdb.com' + i['href'], i.contents[0]))
                    except:
                        continue
                correct_data = {
                        'title': title,
                        'genres': [g.contents[0] for g in genres],
                        'runtime': movie.find('span','runtime').contents[0].split()[0],
                        'rating': movie.find('span','value').contents[0],
                        'released': movie.find('span','year_type').contents[0][1:-1],
                        'description':  movie.find('span', 'outline').contents[0],
                        'directors': directors,
                        'actors': actors,
                    }

        for key, val in data.iteritems():
            if key in ('actors', 'directors'):
                for i in data[key]:
                    try:
                        if i not in correct_data[key]:
                            cls.assertEquals(True, False, msg, msg_success)
                            return
                    except:
                        cls.assertEquals(True, False, msg, msg_success)
                        return
            else:
                try:
                    if data[key] != correct_data[key]:
                        cls.assertEquals(True, False, msg, msg_success)
                        return
                except:
                    cls.assertEquals(True, False, msg, msg_success)
                    return
        cls.assertEquals(True, True, msg, msg_success)

    @classmethod
    def _get_person_data(cls, url, name):
        res = {'name': name}
        try:
            text = requests.get(url).text
        except:
            return res
        an_actor = BeautifulSoup(text, 'html.parser')
        info = an_actor.find('table', attrs={'id': 'name-overview-widget-layout'})
        image = info.find('div', 'image').find('img')
        if image is not None:
            res['image_url'] = image['src']
        else:
            res['image_url'] = ''
        birth_data = info.find('div', attrs={'id': 'name-born-info'})
        if birth_data is not None:
            res['born'] = birth_data.find('time')['datetime']
            birth_place = birth_data.findAll('a')[-1].contents[0]
            birth_place = birth_data.findAll('a')[-1].contents[0].split(',')
            res['country'] = birth_place[-1].strip()
            res['city'] = birth_place[0].strip()
        else:
            res['born'] = res['country'] = res['city'] = ''
        try:
            death_data = info.find('div', attrs={'id': 'name-death-info'})
            res['died'] = death_data.find('time')['datetime']
        except:
            res['died'] = ''
        return res

    # Lab 7.2
    @classmethod
    def resetDatabaseRecords(cls):
        query = """
            CREATE (hanks:Person { name:'Tom Hanks', born:1956, country:'USA' })
            CREATE (sinise:Person { name:'Gary Sinise', born:1955, country:'USA' })
            CREATE (zemeckis:Person { name:'Robert Zemeckis', born:1952, country:'USA' })
            CREATE (forrest_gump:Movie { title:"Forrest Gump", released:1994, duration_min:142,
                                        country:"USA", lang:"English", box_office_Mdol:677.9 })
            CREATE (hanks)-[:ACTED_IN {role:"Forrest Gump"}]->(forrest_gump)
            CREATE (sinise)-[:ACTED_IN {role:"Lieutenant Dan Taylor"}]->(forrest_gump)
            CREATE (zemeckis)-[:DIRECTED]->(forrest_gump)

            CREATE (duncan:Person { name:'Michael Clarke Duncan', born:1957, country:'USA' })
            CREATE (darabont:Person { name:'Frank Darabont', born:1959, country:'France' })
            CREATE (king:Person { name:'Stephen King', born:1947, country:'USA' })
            CREATE (green_mile:Movie { title:"The Green Mile", released:1999, duration_min:188,
                                        country:"USA", lang:"English", box_office_Mdol:290.7 })
            CREATE (hanks)-[:ACTED_IN {role:"Paul Edgecomb"}]->(green_mile)
            CREATE (sinise)-[:ACTED_IN {role:"Burt Hammersmith"}]->(green_mile)
            CREATE (duncan)-[:ACTED_IN {role:"John Coffey"}]->(green_mile)
            CREATE (darabont)-[:DIRECTED]->(green_mile)
            CREATE (king)-[:BASED_ON]->(green_mile)

            CREATE (single_actor:Person { name:'Sylvester Stallone', born:1946, country:'USA' })

            CREATE (di_caprio:Person { name:'Leonardo DiCaprio', born:1974, country:'USA' })
            CREATE (inception:Movie { title:"Inseption", released:2010, duration_min:148,
                                        country:"USA", lang:"English", box_office_Mdol:825.5 })
            CREATE (di_caprio)-[:ACTED_IN]->(inception)

            CREATE (matrix1:Movie { title: 'The Matrix', released: 1999, duration_min: 136, box_office_Mdol: 463.5 })
            CREATE (matrix2:Movie { title: 'The Matrix Reloaded', released: 2003, duration_min: 138, box_office_Mdol: 742.1 })
            CREATE (matrix3:Movie { title: 'The Matrix Revolutions', released: 2003, duration_min: 129, box_office_Mdol: 427.3 })
            CREATE (keanu:Person { name: 'Keanu Reeves', born: 1964, country: "Canada" })
            CREATE (laurence:Person { name: 'Laurence Fishburne', born: 1961, country: "USA" })
            CREATE (carrieanne:Person { name: 'Carrie-Anne Moss', born: 1967, country: "Canada" })
            CREATE (keanu)-[:ACTED_IN { role: 'Neo' }]->(matrix1)
            CREATE (keanu)-[:ACTED_IN { role: 'Neo' }]->(matrix2)
            CREATE (keanu)-[:ACTED_IN { role: 'Neo' }]->(matrix3)
            CREATE (laurence)-[:ACTED_IN { role: 'Morpheus' }]->(matrix1)
            CREATE (laurence)-[:ACTED_IN { role: 'Morpheus' }]->(matrix2)
            CREATE (laurence)-[:ACTED_IN { role: 'Morpheus' }]->(matrix3)
            CREATE (carrieanne)-[:ACTED_IN { role: 'Trinity' }]->(matrix1)
            CREATE (carrieanne)-[:ACTED_IN { role: 'Trinity' }]->(matrix2)
            CREATE (carrieanne)-[:ACTED_IN { role: 'Trinity' }]->(matrix3)
        """
        return query

    # Lab 8.1 Ex. 1
    @classmethod
    def twitterFriendsList(cls, friends, url, auth, params, msg="", msg_success=""):
        res = requests.get(url, auth=auth, params=params)
        data = res.json()
        fr = []
        for i in data['users']:
            fr.append({'name': i['name'], 'followers_count': i['followers_count']})
        fr.sort(key=lambda x: -x['followers_count'])
        cls.assertEquals(friends, fr, msg, msg_success)

    # Lab 8.1 Ex. 2
    @classmethod
    def twitterRecentTweets(cls, tweets, url, auth, params, msg="", msg_success=""):
        res = requests.get(url, auth=auth, params=params)
        data = res.json()
        result = []
        for i in data:
            if i['retweet_count'] > 0:
                result.append({
                        'created_at':i['created_at'],
                        'author':i['user']['name'],
                        'text':i['text'],
                        'retweet_count': i['retweet_count']
                    })
        cls.assertEquals(tweets, result, msg, msg_success)

    # Lab 8.1 Ex. 3
    @classmethod
    def twitterHashtagsTweets(cls, tweets, url, msg="", msg_success=""):
        if url != 'https://stream.twitter.com/1.1/statuses/filter.json?track=twitter,tweet,world':
            cls.assertEquals(True, False, 'Incorrect URL', '')
            return
        if not isinstance(tweets, list):
            cls.assertEquals(True, False, 'Incorrect data type', '')
            return
        if isinstance(tweets, list) and len(tweets) != 5:
            cls.assertEquals(True, False, 'Incorrect content', '')
            return
        if isinstance(tweets, list) and len(tweets) == 5 and False in map(lambda x: isinstance(x, list), tweets):
            cls.assertEquals(True, False, 'Incorrect content', '')
            return
        i = 0
        while True:
            try:
                x = tweets[0][i]['created_at']
                break
            except:
                i += 1
        i = -1
        while True:
            try:
                y = tweets[4][i]['created_at']
                break
            except:
                i -= 1
        diff = parser.parse(y).minute*60 + parser.parse(y).second - (parser.parse(x).minute*60 + parser.parse(x).second)
        cls.assertEquals(0 < diff <= 301, True, msg, msg_success)

    # Lab 8.1 Ex. 3
    @classmethod
    def twitterHashtagsTweetsCount(cls, amount_list, tweets, url, msg="", msg_success=""):
        if url != 'https://stream.twitter.com/1.1/statuses/filter.json?track=twitter,tweet,world':
            cls.assertEquals(True, False, 'Incorrect URL', '')
            return
        try:
            x = []
            for group in tweets:
                c = 0
                for i in group:
                    if ('lang' in i and i['lang'] == 'en') or ('user' in i and i['user']['followers_count'] > 1000):
                        c += 1
                x.append(c)
            cls.assertEquals(x, amount_list, msg, msg_success)
        except:
            cls.assertEquals(False, True, msg, msg_success)

    # Lab 8.1 Ex. 4
    @classmethod
    def twitterBillGates(cls, data, api, msg="", msg_success=""):
        BillGates = api.get_user("BillGates")
        result = {'created_at': BillGates.created_at, 'last_tweet_text': api.home_timeline(BillGates.id)[0].text}
        cls.assertEquals(data, result, msg, msg_success)

    # Lab 8.2 Ex. 5.1
    @classmethod
    def existCollections(cls, client, msg="", msg_success=""):
        cls.assertEquals(True, 'users' in client.twitter.collection_names() and 'tweets' in client.twitter.collection_names(), msg, msg_success)

    # Lab 8.2 Ex. 5.2
    @classmethod
    def countRecord(cls, data, client, msg="", msg_success=""):
        result = client.twitter.tweets.count()
        cls.assertEquals(2500, result, msg, msg_success)

    # Lab 8.2 Ex. 5.3
    @classmethod
    def existField(cls, data, client, msg="", msg_success=""):
        q_t = {
            "created_at": {"$exists": True},
            "author_id": {"$exists": True},
            "author_name": {"$exists": True},
            "retweet_count": {"$exists": True},
            "id": {"$exists": True},
            "lang": {"$exists": True},
            "source": {"$exists": True},
            "text": {"$exists": True}
        }
        q_u = {
            "created_at": {"$exists": True},
            "id": {"$exists": True},
            "name": {"$exists": True},
            "description": {"$exists": True},
            "followers_count": {"$exists": True},
            "friends_count": {"$exists": True},
            "lang": {"$exists": True},
            "profile_image_url": {"$exists": True},
            "location": {"$exists": True},
            "time_zone": {"$exists": True},
            "tweets": {"$exists": True}
        }
        result = client.twitter.tweets.count() == client.twitter.tweets.count(q_t) \
                 and client.twitter.users.count() == client.twitter.users.count(q_u)
        if result:
            for i in client.twitter.users.find():
                if i['tweets'] != cls._tweets_ids(i['id'], client.twitter.tweets):
                    result = False
                    break
        cls.assertEquals(True, result, msg, msg_success)

    @classmethod
    def _tweets_ids(cls, author_id, collection):
        return list( set( list(collection.aggregate([
            {"$match": {"author_id":author_id }},
            {"$group": {"_id": {"author_id": "$author_id"}, "ids": {"$push": "$id"}} },
            {"$project": {"ids": 1}}
        ]))[0]['ids'] ) )

    # Lab 8.2 Ex. 5.4
    @classmethod
    def bigDataTweets(cls, client, msg="", msg_success=""):
        td = timedelta(minutes=60)
        start = list(client.twitter.tweets.aggregate([
                     {"$sort": {"created_at": 1} }, {"$limit": 1}, {"$project": {"created_at": 1} }
                ]))[0]['created_at']
        end = list(client.twitter.tweets.aggregate([
                     {"$sort": {"created_at": -1} }, {"$limit": 1}, {"$project": {"created_at": 1} }
                ]))[0]['created_at']
        new_col = list(client.twitter.tweets.aggregate([{
                        "$match":{
                            "text": {"$regex": "#BigData"},
                            "retweet_count":0,
                            "lang": "en",
                            "created_at": {"$gte": end-td}
                        }
                    }]))

        client.twitter['test000000'].insert_many(new_col)
        begin = list(client.twitter.test000000.aggregate([
                    {"$sort": {"created_at": 1} }, {"$limit": 1}, {"$project": {"created_at": 1} }
                ]))[0]['created_at']

        col_name = 'bigdata_tweets_' + begin.strftime("%Y_%m_%d_%H_%M_%S") + '_' + end.strftime("%Y_%m_%d_%H_%M_%S")
        client.twitter[col_name+'2'].insert_many(new_col)

        if col_name in client.twitter.collection_names():
            try:
                cls.assertEquals(True, client.twitter[col_name].count() == client.twitter[col_name+'2'].count(), msg, msg_success)
            except:
                cls.assertEquals(True, False, msg, msg_success)
        else:
            cls.assertEquals(True, False, msg, msg_success)

    # Lab 8.2 Ex. 5.5
    @classmethod
    def top5Tweets(cls, data, client, msg="", msg_success=""):
        result = {}
        for lang in client.twitter.tweets.find().distinct("lang"):
            query = [
                     {"$match": {"lang": lang} },
                     {"$group": {"_id": "$author_name",
                                 "author_name": {"$first": "$author_name"},
                                 "created_at": {"$first": "$created_at"},
                                 "retweet_count": {"$first": "$retweet_count"},
                                 "text": {"$first": "$text"},}},
                     {"$sort": {"retweet_count": -1, "author_name": 1} },
                     {"$limit": 5}
            ]
            result[lang] = []
            for i in client.twitter.tweets.aggregate(query):
                del(i['_id'])
                result[lang].append(i)
        cls.assertEquals(data, result, msg, msg_success)

    # Lab 8.2 Ex. 5.6
    @classmethod
    def timeZoneTweets(cls, data, client, msg="", msg_success=""):
        result = {}
        for i in client.twitter.users.aggregate([{"$group": {"_id": {"time_zone": "$time_zone"}}}]):
            tz = i['_id']['time_zone']
            if tz is not None:
                q = [
                     {"$match": {"time_zone": tz, "$or":[ {"lang": "en"}, {"lang": "es"}, {"lang": "fr"} ]} },
                     {"$project": {"name": 1, "profile_image_url": 1, "tweets": 1, "ff": {"$add":["$friends_count","$followers_count"]}} },
                     {"$sort": {"ff": -1} },
                     {"$limit": 1},
                     {"$project": {"name": 1, "profile_image_url": 1, "tweets": 1} }
                ]
                t = list(client.twitter.users.aggregate(q))
                if(len(t)):
                    del(t[0]['_id'])
                    t[0]['tweets'] = cls._getTweetsByIDS(t[0]['tweets'], client)
                    result[tz] = t[0]
        cls.assertEquals(data, result, msg, msg_success)

    @classmethod
    def _getTweetsByIDS(cls, ids, client):
        ids = list(set(ids))
        result = {}
        for i in list(client.twitter.tweets.aggregate([
                {"$match": {"id":{"$in":ids}}},
                {"$project": {'_id':-1,"id":1,"created_at":1,"text":1}}
            ])):
            del(i['_id'])
            t = i.copy()
            del(t['id'])
            result[i['id']] = t
        return result.values()

    # Lab 8.3 Ex. 1
    @classmethod
    def cassandraRating(cls, data, msg="", msg_success=""):
        correct = { # '(movie_id, person_id)': rating
            '(2, 1)': 4.87, '(2, 2)': 4.87, '(2, 3)': 4.87, '(1, 1)': 4.5, '(1, 2)': 4.5, '(1, 3)': 4.5
        }
        if len(data) < 6:
            cls.assertEquals(True, False, msg, msg_success)
            return
        for key, val in data.iteritems():
            if correct[key] != round(val, 2):
                cls.assertEquals(True, False, msg, msg_success)
                return
        cls.assertEquals(True, True, msg, msg_success)

    # Lab 8.3 Ex. 2
    @classmethod
    def cassandraTaxi(cls, data, msg="", msg_success=""):
        correct = {
            'movie_released': 1998,
            'movie_title': u'Taxi',
            'person_role': u'',
            'movie_duration_min': 86,
            'person_name': u'Samy Naceri',
            'movie_country': u'France',
            'rating': None,
            'person_born': 1961,
            'person_country': u'France'
        }
        exists = False
        for i in data:
            if i == correct:
                exists = True
                break
        cls.assertEquals(True, exists, msg, msg_success)

    # Lab 8.3 Ex. 4
    @classmethod
    def cassandraGarySinise(cls, data, msg="", msg_success=""):
        correct = {'Forrest Gump': 'Lieutenant Dan Taylor', 'The Green Mile': 'Burt Hammersmith'}
        yes = True
        for key, val in data.iteritems():
            try:
                if correct[key] != val:
                    yes = False
                    break
            except:
                cls.assertEquals(True, False, msg, msg_success)
                return
        cls.assertEquals(True, yes, msg, msg_success)

    @classmethod
    def checkLDAModel(cls, model, corpus, result, number):
        path_to_data = site.getsitepackages()[0]+"/test_helper/data/"
        load_dict = gensim.corpora.Dictionary.load(path_to_data + "ex3dict.txt")
        a = [i[1] for i in model.id2word.id2token.items()]
        b = [i[1] for i in load_dict.id2token.items()]
        cls.assertEquals(sorted(a),sorted(b),'Dictionary is incorrect', 'Exercise %d.1 is successful' %number)
        with open(path_to_data + 'ex3corpus.txt','r') as fobj:
            load_corpus = fobj.read();
        cls.assertEquals(str(corpus), load_corpus,'Corpus is incorrect', 'Exercise %d.2 is successful' % number)
        cls.assertEquals(model.passes, 20, "Passes value is incorrect", "Exercise %d.3 is successful" % number)
        tt = model.top_topics(corpus, 3)
        check = [[word[1] for word in [sub[0] for sub in tt][0]], [word[1] for word in [sub[0] for sub in tt][1]]]
        cls.assertEquals(result, check, "There is a mistake","Exercise %d.4 is successful" % number)

    @classmethod
    def checkDoc2Vec(cls,model, result, number):
        cls.assertEquals(model.window, 15, "window value is incorrect", "Exercise %d.1 is successful" % number )
        cls.assertEquals(model.min_count, 1,"min_count value is incorrect", "Exercise %d.2 is successful" % number)
        cls.assertEquals(model.sample, 1e-4, "sample value is incorrect", "Exercise %d.3 is successful" % number)
        cls.assertEquals(model.negative, 5, "negative value is incorrect", "Exercise %d.4 is successful" % number)
        cls.assertEquals(model.seed, 42, "seed value is incorrect", "Exercise %d.5 is successful" % number)
        cls.assertEquals([elem[0] for elem in model.most_similar('google')], result, "There is a mistake", "Exercise %d.6 is successful" % number)
