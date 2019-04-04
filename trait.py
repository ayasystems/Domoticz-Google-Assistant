# -*- coding: utf-8 -*-

import requests

from config import (DOMOTICZ_URL, U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ, 
    groupDOMAIN, sceneDOMAIN, lightDOMAIN, switchDOMAIN, blindsDOMAIN, screenDOMAIN, climateDOMAIN, tempDOMAIN, lockDOMAIN,
    attribBRIGHTNESS, attribTHERMSTATSETPOINT)
       
PREFIX_TRAITS = 'action.devices.traits.'
TRAIT_ONOFF = PREFIX_TRAITS + 'OnOff'
TRAIT_DOCK = PREFIX_TRAITS + 'Dock'
TRAIT_STARTSTOP = PREFIX_TRAITS + 'StartStop'
TRAIT_BRIGHTNESS = PREFIX_TRAITS + 'Brightness'
TRAIT_COLOR_SPECTRUM = PREFIX_TRAITS + 'ColorSpectrum'
TRAIT_COLOR_TEMP = PREFIX_TRAITS + 'ColorTemperature'
TRAIT_SCENE = PREFIX_TRAITS + 'Scene'
TRAIT_TEMPERATURE_CONTROL = PREFIX_TRAITS + 'TemperatureControl'
TRAIT_TEMPERATURE_SETTING = PREFIX_TRAITS + 'TemperatureSetting'
TRAIT_LOCKUNLOCK = PREFIX_TRAITS + 'LockUnlock'
TRAIT_FANSPEED = PREFIX_TRAITS + 'FanSpeed'
TRAIT_MODES = PREFIX_TRAITS + 'Modes'
TRAIT_OPEN_CLOSE = PREFIX_TRAITS + 'OpenClose'

PREFIX_COMMANDS = 'action.devices.commands.'
COMMAND_ONOFF = PREFIX_COMMANDS + 'OnOff'
COMMAND_DOCK = PREFIX_COMMANDS + 'Dock'
COMMAND_STARTSTOP = PREFIX_COMMANDS + 'StartStop'
COMMAND_PAUSEUNPAUSE = PREFIX_COMMANDS + 'PauseUnpause'
COMMAND_BRIGHTNESS_ABSOLUTE = PREFIX_COMMANDS + 'BrightnessAbsolute'
COMMAND_COLOR_ABSOLUTE = PREFIX_COMMANDS + 'ColorAbsolute'
COMMAND_ACTIVATE_SCENE = PREFIX_COMMANDS + 'ActivateScene'
COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT = (
    PREFIX_COMMANDS + 'ThermostatTemperatureSetpoint')
COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE = (
    PREFIX_COMMANDS + 'ThermostatTemperatureSetRange')
COMMAND_THERMOSTAT_SET_MODE = PREFIX_COMMANDS + 'ThermostatSetMode'
COMMAND_LOCKUNLOCK = PREFIX_COMMANDS + 'LockUnlock'
COMMAND_FANSPEED = PREFIX_COMMANDS + 'SetFanSpeed'
COMMAND_MODES = PREFIX_COMMANDS + 'SetModes'
COMMAND_OPEN_CLOSE = PREFIX_COMMANDS + 'OpenClose'

TRAITS = []


def register_trait(trait):
    """Decorate a function to register a trait."""
    TRAITS.append(trait)
    return trait
    
def _google_temp_unit(units):
    """Return Google temperature unit."""
    if units == TEMP_FAHRENHEIT:
        return 'F'
    return 'C'
    
    
class _Trait:
    """Represents a Trait inside Google Assistant skill."""

    commands = []

    def __init__(self, state):
        """Initialize a trait for a state."""
        self.state = state

    def sync_attributes(self):
        """Return attributes for a sync request."""
        raise NotImplementedError

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        raise NotImplementedError

    def can_execute(self, command, params):
        """Test if command can be executed."""
        return command in self.commands

    async def execute(self, command, params):
        """Execute a trait command."""
        raise NotImplementedError


