import datetime
import xml.etree.ElementTree as ET
import requests

# Link ng source EPG XML ng Pickleball TV (paltan batay sa gamit mong URL)
SOURCE_EPG_URL = "https://raw.githubusercontent.com/iptv-org/epg/master/sites/example.com.xml"

def fix_tba_epg():
    print("Fetching EPG data...")
    try:
        response = requests.get(SOURCE_EPG_URL, timeout=30)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            # Loop sa lahat ng program titles
            for programme in root.findall('programme'):
                for title in programme.findall('title'):
                    if not title.text or "to be announced" in title.text.lower() or "tba" in title.text.lower():
                        # Palitan ang TBA ng custom label
                        title.text = "Pickleball TV Live & Replays"
            
            tree = ET.ElementTree(root)
            tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
            print("EPG updated and saved successfully.")
            return
    except Exception as e:
        print(f"Error fetching EPG: {e}")

    # Fallback generator kapag walang ma-fetch
    print("Generating fallback EPG...")
    tv = ET.Element('tv')
    channel = ET.SubElement(tv, 'channel', id="PickleballTV.us")
    display_name = ET.SubElement(channel, 'display-name')
    display_name.text = "Pickleball TV"

    now = datetime.datetime.now(datetime.timezone.utc)
    for i in range(24):
        start_time = now + datetime.timedelta(hours=i*2)
        end_time = start_time + datetime.timedelta(hours=2)
        
        programme = ET.SubElement(tv, 'programme', {
            'start': start_time.strftime("%Y%m%m%H%M%S +0000"),
            'stop': end_time.strftime("%Y%m%m%H%M%S +0000"),
            'channel': "PickleballTV.us"
        })
        title = ET.SubElement(programme, 'title')
        title.text = "Pickleball TV 24/7 Coverage"

    tree = ET.ElementTree(tv)
    tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    fix_tba_epg()
