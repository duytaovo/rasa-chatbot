from typing import Any, Text, Dict,Union, List,Optional ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import re
from database.connect import get_database_connection
import pandas as pd
import logging
import json
from datetime import datetime
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction
)

from actions import config
from actions.api import community_events
from actions.api.algolia import AlgoliaAPI
from actions.api.discourse import DiscourseAPI
from actions.api.gdrive_service import GDriveService
from actions.api.mailchimp import MailChimpAPI
from actions.api.rasaxapi import RasaXAPI

USER_INTENT_OUT_OF_SCOPE = "out_of_scope"

logger = logging.getLogger(__name__)

INTENT_DESCRIPTION_MAPPING_PATH = "actions/intent_description_mapping.csv"
class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        camera = tracker.get_slot('camera')
        ram = tracker.get_slot('RAM')
        battery = tracker.get_slot('battery')

        dispatcher.utter_message(text='Here are your search results')
        dispatcher.utter_message(text='The features you entered: ' + str(camera) + ", " + str(ram) + ", " + str(battery))
        return []
########################


class ProductSearchForm(FormValidationAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "product_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('category') == 'phone':
            return ["ram","battery","camera","budget"]
        elif tracker.get_slot('category') == 'laptop':
            return ["ram","battery_backup","storage_capacity","budget"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"ram":[self.from_text()],
        "camera":[self.from_text()],
        "battery":[self.from_text()],
        "budget":[self.from_text()],
        "battery_backup":[self.from_text()],
        "storage_capacity":[self.from_text()]
        }


    def validate_battery_backup(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            battery_backup_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_backup_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_backup_int < 50:
            return {"battery_backup":battery_backup_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery_backup")

            return {"battery_backup":None}

    def validate_storage_capacity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            storage_capacity_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            storage_capacity_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if storage_capacity_int < 2000:
            return {"storage_capacity":storage_capacity_int}
        else:
            dispatcher.utter_message(template="utter_wrong_storage_capacity")

            return {"storage_capacity":None}

    def validate_ram(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            ram_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            ram_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if ram_int < 50:
            return {"ram":ram_int}
        else:
            dispatcher.utter_message(template="utter_wrong_ram")

            return {"ram":None}

    def validate_camera(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            camera_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            camera_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if camera_int < 150:
            return {"camera":camera_int}
        else:
            dispatcher.utter_message(template="utter_wrong_camera")

            return {"camera":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # i want the ram
        try:
            budget_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            budget_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if budget_int < 4000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(template="utter_wrong_budget")

            return {"budget":None}

    def validate_battery(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            battery_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_int < 8000:
            return {"battery":battery_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery")

            return {"battery":None}


    
    # USED FOR DOCS: do not rename without updating in docs
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot('category') == 'phone':
            dispatcher.utter_message(text="Please find your searched items here: Phones..")

        elif tracker.get_slot('category') == 'laptop':
            dispatcher.utter_message(text="Please find your searched items here: Laptops..")
        category = tracker.get_slot('category')
        #Open a database connection
        db = get_database_connection()
        ram = tracker.get_slot('ram')
        battery = tracker.get_slot('battery')
        battery_backup = tracker.get_slot('battery_backup')
        storage_capacity = tracker.get_slot('storage_capacity')
        camera = tracker.get_slot('camera')
        budget = tracker.get_slot('budget')

        #prepare a cursor object
        cursor = db.cursor()
        if category == 'phone':
            cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND back_camera_megapixel >= %s AND \
                battery_mah >= %s AND price_usd <= %s AND category= %s", [int(ram),\
                int(camera), int(battery), int(budget), 'phone'])
        elif category == 'laptop':
            cursor.execute("SELECT product_url FROM products WHERE ram >= %s AND storage >= %s AND \
                battery_backup >= %s AND price_usd <= %s AND category= %s", [int(ram),\
                int(storage_capacity), int(battery_backup), int(budget), 'laptop'])
        products = cursor.fetchall()
        if len(products) != 0:
            for x in products:
                dispatcher.utter_message(text=x[0])
        else:
            dispatcher.utter_message(text="Looks like there aren't any products that match your search.")       
        dispatcher.utter_message(template='utter_select_next')

        return [SlotSet('ram',None),SlotSet('camera',None),SlotSet('battery_backup',None),\
        SlotSet('battery',None),SlotSet('storage_capacity',None),SlotSet('budget',None)]

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_fallback")

        return []

class YourResidence(Action):

    def name(self) -> Text:
        return "action_your_residence"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        dispatcher.utter_message(template="utter_residence")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]
    

class ActionSearchResult(Action):

	def name(self) -> Text:
		return "action_search_results"

	def run(self, dispatcher: CollectingDispatcher,
	        tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

			category = tracker.get_slot('category')
			try:
				price = int(re.findall(r'[0-9]+',tracker.get_slot('price'))[0])
			except:
				price = 0
			try:
				ram = int(re.findall(r'[0-9]+',tracker.get_slot('ram'))[0])
			except:
				ram = 0
			try:
				camera = int(re.findall(r'[0-9]+',tracker.get_slot('camera'))[0])
			except:
				camera = 0
			df = pd.read_csv('/Users/voduytao/Documents/rasa-chatbot/actions/phones_laptops_database.csv')

			output = []
			output.append({'product_url': 'https://support.apple.com/library/content/dam/edam/applecare/images/en_US/iphone/iphone-14-pro-max-colors.png'})
			if category == 'phone':
				output = df[(df['category']=='phone') & (df['price_usd'] <= price) & (df['back_camera_megapixel'] >= camera)]
			elif category == 'laptop':
				output = df[(df['category']=='laptop') & (df['price_usd'] <= price) & (df['ram'] >= ram)]

			for url in output['product_url']:
				dispatcher.utter_message(image=url)

			return []  		 


# ----------------------------------------------------------------
# rasa-demo
class ActionSubmitSubscribeNewsletterForm(Action):
    def name(self) -> Text:
        return "action_submit_subscribe_newsletter_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        """Once we have an email, attempt to add it to the database"""

        email = tracker.get_slot("email")
        client = MailChimpAPI(config.mailchimp_api_key)
        subscription_status = client.subscribe_user(config.mailchimp_list, email)

        if subscription_status == "newly_subscribed":
            dispatcher.utter_message(template="utter_confirmationemail")
        elif subscription_status == "already_subscribed":
            dispatcher.utter_message(template="utter_already_subscribed")
        elif subscription_status == "error":
            dispatcher.utter_message(template="utter_could_not_subscribe")
        return []


class ValidateSubscribeNewsletterForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_subscribe_newsletter_form"

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if MailChimpAPI.is_valid_email(value):
            return {"email": value}
        else:
            dispatcher.utter_message(template="utter_no_email")
            return {"email": None}


class ActionSubmitSalesForm(Action):
    def name(self) -> Text:
        return "action_submit_sales_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        """Once we have all the information, attempt to add it to the
        Google Drive database"""

        import datetime

        budget = tracker.get_slot("budget")
        company = tracker.get_slot("company")
        email = tracker.get_slot("business_email")
        job_function = tracker.get_slot("job_function")
        person_name = tracker.get_slot("person_name")
        use_case = tracker.get_slot("use_case")
        date = datetime.datetime.now().strftime("%d/%m/%Y")

        sales_info = [company, use_case, budget, date, person_name, job_function, email]

        try:
            gdrive = GDriveService()
            gdrive.append_row(
                gdrive.SALES_SPREADSHEET_NAME, gdrive.SALES_WORKSHEET_NAME, sales_info
            )
            dispatcher.utter_message(template="utter_confirm_salesrequest")
            return []
        except Exception as e:
            logger.error(
                f"Failed to write data to gdocs. Error: {e.message}",
                exc_info=True,
            )
            dispatcher.utter_message(template="utter_salesrequest_failed")
            return []


class ValidateSalesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_sales_form"

    def validate_business_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if MailChimpAPI.is_valid_email(value):
            return {"business_email": value}
        else:
            dispatcher.utter_message(template="utter_no_email")
            return {"business_email": None}


class ActionExplainSalesForm(Action):
    """Returns the explanation for the sales form questions"""

    def name(self) -> Text:
        return "action_explain_sales_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        requested_slot = tracker.get_slot("requested_slot")

        sales_form_config = domain.get("forms", {}).get("sales_form", {})
        sales_form_required_slots = list(sales_form_config.keys())

        if requested_slot not in sales_form_required_slots:
            dispatcher.utter_message(
                template="Sorry, I didn't get that. Please rephrase or answer the question "
                "above."
            )
            return []

        dispatcher.utter_message(template=f"utter_explain_{requested_slot}")
        return []


class ActionExplainFaqs(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self) -> Text:
        return "action_explain_faq"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        topic = tracker.get_slot("faq")

        if topic in ["channels", "languages", "ee", "slots", "voice"]:
            dispatcher.utter_message(template=f"utter_faq_{topic}_more")
        else:
            dispatcher.utter_message(template="utter_no_further_info")

        return []


class ActionSetFaqSlot(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self) -> Text:
        return "action_set_faq_slot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        full_intent = (
            tracker.latest_message.get("response_selector", {})
            .get("faq", {})
            .get("full_retrieval_intent")
        )
        if full_intent:
            topic = full_intent.split("/")[1]
        else:
            topic = None

        return [SlotSet("faq", topic)]


class ActionPause(Action):
    """Pause the conversation"""

    def name(self) -> Text:
        return "action_pause"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        return [ConversationPaused()]


class ActionStoreUnknownProduct(Action):
    """Stores unknown tools people are migrating from in a slot"""

    def name(self) -> Text:
        return "action_store_unknown_product"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        # if we dont know the product the user is migrating from,
        # store their last message in a slot.
        return [SlotSet("unknown_product", tracker.latest_message.get("text"))]


class ActionStoreUnknownNluPart(Action):
    """Stores unknown parts of nlu which the user requests information on
    in slot.
    """

    def name(self) -> Text:
        return "action_store_unknown_nlu_part"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        # if we dont know the part of nlu the user wants information on,
        # store their last message in a slot.
        return [SlotSet("unknown_nlu_part", tracker.latest_message.get("text"))]


class ActionStoreBotLanguage(Action):
    """Takes the bot language and checks what pipelines can be used"""

    def name(self) -> Text:
        return "action_store_bot_language"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        spacy_languages = [
            "english",
            "french",
            "german",
            "spanish",
            "portuguese",
            "french",
            "italian",
            "dutch",
        ]
        language = tracker.get_slot("language")
        if not language:
            return [
                SlotSet("language", "that language"),
                SlotSet("can_use_spacy", False),
            ]

        if language.lower() in spacy_languages:
            return [SlotSet("can_use_spacy", True)]
        else:
            return [SlotSet("can_use_spacy", False)]


class ActionStoreEntityExtractor(Action):
    """Takes the entity which the user wants to extract and checks
    what pipelines can be used.
    """

    def name(self) -> Text:
        return "action_store_entity_extractor"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        spacy_entities = ["place", "date", "name", "organisation"]
        duckling = [
            "money",
            "duration",
            "distance",
            "ordinals",
            "time",
            "amount-of-money",
            "numbers",
        ]

        entity_to_extract = next(tracker.get_latest_entity_values("entity"), None)

        extractor = "CRFEntityExtractor"
        if entity_to_extract in spacy_entities:
            extractor = "SpacyEntityExtractor"
        elif entity_to_extract in duckling:
            extractor = "DucklingHTTPExtractor"

        return [SlotSet("entity_extractor", extractor)]


class ActionSetOnboarding(Action):
    """Sets the slot 'onboarding' to true/false dependent on whether the user
    has built a bot with rasa before"""

    def name(self) -> Text:
        return "action_set_onboarding"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        user_type = next(tracker.get_latest_entity_values("user_type"), None)
        is_new_user = intent == "how_to_get_started" and user_type == "new"
        if intent == "affirm" or is_new_user:
            return [SlotSet("onboarding", True)]
        elif intent == "deny":
            return [SlotSet("onboarding", False)]
        return []


class ActionSubmitSuggestionForm(Action):
    def name(self) -> Text:
        return "action_submit_suggestion_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        dispatcher.utter_message(template="utter_thank_suggestion")
        return []


class ActionStoreProblemDescription(Action):
    """Stores the problem description in a slot."""

    def name(self) -> Text:
        return "action_store_problem_description"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        problem = tracker.latest_message.get("text")
        timestamp = tracker.events[-1]["timestamp"]
        date = datetime.now().strftime("%d/%m/%Y")
        message_link = f"{config.rasa_x_host_schema}://{config.rasa_x_host}/conversations/{tracker.sender_id}/{timestamp}"
        row_values = [date, problem, message_link]

        gdrive = GDriveService()
        gdrive.append_row(
            gdrive.ISSUES_SPREADSHEET_NAME, gdrive.PLAYGROUND_WORKSHEET_NAME, row_values
        )

        return [SlotSet("problem_description", None)]


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self) -> Text:
        return "action_greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_message(response="utter_greet_name", name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_message(response="utter_greet_noname")
                return []
            else:
                dispatcher.utter_message(response="utter_greet")
                dispatcher.utter_message(response="utter_inform_privacypolicy")
                return [SlotSet("shown_privacy", True)]
        return []


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv(INTENT_DESCRIPTION_MAPPING_PATH)
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = intent_ranking[0].get(
                "confidence"
            ) - intent_ranking[1].get("confidence")
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]

        # for the intent name used to retrieve the button title, we either use
        # the name of the name of the "main" intent, or if it's an intent that triggers
        # the response selector, we use the full retrieval intent name so that we
        # can distinguish between the different sub intents
        first_intent_names = [
            intent.get("name", "")
            if intent.get("name", "") not in ["faq", "chitchat"]
            else tracker.latest_message.get("response_selector")
            .get(intent.get("name", ""))
            .get("ranking")[0]
            .get("intent_response_key")
            for intent in intent_ranking
        ]
        if "nlu_fallback" in first_intent_names:
            first_intent_names.remove("nlu_fallback")
        if "/out_of_scope" in first_intent_names:
            first_intent_names.remove("/out_of_scope")
        if "out_of_scope" in first_intent_names:
            first_intent_names.remove("out_of_scope")

        if len(first_intent_names) > 0:
            message_title = (
                "Sorry, I'm not sure I've understood you correctly 🤔 Do you mean..."
            )

            entities = tracker.latest_message.get("entities", [])
            entities = {e["entity"]: e["value"] for e in entities}

            entities_json = json.dumps(entities)

            buttons = []
            for intent in first_intent_names:
                button_title = self.get_button_title(intent, entities)
                if "/" in intent:
                    # here we use the button title as the payload as well, because you
                    # can't force a response selector sub intent, so we need NLU to parse
                    # that correctly
                    buttons.append({"title": button_title, "payload": button_title})
                else:
                    buttons.append(
                        {"title": button_title, "payload": f"/{intent}{entities_json}"}
                    )

            buttons.append({"title": "Something else", "payload": "/out_of_scope"})

            dispatcher.utter_message(text=message_title, buttons=buttons)
        else:
            message_title = (
                "Sorry, I'm not sure I've understood "
                "you correctly 🤔 Can you please rephrase?"
            )
            dispatcher.utter_message(text=message_title)

        return []

    def get_button_title(self, intent: Text, entities: Dict[Text, Text]) -> Text:
        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        return button_title.format(**entities)


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        # Fallback caused by TwoStageFallbackPolicy
        last_intent = tracker.latest_message["intent"]["name"]
        if last_intent in ["nlu_fallback", USER_INTENT_OUT_OF_SCOPE]:
            return [SlotSet("feedback_value", "negative")]

        # Fallback caused by Core
        else:
            dispatcher.utter_message(template="utter_default")
            return [UserUtteranceReverted()]


class ActionRestartWithButton(Action):
    def name(self) -> Text:
        return "action_restart_with_button"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        dispatcher.utter_message(template="utter_restart_with_button")


class ActionCommunityEvent(Action):
    """Utters Rasa community events."""

    def __init__(self) -> None:
        self.last_event_update = None
        self.events = None
        self.events = self._get_events()

    def name(self) -> Text:
        return "action_get_community_events"

    def _get_events(self) -> List[community_events.CommunityEvent]:
        if self.events is None or self._are_events_expired():
            logger.debug("Getting events from website.")
            self.last_event_update = datetime.now()
            self.events = community_events.get_community_events()

        return self.events

    def _are_events_expired(self) -> bool:
        # events are expired after 1 hour
        return (
            self.last_event_update is None
            or (datetime.now() - self.last_event_update).total_seconds() > 3600
        )

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        events = self._get_events()
        location = next(tracker.get_latest_entity_values("location"), None)
        events_for_location = None
        if location:
            location = location.title()
            events_for_location = [
                e
                for e in events
                if e.city.lower() == location.lower()
                or e.country.lower() == location.lower()
            ]

        if not events:
            dispatcher.utter_message(
                text="Looks like we don't have currently have any Rasa events planned."
            )
        else:
            self._utter_events(
                tracker, dispatcher, events, events_for_location, location
            )

        return []

    @staticmethod
    def _utter_events(
        tracker: Tracker,
        dispatcher: CollectingDispatcher,
        events: List,
        events_for_location: List,
        location: Text,
    ) -> None:

        text = tracker.latest_message.get("text") or ""
        only_next = True if "next" in text else False

        if location:
            if not events_for_location:
                header = (
                    f"Sorry, there are currently no events in {location}. \n\n"
                    "However, here are the upcoming Rasa events:"
                )
                if only_next:
                    header = (
                        f"Sorry, there are currently no events in {location}. \n\n"
                        "However, here is the next Rasa event:"
                    )

            else:
                events = events_for_location
                header = f"Here are the upcoming Rasa events in {location}:"
                if only_next:
                    header = f"Here is the next event in {location}:"

        else:
            header = "Here are the upcoming Rasa events:"
            if only_next:
                header = "Here is the next Rasa event:"

        if only_next:
            events = events[0:1]

        event_items = [f"- {e.name_as_link()} in {e.city}" for e in events]
        events = "\n".join(event_items)
        dispatcher.utter_message(
            text=f"{header} \n\n {events} \n\n We hope to see you there!"
        )


def get_last_event_for(tracker, event_type: Text, skip: int = 0) -> Optional[EventType]:
    skipped = 0
    for e in reversed(tracker.events):
        if e.get("event") == event_type:
            skipped += 1
            if skipped > skip:
                return e
    return None


class ActionDocsSearch(Action):
    def name(self):
        return "action_docs_search"

    def run(self, dispatcher, tracker, domain):
        docs_found = False
        search_text = tracker.latest_message.get("text")

        # Search of docs pages
        algolia_result = None
        algolia = AlgoliaAPI(
            config.algolia_app_id, config.algolia_search_key, config.algolia_docs_index
        )
        if search_text == "/technical_question{}":
            # If we're in a TwoStageFallback we need to look back one more user utterance
            # to get the actual text
            last_user_event = get_last_event_for(tracker, "user", skip=2)
            if last_user_event:
                search_text = last_user_event.get("text")
                algolia_result = algolia.search(search_text)
        else:
            algolia_result = algolia.search(search_text)

        if (
            algolia_result
            and algolia_result.get("hits")
            and len(algolia_result.get("hits")) > 0
        ):
            docs_found = True
            hits = [
                hit
                for hit in algolia_result.get("hits")
                if "Rasa X Changelog " not in hit.get("hierarchy", {}).values()
                and "Rasa Open Source Change Log "
                not in hit.get("hierarchy", {}).values()
            ]
            if not hits:
                hits = algolia_result.get("hits")
            doc_list = algolia.get_algolia_link(hits, 0)
            doc_list += (
                "\n" + algolia.get_algolia_link(hits, 1)
                if len(algolia_result.get("hits")) > 1
                else ""
            )

            dispatcher.utter_message(
                text="I can't answer your question directly, but I found the following from the docs:\n"
                + doc_list
            )

        else:
            dispatcher.utter_message(
                text=(
                    "I can't answer your question directly, and also "
                    "found nothing in our documentation that would help."
                )
            )

        return [SlotSet("docs_found", docs_found)]


class ActionForumSearch(Action):
    def name(self):
        return "action_forum_search"

    def run(self, dispatcher, tracker, domain):
        search_text = tracker.latest_message.get("text")
        # If we're in a TwoStageFallback we need to look back two more user utterance to get the actual text
        if search_text == "/technical_question{}" or search_text == "/deny":
            last_user_event = get_last_event_for(tracker, "user", skip=3)
            if last_user_event:
                search_text = last_user_event.get("text")
            else:
                dispatcher.utter_message(text="Sorry, I can't answer your question.")
                return []

        # Search forum
        discourse = DiscourseAPI("https://forum.rasa.com/search")
        disc_res = discourse.query(search_text)
        disc_res = disc_res.json()

        if disc_res and disc_res.get("topics") and len(disc_res.get("topics")) > 0:
            forum = discourse.get_discourse_links(disc_res.get("topics"), 0)
            forum += (
                "\n" + discourse.get_discourse_links(disc_res.get("topics"), 1)
                if len(disc_res.get("topics")) > 1
                else ""
            )

            dispatcher.utter_message(
                text=f"I found the following from our forum:\n{forum}"
            )
        else:
            dispatcher.utter_message(
                text=(
                    "I did not find any matching issues on our [forum](https://forum.rasa.com/):\n"
                    "I recommend you post your question there."
                )
            )

        return []


class ActionTagFeedback(Action):
    """Tag a conversation in Rasa X as positive or negative feedback"""

    def name(self):
        return "action_tag_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        feedback = tracker.get_slot("feedback_value")

        if feedback == "positive":
            label = '[{"value":"postive feedback","color":"76af3d"}]'
        elif feedback == "negative":
            label = '[{"value":"negative feedback","color":"ff0000"}]'
        else:
            return []

        rasax = RasaXAPI()
        rasax.tag_convo(tracker, label)

        return []


class ActionTagDocsSearch(Action):
    """Tag a conversation in Rasa X according to whether the docs search was helpful"""

    def name(self):
        return "action_tag_docs_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirm":
            label = '[{"value":"docs search helpful","color":"e5ff00"}]'
        elif intent == "deny":
            label = '[{"value":"docs search unhelpful","color":"eb8f34"}]'
        else:
            return []

        rasax = RasaXAPI()
        rasax.tag_convo(tracker, label)

        return []


class ActionTriggerResponseSelector(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self) -> Text:
        return "action_trigger_response_selector"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        retrieval_intent = tracker.get_slot("retrieval_intent")
        if retrieval_intent:
            dispatcher.utter_message(template=f"utter_{retrieval_intent}")

        return [SlotSet("retrieval_intent", None)]
