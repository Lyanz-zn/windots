#Requires AutoHotkey v2.0

toggleState := false

!g:: {
    global toggleState
    toggleState := !toggleState
    if (toggleState) {
        Run('glazewm command wm-exit', , 'Hide')
        Run('thide show', , 'Hide')
    } else {
        Run('glazewm start', , 'Hide')
        Run('thide hide', , 'Hide')
    }
}
