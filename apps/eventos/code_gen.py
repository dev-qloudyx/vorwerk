import secrets
import string
from .models import BBCode, Evento, Reward, StoreCode
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
    
    def generate_bb_code(request, code):
        # Define the length and characters to use for the BBCode
        code_length = 5
        characters = string.digits + string.ascii_uppercase

        # Check if the provided code exists in StoreCode table
        store_code = StoreCode.objects.filter(code=code).first()
        if store_code:
            # Check if there is already a corresponding BBCode for this StoreCode
            bb_code = BBCode.objects.filter(store_code=store_code).first()
            if bb_code and bb_code.user != request.user:
                return "BBCode already redeemed"
            else:
                # If there is no BBCode for this StoreCode, create a new unique BBCode
                new_code = None
                while not new_code:
                    code_suffix = ''.join(secrets.choice(characters.replace('0', '').replace('O', '').replace('o', '').replace('I', '').replace('l', '')) for i in range(code_length))
                    new_code = 'BB' + code_suffix
                    if BBCode.objects.filter(code=new_code).exists():
                        new_code = None
                
                # Create a new BBCode object for this StoreCode
                bb_code = BBCode(code=new_code, store_code=store_code, user=request.user)
                
                # Count BBCode objects
                count = BBCode.objects.count()

                # Set the 'valid' field based on the count of existing BBCode objects
                if  count <= 5000:
                    bb_code.valid = True
                
                # Save the BBCode object
                bb_code.save()
                
                # Mark the StoreCode as redeemed
                store_code.is_redeemed = True
                store_code.save()
                
                # Return a success message with the BBCode generated
                return bb_code.code
        else:
            # If the provided code doesn't exist in StoreCode table, return an error message
            return "Code not valid"


    def send_message(**kwargs):
        
        # get the data from the request object
        sender="Vorwerk"
        msisdn=kwargs['From']
        priority=50
        messageText=""
        workingDays=True
        isFlash=False
        mobileOperator=kwargs['mnc']
        
        
        # construct the payload for the API endpoint
        payload = {
            'username': 'Qloudyx',
            'password': 'qloudyx123',
            'partnerEventId':'',
            'timezone':'',
            'partnerMsgId':'',
            'sender': sender,
            'msisdn': msisdn,
            'mobileOperator':mobileOperator,
            'priority':priority,
            'expirationDatetime':'',
            'messageText':messageText,
            'scheduleDatetime':'',
            'beginTime':'',
            'endTime':'',
            'workingDays': workingDays,
            'isFlash': isFlash
        }

        headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': str(len(payload))
        }



        #Check if a message with the given Msg(BBCODE) already exists  
        #If it doesn't exist, save the message
        try:
            bb_code = BBCode.objects.get(code=kwargs['Msg'])
            if bb_code.valid:
               
                next_reward = Reward.objects.filter(is_redeemed=False).order_by('id').first()

                if next_reward:
                    next_reward.is_redeemed = True
                    next_reward.bbcode = bb_code
                    next_reward.user=bb_code.user
                    next_reward.save()

                # BBCode object with the given code exists and is valid
                link = 'https://diaabertobimby.bimby.pt/passatempo/'
                payload['messageText'] = f"O seu código foi confirmado com sucesso. Aceda à app em {link} para ver o seu prémio."
            else:
                # BBCode object with the given code exists but is invalid
                payload['messageText'] = "Infelizmente todos os prémios já foram atribuídos. Obrigada."
            #response = requests.post('https://apitest.usendit.pt/v2/remoteusendit.asmx', data=payload, headers=headers)
            response = requests.post('https://api.usendit.pt/v2/remoteusendit.asmx/SendMessage', data=payload, headers=headers)

            # If a BBCode object with the given code exists, return a 200 response with "OK" result
        except BBCode.DoesNotExist:
            # BBCode object with the given code doesn't exist
            payload['messageText'] = f"O código que enviou não está correto. Tente novamente."
            #response = requests.post('https://apitest.usendit.pt/v2/remoteusendit.asmx', data=payload, headers=headers)
            response = requests.post('https://api.usendit.pt/v2/remoteusendit.asmx/SendMessage', data=payload, headers=headers)
        
        return JsonResponse({
            'status_code': response.status_code,
            'content': response.content.decode()
        })
    

    ### NOT USED ###

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
    
    
    def test_reward(request, bb_code):
        bbcode = BBCode.objects.get(code=bb_code)
        last_reward = Reward.objects.last()
        if last_reward:
            last_reward_type = last_reward.reward_type
            reward_num = (int(last_reward_type[-1]) % 5) + 1
        else:
            reward_num = 1

        reward_type, _ = Reward.REWARD_CHOICES[reward_num - 1]

        reward = Reward.objects.create(bbcode=bbcode, reward_type=reward_type, user=bbcode.user)
        reward.save()
        return HttpResponse(reward.reward_type)


