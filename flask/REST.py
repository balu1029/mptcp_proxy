from flask import Flask, json, request
import dnspython as dns
import dns.resolver
import sys


resources = []                                          # list of settings 
setting_temp={	"ip":"",                                # template for storing a single setting
		"enable":"",
		"scheduler":"",
		"path_manager":""
	  }
file_path = "./res/mptcp_settings"                      # file path to settings file - script has to be startet from the root of the project folder
api = Flask(__name__)

@api.route('/resources', methods=['GET'])               # get method sends full list of settings to Client
def get_resources():
  resources.clear()
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    print(words[0])
    if words[0][0] != ".":
      setting = setting_temp.copy()                     # make a copy of the settings object and fil it with the values according to the file
      setting["ip"] = words[0].strip()
      setting["enable"] = words[1].strip()
      setting["scheduler"] = words[2].strip()
      setting["path_manager"] = words[3].strip()
      resources.append(setting)
  return json.dumps(resources)
  
@api.route('/resources', methods=['POST'])              # post method to add a new setting to the file - returns the current settings
def post_resource():
  double = False
  req = request.get_json()
  resources.clear()
  result = dns.resolver.resolve(req["ip"].strip(), 'A') # resolve the posted dns name to a (or many) ip-addresses
  
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    print(words[0])
    if words[0][0] != ".":
      for ipval in result:
        if words[0].strip() == ipval.to_text():         # check if setting already exists
          double = True
      setting = setting_temp.copy()
      setting["ip"] = words[0].strip()
      setting["enable"] = words[1].strip()
      setting["scheduler"] = words[2].strip()
      setting["path_manager"] = words[3].strip()
      resources.append(setting)
  if not double:                                        # if setting doesnt already exist, append posted values
    for ipval in result:
      settings = setting_temp.copy()
      settings = request.get_json()
      settings["ip"] = ipval.to_text()
      resources.append(settings)
  file.close()
  
  file = open(file_path, "w")
  for res in resources:                                  # write all values back to the file
    file.write(res["ip"] + "," + res["enable"] + "," + res["scheduler"] + "," + res["path_manager"] + "\n")
  file.write(".")
  file.close()
  return json.dumps(resources)

@api.route('/resources/<ip>', methods=['DELETE'])        # delete method for deleting a single setting indexed by its ip-address
def delete_resource(ip):
  resources.clear()
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    if words[0][0] != ".":
      if words[0].strip() != ip:                         # get all values but the value with the given ip
        setting = setting_temp.copy()
        setting["ip"] = words[0].strip()
        setting["enable"] = words[1].strip()
        setting["scheduler"] = words[2].strip()
        setting["path_manager"] = words[3].strip()
        resources.append(setting)
  file.close()
  
  file = open(file_path, "w")
  for res in resources:                                   # write these values back to the file
    file.write(res["ip"] + "," + res["enable"] + "," + res["scheduler"] + "," + res["path_manager"] + "\n")
  file.write(".")
  file.close()
  return json.dumps(resources)

if __name__ == '__main__':
    if len(sys.argv) > 1:                                 # if an argument is given, run the server on this ip-address
      api.run(host=sys.argv[1])
    else:                                                 # if no argument given, run the server on localhost
      api.run()
