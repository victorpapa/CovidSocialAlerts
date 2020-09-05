import csv
import os

def generate_social_network_csv():
    txt_file_name = os.path.join(os.getcwd(), "..", "..", "res", "facebook_combined.txt")
    txt_file = open(txt_file_name, "r")
    csv_file_name = os.path.join(os.getcwd(), "..", "..", "res", "facebook_combined.csv")
    csv_file = open(csv_file_name, "w+")
    csv_writer = csv.writer(csv_file)

    for line in txt_file:
        words = line.split()
        csv_writer.writerow(words)

if __name__ == "__main__":
    generate_social_network_csv()
    
        
