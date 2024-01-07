from pyosint.core.constants.headers import UA
import requests

data = None

# web text -> links
# URL = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ru&source=gcsc&gss=.ru&cselibv=3bd4ac03c21554b3&cx=partner-pub-5723066625223773%3A1728805441&q=Cyberpunk+2077&safe=active&cse_tok=AB-tC_6JQ3ovdKWxGDoKDfxyzcsb%3A1703972207599&exp=csqr%2Ccc%2Capo&callback=google.search.cse.api10509"

# web text -> videos links
# URL = "https://getyarn.io/yarn-find?text=clown"

# web domain
# URL = "https://intodns.com/check/?domain=yadro.com"

# web domain
# URL = "https://columbus.elmasy.com/report/intel.com"

# web domain
# URL = "https://www.nslookup.io/api/v1/records"
# data = {"domain":"yadro.com","dnsServer":"cloudflare"}

# web domain
# URL = "https://dnsspy.io/scan/yadro.com"

# web domain
# URL = "https://dnsrepo.noc.org/?search=yadro.com"

# web domain
# URL = "http://dnshistory.org/dns-records/intel.com"

# web domain
# URL = "https://api.mnemonic.no/pdns/v3/search"
# data = {
#   "offset": 0,
#   "limit": 25,
#   "query": "yadro.com",
#   "aggregateResult": True,
#   "includeAnonymousResults": True,
# }

# web domain
# URL = "https://rapiddns.io/s/intel.com#result"

# web domain
# URL = "https://www.ssltools.com/api/dns"
# data = {"url": "yadro.com"}

# web mac
#URL = "https://www.macvendorlookup.com/oui.php?mac=00-15-F2-20-4D-6C"

# web mac
# URL = "https://maclookup.app/search/result?mac=00-15-F2-20-4D-6E"

# web mac
# URL = "https://mac.lc/address/00-15-F2-20-4D-64"

# web domain -> tech
#URL = "https://sitereport.netcraft.com/?url=http://intel.com&ajax=dcg"

# web domain -> tech
# URL = "https://builtwith.com/?q=intel.com"

# web domain -> tech
# URL = "https://webtechsurvey.com/search?q=yadro.com"

# web domain
# URL = "https://otx.alienvault.com/otxapi/indicators/domain/analysis/yadro.com"
# URL = "https://otx.alienvault.com/otxapi/indicators/domain/passive_dns/yadro.com"
# URL = "https://otx.alienvault.com/otxapi/indicators/domain/geo/yadro.com"

# web domain
# URL = "https://www.infobyip.com/ip-ucoz.ru.html"

# web ip
# URL = "https://nerd.cesnet.cz/nerd/ips/?subnet=1.1.1.1&hostname=&asn=&source_op=or&cat_op=or&bl_op=or&tag_op=or&sortby=rep&limit=20"

# web domain -> screenshot
# URL = "https://prod-alt.screenshot.api.visualping.io/screenshot/fastshot"
# data = {"renderer":"6.1.0","target_device":"4","url":"yadro.com","wait_time":"2","alert_error":True,"getAllText":False,"getHTMLTree":True,"preactions":{"active":False,"actions":[]}}

# web domain
#  URL = "https://blacklight.api.themarkup.org/graphic-api"
#  data = {
#      "inUrl": "http://intel.com",
#      "device": "mobile"
#  }

# web domain
# URL = "https://well-known.dev/?q=intel.com#results"

# web domain
# URL = "https://api.cookieserve.com/get_scan_result?url=intel.com"

# web domain
# URL = "https://host.io/search?domain=yadro.com"

# web domain
# URL = "https://www.urlvoid.com/scan/intel.com/"

# web domain
# URL = "https://hypestat.com/info/ucoz.ru"

# web domain
# URL = "https://www.clearwebstats.com/task.php?q=intel.com&t=auto"

# web domain
# URL = "https://sitecheck.sucuri.net/api/v3/?scan=intel.com"

# web domain
# URL = "https://www.similarsites.com/api/site/intel.com"

# web domain
# URL = "https://check-host.net/ip-info?host=intel.com"

# web domain
# URL = "https://ip2geolocation.com/?ip=intel.com"

# web domain
# URL = "https://ipgeolocation.io/ip-location/intel.com"

# web ip
# URL = "https://db-ip.com/demo/home.php?s=49.43.32.34"

# web domain
# URL = "https://whoisrequest.com/whois/yadro.com"

# web ip
# URL = "https://api.facha.dev/v1/ip/1.1.1.1"

# web domain
# URL = "https://web-check.as93.net/.netlify/functions/get-ip?url=https://intel.com"
# URL = "https://web-check.as93.net/.netlify/functions/ssl?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/whois?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/quality?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/cookies?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/headers?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/dns?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/http-security?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/social-tags?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/threats?url=https://yadro.com"
# URL = "https://web-check.as93.net/.netlify/functions/mail-config?url=https://yadro.com"

URL = "https://suip.biz/?act=subfinder"
data = """
------WebKitFormBoundaryMcE87KQTAtVfcMAW
Content-Disposition: form-data; name="url"

yadro.com
------WebKitFormBoundaryMcE87KQTAtVfcMAW
Content-Disposition: form-data; name="Submit1"

Submit
------WebKitFormBoundaryMcE87KQTAtVfcMAW--
"""

def main():
    if data:
        a = requests.post(URL, headers={"User-Agent": UA}, data=data).content
    else:
        a = requests.get(URL, headers={"User-Agent": UA}).content
    print(a)


if __name__ == "__main__":
    main()
