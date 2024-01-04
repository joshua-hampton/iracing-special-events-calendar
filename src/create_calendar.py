from icalendar import Calendar, Event
import yaml
from datetime import datetime as dt
import pytz


def init_calendar(prodid):
    cal = Calendar()
    cal.add('prodid',prodid)
    cal.add('version', '2.0')
    cal.add('method','PUBLISH')
    return cal


def add_event(cal, event_dict):
    """
    event_dict - a dictionary with event info, where the key is the name of event property
    """
    event = Event()
    for k, v in event_dict.items():
        event.add(k, v)
    cal.add_component(event)


def write_calendar(cal, save_file):
    f = open(save_file, 'wb')
    f.write(cal.to_ical())
    f.close()


def read_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        race_event = yaml.safe_load(file)
    return race_event[0]["event"]


def create_event(race_event):
    uk_timezone = pytz.timezone('Europe/London')
    description = create_event_description(race_event)
    event_dict = {
        "uid": f"{race_event["name"].replace(" ","_")}_{int(dt.fromisoformat(race_event["start_date"]).timestamp())}",
        "dtstamp": dt.now().astimezone(uk_timezone),
        "dtstart": dt.fromisoformat(race_event["start_date"]),
        "dtend": dt.fromisoformat(race_event["end_date"]),
        "summary": race_event["name"],
        "location": race_event["location"].split("-")[0].strip() if race_event["location"] != None else "Unknown",
        "description": description,
        "sequence": race_event["iteration"],
    }
    return event_dict


def create_event_description(race_event):
    description = f"{race_event["text_description"]}"
    if race_event["split_times"] != [None] or race_event["cars"] != [None]:
        event_info_text = create_event_info(race_event)
        description += f"\n\n{event_info_text}"
    if race_event["location"] != None or race_event["sim_start_date"] != [None]:
        sim_info_text = create_sim_info(race_event)
        description += f"\n\n{sim_info_text}"
    if (race_event["warmup"] != None or race_event["qualifying"] != None or race_event["race_length"] != None or
        race_event["weather"] != None or race_event["sky"] != None or race_event["team_event"] != None or
        race_event["drive_through_limit"] != None):
        session_info_text = create_session_info(race_event)
        description += f"\n\n{session_info_text}"
    return description


def create_event_info(race_event):
    event_info_text = f"Event Information:\nDate: {dt.fromisoformat(race_event["start_date"]).strftime("%d %B")} - {dt.fromisoformat(race_event["end_date"]).strftime("%d %B")}"
    if race_event["split_times"] != [None]:
        event_info_text += "\nTime slots:"
        for t in race_event["split_times"]:
            event_info_text += f"\n  {t}"
    if race_event["cars"] != [None]:
        event_info_text += "\nCars:"
        if isinstance(race_event["cars"], list):
            for veh in race_event["cars"]:
                event_info_text += f"\n  {veh}"
        elif isinstance(race_event["cars"], dict):
            for cls,veh in race_event["cars"].items():
                event_info_text += f"\n  {cls}"
                if isinstance(veh, str) and veh != None:
                    event_info_text += f"\n    {veh}"
                elif isinstance(veh, list) and veh != [None]:
                    for i in veh:
                        event_info_text += f"\n    {i}"
    return event_info_text
    


def create_sim_info(race_event):
    sim_info_text = "Sim Information:"
    if race_event["location"] != None:
        sim_info_text += f"\nTrack: {race_event["location"]}"
    if race_event["sim_start_date"] != None:
        sim_info_text += f"\nSim Start Time: {dt.fromisoformat(race_event["sim_start_date"]).strftime("%A %d %B %Y, %H:%M")}"
    return sim_info_text


def create_session_info(race_event):
    session_info_text = "Session Information:"
    if race_event["warmup"] != None:
        session_info_text += f"\n Warmup: {race_event["warmup"]}"
    if race_event["qualifying"] != None:
        session_info_text += f"\n Qualifying: {race_event["qualifying"]}"
    if race_event["race_length"] != None:
        session_info_text += f"\n Race: {race_event["race_length"]}"
    if race_event["weather"] != None:
        session_info_text += f"\n Weather: {race_event["weather"]}"
    if race_event["sky"] != None:
        session_info_text += f"\n Sky: {race_event["sky"]}"
    if race_event["team_event"] != None:
        if isinstance(race_event["team_event"], bool):
            race_event["team_event"] = "yes" if race_event["team_event"] else "no"
        session_info_text += f"\n Team Event: {race_event["team_event"]}"
    if race_event["drive_through_limit"] != None:
        initial, recurring = race_event["drive_through_limit"].split(",")
        session_info_text += f"\n Drive Through Limit: {initial} incidents, then every {recurring} incidents."
    return session_info_text


def main(yaml_files, save_file):
    cal = init_calendar(f"-//JMRH//iracing//special_events v1.0//EN")
    for y in yaml_files:
        race_event = read_yaml(y)
        event_dict = create_event(race_event)
        add_event(cal, event_dict)
    write_calendar(cal, save_file)


if __name__ == "__main__":
    import sys
    save_file = sys.argv[1]
    yaml_files = sys.argv[2:]
    main(yaml_files, save_file)
