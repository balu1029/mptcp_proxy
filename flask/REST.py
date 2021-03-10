from flask import Flask, json, request
import dnspython as dns
import dns.resolver


resources = []
setting_temp={	"ip":"",
		"enable":"",
		"scheduler":"",
		"path_manager":""
	  }
file_path = "../res/mptcp_settings"
api = Flask(__name__)

@api.route('/resources', methods=['GET'])
def get_resources():
  resources.clear()
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    print(words[0])
    if words[0][0] != ".":
      setting = setting_temp.copy()
      setting["ip"] = words[0].strip()
      setting["enable"] = words[1].strip()
      setting["scheduler"] = words[2].strip()
      setting["path_manager"] = words[3].strip()
      resources.append(setting)
  return json.dumps(resources)
  
@api.route('/resources', methods=['POST'])
def post_resource():
  double = False
  req = request.get_json()
  resources.clear()
  result = dns.resolver.resolve(req["ip"].strip(), 'A')
  
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    print(words[0])
    if words[0][0] != ".":
      for ipval in result:
        if words[0].strip() == ipval.to_text():
          double = True
      setting = setting_temp.copy()
      setting["ip"] = words[0].strip()
      setting["enable"] = words[1].strip()
      setting["scheduler"] = words[2].strip()
      setting["path_manager"] = words[3].strip()
      resources.append(setting)
  if not double:
    for ipval in result:
      settings = setting_temp.copy()
      settings = request.get_json()
      settings["ip"] = ipval.to_text()
      resources.append(settings)
  file.close()
  
  file = open(file_path, "w")
  for res in resources:
    file.write(res["ip"] + "," + res["enable"] + "," + res["scheduler"] + "," + res["path_manager"] + "\n")
  file.write(".")
  file.close()
  return json.dumps(resources)

@api.route('/resources/<ip>', methods=['DELETE'])
def delete_resource(ip):
  resources.clear()
  file = open(file_path, "r")
  for line in file:
    words = line.split(",")
    if words[0][0] != ".":
      if words[0].strip() != ip:
        print("in")
        setting = setting_temp.copy()
        setting["ip"] = words[0].strip()
        setting["enable"] = words[1].strip()
        setting["scheduler"] = words[2].strip()
        setting["path_manager"] = words[3].strip()
        resources.append(setting)
  file.close()
  
  file = open(file_path, "w")
  for res in resources:
    file.write(res["ip"] + "," + res["enable"] + "," + res["scheduler"] + "," + res["path_manager"] + "\n")
  file.write(".")
  file.close()
  return json.dumps(resources)

if __name__ == '__main__':
    api.run(host="192.168.2.115")
