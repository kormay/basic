"""
Thunder Chen<nkchenz@gmail.com> 2007.9.1
"""
try:
    import xml.etree.ElementTree as ET
except:
    import cElementTree as ET  # for 2.4

from object_dict import object_dict
import re


class XML2Dict(object):
    reg = re.compile(r"\{\S*\}")
    def __init__(self):
        pass

    def _parse_node(self, tree):
        content_tree = object_dict()
        content_tree[self._namespace_split(tree.tag)] = self._child_node(tree)
        return content_tree

    def _child_node(self, node):
        node_tree = object_dict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for (k, v) in node.attrib.items():
            node_tree[k] = v
        # Save childrens
        for child in node.getchildren():
            childTree = self._child_node(child)
            tag = self._namespace_split(child.tag)
            if tag not in node_tree:  # the first time, so store it in dict
                node_tree[tag] = childTree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old]  # multi times, so change old dict to a list
            node_tree[tag].append(childTree)  # add the new one

        return node_tree

    def _namespace_split(self, tag):
        """
           Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
             ns = http://cs.sfsu.edu/csc867/myscheduler
             name = patients
        """
        return self.reg.sub('', tag)

    def parse(self, file):
        """parse a xml file to a dict"""
        f = open(file, 'r')
        return self.fromstring(f.read())

    def fromstring(self, s):
        """parse a string"""
        t = ET.fromstring(s)
        return self._parse_node(t)
        # return object_dict({root_tag: root_tree})


if __name__ == '__main__':
    s = """<?xml version="1.0" encoding="utf-8" ?>
    <result>
        <count n="1">10</count>
        <data><ids><id>491691</id></ids><name>test</name></data>
        <data><id>491692</id><name>test2</name></data>
        <data><id>503938</id><name>hello, world</name></data>
    </result>"""

    test = '''<?xml version="1.0" encoding="utf-8"?>
<ArrayOfString xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://WebXml.com.cn/">
  <string>宝安区 （广东）</string>
  <string>博罗县 （广东）</string>
  <string>潮南区 （广东）</string>
  <string>潮阳区 （广东）</string>
  <string>潮州市 （广东）</string>
  <string>澄海区 （广东）</string>
  <string>从化市 （广东）</string>
  <string>大埔县 （广东）</string>
  <string>德庆县 （广东）</string>
  <string>电白县 （广东）</string>
  <string>东莞市 （广东）</string>
  <string>斗门县 （广东）</string>
  <string>恩平市 （广东）</string>
  <string>番禺区 （广东）</string>
  <string>丰顺县 （广东）</string>
  <string>封开县 （广东）</string>
  <string>佛冈县 （广东）</string>
  <string>佛山市 （广东）</string>
  <string>高明区 （广东）</string>
  <string>高要市 （广东）</string>
  <string>高州市 （广东）</string>
  <string>广东 （广东）</string>
  <string>广宁县 （广东）</string>
  <string>广州市 （广东）</string>
  <string>海丰县 （广东）</string>
  <string>和平县 （广东）</string>
  <string>河源市 （广东）</string>
  <string>鹤山市 （广东）</string>
  <string>花都区 （广东）</string>
  <string>化州市 （广东）</string>
  <string>怀集县 （广东）</string>
  <string>惠东县 （广东）</string>
  <string>惠来县 （广东）</string>
  <string>惠阳区 （广东）</string>
  <string>惠州市 （广东）</string>
  <string>江门市 （广东）</string>
  <string>蕉岭县 （广东）</string>
  <string>揭西县 （广东）</string>
  <string>揭阳市 （广东）</string>
  <string>开平市 （广东）</string>
  <string>乐昌市 （广东）</string>
  <string>雷州市 （广东）</string>
  <string>连南县 （广东）</string>
  <string>连平县 （广东）</string>
  <string>连山县 （广东）</string>
  <string>连州市 （广东）</string>
  <string>廉江市 （广东）</string>
  <string>龙川县 （广东）</string>
  <string>龙岗区 （广东）</string>
  <string>龙门县 （广东）</string>
  <string>陆丰市 （广东）</string>
  <string>陆河县 （广东）</string>
  <string>罗定市 （广东）</string>
  <string>茂名市 （广东）</string>
  <string>梅州市 （广东）</string>
  <string>南澳县 （广东）</string>
  <string>南海区 （广东）</string>
  <string>南雄市 （广东）</string>
  <string>平远县 （广东）</string>
  <string>普宁市 （广东）</string>
  <string>清远市 （广东）</string>
  <string>曲江县 （广东）</string>
  <string>饶平县 （广东）</string>
  <string>仁化县 （广东）</string>
  <string>乳源县 （广东）</string>
  <string>三水区 （广东）</string>
  <string>汕头市 （广东）</string>
  <string>汕尾市 （广东）</string>
  <string>韶关市 （广东）</string>
  <string>深圳市 （广东）</string>
  <string>始兴县 （广东）</string>
  <string>顺德区 （广东）</string>
  <string>四会市 （广东）</string>
  <string>遂溪县 （广东）</string>
  <string>台山市 （广东）</string>
  <string>翁源县 （广东）</string>
  <string>吴川市 （广东）</string>
  <string>五华县 （广东）</string>
  <string>新丰县 （广东）</string>
  <string>新会区 （广东）</string>
  <string>新兴县 （广东）</string>
  <string>信宜市 （广东）</string>
  <string>兴宁市 （广东）</string>
  <string>徐闻县 （广东）</string>
  <string>阳江市 （广东）</string>
  <string>阳山县 （广东）</string>
  <string>阳西县 （广东）</string>
  <string>英德市 （广东）</string>
  <string>郁南县 （广东）</string>
  <string>云浮市 （广东）</string>
  <string>增城市 （广东）</string>
  <string>湛江市 （广东）</string>
  <string>肇庆市 （广东）</string>
  <string>中山市 （广东）</string>
  <string>珠海市 （广东）</string>
  <string>紫金县 （广东）</string>
</ArrayOfString>'''
    xml = XML2Dict()
    r = xml.fromstring(s)
    print(r)
    # print(r.result.count.value)
    # print(r.result.count.n)

    # for data in r.result.data:
    #     print(data.id, data.name)
