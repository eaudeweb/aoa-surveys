import json

def get_dict(obj):
	return dict(obj.__dict__)

def get_local(obj):
	return getattr(obj, '_local_properties', {})

def get_geo(geo):
	result = {}
	result['lat'] = str(getattr(geo, 'lat', None))
	result['lon'] = str(getattr(geo, 'lon', None))
	result['address'] = getattr(geo, 'address', None)
	return result

def get_file(file_obj):
	if not file_obj:
		return None

	result = {}
	result["url"] = "/" + "/".join(file_obj.filename[:-1]) + "/w_assessment-upload/index_html?as_attachment:int=1"
	result["title"] = file_obj.title
	return result

def get_json(obj):
	data = json.dumps(obj, indent=2)
	return data.decode('raw-unicode-escape').encode('utf-8')
