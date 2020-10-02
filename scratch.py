"""

    Divide & Conquer
    WSU CPTS 451
    Spring 2020
    Milestone 2

"""

import json
import os
import psycopg2


def main():
    # Parsing JSON data and populating the database
    parse_business()
    parse_checkin()
    parse_tip()
    parse_user()

    # Loading application GUI


def clean_sql_string(string):
    return string.replace("'", "`").replace("\n", " ")


def parse_business():
    # Specifying file names
    json_file = "json data/yelp_business.JSON"
    output_file = "output/business.txt"

    # Creating folder to store output files if it doesn't already exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Opening JSON file
    with open(json_file, 'r') as f:
        out_file = open(output_file, 'w')
        line = f.readline()
        line_count = 0

        content = json.loads(line)
        headers = []

        for key in content:
            headers.append(key)

        headers.pop()
        out_file.write("Headers: {}\n\n".format(headers))

        # Connecting to database
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cpts451'")
        except:
            print("ERROR - Unable to connect to database.")

        cur = conn.cursor()

        # Reading and extracting data from each JSON object
        while line:
            # Extracting data from the current JSON object
            data = json.loads(line)

            business_id = data["business_id"]
            name = data["name"]
            address = data["address"]
            city = data["city"]
            state = data["state"]
            postal_code = data["postal_code"]
            latitude = str(data["latitude"])
            longitude = str(data["longitude"])
            stars = str(data["stars"])
            review_count = str(data["review_count"])
            is_open = str(data["is_open"])
            attributes = str(data["attributes"])
            categories = str(data["categories"].split(", "))

            # Inserting record into database
            sql_str = "INSERT INTO business(business_id, " \
                      "business_name, " \
                      "address, " \
                      "city, " \
                      "state_name, " \
                      "zip_code, " \
                      "latitude, " \
                      "longitude, " \
                      "business_avg_star, " \
                      "review_count, " \
                      "is_open, " \
                      "num_of_tips, " \
                      "num_of_checkins) " \
                      "VALUES('" + data['business_id'] + "', '" +\
                      clean_sql_string(data["name"]) + "', '" + \
                      clean_sql_string(data["address"]) + "', '" + \
                      clean_sql_string(data["city"]) + "', '" + \
                      clean_sql_string(data["state"]) + "', '" + \
                      str(int(data["postal_code"])) + "', " + \
                      str(data["latitude"]) + ", " + \
                      str(data["longitude"]) + ", " + \
                      str(data["stars"]) + ", " + \
                      str(data["review_count"]) + ", " + \
                      is_open + ", 0, 0);"

            try:
                cur.execute(sql_str)
            except:
                print("ERROR - Insert statement failed on business table.")

            conn.commit()

            # Writing parsed data to file
            out_file.write("Business:\t\t{}, {}\n".format(name, business_id))
            out_file.write("Location:\t\t{} {} {} {}, ({}, {})\n".format(address,
                                                                         city,
                                                                         state,
                                                                         postal_code,
                                                                         latitude,
                                                                         longitude))
            out_file.write("Reviews:\t\t{}, {}\n".format(stars, review_count))
            out_file.write("Open:\t\t\t{}\n".format(is_open))
            out_file.write("Attributes:\t\t{}\n".format(attributes))
            out_file.write("Categories:\t\t{}\n".format(categories))

            out_file.write('\n')

            # Reading next line and incrementing line counter
            line = f.readline()
            line_count += 1

    # Display number of records processed
    out_file.write("Processed {} records.".format(line_count))

    # Closing file
    out_file.close()
    f.close()

    # Printing results
    print("Processed: {}, Lines: {}, Output: {}".format(json_file, line_count, output_file))


