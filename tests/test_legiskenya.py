import pytest 
from legiscrapor.legiskenya import legisKenya
import os 

@pytest.fixture
def kl_web():
    '''Returns a LegisKenya instance'''
    return legisKenya()

def test_language(kl_web):
    assert kl_web.language == "English"

def test_country(kl_web):
    assert kl_web.country == "Kenya"

def test_search_laws(kl_web,capfd):
    kl_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)

    k = 'climate'

    hrefs = kl_web.search_laws(k)
    #out,err = capfd.readouterr()
    #patterns = ['Law','Parliament','Legal']
    #for p in patterns: 
    #    assert re.search(p,out)
    assert len(hrefs) == 19
    hrefs.sort()
    links = ['http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=CAP.%20198&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=CAP.%20326&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2011%20of%202016&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2013%20of%202019&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2014%20of%202019&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2016%20of%202013&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2019%20of%202011&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%202%20of%202000&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%202%20of%202009&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2021%20of%202017&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2024%20of%202011&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2026%20of%202015&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2028%20of%202011&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%204%20of%202006&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%204%20of%202016&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2043%20of%202016&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2047%20of%202013&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%206%20of%202012&term=climate','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%208%20of%201999&term=climate']
    links.sort()
    assert hrefs == links 
    kl_web.teardown()
