import dpkt
import socket
import pygeoip


gi = pygeoip.GeoIP('GeoLiteCity.dat')

def retKML(dest_ip, src_ip):
    if(src_ip == '10.0.2.15'): src_ip = '157.38.30.116'
    elif(dest_ip == '10.0.2.15'): dest_ip = '157.38.30.116'
    dest = gi.record_by_name(dest_ip)
    src = gi.record_by_name(src_ip)

    try:
        dest_long = dest['longitude']
        dest_lat = dest['latitude']
        src_long = src['longitude']
        src_lat = src['latitude']
        kml = (
        '<Placemark>\n'
        '<name>%s</name>\n'
        '<extrude>1</extrude>\n'
        '<styleUrl>#transBluePoly</styleUrl>\n'
        '<LineString>\n'
        '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
        '</LineString>\n'
        '</Placemark>\n'
        )%(dest_ip, dest_long, dest_lat, src_long, src_lat)
        return kml
    except:
        return ''



def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dest = socket.inet_ntoa(ip.dst)
            KML = retKML(dest,src)
            kmlPts += KML
        except:
            pass
    return kmlPts

def main():
    f = open('wire.pcap','rb')
    pcap = dpkt.pcap.Reader(f)
    kmlheader = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        '<Document>\n'
        '<Style id="yellowLineGreenPoly">\n'
        '<LineStyle>\n'
        '<width>1</width>\n'
        '<color>7f00ff00</color>\n'
        '</LineStyle>\n'
        '</Style>\n'
    )
    
    kmlfooter = (
        '</Document>\n'
        '</kml>\n'
        )

    kmldocument = kmlheader + plotIPs(pcap) + kmlfooter

    res = open("plot.kml", "a")
    res.write(kmldocument)
    res.close()
    f.close()

if __name__ == '__main__':
    main()