@register_trait
class OnOffTrait(_Trait):
    """Trait to offer basic on and off functionality.
    https://developers.google.com/actions/smarthome/traits/onoff
    """

    name = TRAIT_ONOFF
    commands = [
        COMMAND_ONOFF
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""

        return domain in (
            groupDOMAIN,
            switchDOMAIN,
            lightDOMAIN,
        )

    def sync_attributes(self):
        """Return OnOff attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return OnOff query attributes."""
        return {'on': self.state.state != "Off"}

    def execute(self, command, params):
        """Execute an OnOff command."""
        
        domain = self.state.domain
        
        if domain == groupDOMAIN:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchscene&idx=' + self.state.id + '&switchcmd=' + ('On' if params['on'] else 'Off')
        else:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + ('On' if params['on'] else 'Off')
        
        #print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        #print(r.status_code)
        # if r.status_code == 200:
            # pass
        
@register_trait
class SceneTrait(_Trait):
    """Trait to offer scene functionality.
    https://developers.google.com/actions/smarthome/traits/scene
    """

    name = TRAIT_SCENE
    commands = [
        COMMAND_ACTIVATE_SCENE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in sceneDOMAIN

    def sync_attributes(self):
        """Return scene attributes for a sync request."""
        # Neither supported domain can support sceneReversible
        return {}

    def query_attributes(self):
        """Return scene query attributes."""
        return {}

    def execute(self, command, params):
        """Execute a scene command."""
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchscene&idx=' + self.state.id + '&switchcmd=On'
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        # if r.status_code == 200:
            # pass

@register_trait
class BrightnessTrait(_Trait):
    """Trait to control brightness of a device.
    https://developers.google.com/actions/smarthome/traits/brightness
    """

    name = TRAIT_BRIGHTNESS
    commands = [
        COMMAND_BRIGHTNESS_ABSOLUTE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == lightDOMAIN:
            return features & attribBRIGHTNESS

        return False

    def sync_attributes(self):
        """Return brightness attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return brightness query attributes."""
        domain = self.state.domain
        response = {}

        if domain == lightDOMAIN:
            brightness = self.state.level
            response['brightness'] = brightness

        return response

    def execute(self, command, params):
        """Execute a brightness command."""
        #domain = self.state.domain
        
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(params['brightness'])
        #print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        #print(r.status_code)
        # if r.status_code == 200:
            # pass            
            
            
@register_trait
class OpenCloseTrait(_Trait):
    """Trait to offer open/close control functionality.
    https://github.com/actions-on-google/smart-home-nodejs/issues/253
    """

    name = TRAIT_OPEN_CLOSE
    commands = [
        COMMAND_OPEN_CLOSE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in (blindsDOMAIN,
                            screenDOMAIN)

    def sync_attributes(self):
        """Return scene attributes for a sync request."""
        # Neither supported domain can support sceneReversible
        return {}

    def query_attributes(self):
        """Return scene query attributes."""
        return {}

    def execute(self, command, params):
        """Execute a scene command."""

        p = params.get('openPercent', 50)
        
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd='
        
        if p == 100:
            #open
            url += 'Off'
        elif p == 0:
            #close
            url += 'On'
        else:
            #stop
            url += 'Stop'

        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))

        
@register_trait 
class TemperatureSettingTrait(_Trait):
    """Trait to offer handling both temperature point and modes functionality.

    https://developers.google.com/actions/smarthome/traits/temperaturesetting
    """

    name = TRAIT_TEMPERATURE_SETTING
    commands = [
        COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT,
        #COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE,
        COMMAND_THERMOSTAT_SET_MODE,
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == climateDOMAIN:
            return features & attribTHERMSTATSETPOINT
        else:    
            return domain in tempDOMAIN

    def sync_attributes(self):
        """Return temperature point and modes attributes for a sync request."""       
        
        return {'availableThermostatModes': 'off,heat,cool,on',
                'thermostatTemperatureUnit': 'C'}

    def query_attributes(self):
        """Return temperature point and modes query attributes."""
        domain = self.state.domain
        response = {}
        
        if domain == tempDOMAIN:
            response['thermostatMode'] = 'off'
            current_temp = self.state.temp
            if current_temp is not None:
                response['thermostatTemperatureAmbient'] = current_temp
            current_humidity = self.state.humidity
            if current_humidity is not None:
                response['thermostatHumidityAmbient'] = current_humidity
            
        if domain == climateDOMAIN:
            response['thermostatMode'] = 'heat'
            current_temp = self.state.state
            if current_temp is not None:
                response['thermostatTemperatureAmbient'] = float(current_temp)
            setpoint = self.state.setpoint
            if setpoint is not None:
                response['thermostatTemperatureSetpoint'] = float(setpoint)
            
        return response
        
    def execute(self, command, params):
        """Execute a temperature point or mode command."""
        # All sent in temperatures are always in Celsius
        if command == COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=setsetpoint&idx=' + self.state.id + '&setpoint=' + str(params['thermostatTemperatureSetpoint'])

        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        # print(r.status_code)
          
@register_trait
class LockUnlockTrait(_Trait):
    """Trait to lock or unlock a lock.
    https://developers.google.com/actions/smarthome/traits/lockunlock
    """

    name = TRAIT_LOCKUNLOCK
    commands = [
        COMMAND_LOCKUNLOCK
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain == lockDOMAIN

    def sync_attributes(self):
        """Return LockUnlock attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return LockUnlock query attributes."""
        return {'isLocked': self.state.state}

    def execute(self, command, params):
        """Execute an LockUnlock command."""
        
        if self.state.switchtype == 'Door Lock Inverted':
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + ('Off' if params['lock'] else 'On')
        else:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + ('On' if params['lock'] else 'Off')
        
        #print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        # print(r.status_code)