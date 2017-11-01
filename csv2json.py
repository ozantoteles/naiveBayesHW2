import csv, json

csvFile = open('data/tweets2.csv', 'r', encoding="utf8")

fieldNames = ("id","handle","text","is_retweet","original_author","time","in_reply_to_screen_name","in_reply_to_status_id","in_reply_to_user_id","is_quote_status","lang","retweet_count","favorite_count","longitude","latitude","place_id","place_full_name","place_name","place_type","place_country_code","place_country","place_contained_within","place_attributes","place_bounding_box","source_url","truncated","entities","extended_entities")

reader = csv.DictReader(csvFile, fieldNames)

for row in reader:
    items = list(row.items())
    jsonFileName = str(items[0][1])
    jsonFile = open('dumpKaggle/'+jsonFileName+'.json', 'w')
    json.dump(row, jsonFile)
    jsonFile.close()