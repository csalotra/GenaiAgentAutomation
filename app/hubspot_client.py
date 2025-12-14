import os
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate

load_dotenv()

client = HubSpot(access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")) #Place your access token in the .env file

def create_or_update_contact(email: str, company: str = "" ) -> dict:
  """
  Create a hubspot contact
  """

  properties ={
    "email":email
  }

  if company:
        properties["company"] = company

  try:
    contact_input = SimplePublicObjectInputForCreate(
        properties=properties
    )

    response = client.crm.contacts.basic_api.create(
        simple_public_object_input_for_create=contact_input
    )

    return {
        "status": "created",
        "contact_id": response.id
    }

  except Exception as e:
      return {
          "status": "error",
          "error": str(e)
      }

   