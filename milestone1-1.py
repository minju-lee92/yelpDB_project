"""

    Divide & Conquer
    WSU CPTS 451
    Spring 2020
    Milestone 1-1

"""

import json
import os


def main():
    parse_business()
    parse_checkin()
    parse_tip()
    parse_user()


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

            for item in tuples:
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
