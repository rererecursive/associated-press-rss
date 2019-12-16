# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import XmlItemExporter
from scrapy.utils.python import is_listlike

class ApPipeline(object):

	def __init__(self):
		self.first_item = True
		self.file_name = 'output.xml'
		self.file_handler = open(self.file_name, 'ab')
		self.exporter = RssXmlItemExporter(
									self.file_handler,
									root_element='channel',
									item_element='item',
									fields_to_export = ['title', 'link', 'description', 'guid', 'pub_date'],
									indent=2)

		self.exporter.start_exporting()

	def process_item(self, item, spider):
		if self.first_item:
			self.exporter.export_item(item, start=False, end=False)
			self.first_item = False
		else:
			self.exporter.export_item(item)

		return item

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file_handler.close()


class RssXmlItemExporter(XmlItemExporter):

  def __init__(self, file, **kwargs):
    super().__init__(file, **kwargs)
    self.root_root_element = 'rss'

  def start_exporting(self, attrs={}):
    self.xg.startDocument()
    self.xg.startElement(self.root_root_element, {'version': '2.0'})
    self._beautify_newline(new_item=True)
    self.xg.startElement(self.root_element, {})
    self._beautify_newline(new_item=True)

  def export_item(self, item, start=True, end=True):
    if start:
      self._beautify_indent(depth=1)
      self.xg.startElement(self.item_element, {})
      self._beautify_newline()

    for name, value in self._get_serialized_fields(item, default_value=''):
      attrs = {}
      if name == 'guid':
        attrs = {'isPermaLink': 'true'}

      self._export_xml_field(name, value, depth=2, attrs=attrs)

    if end:
      self._beautify_indent(depth=1)
      self.xg.endElement(self.item_element)
      self._beautify_newline(new_item=True)

  def finish_exporting(self):
    self.xg.endElement(self.root_element)
    self._beautify_newline(new_item=True)
    self.xg.endElement(self.root_root_element)
    self.xg.endDocument()

  def _export_xml_field(self, name, serialized_value, depth, attrs={}):
    self._beautify_indent(depth=depth)
    self.xg.startElement(name, attrs)
    if hasattr(serialized_value, 'items'):
      self._beautify_newline()
      for subname, value in serialized_value.items():
        self._export_xml_field(subname, value, depth=depth+1)
      self._beautify_indent(depth=depth)
    elif is_listlike(serialized_value):
      self._beautify_newline()
      for value in serialized_value:
        self._export_xml_field('value', value, depth=depth+1)
      self._beautify_indent(depth=depth)
    elif isinstance(serialized_value, str):
      self.xg.characters(serialized_value)
    else:
      self.xg.characters(str(serialized_value))
    self.xg.endElement(name)
    self._beautify_newline()
