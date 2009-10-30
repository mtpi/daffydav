#!/usr/bin/env python
# encoding: utf-8
"""
winnt.py

From pyftpdlib project
*WARNING*: untested
"""

import win32security, pywintypes, win32con

from daffydav.authenticators import Authenticator

class WinNtAuthenticator(Authenticator):
    
    def _validate(self):
        try:
            win32security.LogonUser(self.username, None, self.password,
                win32con.LOGON32_LOGON_INTERACTIVE,
                win32con.LOGON32_PROVIDER_DEFAULT)
            return True
        except pywintypes.error:
            return False
    
    def get_home_dir(self):
        """Return the user's profile directory."""
        import _winreg, win32api
        sid = win32security.ConvertSidToStringSid(
                win32security.LookupAccountName(None, self.username)[0])
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
              r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"+"\\"+sid)
        except WindowsError:
            raise ftpserver.AuthorizerError("No profile directory defined for %s "
                                            "user" %self.username)
        value = _winreg.QueryValueEx(key, "ProfileImagePath")[0]
        return win32api.ExpandEnvironmentStrings(value)
    
    def _impersonate_user(self):
        handler = win32security.LogonUser(self.username, None, self.password,
                      win32con.LOGON32_LOGON_INTERACTIVE,
                      win32con.LOGON32_PROVIDER_DEFAULT)
        win32security.ImpersonateLoggedOnUser(handler)
        handler.Close()

    def _terminate_impersonation(self):
        win32security.RevertToSelf()
