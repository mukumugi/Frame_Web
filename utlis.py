import ccmapi.v0 as api
from ccmapi.v0.config import config as ccm_config

from config import env_config
import requests

ccm_config.api_url = env_config.ccm_api
session = requests.Session()

userid, cookie = api.account.login(env_config.username, env_config.pwd, session=session)

def create_frame(idx):
    dev_name = 'Frame_' + str(idx)
    p_id = api.project.create(dev_name, session=session)
    api.project.on(p_id, session=session)
    ido_id = api.deviceobject.create(p_id, 'PGSmartphone', ['PlayAck-O', 'Correct', 'Wrong', 'Name-I', 'Play-I', 'Acceleration'],session=session)
    odo_id = api.deviceobject.create(p_id, 'PortraitGuess', ['PlayAck-I', 'End', 'Forward', 'Name-O', 'Mode'],
                                     session=session)
    weather_id =api.deviceobject.create(p_id, 'Weather', ['Name-I'], session=session)

    api.networkapplication.create(p_id, [(ido_id, 'Acceleration'), (odo_id, 'Forward'), (odo_id, 'End')], session=session)
    api.networkapplication.create(p_id, [(ido_id, 'Correct'), (odo_id, 'End')], session=session)
    api.networkapplication.create(p_id, [(ido_id, 'Wrong'), (odo_id, 'Forward')], session=session)
    api.networkapplication.create(p_id, [(ido_id, 'Name-I'), (odo_id, 'Name-O')], session=session)
    api.networkapplication.create(p_id, [(ido_id, 'Play-I'), (odo_id, 'Mode')], session=session)
    api.networkapplication.create(p_id, [(ido_id, 'PlayAck-O'), (odo_id, 'PlayAck-I')], session=session)
    api.networkapplication.create(p_id, [(weather_id, 'Name-I'), (odo_id, 'Name-O')], session=session)

    return p_id, ido_id, odo_id, dev_name

def delete_frame(p_id):
    api.project.delete(p_id, session=session)

def bind_frame(p_id, do_id, d_id):
    api.device.bind(p_id, do_id, d_id, session=session)

def unbind_frame(p_id, do_id):
    api.device.unbind(p_id, do_id, session=session)