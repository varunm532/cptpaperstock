from model.users import House

from __init__ import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
import pandas as pd

def initImages():
    with app.app_context():
        file_path = "imageData.csv"
        csvdict = pd.read_csv(file_path).set_index('ADDRESS')['IMAGE'].to_dict()

        houses = House.query.all()

        for house in houses:
            if house.address in csvdict:
                house.update(image=csvdict[house.address])
                db.session.commit()
            else:
                print(f"No image found for address: {house.address}")

def initHouses():
    with app.app_context():
        """Create database and tables"""
        print("Creating college tables")
        db.create_all()
        # Specify the file path
        file_path = "housesdata.csv"
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            try:
                # Extract the relevant data from each row
                price = float(row['PRICE']) if row['PRICE'] else 0
                beds = int(row['BEDS']) if row['BEDS'] else 0
                baths = int(row['BATHS']) if row['BATHS'] else 0
                address = row['ADDRESS']
                lat = row['LATITUDE']
                long = row['LONGITUDE']
                sqfeet = int(row['SQUARE FEET']) if row['SQUARE FEET'] else 0

                # Create a House instance and add it to the session
                try:
                    house = House(price, beds, baths, address, lat, long, sqfeet)
                    db.session.add(house)
                    db.session.commit()
                except:
                    continue
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate house, or error: {house.name}")
            except Exception as e_inner:
                print(f"Error adding house at index {index}: {str(e_inner)}")