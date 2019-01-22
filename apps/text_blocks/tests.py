from django import template
from django.test import TestCase
from django.core.cache import cache
from django import db

from text_blocks.models import TextBlock
from .settings import CACHE_PREFIX


class BasicTextBlockTests(TestCase):

    def setUp(self):
        self.testblock = TextBlock.objects.create(
            slug='block',
            header='HEADER',
            content='CONTENT'
        )

    def testCacheReset(self):
        """
        Tests if TextBlock.save() resets the cache.
        """
        tpl = template.Template('{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" 60 {% templatetag closeblock %}')
        tpl.render(template.Context({}))

        cache_key = '%s:%s' % (CACHE_PREFIX, 'block')

        self.assertNotEqual(None, cache.get(cache_key))
        block = TextBlock.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()


class TextBlockTagTests(TestCase):
    def setUp(self):
        self.testblock = TextBlock.objects.create(
            slug='block',
            header='HEADER',
            content='CONTENT'
        )

    def testExistingTemplate(self):
        tpl = template.Template(
            '{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" {% templatetag closeblock %}')
        output = tpl.render(template.Context({}))
        self.assertIn(self.testblock.content, output)
        self.assertIn(self.testblock.slug, output)

    def testUsingMissingTemplate(self):
        tpl = template.Template('{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" using="missing_template.html" {% templatetag closeblock %}')
        exception = template.TemplateDoesNotExist
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testSyntax(self):
        tpl = template.Template(
            '{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" {% templatetag closeblock %}')
        tpl.render(template.Context({}))
        tpl = template.Template(
            '{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" 123 {% templatetag closeblock %}')
        tpl.render(template.Context({}))
        tpl = template.Template('{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" using="text_blocks/textblock.html" {% templatetag closeblock %}')
        tpl.render(template.Context({}))
        tpl = template.Template('{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock "block" 123 using="text_blocks/textblock.html" {% templatetag closeblock %}')
        tpl.render(template.Context({}))

    def testBlockAsVariable(self):
        tpl = template.Template(
            '{% templatetag openblock %} load text_block_tags {% templatetag closeblock %}{% templatetag openblock %} textblock blockvar {% templatetag closeblock %}')
        tpl.render(template.Context({'blockvar': 'block'}))
