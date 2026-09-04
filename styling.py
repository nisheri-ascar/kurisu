PHASE_DONE = "🟢 Phase "
PHASE_ERROR = "🔴 Phase "
PHASE_INPROGRESS = "🔶 Phase "
b = "**"
st = "-# "

#phase_header_text("fail", 0, 3)
def phase_header_text(level_status, level_current, level_max):
	if level_status == "success":
		text = f"{b}{PHASE_DONE}{level_current}/{level_max}{b}"
	elif level_status == "fail":
		text = f"{b}{PHASE_ERROR}{level_current}/{level_max}{b}"
	elif level_status == "inprogress":
		text = f"{b}{PHASE_INPROGRESS}{level_current}/{level_max}{b}"
	else:
		text = "unknown"
	return text
