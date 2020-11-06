import xml.etree.ElementTree as ET


def update_param(name, val, root):
    xpath = name.replace(".", "/")
    el = root.findall("./{}".format(xpath))
    if(len(el) == 1):
        el = el[0]
    else:
        el = el[1]
    #print("{}: {}, {}".format(name, el.text, el.get('units')))
    value = str(val)
    if value.find(':') == -1:
        el.text = value
    else:
        t, u, v = value.split(':')
        el.set('type', t)
        el.set('units', u)
        el.text = v

def params_to_xml(params, default_xml, xml_out):
    """
    
    :param params: input parameter values dictionary - key is parameter name, value is
    formatted string "type:units:val", or "val".
    """
    root = ET.parse(default_xml)
    for p in params:
        update_param(p, params[p], root)
    root.write(xml_out)

