#Requires AutoHotkey v2.0
if !A_IsAdmin {
    Run('*RunAs "' A_ScriptFullPath '"')
    ExitApp
}

; # == Win   ! == alt

Pause::PrintScreen
vk07::Send("#{PrintScreen}")
