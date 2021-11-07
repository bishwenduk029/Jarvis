import webbrowser
from os import environ
from re import search, sub

import requests
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError
from wolframalpha import Client
from wordninja import split as splitter

from peripherals.audio_input import listener
from peripherals.audio_output import say

think_id = environ.get('think_id')


def alpha(text: str) -> bool:
    """Uses wolfram alpha API to fetch results for uncategorized phrases heard.

    Args:
        text: Takes the voice recognized statement as argument.

    Raises:
        Broad ``Exception`` clause indicating that the Full Results API did not find an input parameter while parsing.

    Returns:
        bool:
        Boolean True if wolfram alpha API is unable to fetch consumable results.

    References:
        `Error 1000 <https://products.wolframalpha.com/show-steps-api/documentation/#:~:text=(Error%201000)>`__
    """
    if not think_id:
        return False
    alpha_client = Client(app_id=think_id)
    # noinspection PyBroadException
    try:
        res = alpha_client.query(text)
    except Exception:
        return True
    if res['@success'] == 'false':
        return True
    else:
        try:
            response = next(res.results).text.splitlines()[0]
            response = sub(r'(([0-9]+) \|)', '', response).replace(' |', ':').strip()
            if response == '(no data available)':
                return True
            say(text=response)
        except (StopIteration, AttributeError):
            return True


def google(query: str, suggestion_count: int = 0) -> bool:
    """Uses Google's search engine parser and gets the first result that shows up on a google search.

    Notes:
        - If it is unable to get the result, Jarvis sends a request to ``suggestqueries.google.com``
        - This is to rephrase the query and then looks up using the search engine parser once again.
        - ``suggestion_count`` is used to limit the number of times suggestions are used.
        - ``suggestion_count`` is also used to make sure the suggestions and parsing don't run on an infinite loop.
        - This happens when ``google`` gets the exact search as suggested ones which failed to fetch results earlier.

    Args:
        suggestion_count: Integer value that keeps incrementing when ``Jarvis`` looks up for suggestions.
        query: Takes the voice recognized statement as argument.

    Returns:
        bool:
        Boolean ``True`` if google search engine is unable to fetch consumable results.
    """
    search_engine = GoogleSearch()
    results = []
    try:
        google_results = search_engine.search(query, cache=False)
        a = {"Google": google_results}
        results = [result['titles'] for k, v in a.items() for result in v]
    except NoResultsOrTrafficError:
        suggest_url = "https://suggestqueries.google.com/complete/search"
        params = {
            "client": "firefox",
            "q": query,
        }
        response = requests.get(suggest_url, params)
        if not response:
            return True
        try:
            suggestion = response.json()[1][1]
            suggestion_count += 1
            if suggestion_count >= 3:  # avoids infinite suggestions over the same suggestion
                say(text=response.json()[1][0].replace('=', ''), run=True)  # picks the closest match for google search
                return False
            else:
                google(suggestion, suggestion_count)
        except IndexError:
            return True
    if results:
        [results.remove(result) for result in results if len(result.split()) < 3]  # removes results with dummy words
    else:
        return False
    if results:
        results = results[0:3]  # picks top 3 (first appeared on Google)
        results.sort(key=lambda x: len(x.split()), reverse=True)  # sorts in reverse by the word count of each sentence
        output = results[0]  # picks the top most result
        if '\n' in output:
            required = output.split('\n')
            modify = required[0].strip()
            split_val = ' '.join(splitter(modify.replace('.', 'rEpLaCInG')))
            sentence = split_val.replace(' rEpLaCInG ', '.')
            repeats = []
            [repeats.append(word) for word in sentence.split() if word not in repeats]
            refined = ' '.join(repeats)
            output = refined + required[1] + '.' + required[2]
        output = output.replace('\\', ' or ')
        match_word = search(r'(\w{3},|\w{3}) (\d,|\d|\d{2},|\d{2}) \d{4}', output)
        if match_word:
            output = output.replace(match_word.group(), '')
        output = output.replace('\\', ' or ')
        say(text=output, run=True)
        return False
    else:
        return True


def google_search(phrase: str = None) -> None:
    """Opens up a google search for the phrase received. If nothing was received, gets phrase from user.

    Args:
        phrase: Takes the phrase spoken as an argument.
    """
    phrase = phrase.split('for')[-1] if 'for' in phrase else None
    if not phrase:
        say(text="Please tell me the search phrase.", run=True)
        converted = listener(timeout=3, phrase_limit=5)
        if converted == 'SR_ERROR':
            return
        elif 'exit' in converted or 'quit' in converted or 'xzibit' in converted or 'cancel' in converted:
            return
        else:
            phrase = converted.lower()
    search_query = str(phrase).replace(' ', '+')
    unknown_url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(unknown_url)
    say(text=f"I've opened up a google search for: {phrase}.")
