FieryPath_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FieryPath_OnTransition
	.byte 0

FieryPath_OnTransition:
	call_if_unset FLAG_GARBAGEFLAG, FieryPath_EventScript_MoveScottToFallarbor
	setflag FLAG_GARBAGEFLAG
	end

FieryPath_EventScript_MoveScottToFallarbor::
	setflag FLAG_GARBAGEFLAG
	clearflag FLAG_GARBAGEFLAG
	return

