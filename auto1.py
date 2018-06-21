# import necessary modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from google.cloud import translate
from Seqmatch import similarity, apostrophe_checker
from html.parser import HTMLParser
from sys import exit
import os

# set global vars
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Avid_influence.json"
driver = webdriver
api_key = 'AIzaSyAdiQFUXy5Dgr4coKTWwWJllIM5oVRUruc'
signIn = 'sign-in-btn'
gotoUsername = 'top_login'
gotoPassword = 'top_password'
wrongChallenges = []
startpractice = 'Strengthen skills'
untimed = '_1pp2C'
timed = '_3XJPq'
translate_client = translate.Client()
h = HTMLParser()
targLang = ''
rerun = 'yes'


def isitRight():
        print( "Please correct it. Type Enter when done.")
        RightText = input("> ")
        loadResponse = driver.find_element_by_xpath('//*[@data-test="challenge-translate-input"]')
        loadResponse.clear()
        loadResponse.send_keys(RightText)
        return 'Corrected'


def welcome():
    print( "Welcome to the AutoDuolingo program!")
    sleep(1)
    print( "Lets get started, shall we?")
    sleep(1)
    print( "Launching page...")
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    chrome_options.add_argument('disable-infobars')
    driver = driver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get("https://www.duolingo.com")

def setup():
    username = input("Please type your username: ")
    password = input("And your password: ")
    clickLogin = driver.find_element_by_id(signIn)
    clickLogin.click()
    print( "Logging in...")
    uField = driver.find_element_by_id(gotoUsername)
    uField.clear()
    uField.send_keys(username)
    pField = driver.find_element_by_id(gotoPassword)
    pField.clear()
    pField.send_keys(password)
    driver.find_element_by_id('login-button').click()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "_6t5Uh")))

# detects the language functionality
def detect_my_language():
    print( "Autodetecting language...")
    sleep(1)
    detLang = driver.find_element_by_tag_name('h1')
    myLanguage = detLang.text
    languageFilter = ['Italian', 'French', 'German', 'Spanish']
    tgl = None
    for lang in languageFilter:
        if lang in myLanguage:
            tgl = lang
    print( "The program detected you are learning %s. Is this correct?" % tgl)
    langConfirm = input("Type 'yes' or 'no': > ")
    if langConfirm == 'yes':
        print( "Great!")
        tgl = tgl.lower()
    elif langConfirm == 'no':
        print( "What language are you learning?")
        tgl = input("> ")
        tgl = tgl.lower()
    set_target(tgl)


def set_target(tgl):
    global targLang
    if tgl == "italian":
        targLang = 'it'
    elif tgl == "french":
        targLang = 'fr'
    elif tgl == 'german':
        targLang = 'de'
    elif tgl == "spanish":
        targLang = 'es'


def skill_or_practice():
	print("Do you want to (A)strengthen skills or (B)practice a topic?")
	target = input("> ")
	if target.lower() == "a":
		driver.get('https://duolingo.com/practice')
		start_practice()
	elif target.lower() == "b":
		practice_topic()
	else:
		print("choose a valid option.")
		skill_or_practice()

def practice_topic():
    skills = driver.find_elements_by_css_selector('._3qO9M')

    list_of_skills = []
    for skill in skills:
    	list_of_skills.append(skill.text)

    desired_skill = input("Which skill would you like to learn? ")

    matching_skills = [skill for skill in list_of_skills if desired_skill in skill]

    if len(matching_skills) > 1:
    	print("Matching choices are: ")
    	for skill in matching_skills:
    		print(skill)
    	print("Which one do you choose? ")
    	chosen_skill = input()
    elif len(matching_skills) == 0:
    	print("Could not find a matching skill.")
    	exit()
    else:
    	chosen_skill = matching_skills[0]

    driver.find_element_by_partial_link_text(chosen_skill).click()
    sleep(1)
    driver.find_element_by_class_name('_3ntRm').click()


def start_practice():
    print( "Do you want to")
    print( "(a)Practice without a timer, or")
    print( "(b)Start timed practice")
    timedOrNot = input("> ")
    if timedOrNot == 'a':
        print( "Strengthening skills without timer...")
        withoutTimer = driver.find_element_by_class_name(untimed)
        withoutTimer.click()
    elif timedOrNot == 'b':
        print( "Strengthening skills with timer...")
        withTimer = driver.find_element_by_class_name(timed)
        withTimer.click()


def TranslateEngine():
    print("Type 'end' if at the end, or 'quit' to quit.")
    print("Else, just hit enter.")
    while True:
        try:
            sleep(1)
            header_text = driver.find_element_by_xpath('//*[@data-test="challenge-header"]').text
            if "Write this" in header_text:
                type_The_trans()
            elif "Type what you hear" in header_text:
                type_what_heard()
            elif "correct meaning" in header_text:
                mark_Cor_trans()
            elif "Select the missing word" in header_text:
                select_missing()
        except:
            finished_Lesson()
            break


