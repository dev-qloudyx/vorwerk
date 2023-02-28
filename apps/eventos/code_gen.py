import secrets
import string
from .models import BBCode, Evento, StoreCode
from django.http import HttpResponse
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
import requests
import random
from django.contrib import messages

# Code Generation logic 
class CodeGeneration:
    
    def generate_store_codes(request, num_codes, eventid):

        try:
            evento = Evento.objects.get(id=eventid)
        except:
            return HttpResponse(f"Evento {eventid} não existe")
        # Set the length and characters to use for the codes
        code_length = 5
        characters = string.digits + string.ascii_uppercase
        
        # Use a set to store unique codes
        codes = set()
        batch_size = 100
        # Generate codes in batches and try to save them to the database
        while len(codes) < num_codes:
            batch = []
            while len(batch) < batch_size:
                # .replace -> Avoids characters that could be easily confused with others.
                code = ''.join(secrets.choice(characters.replace('0', '').replace('O', '').replace('o', '').replace('I', '').replace('l', '')) for i in range(code_length))
                if any(c.isalpha() for c in code) and not all(c.isdigit() for c in code):
                    batch.append(code)

            # Try to save the batch to the database
            try:
                # is a list comprehension that creates a list of StoreCode instances, with each instance's code attribute set to a value from the batch list.
                StoreCode.objects.bulk_create([StoreCode(code=code, event=evento) for code in batch])
                # If the batch is saved successfully, add the codes to the set
                codes.update(batch)
            except IntegrityError:
                # If there's an IntegrityError, it means there's at least one
                # duplicate code in the batch, so ignore it and move on to the next
                # like a raise because of unique constrain
                pass

        # Return a response indicating that 100.000 unique codes were generated
        return num_codes

    def list_duplicate_store_codes(request):
        # Double Check
        # Query the database for all StoreCodes that appear more than once
        duplicates = StoreCode.objects.values('code').annotate(count=Count('id')).filter(count__gt=1)
        # Extract the code values from the queryset
        codes = [d['code'] for d in duplicates]
        # Return the list of duplicate codes as a JSON response
        return JsonResponse({'codes': codes})

    def generate_bb_code(request, code):
        # Define the length and characters to use for the BBCode
        code_length = 5
        characters = string.digits + string.ascii_uppercase
        
        # Check if the provided code exists in StoreCode table
        store_code = StoreCode.objects.filter(code=code).first()
        if store_code:
            # Check if there is already a corresponding BBCode for this StoreCode
            bb_code = BBCode.objects.filter(store_code=store_code).first()
            if bb_code:
                # If there is already a BBCode for this StoreCode, return it
                return "BBCode already exists for this StoreCode: {}".format(bb_code.code)
            else:
                # If there is no BBCode for this StoreCode, create a new unique BBCode
                new_code = None
                while not new_code:
                    code_suffix = ''.join(secrets.choice(characters.replace('0', '').replace('O', '').replace('o', '').replace('I', '').replace('l', '')) for i in range(code_length))
                    new_code = 'BB' + code_suffix
                    if BBCode.objects.filter(code=new_code).exists():
                        new_code = None
                
                # Create a new BBCode object for this StoreCode
                bb_code = BBCode.objects.create(code=new_code, store_code=store_code, user=request.user)
                # Mark the StoreCode as redeemed
                store_code.is_redeemed = True
                store_code.save()
                # Return a success message with the BBCode generated
                return "Generated BBCode: {}".format(bb_code.code)
        else:
            # If the provided code doesn't exist in StoreCode table, return an error message
            return "Code not valid"

    def select_codes(request, num_codes, eventid):
        
        #Instantiate event
        event = Evento.objects.get(id=eventid)

        # Get the code pool of un-redeemed and unpicked codes
        code_pool = StoreCode.objects.filter(event=event, is_redeemed=False, picked=False)
        
        # Check if the requested number of codes is greater than the code pool size
        if num_codes > len(code_pool):
            messages.error(request,f'Somente {code_pool.count()} códigos disponíveis... Favor gerar mais códigos...')
            return None, code_pool  # or return an error message
            
        # Check if the requested number of codes is negative
        if num_codes <= 0:
            messages.error(request,f'Somente {code_pool.count()} códigos disponíveis... Favor gerar mais códigos...')
            return None, code_pool  # or return an error message
        
        # Select the specified number of codes from the code pool
        selected_codes = random.sample(list(code_pool), num_codes)
        
        # Update the selected codes to mark them as picked
        for code in selected_codes:
            code.picked = True
            code.save()

        return selected_codes

    def send_message(request,**kwargs):
    # get the data from the request object
        sender=""
        msisdn=""
        priority=1
        messageText=""
        workingDays="g"
        isFlash=""

        # construct the payload for the API endpoint
        payload = {
            'username': "Qloudyx",
            'password': "Sendit123*",
            'sender': sender,
            'msisdn': msisdn,
            'priority':priority,
            'messageText':messageText,
            'workingDays': workingDays,
            'isFlash': isFlash
            # and so on for other parameters
        }

        #Check if a message with the given Msg(BBCODE) already exists  
        #If it doesn't exist, save the message
        try:
            BBCode.objects.get(code=request.data.get('Msg'))
            # make a POST request to the API endpoint
            payload['messageText'] = "Código BB válido"
            response = requests.post('https://apitest.usendit.pt/v2/remoteusendit.asmx/SendMessage', data=payload)
            # If a BBCode object with the given code exists, return a 200 response with "OK" result
        except BBCode.DoesNotExist:
                # If a BBCode object with the given code doesn't exist, delete the message and return a 404 response with "NOK" result
            payload['messageText'] = "Código BB inválido"
            response = requests.post('https://apitest.usendit.pt/v2/remoteusendit.asmx/SendMessage', data=payload)

        return JsonResponse({
            'status_code': response.status_code,
            'content': response.content.decode()
        })
        