def parse_checkin():
    # Specifying file names
    json_file = "json data/yelp_checkin.JSON"
    output_file = "output/checkin.txt"

    # Creating folder to store output files if it doesn't already exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Opening JSON file
    with open(json_file, 'r') as f:
        out_file = open(output_file, 'w')
        line = f.readline()
        line_count = 0

        content = json.loads(line)
        headers = []

        for key in content:
            headers.append(key)

        out_file.write("Headers: {}\n\n".format(headers))

        # Connecting to database
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cpts451'")
        except:
            print("ERROR - Unable to connect to database.")

        cur = conn.cursor()

        # Reading and extracting data from each JSON object
        while line:
            data = json.loads(line)
            out_file.write("Business:\t{}\n".format(data["business_id"]))
            out_file.write("Check-ins:\t")

            date = data["date"]
            current = ""
            split_dates = []
            tuples = []

            for char in date:
                if char != ",":
                    current += char
                else:
                    split_dates.append(current)
                    current = ""

            split_dates.append(current)

            for date in split_dates:
                year = date[0:4]
                month = date[5:7]
                day = date[8:10]
                time = date[11:19]

                tuples.append((year, month, day, time))

            # Inserting records into database and generating text output.
            for item in tuples:
                sql_str = "INSERT INTO yelpcheckin(business_id, " \
                          "checkin_year, " \
                          "checkin_month, " \
                          "checkin_day, " \
                          "checkin_time) " \
                          "VALUES('" + data['business_id'] + "', " + \
                          item[0] + ", " + \
                          item[1] + ", " + \
                          item[2] + ", '" + \
                          item[3] + "'" \
                          ");"

                try:
                    cur.execute(sql_str)
                except:
                    print("ERROR - Insert statement failed on checkin table.")

                conn.commit()

                out_file.write(str(item))

            out_file.write('\n\n')

            line = f.readline()
            line_count += 1

    # Display number of records processed
    out_file.write("Processed {} records.".format(line_count))

    # Closing file
    out_file.close()
    f.close()

    # Printing results
    print("Processed: {}, Lines: {}, Output: {}".format(json_file, line_count, output_file))


def parse_tip():
    # Specifying file names
    json_file = "json data/yelp_tip.JSON"
    output_file = "output/tip.txt"

    # Creating folder to store output files if it doesn't already exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Opening JSON file
    with open(json_file, 'r') as f:
        out_file = open(output_file, 'w')
        line = f.readline()
        line_count = 0

        content = json.loads(line)
        headers = []

        for key in content:
            headers.append(key)

        out_file.write("Headers: {}\n\n".format(headers))

        # Reading and extracting data from each JSON object
        while line:
            data = json.loads(line)
            business_id = data["business_id"]
            date = data["date"]
            likes = str(data["likes"])
            text = data["text"]
            user_id = data["user_id"]

            out_file.write("Business:\t\t{}\n".format(business_id))
            out_file.write("User:\t\t\t{}\n".format(user_id))
            out_file.write("Date & Likes:\t{}, {}\n".format(date, likes))
            out_file.write("Tip:\t\t\t{}\n".format(text))

            out_file.write('\n')

            line = f.readline()
            line_count += 1

    # Display number of records processed
    out_file.write("Processed {} records.".format(line_count))

    # Closing file
    out_file.close()
    f.close()

    # Printing results
    print("Processed: {}, Lines: {}, Output: {}".format(json_file, line_count, output_file))


def parse_user():
    # Specifying file names
    json_file = "json data/yelp_user.JSON"
    output_file = "output/user.txt"

    # Creating folder to store output files if it doesn't already exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Opening JSON file
    with open(json_file, 'r') as f:
        out_file = open(output_file, 'w')
        line = f.readline()
        line_count = 0

        content = json.loads(line)
        headers = []

        for key in content:
            headers.append(key)

        out_file.write("Headers: {}\n\n".format(headers))

        # Reading and extracting data from each JSON object
        while line:
            data = json.loads(line)
            average_stars = str(data["average_stars"])
            cool = str(data["cool"])
            fans = str(data["fans"])
            friends = str(data["friends"])
            funny = str(data["funny"])
            name = data["name"]
            tip_count = str(data["tipcount"])
            useful = str(data["useful"])
            user_id = data["user_id"]
            yelping_since = data["yelping_since"]

            out_file.write("User:\t\t\t{}, {}\n".format(name, user_id))
            out_file.write("Since:\t\t\t{}\n".format(yelping_since))
            out_file.write("Metrics:\t\t{}, {}, {}\n".format(average_stars, cool, funny))
            out_file.write("Tips & Useful:\t{}, {}\n".format(tip_count, useful))
            out_file.write("Fans & Friends:\t{}, {}\n".format(fans, friends))

            out_file.write('\n')

            line = f.readline()
            line_count += 1

    # Display number of records processed
    out_file.write("Processed {} records.".format(line_count))

    # Closing file
    out_file.close()
    f.close()

    # Printing results
    print("Processed: {}, Lines: {}, Output: {}".format(json_file, line_count, output_file))


if __name__ == "__main__":
    main()