def type_The_trans():
    query = []
    badResponse = ["Correct solution:", "used the wrong word", "plural", "instead of"]
    global wrongChallenges
    sText = driver.find_elements_by_xpath('//*[@data-test="hint-token"]')
    for q in sText:
        query.append(q.text)
    tText = ' '.join(query)
    setLang = translate_client.detect_language(tText)['language']
    sleep(1)
    if setLang == 'en':
        engToFor = translate_client.translate(tText, target_language=targLang)[
            'translatedText']
        engToFor = h.unescape(engToFor)
        try:
            loadResponse = driver.find_element_by_xpath('//*[@data-test="challenge-translate-input"]')
        except:
            driver.find_element_by_class_name('_2TNr1').click()
            loadResponse = driver.find_element_by_xpath('//*[@data-test="challenge-translate-input"]')
        loadResponse.send_keys(engToFor)
        if tText in wrongChallenges:
            print("This question was counted wrong before. Please type the correct answer.")
            wrongChallenges.remove(tText)
            isitRight()
        loadResponse.send_keys(Keys.ENTER)
        h2 = driver.find_element_by_tag_name('h2')
        for b in badResponse:
            if b in h2.text:
                wrongChallenges.append(tText)
    else:
        foreign_text = apostrophe_checker(query)
        tText = ' '.join(foreign_text)
        foreignToEng = translate_client.translate(tText, target_language='en')[
            'translatedText']
        foreignToEng = h.unescape(foreignToEng)
        try:
            loadResponse = driver.find_element_by_xpath('//*[@data-test="challenge-translate-input"]')
        except:
            driver.find_element_by_class_name('_2TNr1').click()
            loadResponse = driver.find_element_by_xpath('//*[@data-test="challenge-translate-input"]')
        loadResponse.send_keys(foreignToEng)
        if tText in wrongChallenges:
            print("This question was counted wrong before. Please type the correct answer.")
            wrongChallenges.remove(tText)
            isitRight()
        loadResponse.send_keys(Keys.ENTER)
        h2 = driver.find_element_by_tag_name('h2')
        for b in badResponse:
            if b in h2.text:
                wrongChallenges.append(tText)
    reset_wait_n_go()


def mark_Cor_trans():
    query = []
    initsentence = driver.find_element_by_class_name('KRKEd')
    text = initsentence.text
    translation = translate_client.translate(
        text, target_language=targLang)['translatedText']
    translation = h.unescape(translation)
    choices = driver.find_elements_by_xpath(
        '//*[@data-test="challenge-judge-options"]//li')
    for choice in choices:
        query.append(choice.text)
    correctedText = similarity(translation, query)
    tickboxes = driver.find_elements_by_xpath("//*[@data-test='challenge-judge-options']//label")
    for box in tickboxes:
        if correctedText in box.text:
            box.click()
    print( "I've selected: ")
    print( correctedText )
    print( "If there are more solutions, type it's box number.")
    print( "Otherwise, hit enter.")
    txtbox = input("> ")
    txtbox = [t for t in txtbox if t.isdigit()]
    for x in txtbox:
        tickbox = driver.find_element_by_xpath("//*[@data-test='challenge-judge-options']//li[{}]/label/div[2]".format(x))
        tickbox.click()
    reset_wait_n_go()
    reset_wait_n_go()


def type_what_heard():
    print( "Please type your answer here! Type replay to replay.")
    answer = input("> ")
    while 'replay' in answer:
        slowOrNorm = input("(1) Normal or (2) Slow? ")
        if slowOrNorm == '1':
            replay = driver.find_element_by_class_name('_3Knei')
            replay.click()
        elif slowOrNorm == '2':
            replay = driver.find_element_by_class_name('_jK6-')
            replay.click()
        answer = input("> ")
    loadResponse = driver.find_element_by_xpath("//*[@data-test='challenge-listentap-input']")
    loadResponse.send_keys(answer)
    loadResponse.send_keys(Keys.ENTER)
    reset_wait_n_go()


def select_missing():
    all_words = driver.find_elements_by_xpath("//*[@data-test='challenge-select']")
    wordbank = []
    for word in all_words:
        wordbank.append(word.text)
    words = [w[2:] for w in wordbank]
    numbers = [w[0] + "] " for w in wordbank] 
    print( "Your choices are: ")
    stack = list(zip(numbers, words))
    for s in stack:
        print( s[0], s[1])
    number_choice = input("Which do you choose? ")
    for word in all_words:
        if number_choice in word.text:
            word.click()
    reset_wait_n_go()
    reset_wait_n_go()


def reset_wait_n_go():
    next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@data-test='player-next']"))
        )
    next_button = driver.find_element_by_xpath("//*[@data-test='player-next']")
    next_button.click()


def finished_Lesson():
    print( "We made it! Yay!")
    print( "Loading home page...")
    sleep(3)
    try:
        while True:
            cont = driver.find_element_by_xpath("//*[@data-test='player-next']")
            cont.click()
    except:
        driver.get("https://duolingo.com")


# Commands listed here.
if __name__ == "__main__":
	welcome()
	setup()
	while (rerun == 'yes'):
	    try:
	        detect_my_language()
	        skill_or_practice()
	        TranslateEngine()
	        rerun = input("Run again? Type yes or no: ")
	    except Exception as e:
	        raise e
	        break
	print( "Closing down the window...")
	sleep(1)
	driver.quit()
