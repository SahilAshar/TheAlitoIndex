#!/usr/bin/env python3

import asyncio, io, glob, os, sys, time, uuid, requests, csv
import argparse
from urllib.parse import urlparse
from urllib.request import urlretrieve
from urllib.error import HTTPError
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType


# Used in the Person Group Operations,  Snapshot Operations, and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = 'alito-group'
# Used for the Snapshot and Delete Person Group examples.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

DEBUG = False

def do_auth():
    # Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
    # This key will serve all examples in this document.
    KEY = 'your-key-here'

    # Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
    # This endpoint will be used in all examples in this quickstart.
    ENDPOINT = 'your-endpoint-here'

    # Create an authenticated FaceClient.
    return FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def delete_group(face_client):
    face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
    print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))

def create_group(face_client):
    ''' 
    Create the PersonGroup
    '''
    # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
    print('Person group:', PERSON_GROUP_ID)
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

def create_alito_group_person(face_client):
    # Define Alito Person Group Person object
    alito = face_client.person_group_person.create(PERSON_GROUP_ID, "Alito")

    alito_images = []

    for file in os.listdir("Alito"):
        if file.startswith("alito_"):
            alito_images.append(os.path.join("Alito", file))

    print(alito_images)

    # Add to a Alito person
    for image in alito_images:
        a = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, alito.person_id, a)
        print("added | " + image)

    ''' 
    Train PersonGroup
    '''
    print()
    print('Training the person group...')
    # Train the person group
    face_client.person_group.train(PERSON_GROUP_ID)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)

# ---------------


def write_congress_filenames(congress_num):
    with open('output/' + congress_num + '_filenames.csv', 'w', newline='') as csvfile:
        fieldnames = ['filename']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for file in os.listdir("congress/" + congress_num):
            if file.endswith(".jpg"):
                    writer.writerow({'filename': os.path.join("congress/" + congress_num, file)})
                    # test.append(os.path.join("Test", file))

def write_congress_confidence(congress_num, alito):
    with open('output/' + congress_num + '_filenames.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        with open('output/' + congress_num + '_confidence.csv', 'w', newline='') as csvfile:
            fieldnames = ['filename', 'face_id', 'confidence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for row in reader:
                image = open(row['filename'], 'r+b')
                faces = face_client.face.detect_with_stream(image)
                if len(faces) < 1:
                    continue
                confidence = face_client.face.verify_face_to_person(faces[0].face_id, alito.person_id, PERSON_GROUP_ID).confidence
                writer.writerow({'filename': row['filename'], 'face_id': faces[0].face_id, 'confidence': confidence})

def download_images(congress_num):

    # bioguide_id = ''
    # url = "https://theunitedstates.io/images/congress/450x550/" + bioguide_id + ".jpg"


    with open('data/' + congress_num + '_congress.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            bioguide_id = row['URL'][-7:]
            url = "https://theunitedstates.io/images/congress/450x550/" + bioguide_id + ".jpg"
            outfile = "congress/" + congress_num + "/" + bioguide_id + ".jpg"

            print(url)

            if os.path.isfile(outfile):
                print(" Image already exists:", outfile)
            else:
                try:
                    fn, info = urlretrieve(url, outfile)

                    if info["Content-Type"] != "image/jpeg":
                        os.unlink(fn)
                        raise HTTPError()
                    
                except HTTPError as e:
                    print("Image not available:", e)
                
                
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Scrape https://memberguide.gpo.gov and save "
                    "members' photos named after their Bioguide IDs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-n', '--congress', default='113',
        help="Congress session number, for example: 112, 113, 114, 115, P for Presidents, and J for SCOTUS Judges")
    parser.add_argument(
        '-d', '--download', default='n',
        help="y/n to download and update all images for all Congressional sessions.")

    args = parser.parse_args()

    face_client = do_auth()

    if DEBUG == True:
        delete_group(face_client)
        create_group(face_client)
        create_alito_group_person(face_client)
    elif DEBUG == False:
        alito = face_client.person_group_person.list(PERSON_GROUP_ID)[0]

    if args.download == 'y':
        congresses = ["110", "111", "112", "113", "114", "115"]
        
        for congress_num in congresses:
            download_images(congress_num)

    print()
    print()
    print("Starting Analysis for the " + args.congress + "th Congress.")

    write_congress_filenames(args.congress)
    
    print()
    print("Creating Facial Confidence Levels for the " + args.congress + "th Congress.")
    
    write_congress_confidence(args.congress, alito)

    print()
    print(args.congress+"th Congress Analysis Complete.")

    


        
