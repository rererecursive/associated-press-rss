from scrapy.exporters import XmlItemExporter
from scrapy.utils.python import is_listlike

class ApPipeline(object):

	def __init__(self, file_name):
		self.first_item = True
		self.file_name = file_name
		self.file_handler = open(self.file_name, 'wb')
		self.exporter = RssXmlItemExporter(
			self.file_handler,
			root_element='channel',
			item_element='item',
			fields_to_export = ['title', 'link', 'description', 'guid', 'pubDate', 'lastBuildDate'],
			indent=2)

		self.exporter.start_exporting()

	def process_item(self, item, spider):
		if self.first_item:
			# The first item comes from main.py with the information for <channel>
			self.exporter.export_item(item, write_start=False, write_end=False)
			self.first_item = False
		else:
			self.exporter.export_item(item)

		return item

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file_handler.close()

	@classmethod
	def from_crawler(cls, crawler):
		file_name = crawler.settings.__dict__['attributes']['LAMBDA_OUTPUT_FILENAME']
		print("Output filename:", file_name)
		return cls(file_name)


class RssXmlItemExporter(XmlItemExporter):
	def __init__(self, file, **kwargs):
		super().__init__(file, **kwargs)
		self.root_root_element = 'rss'

	# Override so that we can write two root elements
	def start_exporting(self, attrs={}):
		self.xg.startDocument()
		self.xg.startElement(self.root_root_element, {'version': '2.0'})
		self._beautify_newline(new_item=True)
		self.xg.startElement(self.root_element, {})
		self._beautify_newline(new_item=True)

	def export_item(self, item, write_start=True, write_end=True):
		if write_start:
			self._beautify_indent(depth=1)
			self.xg.startElement(self.item_element, {})
			self._beautify_newline()

		# Add the 'isPermalink' attribute to each RSS item
		for name, value in self._get_serialized_fields(item, default_value=''):
			attrs = {}
			if name == 'guid':
				attrs = {'isPermaLink': 'true'}

			self._export_xml_field(name, value, depth=2, attrs=attrs)

		if write_end:
			self._beautify_indent(depth=1)
			self.xg.endElement(self.item_element)
			self._beautify_newline(new_item=True)

	# Override so that we can write two root elements
	def finish_exporting(self):
		self.xg.endElement(self.root_element)
		self._beautify_newline(new_item=True)
		self.xg.endElement(self.root_root_element)
		self.xg.endDocument()

	# Override so that we can pass in custom attrs to startElement()
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
